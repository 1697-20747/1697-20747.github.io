---
title: "How Neural Networks Learn to Tell a Cat From a Dog, Part I: A Plain Network"
subtitle: "A from-scratch, runnable walkthrough of image classification -- the entry point into how neural nets 'see' -- following scikit-learn's own supervised-learning method"
status: DRAFT
series: "How Neural Networks Learn to See (1 of 3)"
category: comp-science
date: 2026-09-13
tags: ["neural-networks", "machine-learning", "python", "scikit-learn", "image-classification", "computer-vision"]
showToc: true
tocopen: true
---

*This is a draft, part one of a three-part series. What's built and run below is image classification -- one label per image, "cat" or "dog." Part II takes the exact same data and swaps in a convolutional network (a CNN) to show, concretely, what that architecture change buys you. Part III goes one step further, fine-tuning a pretrained YOLO26 backbone on the same images.*

## What this post actually builds

A neural network that looks at a small photograph and outputs "cat" or "dog," built two ways at once: as a working explanation of the mechanics (what a neuron is, what a weight is, what "training" actually updates), and as a runnable Python script using scikit-learn's own workflow conventions. Every number quoted below -- accuracy, loss values, epoch counts -- comes from actually executing the script against real photographs, not from a textbook.

## The classic example, and where it came from

"Cats vs. dogs" isn't an arbitrary teaching example. It's a specific, well-documented dataset with an unusual origin: Microsoft Research's **Asirra** ("Animal Species Image Recognition for Restricting Access") project used it as a CAPTCHA -- a 2007 paper describes asking users to pick out the cats from a grid of 12 cat-and-dog photos, something humans got right 99.6% of the time in under 30 seconds but which was, at the time, hard for a computer. The images came from a partnership between Microsoft and Petfinder.com, drawn from a pool of roughly three million annotated adoption photos.((MachineLearningMastery, [How to Develop a Convolutional Neural Network to Classify Photos of Dogs and Cats](https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/), summarizing the Asirra paper and Kaggle competition details.)) In 2013, Kaggle turned it into a public competition -- 25,000 labelled training photos, 12,500 unlabelled test photos -- and it's been the standard first project for image classification ever since. The winner that year, using convolutional networks, hit roughly 98.9% accuracy; today it's genuinely a "hello world," with hand-built models comfortably clearing 80% and transfer learning pushing past 90%.((Same source as above.)) That's the same dataset used below.

## Following scikit-learn's method

The request behind this post was to follow the workflow at scikit-learn's [Supervised learning](https://scikit-learn.org/stable/supervised_learning.html) guide, which walks through roughly twenty families of algorithm (linear models, SVMs, trees, ensembles, and so on) using the same shape of code each time. Section 1.17 of that guide, [Neural network models (supervised)](https://scikit-learn.org/stable/modules/neural_networks_supervised.html), covers exactly one architecture: the **multi-layer perceptron** (MLP) -- a plain, fully-connected feed-forward network trained by backpropagation, exposed as `sklearn.neural_network.MLPClassifier`. That's the network built and trained below.

The shape of the code that scikit-learn's guide uses everywhere, MLP included, is the same five steps:

1. Load data into a 2-D array `X` (rows = samples, columns = features) and a label vector `y`.
2. Split into training and test sets with `train_test_split`, so the model is graded on data it never saw.
3. Wrap preprocessing and the estimator together in a `Pipeline`, most commonly a `StandardScaler` feeding the classifier.
4. Call `.fit(X_train, y_train)`.
5. Call `.predict(X_test)` and score it -- `classification_report`, `confusion_matrix`, `accuracy_score`.

Every one of those five steps appears, in order, in `train_nn.py` below. The only thing specific to *images* is what goes into `X` before step 1: pixel values, flattened into one long row per image.

## What an MLP does with an image (and what it can't)

An `MLPClassifier` has no idea it's looking at a picture. Step one of the pipeline is `img.flatten()` -- a 48×48 pixel image with 3 colour channels becomes a single row of 48×48×3 = 6,912 numbers, in a fixed order, and every spatial relationship between neighbouring pixels is thrown away as far as the network's architecture is concerned. The pixel at the top-left corner and the pixel at the bottom-right are just feature #1 and feature #6,912 -- adjacent columns in a spreadsheet, no more related to each other structurally than columns 1 and 500 of any other dataset scikit-learn might ingest.

