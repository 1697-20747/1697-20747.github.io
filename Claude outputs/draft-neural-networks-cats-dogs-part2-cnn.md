---
title: "How Neural Networks Learn to Tell a Cat From a Dog, Part II: Adding Convolution"
subtitle: "Same data, same test set, same everything except the architecture -- what a CNN actually buys you over a flattened MLP"
status: DRAFT
series: "How Neural Networks Learn to See (2 of 3)"
category: comp-science
date: 2026-09-14
tags: ["neural-networks", "machine-learning", "python", "pytorch", "image-classification", "computer-vision", "cnn"]
showToc: true
tocopen: true
---

*This is a draft, part two of a three-part series. [Part I](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog/) built a plain, fully-connected network (an MLP) on the Kaggle Dogs vs. Cats dataset and hit its ceiling for a specific, identifiable reason: it flattens every image into a row of numbers before it ever sees it, throwing away which pixels are next to which. This post keeps the data, the test set, and the training recipe identical, and changes exactly one thing -- the network -- to show what that costs. [Part III](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog-part-3/) goes further again, swapping this from-scratch CNN for a pretrained one.*

## What changes, and what doesn't

Everything below uses the same 120-image held-out test set Part I reserved, the same 48×48 image size, the same Adam optimiser, the same early-stopping idea, and the same train/validation split logic. The only variable is the model: Part I's `MLPClassifier` flattens each image into 6,912 numbers before its first layer ever runs; this post's network keeps the image as a 48×48 grid with 3 colour channels and runs it through **convolutional** layers first. That's a controlled comparison, not a different experiment -- any difference in the result traces back to that one architectural change.

## Why convolution, concretely

Part I's "What an MLP does with an image" section named the limitation in the abstract: flattening throws away spatial structure, so a pixel and the pixel next to it are no more related, as far as the network's first layer is concerned, than two pixels on opposite corners of the image. Convolution fixes this directly, and it's worth working through exactly how.

A convolutional layer doesn't have one weight per input feature the way a fully-connected layer does. It has a small set of learned **filters** -- for example sixteen separate 3×3×3 filters (3 pixels by 3 pixels, across all 3 colour channels) -- and each filter slides across every position in the image, computing a weighted sum of the 3×3×3 patch under it at each stop. The output at each position is one number per filter: how strongly that particular pattern (an edge at a certain angle, a patch of a certain colour, eventually -- in deeper layers -- something like "fur texture" or "pointed ear") showed up *at that location*. Stack sixteen filters and you get sixteen of these "feature maps," each the same height and width as the input (with padding), each recording where one learned pattern appears.

Two consequences follow directly from that mechanism, and both matter more than they might sound like in the abstract:

**Spatial information survives.** A feature map is still shaped like the image -- an edge detected near the top-left of the input produces a strong response near the top-left of the feature map. Nothing about the ear-shape-detector's output at position (3, 3) is confused with its output at position (40, 40), the way flattening would confuse the equivalent pixels in Part I's network.

**Far fewer weights, not more.** This is the counterintuitive part. A single 3×3×3 filter has only 27 weights (plus a bias) -- and that *same* filter, with those same 27 weights, is reused at every position in the image. Compare that to Part I's first layer, which needed a separate weight for every one of the 6,912 input pixels feeding every one of 128 hidden neurons (884,736 weights just in that one layer). Convolution gets more expressive representations for images specifically out of dramatically fewer parameters, because "an edge detector" is a useful thing to apply everywhere in an image, not a separate thing to relearn at every pixel position.

Pooling layers (`MaxPool2d` below) sit between convolution layers and do one more job: they shrink each feature map by taking the maximum value in each small block (2×2 here), which both reduces computation and makes the network more tolerant of a pattern shifting by a few pixels -- a cat's ear detected slightly left of where it was in training still fires the same detector.

## The library: PyTorch

Part I already established that `sklearn.neural_network` has no convolution support at all -- it isn't a missing feature so much as a deliberate scope boundary of that one module. Building a CNN means moving to a framework that implements it: this post uses [PyTorch](https://pytorch.org/), an open-source deep learning library, in place of scikit-learn for the model and training loop. The surrounding methodology doesn't change -- load data, split into train/validation/test, fit, evaluate -- only the tool that runs the fitting step.

## The training script: `train_cnn.py`

