---
title: "How Neural Networks Learn to Tell a Cat From a Dog"
date: 2026-09-13T09:00:00Z
lastmod: 2026-10-11T15:00:00Z
draft: false
categories: ["comp-science"]
tags: [neural-networks, machine-learning, python, scikit-learn, pytorch, image-classification, computer-vision, YOLO]
description: "The same 25,000 Kaggle cat and dog photos, four ways: a scikit-learn neural network, the identical network in PyTorch, a small convolutional network, and a pretrained YOLOv8 -- every number from code you can run."
showToc: true
tocopen: false
cover:
  image: "/images/comp-science/nn-cats-dogs-kaggle-collage.jpg"
  alt: "Grid of 16 cat photos and 16 dog photos from the Kaggle Dogs vs. Cats test set used in this post"
  caption: "32 of the 120 held-out photos every model below was scored on."
---

*Rewritten 11 October 2026: one dataset (Kaggle Dogs vs. Cats), shorter, and with a
PyTorch run added. Every number below comes from running the code shown, as written.*

Telling a cat photo from a dog photo is the "hello world" of image classification:
one label per image. (Object *detection* -- drawing a box around where the animal is
-- builds on the same machinery, and comes up at the end.) This post trains three
networks from scratch and tests one pretrained network, all on the same photos, to
show what actually makes the difference.

## The data

Kaggle's **Dogs vs. Cats** competition (2013) used 25,000 labelled photos from the
Asirra dataset that Microsoft Research built with Petfinder.com: 12,500 cats and 12,500
dogs, named `cat.0.jpg`, `dog.0.jpg` and so on. Download `train.zip` from Kaggle (a free
account is needed, and you accept the competition rules once); this post used the
*Dogs vs. Cats Redux* edition's copy.

`prepare_data.py` holds back 60 cats and 60 dogs as a test set that no model ever
trains on, shrinks every photo to 48 x 48 pixels, and saves the pixels once so the
training scripts start quickly:

```python
"""Split Kaggle's Dogs vs. Cats train.zip and cache every photo as 48x48 pixels.

Usage: python prepare_data.py path/to/train.zip
Writes test_photos/{cats,dogs}/ (the 120 held-out photos, for YOLOv8 later)
and pets48.npz (pixel arrays + labels for training and testing).
"""
import io
import random
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

IMG_SIZE = 48
TEST_PER_CLASS = 60
SEED = 42

archive = zipfile.ZipFile(sys.argv[1])
names = sorted(n for n in archive.namelist() if n.endswith(".jpg"))
cats = [n for n in names if Path(n).name.startswith("cat.")]
dogs = [n for n in names if Path(n).name.startswith("dog.")]
random.Random(SEED).shuffle(cats)
random.Random(SEED).shuffle(dogs)
print(f"{len(cats)} cat photos, {len(dogs)} dog photos")


def pixels(name):
    img = Image.open(io.BytesIO(archive.read(name))).convert("RGB")
    return np.asarray(img.resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR))


splits = {"train": ([], []), "test": ([], [])}
for label, (cls, pool) in enumerate([("cats", cats), ("dogs", dogs)]):
    for i, name in enumerate(pool):
        split = "test" if i < TEST_PER_CLASS else "train"
        splits[split][0].append(pixels(name))
        splits[split][1].append(label)  # 0 = cat, 1 = dog
        if split == "test":  # keep the full-size test photos for YOLOv8
            out = Path("test_photos") / cls / Path(name).name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(archive.read(name))

np.savez_compressed(
    "pets48.npz",
    X_train=np.stack(splits["train"][0]), y_train=np.array(splits["train"][1]),
    X_test=np.stack(splits["test"][0]), y_test=np.array(splits["test"][1]),
)
print(f"train: {len(splits['train'][1])} photos, test: {len(splits['test'][1])} photos -> pets48.npz")
```

Setup (Python 3.10 or newer) and the first step:

```bash
python3 -m venv venv && source venv/bin/activate
pip install numpy pillow scikit-learn torch ultralytics matplotlib
python prepare_data.py ~/Downloads/train.zip
```