A real object-detection or image-classification system almost always uses a **convolutional** neural network (CNN) instead, precisely because convolution preserves spatial structure. A CNN slides a small learned filter (say 3×3 pixels) across the image and computes a weighted sum at each position, producing a "feature map" that says *where* an edge, a blob of colour, or a texture pattern occurs. Stacking convolution layers lets the network build up a hierarchy -- edges, then textures, then shapes like "ear" or "paw," then whole-object patterns -- while pooling layers between them progressively shrink the map and make the detections more tolerant of the object shifting a few pixels left or right. Real detection networks (YOLO, SSD, Faster R-CNN and similar) bolt a second stage onto that same convolutional backbone: instead of one label for the whole image, they output a grid of candidate boxes, each with its own class score and four numbers describing a bounding box.

`sklearn.neural_network` doesn't implement convolution at all -- it's out of scope for that module, which is why the guide's neural-network section is a page, not a chapter. What it *can* do, and does well, is show every other piece of the puzzle with total transparency: forward pass, activation functions, loss, backpropagation, gradient descent, all in plain matrix multiplication you can inspect line by line. That trade-off -- give up spatial awareness, keep everything else inspectable -- is exactly why this is the right *first* network to build by hand, and Part II picks up this exact limitation and fixes it with a convolutional network on the same data.

## About the images

The code below expects a folder of JPEGs at `data/train/cats/`, `data/train/dogs/`, `data/test/cats/`, `data/test/dogs/`. The images are real photographs from Kaggle's Dogs vs. Cats dataset -- the same one described above -- sorted into that layout by `prepare_kaggle_dataset.py`.

## Building the population, and reserving a test set

Every supervised-learning problem starts with a **population**: every labelled example you could possibly train or test on. For this dataset, that's Kaggle's `train.zip`: 25,000 labelled photographs, 12,500 cats and 12,500 dogs -- already balanced by class, unlike datasets built by cataloguing breeds.((Kaggle, [Dogs vs. Cats Redux: Kernels Edition](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition) -- the same Asirra/Petfinder photo pool described above.))

A model is only as honest as the boundary between what it trained on and what it's graded on. `prepare_kaggle_dataset.py` draws that boundary *before* `train_nn.py` (or anything else) ever touches a single pixel:

```python
def sort_into_splits():
    random.seed(RANDOM_STATE)           # 42, same seed used everywhere in this project
    src = os.path.join(EXTRACT_DIR, "train")
    files = [f for f in os.listdir(src) if f.lower().endswith(".jpg")]

    cats = [f for f in files if f.lower().startswith("cat.")]
    dogs = [f for f in files if f.lower().startswith("dog.")]   # 12,500 of each

    random.shuffle(cats)
    random.shuffle(dogs)

    for label, pool in (("cats", cats), ("dogs", dogs)):
        test_files = pool[:N_TEST_PER_CLASS]    # first 60, after shuffling -- reserved
        train_files = pool[N_TEST_PER_CLASS:]   # everything else -- the training population
        ...
```

Three choices in that function are doing real work, each worth calling out on its own:

**Shuffle before slicing.** Kaggle's filenames are sequential (`cat.0.jpg` through `cat.12499.jpg`), and sequential IDs can quietly correlate with upload batch or photo source. `random.shuffle`, seeded, removes any such ordering before the split happens, and re-running the script reproduces the exact same 120 held-out files every time.

**A fixed count per class, not a fixed fraction of the whole.** `N_TEST_PER_CLASS = 60` is applied to the cat pool and the dog pool *separately* -- 60 cats and 60 dogs, 120 total, a perfectly balanced test set. This dataset's population happens to already be balanced 12,500/12,500, so this choice isn't rescuing the test set from a skewed population the way it would on an unevenly catalogued dataset -- but it's still the right default: it keeps the test set's shape fixed and predictable regardless of what the training pool looks like, which matters once Part II runs a different architecture against the identical 120 images for a fair comparison.

**Reserved once, touched once.** These 120 files are never seen by `train_nn.py` until the single `clf.predict(X_test)` call at the very end, after training and every weight update are already finished. That's what makes the resulting accuracy figure honest rather than optimistic: the network has had literally zero opportunity to memorise anything about these specific 120 photographs.

