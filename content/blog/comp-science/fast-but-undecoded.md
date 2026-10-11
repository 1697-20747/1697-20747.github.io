---
title: "Fast, But Undecoded"
date: 2026-08-30T15:00:00Z
draft: false
categories: ["comp-science"]
tags: [robotics, ros2, raspberry-pi, hailo, computer-vision, object-detection]
description: "Eighth post in the APEX build log. Today: the AI HAT+ ran the newest YOLO generation at real speed and zero CPU load, then handed back nothing usable — because nobody had written the decode step for it yet."
summary: "Got YOLO26 running on the Pi's AI HAT+ by reading the compiled model's own raw output tensors on real hardware, instead of trusting a remembered architecture or settling for an older fallback model."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Eighth post in a build log for an autonomous RC vehicle project,
previously APEX-DC while it ran DonkeyCar, now APEX on ROS 2. Previous
post: [What the Arduino Was Actually
Doing](/blog/comp-science/what-the-arduino-was-actually-doing/), or see
the full series at the bottom of this post.*

---

## What Changed Today

The AI HAT+'s Hailo-8 chip has been sitting on the Pi for weeks, confirmed
present and idle. Today it did real work: `camera_processing_node` went
from stub to a live semantic-detection pipeline, closing out the
project's oldest still-open item — bridging `picamera2`'s Hailo inference
and `rclpy`'s ROS 2 graph across a hard Python-ABI wall the two can't
share a process across. Camera capture, Hailo inference, and detection
tracking all ran together on real hardware for the first time, publishing
a real `/apex/perception/tracked_objects` stream. First live test was an
empty room and reported nothing — correctly, not a bug — which was
useful confirmation on its own before pointing a camera at anything more
interesting.

None of that is the actual story of the day, though. The interesting part
started once the newest model — YOLO26, the generation this project has
said all along it wants — got asked to do that same job.

## The Chip Was Fast. The Model Came With No Instructions.

First check was whether the hardware itself was even worth building
around: `hailortcli fw-control identify` found a real Hailo-8 (not the
smaller Hailo-8L some tutorials assume), and a benchmark against the
Pi's pre-installed `yolo26m.hef` came back at 26.7 FPS, 32.8ms latency,
with the Pi's own CPU sitting at a flat 0% the entire time. The chip was
doing exactly what an AI HAT+ is for.

Wiring that same file into the actual camera pipeline told a different
story. Instead of a list of detections, it returned raw multi-scale
tensors — numbers straight off the model's last layer, with nothing
between them and a class name or a box. A generic Hailo Model Zoo export
ships without baked-in non-max suppression or postprocessing; something
downstream is expected to know how to read it, and nothing here did yet.

The fast way out already existed: the Pi's own `hailo-all` package ships
a `yolov8s` model with postprocessing built in, ten consecutive live
frames confirmed it returning usable boxes in about 10ms each, and that
became the working fallback. It also wasn't the model the project
actually wanted running.

## Reading the Tensors Instead of Guessing

Writing a decoder for YOLO26 from memory was the obvious next move, and
the wrong one — this is a genuinely new detection head, not a
reskinned older one, and guessing its layout from a general sense of
"how YOLO usually works" is exactly the kind of assumption this project
keeps getting burned by. So instead of assuming, `Hailo.describe()` was
pointed at the real compiled file already sitting on the Pi and asked
what it actually outputs: three detection scales, four raw box numbers
per cell (plain distances to each edge, not the more complex encoding
older YOLO versions use), and eighty per-class scores in COCO's order.

The decode formula came from watching what those actual numbers did
across real frames, not a spec sheet — no such spec existed for this
exact compiled artifact. Class channels sat solidly negative except where
something real was in frame; running those through a sigmoid gave a
sane-looking confidence. Box channels behaved like plain distances from a
grid cell's center, not the softmax-over-bins format some other YOLO
generations use. Put together, that was a full decode.

The first real detection it produced was a tight, 92.4%-confident box —
around the checkerboard calibration target, labeled "keyboard." That's
not a bug: a grid of squares is a reasonable nearest match among COCO's
eighty classes for an object that isn't actually any of them, and a
coherent, well-placed box on a real thing in frame is exactly the signal
that the decode math is right, whatever name it hands back.

## Why It Matters

The AI HAT+ was never the hard part — it ran the model it was given
correctly and fast from the first benchmark. The gap was one layer up:
nobody had written down how to turn this specific model's raw output into
an answer, and the honest fix for a documentation gap isn't a best guess,
it's going and reading what the hardware actually produced. That's a
slower path than trusting a remembered architecture, but it's the
difference between shipping the model the project actually wants and
quietly settling for whichever older one happened to come with the
instructions already included.

---

**Previous in the series:** [What the Arduino Was Actually
Doing](/blog/comp-science/what-the-arduino-was-actually-doing/)
**Next in the series:** [Locked In, Never Measured](/blog/comp-science/locked-in-never-measured/)

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
6. [Same Shape, Different Paper](/blog/comp-science/same-shape-different-paper/)
7. [What the Arduino Was Actually Doing](/blog/comp-science/what-the-arduino-was-actually-doing/)
8. **Fast, But Undecoded** (this post)
9. [Locked In, Never Measured](/blog/comp-science/locked-in-never-measured/)
10. [Not Every Pixel Needs an Answer](/blog/comp-science/not-every-pixel-needs-an-answer/)
11. [The Vendor Stack Was the Fix](/blog/comp-science/the-vendor-stack-was-the-fix/)