That gives 24,880 training photos and the 120 test photos, in about 25 seconds.

## 1. A neural network in scikit-learn

The simplest neural network is a **multi-layer perceptron** (MLP). It doesn't see an
image at all: each 48 x 48 colour photo is flattened into one row of 6,912 numbers
(48 x 48 x 3), and every number connects to every neuron in the first layer. Two
hidden layers (128 and 64 neurons) feed one output: cat or dog. Training adjusts the
893,000 connection weights to reduce the error, a batch of 32 photos at a time, and
stops once accuracy on a held-back 15% of the training photos stops improving.

```python
"""A fully connected neural network (MLP) in scikit-learn, trained from scratch.

Every 48x48 photo is flattened into one row of 6,912 numbers (48*48*3):
the network never sees the image as a grid. Needs pets48.npz from
prepare_data.py.
"""
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data = np.load("pets48.npz")
X_train = data["X_train"].reshape(len(data["X_train"]), -1).astype(np.float32) / 255
X_test = data["X_test"].reshape(len(data["X_test"]), -1).astype(np.float32) / 255
y_train, y_test = data["y_train"], data["y_test"]

model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(128, 64),  # two hidden layers
        alpha=1e-4,                    # L2 weight penalty
        batch_size=32,
        learning_rate_init=1e-3,       # Adam optimiser (the default solver)
        early_stopping=True,           # holds back 15% of training data,
        validation_fraction=0.15,      # stops when its accuracy stalls
        n_iter_no_change=10,
        max_iter=200,
        random_state=42,
    ),
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
mlp = model[-1]
print(f"epochs: {mlp.n_iter_}, best validation accuracy: {mlp.best_validation_score_:.3f}")
print(f"test accuracy: {accuracy_score(y_test, pred):.3f}")
print("confusion matrix (rows = true cat/dog, columns = predicted cat/dog):")
print(confusion_matrix(y_test, pred))
```

```text
$ python sklearn_mlp.py
epochs: 25, best validation accuracy: 0.670
test accuracy: 0.692
confusion matrix (rows = true cat/dog, columns = predicted cat/dog):
[[44 16]
 [21 39]]
```

**69.2%** on the test photos: better than a coin flip, but it misses almost a third.
It has to learn "ear" separately at every pixel position an ear could appear in.

## 2. The same network in PyTorch

scikit-learn's `MLPClassifier` is a fixed design. **PyTorch**, the open-source
deep-learning framework started at Meta and now run by the PyTorch Foundation, lets
you build any network layer by layer, and runs it on a GPU (here the Mac's, via
`mps`). It's also what most modern vision models are built on, including YOLOv8 in
step 4.

To check that the framework isn't what matters, `torch_models.py mlp` rebuilds the
scikit-learn network exactly -- 6,912 -> 128 -> 64 -> 2, ReLU, Adam, the same learning
rate, weight penalty, batch size and early-stopping rule -- on the same photos:

```python
"""The same task in PyTorch: the scikit-learn MLP rebuilt, then a small CNN.

Same photos, same 48x48 size, same held-out test set, same optimiser
settings as sklearn_mlp.py. Needs pets48.npz from prepare_data.py.
Usage: python torch_models.py mlp   or   python torch_models.py cnn
"""
import sys

import numpy as np
import torch
from torch import nn
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

torch.manual_seed(42)
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

data = np.load("pets48.npz")
# PyTorch wants images as (count, channels, height, width), values 0-1
X = torch.tensor(data["X_train"]).permute(0, 3, 1, 2).float() / 255
X_test = torch.tensor(data["X_test"]).permute(0, 3, 1, 2).float() / 255
y = torch.tensor(data["y_train"])
y_test = data["y_test"]
# hold back 15% for early stopping, like scikit-learn's early_stopping=True
i_train, i_val = train_test_split(np.arange(len(y)), test_size=0.15, random_state=42, stratify=y)
mean, std = X[i_train].mean(dim=(0, 2, 3), keepdim=True), X[i_train].std(dim=(0, 2, 3), keepdim=True)
X, X_test = (X - mean) / std, (X_test - mean) / std  # standardise, like StandardScaler

if sys.argv[1:] == ["mlp"]:
    # scikit-learn's MLPClassifier(hidden_layer_sizes=(128, 64)), layer for layer
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(48 * 48 * 3, 128), nn.ReLU(),
        nn.Linear(128, 64), nn.ReLU(),
        nn.Linear(64, 2),
    )
else:
    # a small convolutional network: it keeps the image as a grid and
    # learns small filters that slide over it
    def block(c_in, c_out):
        return nn.Sequential(nn.Conv2d(c_in, c_out, 3, padding=1), nn.BatchNorm2d(c_out),
                             nn.ReLU(), nn.MaxPool2d(2))
    model = nn.Sequential(
        block(3, 32), block(32, 64), block(64, 128),  # 48 -> 24 -> 12 -> 6 pixels
        nn.Flatten(), nn.Dropout(0.3),
        nn.Linear(128 * 6 * 6, 128), nn.ReLU(), nn.Linear(128, 2),
    )
model = model.to(device)
print(f"{sum(p.numel() for p in model.parameters()):,} parameters on {device}")

optimiser = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
loss_fn = nn.CrossEntropyLoss()


def predict(images):
    model.eval()
    with torch.no_grad():
        return torch.cat([model(images[i:i + 512].to(device)).argmax(1).cpu()
                          for i in range(0, len(images), 512)]).numpy()


best, best_state, stale = 0.0, None, 0
for epoch in range(1, 201):
    model.train()
    for batch in torch.randperm(len(i_train)).split(32):
        idx = i_train[batch.numpy()]
        optimiser.zero_grad()
        loss = loss_fn(model(X[idx].to(device)), y[idx].to(device))
        loss.backward()
        optimiser.step()
    val_acc = accuracy_score(y[i_val].numpy(), predict(X[i_val]))
    print(f"epoch {epoch}: validation accuracy {val_acc:.3f}")
    if val_acc > best:
        best, stale = val_acc, 0
        best_state = {k: v.clone() for k, v in model.state_dict().items()}
    else:
        stale += 1
        if stale == 10:  # same stopping rule as n_iter_no_change=10
            break

model.load_state_dict(best_state)
pred = predict(X_test)
print(f"best validation accuracy: {best:.3f}")
print(f"test accuracy: {accuracy_score(y_test, pred):.3f}")
print("confusion matrix (rows = true cat/dog, columns = predicted cat/dog):")
print(confusion_matrix(y_test, pred))
# save the trained network (and the standardisation it expects) for gradcam.py
torch.save({"weights": best_state, "mean": mean, "std": std},
           "mlp.pt" if sys.argv[1:] == ["mlp"] else "cnn.pt")
```

```text
$ python torch_models.py mlp
893,250 parameters on mps
epoch 1: validation accuracy 0.630
...
epoch 40: validation accuracy 0.659
best validation accuracy: 0.672
test accuracy: 0.633
confusion matrix (rows = true cat/dog, columns = predicted cat/dog):
[[38 22]
 [22 38]]
```

**63.3%** on test, against 69.2% for scikit-learn. That gap is noise, not a
difference between frameworks: their validation accuracy, measured on 3,732 photos, is
practically identical (67.2% against 67.0%). With only 120 test photos, one standard
error is about four percentage points either way. Same network, same result.

## 3. Change the network, not the framework: a small CNN

`python torch_models.py cnn` swaps the MLP for a small **convolutional neural
network** (CNN) -- same data, same training rules. A CNN keeps the photo as a grid
and learns small 3 x 3 filters that slide across the whole image, so a pattern learned
in one place (an edge, an eye, fur texture) is recognised anywhere. Three blocks of
filters shrink the image from 48 to 24, 12, then 6 pixels while building up from edges
to textures to parts.

```text
$ python torch_models.py cnn
683,906 parameters on mps
epoch 1: validation accuracy 0.790
...
epoch 32: validation accuracy 0.880
best validation accuracy: 0.886
test accuracy: 0.908
confusion matrix (rows = true cat/dog, columns = predicted cat/dog):
[[53  7]
 [ 4 56]]
```