What's left after that reservation -- 12,440 cats and 12,440 dogs, 24,880 images -- becomes the training population `train_nn.py` receives. That script draws a second, different boundary inside *that* pool, for a different reason: `train_test_split(..., test_size=0.15, stratify=y_train_full)` carves off 15% of those 24,880 images as a validation slice, leaving the rest for actual weight updates. Unlike the test reservation, this split is `stratify`d -- kept proportional to the training pool -- because its job is different: the validation slice is watched *during* training, epoch by epoch, purely to decide when to stop (the early-stopping mechanism in step 8 of "Exactly what happens when you run it"). Three pools, three separate jobs: most of the 24,880 images update weights, roughly 15% of them decide when to stop, and 120 -- and only those 120 -- produce the number reported as the model's accuracy.

## The training script: `train_nn.py`

This is the file that actually follows scikit-learn's supervised-learning method end to end. Image loading uses `skimage.io` (scikit-image, another open-source library) purely to read pixels into a numpy array -- no computer-vision logic of its own; everything past that line is five-step scikit-learn boilerplate.

```python
"""
train_nn.py
------------
Trains a feed-forward neural network (an sklearn MLPClassifier, i.e. a
Multi-Layer Perceptron with backpropagation) from scratch -- random
initial weights, no pretrained model -- to tell cat images from dog
images.

Follows the workflow scikit-learn's own "Supervised learning" guide uses
throughout (https://scikit-learn.org/stable/supervised_learning.html),
whose neural-network section is
https://scikit-learn.org/stable/modules/neural_networks_supervised.html:

    1. load data as a flat (n_samples, n_features) array + a label vector
    2. train_test_split
    3. wrap preprocessing + estimator in a Pipeline
    4. StandardScaler to zero-mean/unit-variance the features
    5. fit the estimator
    6. predict on held-out data and score it with classification_report /
       confusion_matrix
"""
import os
import json
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.color import gray2rgb, rgba2rgb
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMG_SIZE = 48
RANDOM_STATE = 42


def load_split(split):
    """Read every image under data/<split>/{cats,dogs}/ into (X, y)."""
    X, y, paths = [], [], []
    for label, class_id in (("cats", 0), ("dogs", 1)):
        folder = os.path.join(DATA_DIR, split, label)
        for fname in sorted(os.listdir(folder)):
            path = os.path.join(folder, fname)
            img = imread(path)                       # (H, W, 3) uint8 array -- real JPEGs vary: gray, RGBA, etc.
            if img.ndim == 4 and img.shape[0] == 1:
                img = img[0]
            if img.ndim == 2:
                img = gray2rgb(img)
            elif img.shape[2] == 4:
                img = rgba2rgb(img)
            img = resize(img, (IMG_SIZE, IMG_SIZE, 3), anti_aliasing=True)  # -> float [0,1]
            X.append(img.flatten())                  # (H*W*3,) 1-D feature vector
            y.append(class_id)
            paths.append(path)
    return np.array(X), np.array(y), paths


def main():
    X_train_full, y_train_full, _ = load_split("train")
    X_test, y_test, test_paths = load_split("test")

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full,
        test_size=0.15, random_state=RANDOM_STATE, stratify=y_train_full,
    )

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation="relu",
            solver="adam",
            alpha=1e-4,
            batch_size=32,
            learning_rate_init=1e-3,
            max_iter=400,
            early_stopping=True,
            n_iter_no_change=15,
            validation_fraction=0.15,
            random_state=RANDOM_STATE,
        )),
    ])

    clf.fit(X_train, y_train)

    mlp = clf.named_steps["mlp"]
    val_acc = accuracy_score(y_val, clf.predict(X_val))
    y_pred = clf.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)

    print(f"Validation accuracy: {val_acc:.3f}")
    print(f"Test accuracy:       {test_acc:.3f}\n")
    print(classification_report(y_test, y_pred, target_names=["cat", "dog"]))
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()
```

*(The version actually executed for this post additionally writes `results.json`, the loss curve, and the confusion matrix array to disk -- trimmed here for readability; the full file is included with the other project files.)*

## Exactly what happens when you run it

Step by step, in the order the code executes:

**1. Image loading (`skimage.io.imread`).** Each JPEG is read into a NumPy array of shape `(H, W, 3)` -- height, width, and three colour channels (red, green, blue), each an integer 0-255.

**2. Resize (`skimage.transform.resize`).** Every image is forced to exactly 48×48 so every feature vector has the same length; `resize` also converts to floating-point values in `[0, 1]` as a side effect, which is why the input has already left 0-255 integer space before scaling ever runs.