```python
"""
train_cnn.py
-------------
Part II companion to train_nn.py: same real data, same train/validation/
test split (identical RANDOM_STATE=42), same image size, same Adam
optimiser and early-stopping idea -- the one thing that changes is the
network itself. Where train_nn.py flattens every image into a 6,912-number
row and feeds it to a plain MLPClassifier, this script keeps the image as
a (3, 48, 48) grid and runs it through a small convolutional neural
network (CNN) instead.
"""
import os
import json
import time
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 48
RANDOM_STATE = 42
BATCH_SIZE = 32
MAX_EPOCHS = 60
PATIENCE = 15


def list_split(split):
    items = []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            items.append((os.path.join(folder, fname), class_id))
    return items


class PetDataset(Dataset):
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        path, class_id = self.items[idx]
        img = Image.open(path).convert("RGB").resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR)
        arr = np.asarray(img, dtype=np.float32) / 255.0
        arr = arr.transpose(2, 0, 1)            # (H, W, 3) -> (3, H, W), channels first
        return torch.from_numpy(arr), class_id


class SmallCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 48x48 -> 24x24
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 24x24 -> 12x12
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 12x12 -> 6x6
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                        # only flattened here, at the very end, for the FC head
            nn.Linear(64 * 6 * 6, 64), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 2),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def main():
    device = torch.device("mps" if torch.backends.mps.is_available()
                           else "cuda" if torch.cuda.is_available() else "cpu")

    train_items = list_split("train")
    test_items = list_split("test")

    y_all = [c for _, c in train_items]
    train_idx, val_idx = train_test_split(
        range(len(train_items)), test_size=0.15, random_state=RANDOM_STATE, stratify=y_all,
    )
    train_loader = DataLoader(PetDataset([train_items[i] for i in train_idx]),
                               batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(PetDataset([train_items[i] for i in val_idx]),
                             batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(PetDataset(test_items), batch_size=BATCH_SIZE, shuffle=False)

    torch.manual_seed(RANDOM_STATE)
    model = SmallCNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    best_val_acc, epochs_no_improve, best_state = 0.0, 0, None
    for epoch in range(1, MAX_EPOCHS + 1):
        model.train()
        for X, y in train_loader:
            X, y = X.to(device), y.to(device)
            optimizer.zero_grad()
            loss = criterion(model(X), y)
            loss.backward()
            optimizer.step()

        model.eval()
        correct, n = 0, 0
        with torch.no_grad():
            for X, y in val_loader:
                X, y = X.to(device), y.to(device)
                correct += (model(X).argmax(1) == y).sum().item()
                n += X.size(0)
        val_acc = correct / n

        if val_acc > best_val_acc:
            best_val_acc, epochs_no_improve = val_acc, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= PATIENCE:
                break

    model.load_state_dict(best_state)
    model.eval()
    all_preds, all_true = [], []
    with torch.no_grad():
        for X, y in test_loader:
            preds = model(X.to(device)).argmax(1).cpu().numpy()
            all_preds.extend(preds.tolist())
            all_true.extend(y.numpy().tolist())

    print(f"Test accuracy: {accuracy_score(all_true, all_preds):.3f}")
    print(classification_report(all_true, all_preds, target_names=["cat", "dog"]))
    print(confusion_matrix(all_true, all_preds))


if __name__ == "__main__":
    main()
```

*(The full file, delivered alongside this post, additionally writes `cnn_results.json` with the same fields `train_nn.py` records, so the two runs are directly comparable -- trimmed here for readability.)*

## Exactly what changed, step by step, against Part I