**90.8%** -- with *fewer* parameters than the MLP (684,000 against 893,000). It
took about 8 minutes on an M2 Pro. The architecture made the difference, not the
size and not the framework.

### What the CNN looked at

Here is, for each class, the brightest test photo the CNN classified correctly with
at least 99% confidence, with the parts it used kept bright and the rest dimmed:

![Two test photos with the regions the CNN used kept bright: two kittens classified as cat at 100%, with the evidence on their faces and ears; a beagle classified as dog at 100%, with the evidence running from its head and ear down to its chest](/images/comp-science/nn-cats-dogs-kaggle-gradcam.png)

**How it reached its answer (inference):**

1. The photo is shrunk to 48 x 48 pixels, scaled to 0-1 and standardised with the
   training photos' mean and spread -- exactly as in training.
2. Three convolution blocks run over it: 32, then 64, then 128 learned 3 x 3 filters,
   each block followed by pooling, so the 48 x 48 image becomes 24 x 24, 12 x 12, then
   6 x 6 grids of increasingly abstract features (edges, then textures, then parts).
3. The final 6 x 6 x 128 grid is flattened into 4,608 numbers and passed through two
   fully connected layers to give **Y**: one score for cat, one for dog. The bigger
   score is the answer; softmax turns the pair into a probability. The kittens scored
   Y = [3.98, -4.92] (100% cat); the beagle Y = [-5.30, 5.41] (100% dog).

**How the picture was made (Grad-CAM):** take the winning score in Y and work out how
much each of the 128 feature maps at the 12 x 12 stage pushed it up (its gradient),
weight each map by that, add them, and keep only the positive evidence. That 12 x 12
map is stretched back over the photo: brighter means it counted more. For the kittens,
the strongest cells are their faces and ears; the blanket and cushion barely count.
For the beagle, the evidence runs down a column from its head and ear to its chest,
while the wall and floor are dimmed. (Not every photo is this clean: on some, a
network this small also leans on the background.)