**3. Flatten.** `.flatten()` reshapes the `(48, 48, 3)` array into a single row of 6,912 numbers, in a fixed raster order (row 0's red, green, blue, then pixel 1's red, green, blue, and so on). This row is the entire input the network will ever see for that image -- one row per image, stacked into the `X` matrix scikit-learn expects.

**4. Train/validation split (`train_test_split`).** 15% of the 24,880-image training pool (roughly 3,732 images) is set aside as a validation set the optimiser watches but never trains on directly -- used only to decide when to stop (step 7).

**5. Scaling (`StandardScaler`).** For each of the 6,912 pixel-channel features, subtract that feature's mean across the training set and divide by its standard deviation. Raw pixel values sit in a narrow, always-positive 0-1 range; gradient descent converges faster and more reliably when every input feature is centred around zero with comparable spread, which is why this step exists in almost every scikit-learn pipeline, image data or not.

**6. Forward pass.** For a single training image, its scaled 6,912-number vector is multiplied by a 6,912×128 weight matrix (plus a bias per hidden unit) to produce 128 numbers -- one per first-hidden-layer neuron. Each of those 128 numbers is passed through the ReLU activation function, `f(x) = max(0, x)`, which zeroes out negative values and passes positive ones through unchanged; this non-linearity is what lets the network represent more than a straight line through pixel space. The resulting 128 activated numbers are multiplied by a second, 128×64 weight matrix into the second hidden layer, ReLU'd again, and finally multiplied by a 64×2 weight matrix into two raw output scores, one for "cat" and one for "dog." A softmax function converts those two raw scores into two probabilities that sum to 1.

**7. Loss and backpropagation.** The network's two output probabilities are compared against the true label using cross-entropy loss (high when the model was confident and wrong, low when it was confident and right). Backpropagation then computes, via the chain rule, exactly how much each of the roughly 893,000 individual weights and biases in the network contributed to that error. The `adam` solver uses those gradients to nudge every weight slightly in the direction that would have reduced the error, scaled by the learning rate.

**8. Epochs and early stopping.** Steps 6-7 repeat over the whole training set, in shuffled batches of 32 images, once per epoch. After each epoch, accuracy on the held-out validation slice from step 4 is checked; because `early_stopping=True`, training stops once 15 consecutive epochs (`n_iter_no_change`) pass without that validation score improving, rather than always running the full `max_iter=400`.

**9. Prediction and scoring.** Once training stops, the exact same scaling learned in step 5 (never refit) is applied to the untouched 120-image test set, a forward pass (step 6 only, no more weight updates) produces a probability for each image, and the higher of the two probabilities becomes the predicted label. `classification_report` and `confusion_matrix` compare those predictions against the true labels the network never saw during training.

## The network's parameters, and what each one controls

| Parameter | Value used | What it controls |
|---|---|---|
| `hidden_layer_sizes` | `(128, 64)` | Two hidden layers, 128 neurons then 64. More neurons/layers can represent more complex functions but risk overfitting a dataset this small. |
| `activation` | `relu` | The non-linearity applied after each hidden layer's weighted sum. Without one, stacking layers would collapse to a single linear function no matter how many layers there are. |
| `solver` | `adam` | The optimisation algorithm that turns gradients into weight updates. Adam adapts its effective step size per-parameter and is scikit-learn's own recommended default for anything beyond toy-sized data. |
| `alpha` | `0.0001` | L2 regularisation strength -- a penalty added to the loss proportional to the sum of squared weights, discouraging any single weight from growing very large and overfitting. |
| `batch_size` | `32` | Number of images averaged into a single gradient estimate before each weight update, rather than updating after every single image (noisy) or the whole dataset at once (slow, memory-heavy). |
| `learning_rate_init` | `0.001` | The initial size of each weight update step. Too large and training diverges or oscillates; too small and it takes forever to converge. |
| `max_iter` | `400` | The hard cap on training epochs, reached only if early stopping doesn't trigger first. |
| `early_stopping` / `n_iter_no_change` / `validation_fraction` | `True` / `15` / `0.15` | Reserves 15% of the training data purely to monitor progress, and halts training once 15 straight epochs produce no improvement on it -- the mechanism described in step 8 above. |
| `random_state` | `42` | Fixes every source of randomness (initial weights, batch shuffling, the validation split) so the run is exactly reproducible. |

Total learnable parameters: 6,912×128 + 128 (first layer weights + biases) + 128×64 + 64 (second layer) + 64×2 + 2 (output layer) = **893,185** individual numbers, every one of them tuned by nothing but the backpropagation loop above, starting from random values.

## Results

