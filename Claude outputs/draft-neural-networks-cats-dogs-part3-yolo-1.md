---
title: "How Neural Networks Learn to Tell a Cat From a Dog, Part III: Transfer Learning with YOLO26"
subtitle: "Fine-tuning a pretrained backbone on the same images, the same split, the same test set -- and being precise about which of three changed variables actually did the work"
status: DRAFT
series: "How Neural Networks Learn to See (3 of 3)"
category: comp-science
date: 2026-09-15
tags: ["neural-networks", "machine-learning", "python", "yolo", "ultralytics", "transfer-learning", "image-classification", "computer-vision"]
showToc: true
tocopen: true
---

*This is a draft, part three of a three-part series. [Part I](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog/) trained a flattening MLP from scratch on Kaggle's Dogs vs. Cats data (63.3% test accuracy). [Part II](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog-part-2/) kept everything identical except the architecture and added convolution (84.2%). This post keeps the same 120-image held-out test set again, but this time doesn't train from scratch at all: it fine-tunes YOLO26n-cls, a classification model pretrained on ImageNet by Ultralytics, and gets 99.2%. The point of this post is not just to report that number -- it's to be precise about *why*, because unlike Part I → Part II, this comparison changes three things at once, not one.*

## The result, up front

```
Model: yolo26n-cls.pt (Ultralytics, ImageNet-pretrained, fine-tuned)
Train: 21,148 images  Validation: 3,732 images  Test: 120 images (identical to Parts I & II)

Test accuracy (never seen during training): 0.992

              precision    recall  f1-score   support

        cats       1.00      0.98      0.99        60
        dogs       0.98      1.00      0.99        60

    accuracy                           0.99       120

Confusion matrix [[TN, FP], [FN, TP]]:
[[59  1]
 [ 0 60]]
```

119 of 120 correct. The single error is one cat classified as a dog; every dog was classified correctly. Compare the three posts on the identical test set:

| | Part I: MLP | Part II: CNN | Part III: YOLO26n-cls |
|---|---|---|---|
| Test accuracy | 63.3% | 84.2% | **99.2%** |
| Errors on 120 test images | 44 | 19 | **1** |
| Parameters | 893,185 | 171,234 | ~2.8M |
| Input resolution | 48×48 | 48×48 | 224×224 |
| Weight initialisation | random | random | ImageNet-pretrained |
| Training data actually used | 21,148 images, from zero | 21,148 images, from zero | 21,148 images, fine-tuning a backbone already trained on 1.28M+ ImageNet images |

That table is also the honest disclosure this post has to lead with, not bury: three things changed between Part II and Part III, not one. A ~16x larger model, a 21.8x larger input image (224² vs 48² = 50,176 vs 2,304 pixel positions), and pretrained weights instead of random initialisation, all changed together. This is not a controlled, single-variable experiment the way Part I → Part II was. It's a demonstration of what happens when you stop constraining yourself to "from scratch, small, and fair to compare" and instead ask "what's the best any of these three tools can actually do on this problem." Worth being explicit about that difference in kind, since conflating the two is exactly the sort of imprecision a post about neural networks shouldn't have.

## Mechanism 1: transfer learning, or why fine-tuning isn't training from zero

Part II's CNN starts every one of its ~171,000 weights at a random value and has to discover, using only the 21,148 images in this dataset, that edges exist, that fur has a particular texture signature, that ears are roughly triangular or floppy blobs near the top of a head. That's a lot to ask of 21,148 images and a network with no prior exposure to anything visual.