```python
"""Which parts of a photo did the CNN use for its answer? (Grad-CAM)

The CNN's output Y is two scores, one for cat and one for dog; the bigger one
is the answer, and softmax turns the pair into a probability. Grad-CAM traces
the winning score back to the last convolutional block -- 128 feature maps on
a 12 x 12 grid over the photo -- weights each map by how much it pushed the
score up, and keeps the positive evidence. Needs cnn.pt from
`python torch_models.py cnn` and test_photos/ from prepare_data.py.
Usage: python gradcam.py [photo.jpg ...]   (default: for each class, the
brightest test photo it classifies correctly with at least 99% confidence)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from PIL import Image


def block(c_in, c_out):  # the same CNN as torch_models.py
    return nn.Sequential(nn.Conv2d(c_in, c_out, 3, padding=1), nn.BatchNorm2d(c_out),
                         nn.ReLU(), nn.MaxPool2d(2))


model = nn.Sequential(
    block(3, 32), block(32, 64), block(64, 128),
    nn.Flatten(), nn.Dropout(0.3),
    nn.Linear(128 * 6 * 6, 128), nn.ReLU(), nn.Linear(128, 2),
)
saved = torch.load("cnn.pt", map_location="cpu")
model.load_state_dict(saved["weights"])
model.eval()

features = {}  # the third block's ReLU output: 128 maps of 12 x 12
model[2][2].register_forward_hook(lambda module, inp, out: features.update(maps=out))

def explain(path):
    """Run one photo through the CNN; return its scores Y, answer, probability, evidence map."""
    photo = Image.open(path).convert("RGB")
    x = torch.tensor(np.asarray(photo.resize((48, 48), Image.BILINEAR))).permute(2, 0, 1)[None].float() / 255
    x = (x - saved["mean"].cpu()) / saved["std"].cpu()
    y = model(x)[0]                       # Y: [cat score, dog score]
    answer = int(y.argmax())
    maps = features["maps"]
    maps.retain_grad()
    y[answer].backward()                  # how does each feature change the winning score?
    weights = maps.grad.mean(dim=(2, 3), keepdim=True)
    cam = torch.relu((weights * maps).sum(1))[0].detach()   # 12 x 12 evidence map
    return photo, y.detach(), answer, torch.softmax(y, 0)[answer].item(), cam / cam.max()


if sys.argv[1:]:
    photos = [Path(p) for p in sys.argv[1:]]
else:  # per class: the brightest photo it gets right with at least 99% confidence
    photos = []
    for folder, label in (("cats", 0), ("dogs", 1)):
        sure = [p for p in sorted(Path("test_photos", folder).glob("*.jpg"))
                if explain(p)[2] == label and explain(p)[3] >= 0.99]
        photos.append(max(sure, key=lambda p: np.asarray(Image.open(p).convert("L")).mean()))

fig, axes = plt.subplots(1, len(photos), figsize=(3.6 * len(photos), 3.9))
for ax, path in zip(np.atleast_1d(axes), photos):
    photo, y, answer, prob, cam = explain(path)
    label = ["cat", "dog"][answer]
    print(f"\n{path.name}: Y = [cat {y[0]:.2f}, dog {y[1]:.2f}] -> {label} ({prob:.0%})")
    cell_w, cell_h = photo.width / 12, photo.height / 12
    top = torch.topk(cam.flatten(), 3).indices
    share = cam.flatten()[top] / cam.sum()
    for rank, (i, s) in enumerate(zip(top.tolist(), share.tolist()), 1):
        r, c = divmod(i, 12)
        print(f"  #{rank} grid cell row {r}, col {c}: pixels x {c * cell_w:.0f}-{(c + 1) * cell_w:.0f}, "
              f"y {r * cell_h:.0f}-{(r + 1) * cell_h:.0f} ({s:.0%} of the evidence)")

    # spotlight: keep what the network used, dim what it ignored
    heat = np.asarray(Image.fromarray(np.uint8(cam.numpy() * 255)).resize(photo.size, Image.BILINEAR)) / 255
    ax.imshow(np.asarray(photo) / 255 * (0.4 + 0.6 * heat[..., None]))
    ax.set_title(f"{path.name}: {label} {prob:.0%}", fontsize=10)
    ax.axis("off")

fig.tight_layout()
fig.savefig("gradcam.png", dpi=150)
print("\nsaved gradcam.png")
```

```text
$ python gradcam.py

cat.2161.jpg: Y = [cat 3.98, dog -4.92] -> cat (100%)
  #1 grid cell row 6, col 10: pixels x 416-457, y 188-219 (3% of the evidence)
  #2 grid cell row 2, col 3: pixels x 125-166, y 62-94 (3% of the evidence)
  #3 grid cell row 2, col 2: pixels x 83-125, y 62-94 (3% of the evidence)

dog.2161.jpg: Y = [cat -5.30, dog 5.41] -> dog (100%)
  #1 grid cell row 4, col 4: pixels x 117-146, y 103-128 (8% of the evidence)
  #2 grid cell row 3, col 4: pixels x 117-146, y 77-103 (7% of the evidence)
  #3 grid cell row 8, col 4: pixels x 117-146, y 205-231 (6% of the evidence)

saved gradcam.png
```

## 4. YOLOv8 is PyTorch too

**YOLOv8**, Ultralytics' family of detection and classification models, is
implemented in PyTorch: load one and its `model` attribute is an ordinary
`torch.nn.Module`. The classification version, `yolov8n-cls`, was pretrained on
ImageNet's 1,000 classes, which include 118 dog breeds and five kinds of domestic
cat. With **no training on these photos at all**, adding up its probabilities for
the cat classes and for the dog classes gives a cat-or-dog answer:

```python
"""YOLOv8 is a PyTorch model: run Ultralytics' pretrained YOLOv8n classifier
on the same 120 held-out photos, with no training on this data at all.

It was trained on ImageNet's 1,000 classes, which include 118 dog breeds
(class ids 151-268) and 5 domestic cats (281-285). For each photo, its
probabilities are added up over all the cat classes and all the dog
classes, and the bigger total wins. Needs test_photos/ from prepare_data.py.
"""
from pathlib import Path

import torch
from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")  # downloads the weights on first use
print("underlying model is a PyTorch module:", isinstance(model.model, torch.nn.Module))

correct = total = 0
for true_label in ("cats", "dogs"):
    for photo in sorted(Path("test_photos", true_label).glob("*.jpg")):
        p = model(photo, verbose=False)[0].probs.data  # 1,000 class probabilities
        guess = "dogs" if p[151:269].sum() > p[281:286].sum() else "cats"
        total += 1
        correct += guess == true_label
print(f"test accuracy: {correct / total:.3f} ({correct}/{total})")
```

```text
$ python yolov8_check.py
underlying model is a PyTorch module: True
test accuracy: 0.867 (104/120)
```

**86.7%** without seeing a single training photo from this dataset -- what it learned
from ImageNet's 1.2 million photos transfers. Fine-tuning it on the 24,880 Kaggle
photos (not done here) would push it higher.

## Results

![Bar chart of test accuracy on the same 120 held-out Kaggle photos: scikit-learn MLP 69.2%, PyTorch same MLP 63.3%, PyTorch small CNN 90.8%, YOLOv8n pretrained with no training 86.7%](/images/comp-science/nn-cats-dogs-kaggle-results.png)

| Model | Trained on these photos? | Parameters | Test accuracy | Time (M2 Pro) |
|---|---|---|---|---|
| scikit-learn MLP | yes, from scratch | 893,185 | 69.2% | 54 s (CPU) |
| PyTorch MLP (same network) | yes, from scratch | 893,250 | 63.3% | 65 s (GPU) |
| PyTorch small CNN | yes, from scratch | 683,906 | **90.8%** | 7.8 min (GPU) |
| YOLOv8n-cls (PyTorch) | no, ImageNet only | about 2.7 million | 86.7% | 11 s |

- **The framework doesn't decide accuracy.** scikit-learn and PyTorch train the same
  MLP to the same level.
- **The architecture does.** Keeping the image as a grid -- a CNN -- is worth over 20
  percentage points here, with fewer parameters.
- **Pretrained knowledge transfers.** A small model trained on a different, much
  larger dataset gets most of the way with no training on this one.
- **120 test photos is a small sample.** Treat differences under about 8 points as
  unproven.

## From classification to detection

Classification gives one label per photo. Detection -- the YOLO family's main job --
also says *where* each object is, as a box, and can find many objects in one frame. The
same Ultralytics package does detection with `YOLO("yolov8n.pt")`; under the hood it's
a CNN like step 3, with a box-predicting head on top. A YOLOv8n detector exported from
PyTorch is what runs on the small NPU in the
[Luckfox build log](/blog/comp-science/the-vendor-stack-was-the-fix/).

### Sources

- Kaggle -- [Dogs vs. Cats](https://www.kaggle.com/c/dogs-vs-cats) and [Dogs vs. Cats Redux: Kernels Edition](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition) (the 25,000 labelled training photos)
- J. Elson, J. Douceur, J. Howell, J. Saul, "Asirra: A CAPTCHA that Exploits Interest-Aligned Manual Image Categorization," ACM CCS 2007 (Microsoft Research and Petfinder.com; origin of the photos)
- scikit-learn -- [Neural network models (supervised)](https://scikit-learn.org/stable/modules/neural_networks_supervised.html) (`MLPClassifier`)
- PyTorch -- [pytorch.org](https://pytorch.org/) and the [PyTorch Foundation](https://pytorch.org/foundation)
- Ultralytics -- [YOLOv8 documentation](https://docs.ultralytics.com/models/yolov8/) and [image classification](https://docs.ultralytics.com/tasks/classify/) (`yolov8n-cls.pt`, pretrained on ImageNet)
- O. Russakovsky et al., "ImageNet Large Scale Visual Recognition Challenge," IJCV 2015 (the 1,000 classes `yolov8n-cls` was trained on)
- Tested with Python 3.14.5, scikit-learn 1.9.1, PyTorch 2.14.1 and Ultralytics 8.4.175 on an Apple M2 Pro
