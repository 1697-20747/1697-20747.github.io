---
title: "Not Every Pixel Needs an Answer"
date: 2026-09-06T19:15:00Z
draft: false
categories: ["comp-science"]
tags: [robotics, ros2, raspberry-pi, computer-vision, stereo-vision, performance]
description: "Tenth post in the APEX build log. Today: a real stereo depth pipeline finally produced correct numbers on real hardware, then turned out to run at a thirtieth of the camera's own frame rate -- and the fix wasn't faster hardware, it was asking for less."
summary: "Got real stereo depth working end to end on the Pi 5, found it could only keep up at 0.97Hz against a 30Hz camera, ruled out three hardware-based fixes, and recovered real-time by trading pixel density for speed instead."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Tenth post in a build log for an autonomous RC vehicle project, previously
APEX-DC while it ran DonkeyCar, now APEX on ROS 2. Previous post: [Locked
In, Never Measured](/blog/comp-science/locked-in-never-measured/), or see
the full series at the bottom of this post.*

---

## What Changed Today

The stereo camera has had a complete, mock-tested dense-depth pipeline
sitting in the codebase for weeks -- disparity matching, triangulation,
the whole path from a raw stereo frame to a metric depth image -- with one
thing missing: a real calibration to run it against. Today that gap
closed. A real checkerboard calibration went in, the depth math got
checked against real captures and fixed where it was wrong, and the
pipeline ran live on the Pi for the first time, subscriber and all. It
produced correct depth. It also produced it at 0.97Hz, against a camera
that outputs frames thirty times a second. The rest of the day was about
that number, not the correctness one.

## Correct Wasn't the Same as Usable

The calibration itself needed a real fix before any of this was
trustworthy: a first full-dataset pass came back at 62% baseline error,
traced to JPEG compression smearing corner positions on far-away shots
rather than anything wrong with the math, and fixed with automatic
outlier rejection -- the working result was 26 of 50 shots, 0.11-0.13px
reprojection error, baseline within 0.7% of the 52mm datasheet spec. Even
with numbers that clean, the first depth readings against real captures
were still 50-83% off and not even consistently biased in one direction.
The cause wasn't the calibration -- it was a simplification upstream of
it, treating "per-eye undistortion" as good enough rectification when the
two lenses actually sat about six pixels out of vertical alignment and 33
pixels apart in principal point, both of which the naive depth formula
quietly assumes away. A real `cv2.stereoRectify()` pass fixed it: the
same three test shots that were 50-83% wrong came back within 8% of
correct, and corner coverage on a real checkerboard jumped from
24-44 out of 70 points to a full 70.

That's the part where "does this pipeline compute the right number"
finally got a yes. It's also the point where a different question showed
up right behind it.

## Three Ways Other Systems Solve This, None Available Here

Once depth was trustworthy enough to time, timing it live was the
obvious next step, and the number it returned -- 0.97Hz, one update
roughly every second against a camera streaming thirty times a second --
was the day's real problem. Dense stereo matching at full resolution is
just expensive: 1280x720 pixels searched across 128 disparities, every
frame, on a general-purpose ARM CPU with nothing dedicated to the job.

The obvious answers all turned out to be the wrong shape for this
project, for three different reasons. Products that do this well in real
time -- RealSense, the OAK-D already sitting in the parts bin, a Boston
Dynamics Spot -- mostly lean on a dedicated stereo-matching ASIC, which
is real, purpose-built silicon this camera simply doesn't have, and
buying one isn't a same-day fix. The Hailo-8 already on this Pi looked
like a plausible shortcut until its own published numbers for
stereo-matching models came back at 10.7fps on automotive-scale test
data -- a chip that's fast at object detection isn't automatically fast
at a structurally different task, and that benchmark's own camera setup
has little in common with this one's much shorter baseline. The OAK-D
itself was the most tempting option, since it already does exactly this
on its own hardware -- ruled out for a reason that had nothing to do with
stereo matching: it's not strong enough to also run the live Hailo YOLO26
detection pipeline alongside it, and giving up detection to get depth
isn't the trade this project wants to make.

## The Fix Was Asking for Less, Not Buying More

None of those three panned out, which turned out to matter less than
expected, because the actual constraint wasn't compute-per-pixel in the
abstract -- it was that dense, photorealistic depth was never what
navigation actually needs. `StereoSGBM`'s cost scales directly with pixel
count times disparity range, and `cv2.stereoRectify()` already has a
mechanism for remapping straight from a full-resolution source down to a
smaller rectified grid in one pass. Pointed a saved AR0144 capture at a
range of scales on the same Pi: full resolution ran at 790ms a frame
(1.27Hz, matching the live number almost exactly), and a quarter-scale
grid ran at 14ms a frame -- 71Hz, well past the camera's own 30fps
ceiling, with coverage actually improving, 86% versus 75%, not degrading.
Downscaling first and searching a proportionally narrower disparity range
turned out to answer the same real question -- how far away is the thing
in front of the vehicle -- for a small fraction of the cost, because
"where exactly, to the pixel" was never the question being asked.