```
Train pool: 21148 images, 6912 features each
Validation set: 3732 images
Held-out test set: 120 images
Training MLPClassifier ...
Stopped after 24 epochs (converged=True)

Validation accuracy: 0.640
Test accuracy:       0.633

              precision    recall  f1-score   support

         cat       0.63      0.63      0.63        60
         dog       0.63      0.63      0.63        60

    accuracy                           0.63       120
   macro avg       0.63      0.63      0.63       120
weighted avg       0.63      0.63      0.63       120

Confusion matrix [[TN, FP], [FN, TP]] (0=cat, 1=dog):
[[38 22]
 [22 38]]
```

63.3% test accuracy on 120 real photographs the network never trained on -- clearly above the 50% a coin flip would get, so the network genuinely learned something from 21,148 flattened pixel vectors, but a long way from what a CNN gets on the identical data (Part II: 84.2%). Because Kaggle's Dogs vs. Cats data is already class-balanced (12,500 cats, 12,500 dogs), the earlier concern about a skewed training population biasing predictions toward one class doesn't apply here -- and the confusion matrix confirms it: 38/22 for cats, 22/38 for dogs, a symmetric error pattern, not a lopsided one. This result isn't a data-imbalance artefact; it's the flattening bottleneck described in "What an MLP does with an image" showing up directly in the numbers. Part II keeps every other variable fixed -- same 21,148/3,732/120 split, same optimiser, same epoch count even (24) -- and changes only the architecture.

## Graphical explanation: how one image actually moves through the network

Reading left to right, mapped onto the code above: a real input image "unrolls" into the input layer, one node per pixel-channel value (6,912 of them). Every connection crossing from one layer to the next is one learned weight -- 6,912×128 of them between the input and the first hidden layer alone. Each hidden-layer node performs the weighted-sum-then-ReLU computation from step 6 above; the two output nodes on the right are `P(cat)` and `P(dog)`, the two numbers softmax produces, which is what actually gets compared to the true label and what the confusion matrix above is built from.

## From here to real object detection

Everything above answers "is this whole image a cat or a dog," which is the necessary first half of understanding how neural networks process visual data. A real detection system built on these same ideas differs in three specific ways, each worth naming precisely rather than gesturing at:

1. **Convolution instead of flattening.** Instead of throwing away pixel adjacency in step 3 above, a convolutional layer slides a small filter (learned, not hand-designed) across the image and produces a feature map that preserves *where* a pattern occurred. Stacking several such layers, usually with pooling layers shrinking the map in between, builds up from edges to textures to object parts to whole objects -- the hierarchy sketched earlier in "What an MLP does with an image." Part II builds exactly this, on the same data, and reports what it changes.
2. **Many predictions per image, not one.** A classifier like the one above outputs exactly one label for the entire image. A detector divides the image into a grid (or proposes candidate regions) and produces a separate class score *and* a bounding box for each cell or region, so an image with three dogs and a cat in it can report all four, each with its own location.
3. **A second loss term for location.** Training a classifier only ever penalises a wrong label. Training a detector additionally penalises a badly-placed box -- typically via something like Intersection-over-Union between the predicted and true boxes -- so the network is optimised for *where*, not only *what*.

The scikit-learn `neural_network` module used throughout this post implements none of the three; that's a deliberate design boundary of the library, not an oversight, and it's why frameworks with GPU-accelerated convolution (PyTorch, TensorFlow/Keras) are where real detection work happens.

## Practical application: this same idea, in a real navigation stack

The theory above isn't confined to sorting pet photos, and there's a live, running example of the next step up rather than a hypothetical one: `apex_ros`, an autonomous RC vehicle build (ROS 2, previously DonkeyCar-based as APEX-DC) documented in this site's own comp-science build log. Swap "cat vs. dog" for "what's on the track ahead," and the same shape of problem applies -- a CNN backbone doing what this post's flattening step deliberately doesn't (preserving spatial position), feeding a detection head that outputs boxes and classes rather than one whole-image label, so the vehicle knows not just *what* it's looking at but *where*.

