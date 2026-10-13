---
title: "Teaching YOLO Your Own Objects"
date: 2026-10-13T15:55:00Z
draft: false
categories: ["comp-science"]
tags: [luckfox, rv1106, yolo, machine-learning, computer-vision, guide]
description: "Fourth post in the Luckfox build log: a short guide to training YOLOv8n on just your own objects and images, instead of the 80 everyday classes it ships with, and getting the result onto the RV1106's NPU."
summary: "YOLOv8n ships knowing 80 everyday things. To detect only your own objects, you don't retrain YOLO from scratch: you keep what it has already learned about images and teach it a new, smaller list of classes from a few hundred of your own labelled photos. Collect, label, fine-tune, convert, deploy."
showToc: true
tocopen: false
---

*Fourth post in the Luckfox build log (previously:
[Thirty Frames on One Core]({{< relref "thirty-frames-on-one-core.md" >}})).
A short guide rather than a progress report.*

---

## Not the Whole of YOLO

The YOLOv8n model on the board was trained by Ultralytics on COCO, a dataset of
80 everyday classes: people, cars, dogs, cups, and so on. If you want it to
find *your* things, such as one particular part, tool, or animal, you don't
need to repeat that training. A detection model has two halves:

- **The backbone** has learned what images are made of: edges, textures,
  shapes, parts of objects. That knowledge is general, and expensive to learn.
- **The head** turns those features into "this box contains class N with this
  confidence". That part is specific to the class list.

**Fine-tuning** keeps the backbone, gives the model a new head sized for your
classes, and trains on your images only. It needs hundreds of images, not
hundreds of thousands, and an hour on a laptop rather than days on a cluster.
You can go further and **freeze** the backbone so only the head learns, which
is the most literal version of "not the whole of YOLO". It's useful when you
have very few images.

## 1. Collect Images From the Camera That Will Use Them

The model learns from what it's shown, so the training images should come from
the board's own camera, in the places it will work: its resolution, its colour,
its lighting, its angle.

- **How many:** about 100–300 images per class to start. Fifty very
  different images beat five hundred near-identical ones.
- **Variety:** near and far, partly hidden, different lighting, different
  backgrounds. If it will run at night, include night.
- **Background images:** add some 10% of images with *none* of your objects
  in them. They teach the model when to say nothing.
- **Hold some back:** keep about 20% aside as a validation set the model never
  trains on. That's how you'll know if it works.

## 2. Label Them

Every object in every image needs a box and a class. Free tools such as
[CVAT](https://www.cvat.ai/), [Label Studio](https://labelstud.io/) or
[makesense.ai](https://www.makesense.ai/) export the YOLO format: one text file
per image, with one line per object:

```
<class id> <centre x> <centre y> <width> <height>     # all 0..1, relative to the image
```

Box every instance, however small or partly visible. A missed object teaches
the model that it's background.

A small file describes the dataset:

```yaml
# mything.yaml
path: datasets/mything
train: images/train
val: images/val
names:
  0: widget
  1: gadget
```

## 3. Fine-Tune

With Ultralytics installed (`pip install ultralytics`), start from the COCO
weights rather than from nothing:

```bash
yolo detect train data=mything.yaml model=yolov8n.pt imgsz=800 epochs=100 device=mps
```

- `model=yolov8n.pt` keeps the learned backbone. That's what makes this
  fine-tuning rather than training from scratch.
- `imgsz=800` matches the 800-pixel-wide input the board uses. Training is
  square; the board's 16:9 800x448 export still works, because the network is
  convolutional.
- `device=mps` uses an Apple Silicon Mac's GPU. Use `cuda` on an Nvidia card,
  or leave it out for the CPU.
- Add `freeze=10` to freeze the backbone's first 10 layers and train only the
  rest, when you have very few images.

Ultralytics reports **mAP50** on the validation images after every epoch: how
often a predicted box overlaps a labelled one by at least half. When it stops
rising, more epochs won't help; more varied images will.

## 4. Convert for the NPU

The board needs two conversions, the same pipeline as the stock model:

1. **To ONNX, with Rockchip's head.** The RV1106's NPU runs a version of the
   YOLOv8 output layer that Rockchip restructured. Their fork of Ultralytics
   (`airockchip/ultralytics_yolov8`) exports it with
   `format="rknn"`, `imgsz=(448, 800)`, `opset=12`.
2. **To RKNN int8,** with rknn-toolkit2 1.6.0, the version matching the board's
   runtime. It needs a few dozen calibration images to set the int8 ranges.
   Use your own camera images here too, not the stock street scenes.

The project's `tools/export_yolov8_rknn.sh` does both in Docker on a Mac. For a
custom model it needs your weights file and calibration folder in place of the
stock ones.

## 5. Teach the Board the New Class List

Two small changes on the board side:

- **Class names:** the labels file lists your classes, one per line, in the
  same order as `names` in the YAML.
- **Class count:** the detection server's decoder currently assumes COCO's 80
  classes and a fixed list of six it keeps. It needs to read the class count
  from the model's output shape instead, which it already does for the input
  size. That's the one code change between this guide and a custom model on
  the board.

Fewer classes also make decoding slightly cheaper: the NPU's class-score output
shrinks from 80 values per grid cell to however many you have.

## 6. Check It Before Trusting It

Measure on images the model has never seen: the validation set, then fresh
footage from the board. The question isn't "does it find my widget in the demo
shot" but "how many widgets does it miss, and how often does it see a widget
that isn't there". The comparison tool from
[Never Stop the Camera]({{< relref "never-stop-the-camera.md" >}}) measures
exactly that for any two models.

## In Short

| Step | Effort |
|---|---|
| Collect 100–300 varied images per class from the board's camera | an afternoon |
| Label them | an hour or two per few hundred images |
| Fine-tune from `yolov8n.pt` | about an hour on a laptop GPU |
| Convert (ONNX, then RKNN int8) | minutes, scripted |
| Server change for a custom class count | small, once |

Most of the effort is in the images. A model fine-tuned on a few hundred good
images of your own objects, taken by the camera that will use it, will usually
beat a general model on that job, with fewer classes and less to go wrong.