## Landing on a Number With Margin

A quarter-scale grid running at 71Hz had more speed than it needed and
less resolution than free headroom would allow, so the next pass
benchmarked the space in between. A scale of 0.35 landed almost exactly
at 30Hz raw compute, which sounds like a match until real ROS overhead --
image decode, `cv_bridge`, the publish call itself -- is added on top, at
which point it would likely fall short of the camera's own frame rate in
practice rather than matching it. 0.30 came out the more honest choice:
384x216, 49Hz, meaningfully better coverage than the quarter-scale pass
(88.2% versus 86.1%), and enough margin over 30Hz to absorb real overhead
rather than being timed out by it. One more real bug came out of this
pass, not a performance one: the disparity search range had been a flat
128 regardless of scale, which would have silently run a mismatched,
unbenchmarked search the moment anyone changed the resolution -- it now
derives automatically from whatever scale is set, using the same formula
the benchmark itself used to reach these numbers.

## A Fourth Option, Parked For Now

None of today's numbers touch the detection side of the pipeline directly
-- that's still `yolo26n` on the Pi 5's own CPU, the subject of
yesterday's post -- but the same underlying problem (four cores, several
subsystems, one shared budget) suggests an option worth naming even
though it didn't get pursued today: move detection and positional
processing off the Pi 5 entirely, onto a small, cheap companion board
dedicated to nothing else. The Luckfox Pico Ultra -- a Rockchip
RV1106-based Linux board, a Cortex-A7 at 1.2GHz plus its own small NPU (1
TOPS INT8 on the base Ultra, half that on the lower-memory Ultra B
variant) for well under the cost of anything already in this project's
parts bin -- fits that role on paper: run a YOLO model locally on its own
silicon, hand the Pi 5 nothing but the resulting detections and
positions, and the Pi's cores never see the cost at all.

The real obstacle sits on the RKNN side, and it's a specific, checkable
one rather than a vague "probably harder." Rockchip's own INT8-only chip
list explicitly includes the RV1106 -- FP16 isn't an option here,
quantization is mandatory -- and Ultralytics' own current YOLO26 RKNN
export path has an open, unresolved report of exactly the kind of gap
this project has already been burned by once: YOLO26 deliberately drops
the DFL+NMS postprocessing older YOLO generations shipped with (the same
architectural change that produced the raw-tensor Hailo gap back in
"Fast, But Undecoded"), and a PyTorch-to-ONNX-to-RKNN-int8 conversion of
it is currently reported to segfault at inference, while the identical
path for YOLOv8/v11 works fine. Same shape of problem, different chip,
different vendor's toolchain -- not a new kind of risk, a repeat of an
already-known one.

Parked, not pursued: chasing that down now would mean re-fighting a fight
this project has already won once, on hardware that isn't purchased yet,
before the current CPU-only detection path is even validated end to end.
Worth keeping on the list for exactly the reason it came up -- it's the
one option here that removes detection's cost from the Pi 5's budget
entirely rather than trading it for less resolution or a smaller model --
just not this week.

## Why It Matters

Yesterday's post ended on an open question: what happens when camera
capture, detection, navigation, and the HUD are all asking the same four
Pi cores for time at once, a full-stack number nobody has ever actually
measured. Today didn't answer that question, but it added a second,
independent example of the same underlying shape -- a completely
different subsystem, stereo depth rather than object detection, hitting
a wall that traces back to the same scarce resource. And the fix here
wasn't different from that post's either: not new hardware, not a
cleverer algorithm, but a real measurement showing that the assumed
requirement -- every pixel, at full resolution, every frame -- was never
actually the requirement at all. A coarse, honestly-labeled grid that
keeps up beats a dense, correct one that can't.

---

**Previous in the series:** [Locked In, Never
Measured](/blog/comp-science/locked-in-never-measured/)
**Next in the series:** [The Vendor Stack Was the
Fix](/blog/comp-science/the-vendor-stack-was-the-fix/)

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
9. [Locked In, Never Measured](/blog/comp-science/locked-in-never-measured/)
10. **Not Every Pixel Needs an Answer** (this post)
11. [The Vendor Stack Was the Fix](/blog/comp-science/the-vendor-stack-was-the-fix/)
