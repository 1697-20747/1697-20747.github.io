---
title: "Thirty Frames on One Core"
date: 2026-10-13T15:30:00Z
author: "1697-20747"
draft: false
categories: ["comp-science"]
tags: [embedded-linux, luckfox, rv1106, computer-vision, performance, hardware-acceleration]
description: "Third post in the Luckfox build log. The detection board's CPU was spending most of its time recolouring pixels. Moving that work onto the chip's 2D engine, and showing every camera frame instead of only detected ones, took the live video from 16 to 30 frames a second."
summary: "The RV1106 has dedicated blocks for 2D image work, JPEG encoding and neural networks, but the single CPU core was still doing the colour conversions. Handing them to the 2D engine (RGA) cut 22 ms of CPU work to 1 ms, and letting video run at the camera's rate while detection runs alongside took the live view from 16.7 to 30 fps. A 3-hour run stayed at 30.0 fps throughout."
showToc: true
tocopen: false
---

*Third post in the Luckfox build log (previously:
[Never Stop the Camera]({{< relref "never-stop-the-camera.md" >}})):
real-time YOLO object detection on a Luckfox Pico Ultra, a small Rockchip RV1106
board with its own NPU.*

---

## Where We Left Off

The last post ended with the board stable and the detector at 16 frames a
second, limited by the NPU. That sounds like the end of the road. It wasn't: the
single CPU core was also at 86%, and most of that wasn't AI work at all. It was
moving pixels from one colour format to another.

## One Chip, Several Engines

The RV1106 isn't just a CPU with an AI accelerator bolted on. Like most camera
chips, it has several fixed-function blocks, each very good at one job:

| Block | What it does | Used here for |
|---|---|---|
| **ISP** (image signal processor) | Turns raw sensor data into a clean picture: exposure, colour, noise reduction | The camera feed, tuned by Rockchip's 3A service |
| **RGA** (raster graphics accelerator) | 2D pixel work: colour conversion, resizing, rotating, copying | Converting and resizing every frame |
| **VENC** (video encoder) | Compresses images: H.264/H.265 video and **JPEG** stills | Turning each finished frame into a JPEG for the browser |
| **NPU** (neural processing unit) | Runs neural networks in int8 arithmetic | YOLOv8n object detection |
| **CPU** (one Cortex-A7 core) | Everything else | Drawing the HUD, networking, glue |

### RGA and JPEG Are Different Jobs

It's easy to lump these together as "the hardware does the images", but they do
different things:

- **The RGA rearranges pixels.** The camera delivers **NV12**, a format that
  stores brightness at full resolution and colour at quarter resolution. The
  neural network and the HUD drawing code want **RGB**, three bytes per pixel.
  Converting between them is simple arithmetic on half a million pixels per
  frame: easy for dedicated hardware, slow for one small CPU core. The RGA
  also resizes, so it can turn the 960x540 camera frame into the model's
  800x448 input in the same pass.
- **The JPEG encoder compresses.** It takes a frame and squeezes it into a JPEG
  that a browser can display, about 20 KB instead of 1.5 MB. Compression means
  transforms, quantisation and entropy coding, a completely different kind of
  work. The encoder wants its input in NV12, so the finished RGB frame with the
  HUD drawn on it has to be converted back first. That conversion is RGA work
  again.

So a frame's journey is: camera (NV12) → **RGA** to RGB → CPU draws the HUD →
**RGA** back to NV12 → **VENC** compresses to JPEG → browser. Meanwhile a
second **RGA** pass makes the small RGB copy that feeds the **NPU**.

Until this week, the CPU did every RGA step itself.

## Measuring First

A small benchmark compared the CPU code with the RGA on the board:

| Conversion (960x540) | CPU | RGA |
|---|---|---|
| Camera NV12 → RGB | 22.0 ms | **1.1 ms** |
| NV12 → RGB, resized to 800x448, one pass | (15 + 6 ms) | **1.1 ms** |
| RGB → NV12 for the JPEG encoder | ~5 ms | **1.0 ms** |

The RGA's colours matched the CPU's to within one level out of 255.

### The Benchmark That Crashed the Board

The first version of that benchmark crashed the kernel. It handed the RGA
ordinary memory, the kind every program allocates. This chip's RGA can't use
that memory: it has no IOMMU, the hardware that would let it follow scattered
memory pages, so it needs one physically contiguous block. The driver rejected
the job correctly, but its error handling left the kernel's bookkeeping for the
program's memory corrupted. When the program exited, the kernel crashed.

The supervisor from the last post did its job: panic, reboot, crash log saved,
board back in a minute. The rule since then: the RGA only ever gets dedicated
DMA buffers, from the same contiguous-memory pool the camera uses. If any RGA
job fails, the server switches back to the CPU path for good.

## What the CPU Gave Back

With all three conversions on the RGA, and the int8 conversion for the NPU
rewritten with NEON (the CPU's own 16-bytes-at-a-time vector instructions):

| Per frame | CPU only | With RGA |
|---|---|---|
| Camera read + colour conversion | 15.9 ms | **4.5 ms** |
| Resize for the model | 6.0 ms | **0** (same RGA pass) |
| Convert to int8 for the NPU | 5.7 ms | **2.0 ms** |
| JPEG (conversion + encode) | 12.4 ms | **3.0 ms** |
| CPU use | 86% | **33%** |

The frame rate barely moved: 16.2 to 16.7 fps. Every frame still waited for its
own detection, and the NPU needs 58 ms per frame whatever the CPU does.

## Stop Waiting for the NPU

The fix was to stop tying video frames to detections:

- **Video runs at the camera's rate.** Every pass through the loop takes the
  newest camera frame, draws the latest detection's boxes on it, and sends it.
- **Detection runs alongside.** Every frame is also resized and staged in the
  NPU's spare input buffer. The moment the NPU finishes one detection, the
  newest staged frame goes in.
- **The cost** is that boxes lag the picture by one detection, about 60–90 ms.
  On a fast-moving object you can see the box trail slightly.

The first try only reached 10 detections a second. A finished detection waited
for the next camera frame before the NPU got new work. Staging every frame, and
checking the NPU every 2 ms while waiting for the camera, brought it back to
14.9.

## The Numbers

| | Last post | Now |
|---|---|---|
| Live video with HUD | 16.7 fps | **30 fps** (the camera's maximum) |
| Detections while someone watches | 16.7 per second | **14.9 per second** |
| Detections, navigation output only | 16.7 per second | **17.1 per second** |
| CPU use while streaming | 86% (at 16 fps) | **~73% (at 30 fps)** |
| JPEG per frame | 12 ms | **3 ms** |

A 3-hour run with a video viewer and a navigation client attached stayed at
30.0 fps and 14.9 detections a second in every sample. There were no resets,
memory stayed flat, and the RGA logged no errors.

Over this build log the live video has gone from 5.4 fps to 30, on one 1.2 GHz
core. Very little of that came from the neural network itself. Most of it came
from finding which part of the chip should be doing each job, and measuring
before believing.

*Next in the Luckfox log: [Teaching YOLO Your Own Objects]({{< relref "teaching-yolo-your-own-objects.md" >}}).*