**Loading.** Part I's `load_split` ends in `.flatten()`, collapsing `(48, 48, 3)` into 6,912 numbers. This script's `PetDataset.__getitem__` keeps the `(3, 48, 48)` shape (channels-first, PyTorch's convention) all the way into the network.

**The network itself.** Three `Conv2d` + `ReLU` + `MaxPool2d` blocks replace Part I's two `Linear` (fully-connected) layers as the feature extractor. Each `Conv2d(in_channels, out_channels, kernel_size=3, padding=1)` learns `out_channels` different 3×3 filters over its input; `MaxPool2d(2)` halves height and width by taking the max of each 2×2 block. After three such blocks, the 48×48 image has become a 6×6 grid of 64 feature maps -- still spatially organised, just much smaller and far more abstract than raw pixels.

**Only the very last step flattens.** `nn.Flatten()` appears exactly once, immediately before the two small fully-connected layers that turn the final 64×6×6 = 2,304-number feature-map stack into 2 class scores. That's the one place this network resembles Part I's approach -- and by then, the flattening is happening to *learned features*, not raw pixels, so the spatial-adjacency information was already used, not thrown away.

**Training loop, written out explicitly.** `MLPClassifier.fit()` hides the epoch loop, the batching, and the early-stopping bookkeeping inside scikit-learn. PyTorch doesn't have a `.fit()` for arbitrary models, so this script writes the loop by hand: for each epoch, iterate over training batches, compute the loss, call `loss.backward()` (PyTorch's automatic differentiation working out every gradient via the chain rule, the same backpropagation math Part I's `MLPClassifier` runs internally), then `optimizer.step()` to apply the update. The early-stopping logic -- track the best validation accuracy, stop after `PATIENCE` epochs without improvement, roll back to the best checkpoint -- is the same idea as `early_stopping=True` / `n_iter_no_change=15` in Part I, just implemented explicitly instead of provided by the library.

## The network's parameters, and what each one controls

| Parameter | Value used | What it controls |
|---|---|---|
| Conv layers | `3→16→32→64` channels, `3×3` kernels, `padding=1` | Each layer learns more filters than the last (16, then 32, then 64), building from simple edge/colour detectors toward more abstract, composite features. `padding=1` keeps the feature map's height and width unchanged by the convolution itself, so only the pooling layers shrink it. |
| `MaxPool2d(2)` | after every conv block | Halves height and width (48→24→12→6), reducing computation and adding tolerance to small shifts in where a pattern appears. |
| Fully-connected head | `2,304 → 64 → 2` | Turns the final spatial feature maps into class scores -- the same job Part I's whole network did, now operating on compact, already-informative features instead of raw pixels. |
| `Dropout(0.3)` | between the two FC layers | Randomly zeroes 30% of that layer's activations during training only, a different overfitting guard than Part I's `alpha` (L2) regularisation -- common in CNNs because their fully-connected head can otherwise memorise the training set. |
| Optimiser | `Adam`, `lr=1e-3` | Identical choice to Part I, for a fair comparison. |
| Loss | `CrossEntropyLoss` | PyTorch's equivalent of the cross-entropy loss `MLPClassifier` uses internally in Part I. |
| Batch size | `32` | Same as Part I. |
| Early stopping | patience `15` epochs, max `60` | Same idea as Part I's `n_iter_no_change=15`; the cap is raised from Part I's 400 only because CNN epochs here are typically cheaper per-epoch on this small image size, not because more epochs were needed. |
| `random_state` / `manual_seed` | `42` | Same seed as Part I, for the data split; PyTorch's own seed for weight initialisation. |

## Results

```
Using device: cpu
Train pool: 21148 images, Validation: 3732 images, Test: 120 images
Total learnable parameters: 171,234
Stopped after 24 epochs (best validation checkpoint restored)

Validation accuracy (best epoch): 0.842
Test accuracy (never seen during training): 0.842

              precision    recall  f1-score   support

         cat       0.83      0.87      0.85        60
         dog       0.86      0.82      0.84        60

    accuracy                           0.84       120
   macro avg       0.84      0.84      0.84       120
weighted avg       0.84      0.84      0.84       120

Confusion matrix [[TN, FP], [FN, TP]] (0=cat, 1=dog):
[[52  8]
 [11 49]]
```

84.2% test accuracy -- 101 of 120 correct, both classes recognised well (86.7% cat recall, 81.7% dog recall, no lopsided bias). Against Part I's 63.3% on the identical 120-image test set, that's a 20.9 percentage-point jump, using 171,234 learnable parameters against Part I's 893,185 -- roughly a fifth as many. And it isn't a fluke of this particular test set: the validation accuracy (0.842, measured on a completely different 3,732-image slice, checked epoch by epoch during training) lands at essentially the same number as the test accuracy, which is what you'd expect from a genuine, well-generalising gain rather than one lucky pass through 120 images.

| | MLP (Part I) | CNN (Part II) |
|---|---|---|
| Test accuracy | 63.3% | **84.2%** |
| Validation accuracy | 64.0% | 84.2% |
| Learnable parameters | 893,185 | **171,234** |
| Cat recall / dog recall | 63% / 63% | 87% / 82% |
| Epochs to converge | 24 | 24 |

## Why the CNN performed better

Three things point at the same underlying explanation, and it's worth being precise about which one it is, since "CNNs are better at images" on its own is just restating the result, not explaining it.

**It's not more capacity.** If the CNN had simply been a bigger, more powerful model, the improvement would be less interesting -- more parameters usually helps, up to a point. Here it's the opposite: the CNN has roughly a fifth of the MLP's parameter count and still gets a 21-point higher score. Whatever the CNN is doing, it isn't "brute-forcing" the problem with more free parameters to fit.

**It's not overfitting dressed up as a win.** An architecture that overfits typically shows a gap between validation and test performance, or between training and validation performance, as it memorises quirks of whatever data it was checked against. The CNN's validation accuracy (84.2%, from the 3,732-image slice watched during training) and test accuracy (84.2%, from the 120 images neither model ever trained on) land on the same number. That consistency is what a genuine improvement in what the model *learned* looks like, not what memorisation looks like.

**It is the thing Part I named in advance: pixel adjacency.** Part I's "What an MLP does with an image" predicted exactly this failure mode before either script ran a single epoch -- a flattened network has no built-in way to know that two neighbouring pixels are neighbours, so it has to independently (re-)discover every local pattern (an edge, a patch of fur, the curve of an ear) at every possible position in the image, using unshared weights for each position. With 21,148 training images, that's not enough examples to learn "pointed ear" at every one of thousands of possible pixel locations independently. The CNN's convolutional filters are explicitly shared across every position by construction -- a single learned 3×3 edge detector gets applied everywhere the image, not relearned per-location -- so the same 21,148 images teach it far more per image, which is the direct mechanical reason 171,234 parameters outperform 893,185 here. This isn't a training artefact of this particular run; it's the structural difference the two scripts were built to isolate.

The one place this comparison should be read cautiously: both networks are still small and both are working from 48×48 downsampled images, so 84.2% is a demonstration of *why* convolution helps, not a benchmark of how good CNN-based cat/dog classification can get -- real systems using larger images, deeper networks, and pretrained backbones (transfer learning) push well past 95% on this exact task, as "The classic example" section back in Part I notes.

## What this comparison is actually testing

It's worth being precise about what changes between the two posts and what that isolates. Both networks see exactly the same 21,148-image training set, the same 3,732-image validation slice, the same 120-image held-out test set, the same image resolution, the same optimiser and learning rate, and materially the same early-stopping philosophy -- both even stopped at epoch 24. The only structural difference is whether the first layers of the network can see pixel adjacency (convolution) or not (flatten-first). The 20.9-point accuracy gap between Part I and Part II is therefore attributable to that one change, not to more data, a different test set, or a different optimiser -- which is what makes this a fair test of "does convolution help," rather than a comparison of two arbitrarily different setups.

## Sources

- PyTorch -- [pytorch.org](https://pytorch.org/) (open-source deep learning framework used for the CNN and training loop in this post)
- [Part I of this series](/blog/comp-science/how-neural-networks-learn-to-tell-a-cat-from-a-dog/) -- the MLP baseline, dataset, and test set this post compares against
- Kaggle -- [Dogs vs. Cats Redux: Kernels Edition](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition) (same dataset as Part I)
- All CNN accuracy/loss/confusion-matrix figures in this post: this project's own `train_cnn.py`, run against the same Kaggle Dogs vs. Cats data Part I uses

*Editorial note (draft): needs Bruce's sign-off before this goes live, and needs Part I's URL slug filled in above once that post is published (currently a guessed slug). `train_cnn.py` has now actually been run on Bruce's own Mac (native Terminal, outside the Cowork device bridge -- required, since a plain `pip install torch` through the bridge pulls multi-gigabyte NVIDIA CUDA packages meant for Linux GPU servers, and both `pytorch.org`'s CPU-only wheel index and kaggle.com itself are blocked by that bridge's governed network regardless), against the same downloaded Kaggle data and the same held-out test set as Part I, and the real numbers are in "Results" above -- 84.2% test accuracy vs. Part I's 63.3%, with a fifth of the parameters. Still open before publish: a real architecture/feature-map diagram, visualising what the trained filters actually picked up, would be a strong addition but isn't required to publish.*