As of the most recent build-log entries, that detection step is real and running -- `yolo26n` performing object detection directly on the Raspberry Pi 5's own CPU -- not a future plan. What *is* still an open, explicitly-parked question in that same log is almost exactly the "why not just use a bigger network" trade-off this post raises: running detection on the Pi 5's general-purpose cores competes with everything else the robot's software needs those same four cores for. The option under consideration is offloading detection entirely onto a small, cheap companion board built for nothing else -- a Luckfox Pico Ultra, a Rockchip RV1106-based Linux board with its own small NPU (1 TOPS INT8) -- so the Pi 5 receives only finished detections and positions rather than paying for the inference itself. It's parked rather than shipped for a concrete, checkable reason, not a vague one: the RV1106 is INT8-only, and the current YOLO26-to-RKNN export path has an open, unresolved bug (the newer YOLO26 architecture drops the DFL+NMS postprocessing older YOLO versions shipped with, and that conversion currently segfaults at inference, while the equivalent YOLOv8/v11 export works). Same underlying idea as the "flatten vs. convolve" trade-off in this post -- pick the right tool for what the hardware actually needs to do -- playing out with real silicon and a real, still-open bug report attached, rather than settled in the abstract.((`apex_ros` build log, this site -- [Same Shape, Different Paper](https://1697-20747.github.io/blog/comp-science/same-shape-different-paper/) for the current architecture (`yolo26n` object detection is labeled "planned" as of that post, three posts before it went live); [Not Every Pixel Needs an Answer](https://1697-20747.github.io/blog/comp-science/not-every-pixel-needs-an-answer/) for the Luckfox Pico Ultra option and the specific RKNN/YOLO26 export blocker, both as of that post's date.))

## Running it yourself

Requires a free Kaggle account, an API key, and having accepted the competition rules once on the [competition page](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition) (the Rules tab) -- the API returns a 403 without that, even with a valid key:

```bash
pip install kaggle pillow numpy scikit-image scikit-learn
python3 prepare_kaggle_dataset.py   # downloads via the Kaggle API, sorts into data/train/{cats,dogs}/, data/test/{cats,dogs}/
python3 train_nn.py                 # trains the MLP, prints the metrics shown above
```

Every random source is seeded (`RANDOM_STATE = 42` throughout, in `prepare_kaggle_dataset.py` as well), so re-running should reproduce the same split and, modulo floating-point nondeterminism in the solver, close to the same numbers reported above.

---

### Sources

- MachineLearningMastery -- [How to Develop a Convolutional Neural Network to Classify Photos of Dogs and Cats](https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/) (Asirra/Petfinder/Microsoft origin story, 2013 Kaggle competition numbers and winning accuracy, benchmark CNN/transfer-learning accuracy figures)
- Kaggle -- [Dogs vs. Cats Redux: Kernels Edition](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition) (dataset: 25,000 labelled training photographs, 12,500 cats / 12,500 dogs)
- scikit-learn -- [Supervised learning](https://scikit-learn.org/stable/supervised_learning.html) (the guide this post's code structure follows)
- scikit-learn -- [Neural network models (supervised)](https://scikit-learn.org/stable/modules/neural_networks_supervised.html) (MLPClassifier documentation: architecture, parameters, defaults)
- All accuracy/loss/confusion-matrix figures in this post: this project's own `train_nn.py`, run against the Kaggle Dogs vs. Cats data via `prepare_kaggle_dataset.py`
- `apex_ros` build log, this site -- [Same Shape, Different Paper](https://1697-20747.github.io/blog/comp-science/same-shape-different-paper/) and [Not Every Pixel Needs an Answer](https://1697-20747.github.io/blog/comp-science/not-every-pixel-needs-an-answer/) (source for the "Practical application" section's navigation example)

*Editorial note (draft): needs Bruce's sign-off before this goes live. Status as of this pass: all synthetic-data content has been removed -- this post is real photographs only, start to finish, sourced from Kaggle's Dogs vs. Cats (switched from the Oxford-IIIT Pet Dataset, a better fit anyway since "The classic example" section already centres on Kaggle's history). `prepare_kaggle_dataset.py` and `train_nn.py` have now actually been run, on Bruce's own Mac (native Terminal, outside the Cowork device bridge -- required, since neither Kaggle's API nor a plain `pip install torch` are reachable through that bridge's governed network), and the real numbers are in "Results" above. Still open before publish: (1) the diagram in "Graphical explanation" is prose-only -- a real rendered figure (built from an actual sample image and the trained weights) would strengthen it but isn't required; (2) four sample test predictions are saved in `sample_predictions.json` alongside the other result files, not yet turned into a figure. Part II (`draft-neural-networks-cats-dogs-part2-cnn.md`) is written, run, and ready alongside this post -- same data, same split, same test set, CNN architecture, 84.2% test accuracy vs. this post's 63.3%.*