YOLO26n-cls starts somewhere else entirely. Before it ever saw a single cat or dog photo from this project, Ultralytics trained it on ImageNet -- roughly 1.28 million photographs spanning 1,000 object categories (dogs and cats among them, but also cars, musical instruments, kitchen tools, birds, furniture, and hundreds more).((Ultralytics, [Classify task documentation](https://docs.ultralytics.com/tasks/classify/) -- YOLO26 classification models table, ImageNet pretraining.)) Learning to tell 1,000 different things apart forces a network's early and middle layers to build genuinely general-purpose visual features: edge and corner detectors, texture and colour-pattern detectors, and, by the deeper layers, detectors for parts like eyes, fur, and limbs that recur across many animal categories, not just cats and dogs specifically. `model.train(data=YOLO_DATA_DIR, ...)` in `train_yolo.py` below doesn't start from zero; it starts from those weights and nudges them -- fine-tunes them -- toward this project's specific 2-class problem. The network doesn't need to (re-)discover what an edge is. It already knows. It only has to learn how the concepts it already has map onto "cat" vs. "dog" specifically, which is a dramatically smaller thing to learn than the whole of vision, and 21,148 images is comfortably enough data for that narrower job even though it clearly wasn't enough to learn vision from nothing in Part II.

This is why "transfer learning" is the standard term, not "extra training": what transfers is the feature representation learned on a much larger, unrelated dataset, not any data or labels from this project's own images.

## Mechanism 2: resolution -- 224×224 vs. 48×48

Part I and Part II both downsize every image to 48×48 before it reaches the network -- a deliberate choice to keep the flattened MLP's input small (6,912 features) and training fast. `train_yolo.py` leaves the image at Ultralytics' default classification input size of 224×224 instead, and says why in its own docstring: YOLO26n-cls's pretrained weights were learned at that resolution, and downsizing to 48px on the way in would throw away exactly the fine detail (whisker texture, eye shape, ear edges) those pretrained filters are tuned to detect, defeating the point of using them at all. 224×224 is 50,176 pixel positions per channel against 48×48's 2,304 -- roughly 21.8x more raw spatial information reaching the network for every single image. Some meaningful share of Part III's accuracy gain is simply "the network can see more," independent of anything about YOLO's architecture specifically -- a plain CNN given 224×224 inputs would also improve over its 48×48 result in Part II, just not to 99.2%.

## Mechanism 3: what YOLO26's architecture contributes -- and what doesn't apply here

YOLO26, released by Ultralytics in 2026, is built primarily as an object-detection model family, and most of its headline architectural changes are specifically about the detection task -- worth naming precisely rather than crediting them all to "YOLO is better," because several of them are structurally absent from the classification run this post actually did:

- **DFL removal.** Earlier YOLO versions used Distribution Focal Loss to regress bounding-box edges as a probability distribution over discretised offsets. YOLO26 removes it, simplifying the detection head and easing export to edge hardware.((Ultralytics, [Why Ultralytics YOLO26 Removes NMS](https://www.ultralytics.com/blog/why-ultralytics-yolo26-removes-nms-and-how-that-changes-deployment); Ultralytics, [YOLO26 model docs](https://docs.ultralytics.com/models/yolo26/).))
- **NMS-free, end-to-end detection head.** YOLO26 adds an optional one-to-one prediction head that outputs a single box per object directly, without the traditional non-maximum-suppression post-processing step that discards duplicate, overlapping detections.((Same sources as above.))
- **Progressive Loss and STAL (Small-Target-Aware Label Assignment).** Training-time changes that shift loss emphasis toward the inference head and improve how small objects get assigned to labels during training -- aimed at small-object detection accuracy.((Ultralytics, [YOLO26 model docs](https://docs.ultralytics.com/models/yolo26/).))

None of those three apply to `yolo26n-cls.pt`. There are no bounding boxes in this task, so there's nothing for DFL or an NMS-free head to do, and STAL is a detection-label-assignment technique with no equivalent in a single-label classification problem. The classification variant used here has no detection head at all -- structurally, it's the YOLO26 backbone (the convolutional feature extractor) feeding a global-average-pool and a single linear layer that outputs 2 class scores, the same basic shape as Part II's CNN, just far deeper and far wider.

What *did* plausibly carry over: the backbone itself, which is the product of several generations of architecture refinement across the YOLO family (efficient, GPU/CPU-friendly convolution blocks, refined over YOLOv8 through YOLO11 to YOLO26), and, per Ultralytics, YOLO26's training recipe uses **MuSGD**, a hybrid optimiser combining SGD with Muon -- an optimisation technique adapted from large language model training and applied to Ultralytics' computer vision models generally, not a classification-specific invention but part of what `model.train()` uses by default across tasks in this framework.((Ultralytics, [YOLO26 model docs](https://docs.ultralytics.com/models/yolo26/) -- MuSGD optimiser.)) Untangling exactly how much of Part III's gain is "better backbone design" versus simply "16x more parameters, pretrained, at 21.8x the input resolution" isn't possible from a single run of one model at one size -- that would need a proper ablation (same backbone size and same resolution, pretrained vs. not; same pretraining, different resolutions; and so on), which is out of scope for a from-scratch teaching series but worth naming as the honest limit of what this post's comparison shows.

## The training script: `train_yolo.py`

Uses [Ultralytics](https://docs.ultralytics.com/) -- an open-source computer vision library -- for the pretrained model and the fine-tuning loop; scikit-learn only for the final accuracy/confusion-matrix scoring, exactly as in Parts I and II.

```python
"""
train_yolo.py
--------------
Part III companion to train_nn.py / train_cnn.py: same real Kaggle Dogs
vs. Cats images, same held-out 120-image test set (60 cats + 60 dogs,
carved out once by prepare_kaggle_dataset.py and never touched again),
same 85/15 train/val split idea (RANDOM_STATE=42) -- the difference is
the model. Where train_cnn.py trains a small CNN from scratch, this
script fine-tunes YOLO26n-cls, a pretrained (ImageNet) classification
backbone from Ultralytics, via transfer learning.

Image size is left at Ultralytics' default (224x224) rather than the
48x48 train_nn.py/train_cnn.py use: YOLO26n-cls's pretrained weights
were learned at that resolution, and downsizing to 48px would cripple
the transfer-learning benefit that's the whole point of using a
pretrained backbone. So this is "best accuracy each approach reaches
on the same images/split", not "same pixel budget for all three".

Usage:
    pip install ultralytics
    python3 train_yolo.py
"""
import os
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from ultralytics import YOLO

ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT, "data")
YOLO_DATA_DIR = os.path.join(ROOT, "data_yolo")
RANDOM_STATE = 42
MAX_EPOCHS = 30        # pretrained backbone, so far fewer epochs than train_cnn.py's from-scratch 60
PATIENCE = 15          # same early-stopping patience as train_nn.py / train_cnn.py
BATCH_SIZE = 32
MODEL = "yolo26n-cls.pt"


def _symlink_split(src_dir, filenames, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    for fname in filenames:
        link = os.path.join(dest_dir, fname)
        if not os.path.exists(link):
            os.symlink(os.path.join(src_dir, fname), link)


def build_yolo_layout():
    """Symlink data/train -> data_yolo/{train,val} (85/15 split, seed 42)
    and data/test -> data_yolo/test, so this script trains/evaluates on
    the identical image set train_nn.py and train_cnn.py used."""
    for label in ("cats", "dogs"):
        train_src = os.path.join(DATA_DIR, "train", label)
        files = sorted(os.listdir(train_src))
        train_files, val_files = train_test_split(
            files, test_size=0.15, random_state=RANDOM_STATE,
        )
        _symlink_split(train_src, train_files, os.path.join(YOLO_DATA_DIR, "train", label))
        _symlink_split(train_src, val_files, os.path.join(YOLO_DATA_DIR, "val", label))

        test_src = os.path.join(DATA_DIR, "test", label)
        test_files = sorted(os.listdir(test_src))
        _symlink_split(test_src, test_files, os.path.join(YOLO_DATA_DIR, "test", label))


def main():
    build_yolo_layout()

    model = YOLO(MODEL)
    train_results = model.train(
        data=YOLO_DATA_DIR,
        epochs=MAX_EPOCHS,
        patience=PATIENCE,
        batch=BATCH_SIZE,
        seed=RANDOM_STATE,
        device="mps",
        project=os.path.join(ROOT, "runs_yolo"),
        name="cats_vs_dogs",
        exist_ok=True,
    )

    best_weights = train_results.save_dir / "weights" / "best.pt"
    best_model = YOLO(str(best_weights))

    test_dir = Path(YOLO_DATA_DIR) / "test"
    class_names = best_model.names               # {0: 'cats', 1: 'dogs'}, alphabetical
    name_to_id = {v: k for k, v in class_names.items()}

    test_paths, y_true = [], []
    for label in ("cats", "dogs"):
        for fname in sorted(os.listdir(test_dir / label)):
            test_paths.append(str(test_dir / label / fname))
            y_true.append(name_to_id[label])

    preds = best_model.predict(test_paths, verbose=False)
    y_pred = [int(p.probs.top1) for p in preds]

    test_acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    print(f"Test accuracy: {test_acc:.3f}")
    print(classification_report(y_true, y_pred, target_names=[class_names[0], class_names[1]]))
    print(cm)


if __name__ == "__main__":
    main()
```

Two implementation details worth flagging, both in service of keeping this a fair comparison against Parts I and II rather than a different experiment wearing the same clothes:

**Symlinks, not copies.** Ultralytics' classification trainer expects an on-disk `<dataset>/{train,val,test}/<class>/` layout, one directory per class. `build_yolo_layout()` builds that with symbolic links into the *same* image files `data/` already holds, rather than copying them -- so this script trains and tests on the literal same JPEGs Part I and Part II used, not a re-downloaded or re-processed copy that could quietly drift.

**Same split, same seed.** `train_test_split(files, test_size=0.15, random_state=42)` on the same file lists, in the same order, reproduces the identical 21,148/3,732 train/validation partition `train_nn.py` and `train_cnn.py` used (this call isn't `stratify`d the way theirs was, but since the underlying pool is already class-balanced 12,440/12,440, that makes no material difference here). The 120-image test set was never touched by any of this -- it's the same fixed files `prepare_kaggle_dataset.py` reserved once, back in Part I, before any of the three models existed.

## A small-sample caveat, in the interest of precision

120 test images means each individual prediction is worth 0.83 percentage points of the reported accuracy. Going from 19 errors (Part II) to 1 error (Part III) is a real, large, and clearly meaningful improvement -- but "99.2%" on a 120-image test set carries a wider margin of uncertainty than the same number would on, say, a 12,000-image test set, and a single flipped prediction would have read as 98.3% instead. None of this weakens the direction or the scale of the result; it's a reason not to treat the third decimal place as more precise than the sample size supports.

## What the network actually looked at: Grad-CAM on the real predictions

Every mechanism argued above is still an argument from first principles -- "convolution preserves spatial structure, so the network can localise patterns." It's possible to check that directly, on this model's actual weights and the actual test images, using **Grad-CAM** (Gradient-weighted Class Activation Mapping).((Selvaraju et al., ["Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization"](https://arxiv.org/abs/1610.02391), ICCV 2017 -- the original method.)) The idea: run an image forward through the network as normal, then run the predicted class's score backward only as far as the last convolutional feature map (here, the 1,280-channel map produced by the Classify head's own conv layer, immediately before it gets pooled down to a single vector per image). The gradient at that layer says how much each spatial location would have to change to move the prediction, which -- averaged per channel and used to weight that channel's activation map -- produces a heatmap of where in the image the decision actually came from.

Run against three of this model's own real test predictions:

![Grad-CAM heatmap, correctly classified cat -- heat concentrated on the near cat's face](/images/comp-science/nn-cats-dogs-part3-gradcam-cat-correct.png)

![Grad-CAM heatmap, correctly classified dog -- heat concentrated on the dog's head and face](/images/comp-science/nn-cats-dogs-part3-gradcam-dog-correct.png)

On both correct predictions, the heat lands exactly where "What an MLP does with an image" (Part I) predicted a spatially-aware network *should* look: the face. Not the background, not the bedding, not an arbitrary corner -- the specific region a person would also point to if asked "how can you tell." That's the concrete, visual version of the parameter-sharing argument from Part II: a network that preserves pixel adjacency can learn "the face region is where the species-distinguishing information is" and then actually look there.

The one misclassified test image is more interesting than a simple failure, and Grad-CAM shows exactly why:

![Grad-CAM heatmap on the misclassified image, labelled cat -- heat concentrated entirely on the dog, not the cat](/images/comp-science/nn-cats-dogs-part3-gradcam-cat-misclassified.png)

![The same image, unmodified -- a dog and a black cat together in one photo, filed under Kaggle's cats/ folder](/images/comp-science/nn-cats-dogs-part3-gradcam-cat-misclassified-original.png)

This test image (`cat.11724.jpg`, ground-truth label "cat" per Kaggle's `cat.N.jpg` naming convention) contains **both a dog and a cat**, photographed together. The dog is larger, better-lit, and more central in the frame; the cat is smaller, mostly in shadow, off to one side. Grad-CAM shows the network's attention sitting almost entirely on the dog's face -- it didn't fail to find a face, and it didn't get confused by fur texture or colour the way a flattened network structurally has to. It looked at the single most prominent animal face in the photograph and classified *that*, correctly, as a dog. The error isn't really a model error at all; it's a single-label dataset applying one class per image to a photo that, by its actual content, has two valid subjects. This is a real, if minor, label-quality artefact in Kaggle's Dogs vs. Cats data, not a shortcoming in the network's mechanism -- and it's the kind of thing that's essentially invisible from a confusion matrix alone, and only became visible by actually asking the model what it was looking at.

## Practical application, revisited: the same model family already running on real hardware

Parts I and II both closed with `apex_ros`, Bruce's real autonomous RC vehicle build, as a live example of these ideas applied to navigation. That reference lands even more directly here: the `apex_ros` build log's most recent entries describe `yolo26n` -- the same nano-scale model in the same YOLO26 family fine-tuned in this post, though there running its full object-detection variant rather than the classification-only one used here -- performing real-time object detection directly on a Raspberry Pi 5's CPU.((`apex_ros` build log, this site -- [Same Shape, Different Paper](https://1697-20747.github.io/blog/comp-science/same-shape-different-paper/), where `yolo26n` object detection is current architecture.)) The mechanism explained above -- a pretrained backbone fine-tuned on a much smaller, task-specific set of images, rather than trained from zero -- is exactly what makes that practical: nobody trains a detection network from random weights on a home robotics project's own, necessarily small, collection of track photos. They start from a backbone Ultralytics already spent a large ImageNet-scale (or COCO-scale, for detection) training run on, and fine-tune. This post's 21,148 fine-tuning images and apex_ros's presumably much smaller set of track photos are doing the same kind of job for the same underlying reason.

## Series summary

| Post | Approach | Test accuracy | What it demonstrates |
|---|---|---|---|
| Part I | MLP, from scratch, `sklearn.neural_network` | 63.3% | The baseline mechanics of a neural network -- and the concrete cost of flattening away spatial structure |
| Part II | CNN, from scratch, PyTorch | 84.2% | What convolution alone buys you, with every other variable held fixed |
| Part III | YOLO26n-cls, fine-tuned, Ultralytics | 99.2% | What capacity, resolution, and transfer learning together buy you, at the cost of no longer being a single-variable comparison |

## Sources

- Ultralytics -- [YOLO26 model documentation](https://docs.ultralytics.com/models/yolo26/) (architecture changes: DFL removal, NMS-free end-to-end head, Progressive Loss, STAL, MuSGD optimiser; benchmark figures)
- Ultralytics -- [Classify task documentation](https://docs.ultralytics.com/tasks/classify/) (YOLO26 classification model table: parameters, ImageNet top-1/top-5 accuracy, 224×224 default input size)
- Ultralytics -- [Why Ultralytics YOLO26 Removes NMS: Here is Why and How it Changes Deployment](https://www.ultralytics.com/blog/why-ultralytics-yolo26-removes-nms-and-how-that-changes-deployment)
- Ultralytics -- [YOLO26: The new standard for edge-first Vision AI](https://www.ultralytics.com/blog/ultralytics-yolo26-the-new-standard-for-edge-first-vision-ai)
- Selvaraju, Cogswell, Das, Vedantam, Parikh, Batra -- [Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization](https://arxiv.org/abs/1610.02391), ICCV 2017 (the Grad-CAM method used in "What the network actually looked at")
- [Part I of this series](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog/) and [Part II](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog-part-2/) -- the MLP and CNN baselines, and the shared dataset/test set this post builds on
- `apex_ros` build log, this site -- [Same Shape, Different Paper](https://1697-20747.github.io/blog/comp-science/same-shape-different-paper/) (real `yolo26n` object detection running on Raspberry Pi 5 CPU)
- All YOLO26n-cls accuracy/confusion-matrix figures in this post: this project's own `train_yolo.py`, run against the same Kaggle Dogs vs. Cats data and held-out test set as Parts I and II

*Editorial note (draft): needs Bruce's sign-off before this goes live, and needs Parts I and II's real URL slugs confirmed once published (Part III's own links above to them are guessed). `train_yolo.py` has been run on Bruce's Mac (native, `device="mps"` -- Apple Silicon GPU acceleration, outside the Cowork device bridge for the same network-access reasons documented in Parts I and II) and the real numbers are in "The result, up front" above: 99.2% test accuracy, 1 error out of 120. Ultralytics architectural claims (DFL removal, NMS-free head, ProgLoss/STAL, MuSGD) are sourced directly from docs.ultralytics.com, fetched 2026-09-15, and explicitly scoped to what does and doesn't apply to the classification-only variant actually used here -- worth a final check against the live docs before publish in case any of it has changed. **Update 2026-09-17**: the four Grad-CAM figures in "What the network actually looked at" are real, generated 2026-09-17 by loading the actual trained `best.pt` weights and running Grad-CAM against the actual test images (including the real single misclassified file, `cat.11724.jpg`) -- not mockups or illustrative placeholders. This is the first rendered figure set in the whole three-part series; the other training artefacts (`runs_yolo/cats_vs_dogs/results.png`, `confusion_matrix.png`, `confusion_matrix_normalized.png`) and Parts I/II's own figures (loss curves, confusion matrices, network-architecture diagrams) are still open. The four Grad-CAM PNGs need copying into `static/images/comp-science/` under the filenames already used in the `![...]` links above.*
