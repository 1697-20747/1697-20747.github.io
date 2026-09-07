---
title: "Locked In, Never Measured"
date: 2026-09-05T15:00:00Z
draft: false
categories: ["comp-science"]
tags: [robotics, ros2, raspberry-pi, computer-vision, object-detection, performance]
description: "Ninth post in the APEX build log. Today: a stereo-vision detector's model choice, picked months ago and called 'locked in' ever since, finally got a stopwatch put on it -- and the number that came back reversed the choice."
summary: "Benchmarked yolo26n against yolo26s on the Pi 5's own CPU for the first time, found the 'locked-in' choice was nearly three times too slow to keep up with the camera, and switched the default on the strength of a real measurement instead of a remembered assumption."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Ninth post in a build log for an autonomous RC vehicle project, previously
APEX-DC while it ran DonkeyCar, now APEX on ROS 2. Previous post: [Fast,
But Undecoded](/blog/comp-science/fast-but-undecoded/), or see the full
series at the bottom of this post.*

---

## What Changed Today

The stereo-vision pipeline detects objects by running a YOLO model twice
every cycle — once on the left camera's frame, once on the right — and
until the Hailo-8 export path gets wired up for it, that model runs
straight through the Pi 5's own CPU, no NPU involved. The module's own
docstring has called this the single highest CPU-risk path in the whole
project since the day it was written. Today, for the first time, that risk
got an actual number instead of a description.

## The Choice That Was Never Timed

Months back, fine-tuning a detector for this pipeline meant picking a base
checkpoint, and the pick was `yolo26s` over the smaller `yolo26n` —
reasonable at the time, still called "an accepted pre-Hailo-export
default" in the code's own comments. But every real FPS number that
existed anywhere in this project for this model family — 26.7 FPS for
`yolo26m`, a community benchmark's 86.5/37.5/23.4/17.9 FPS for
nano/small/medium/large — was measured on the Hailo-8 chip. None of it
was the CPU path the choice was actually about. A choice can sit
comfortably in a codebase for a long time looking settled while nobody's
ever confirmed the one number that would tell you if it's right.

## Putting a Number On It

The fix wasn't complicated, just previously undone: install both
checkpoints in an isolated environment on the real Pi 5 — deliberately
kept separate from the system Python the camera driver depends on, the
same ABI-conflict caution [a hardware bring-up session two posts
back](/blog/comp-science/fast-but-undecoded/) had already paid for once —
force CPU-only execution, and run the model the same way the real pipeline
does: two frames a cycle, at the real camera's per-eye resolution, thirty
timed cycles after a handful of discarded warm-up passes, CPU usage
sampled the whole time from a background thread.

`yolo26n` came back at 466ms per left-right cycle — about 4.3 effective
frames a second, one of the Pi's four cores pegged at 100% the entire
time. `yolo26s` came back at 1.28 seconds per cycle — roughly 1.6 frames a
second, the same single core maxed out, just for nearly three times as
long. A second and a quarter to answer "what's in these two frames" is
slower than the gap between frames on a camera stream running many times
that fast — not tight, not marginal, just not keeping up.

## Why the Locked-In Choice Changed

`yolo26n` becoming the new default isn't "nano is always the safe
choice" — it's this project's own stated rule about not trusting a
number nobody measured, applied to a decision that had quietly gone
unmeasured for months. The training script's base checkpoint flipped back
to `yolo26n`, and the detector module's own documentation now cites the
real cycle times instead of a general "small models are probably fine"
gesture. It's not a free win, either: `yolo26n` still holds one whole core
at 100% for nearly half a second every cycle. It's the better of two real
numbers, not the absence of a cost — that only genuinely goes away once
the Hailo-8 export path is finished, where this project's own hardware
already measured 0% CPU load regardless of which model size runs on it.

## What Wasn't Answered Today

This benchmark measured the model alone, in isolation, on an otherwise
idle Pi. It says nothing about what happens when camera capture, this
detector, reactive obstacle avoidance, hazard response, and the HUD are
all asking the same four cores for time at once — that full-stack
snapshot has never been taken anywhere in this project, benchmark or not,
and stays an open question. Two smaller loose threads came out of today's
numbers too, neither chased down yet: only one of the Pi's four cores
ever lit up during inference, the other three sitting idle the whole run,
which doesn't match how the underlying framework is documented to behave
by default; and Ultralytics' own published Raspberry Pi 5 benchmarks show
a roughly 4.5x gain just from exporting to a different, ARM-optimized
format, with accuracy basically unchanged — a lever that might make the
slower model viable after all, untested here.

## Why It Matters

"Locked in" is a description of how settled a decision looks, not
evidence that it's correct — and the gap between those two can survive
for months if nothing ever puts a stopwatch on it. The interesting part of
today wasn't that the smaller model won; smaller models on constrained
hardware winning is the unsurprising outcome. It's that a choice this
project had been treating as decided turned out to be running on
borrowed numbers from a completely different chip, and stayed that way
right up until someone actually measured the thing the decision was
about.

---

**Previous in the series:** [Fast, But
Undecoded](/blog/comp-science/fast-but-undecoded/)
**Next in the series:** [Not Every Pixel Needs an Answer](/blog/comp-science/not-every-pixel-needs-an-answer/)

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
6. [Same Shape, Different Paper](/blog/comp-science/same-shape-different-paper/)
7. [What the Arduino Was Actually Doing](/blog/comp-science/what-the-arduino-was-actually-doing/)
8. [Fast, But Undecoded](/blog/comp-science/fast-but-undecoded/)
9. **Locked In, Never Measured** (this post)
10. [Not Every Pixel Needs an Answer](/blog/comp-science/not-every-pixel-needs-an-answer/)
