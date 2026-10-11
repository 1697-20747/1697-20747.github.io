---
title: "The Vendor Stack Was the Fix"
date: 2026-10-11T10:30:00Z
draft: false
categories: ["comp-science"]
tags: [robotics, embedded-linux, luckfox, rv1106, buildroot, computer-vision, performance]
description: "First post in the Luckfox build log. A Luckfox Pico Ultra (Rockchip RV1106) detection board got a web UI, then a whole new operating system -- because every hard problem it had come down to running Rockchip's parts outside Rockchip's stack."
summary: "Gave the Luckfox detection board a plug-and-play web UI, found its camera had never had auto-exposure, moved it from Ubuntu to Luckfox's Buildroot image (built and flashed entirely from a Mac), switched to hardware JPEG, and ported the accelerometer back -- with live tilt instruments on the HUD. 5.4fps became 8.9fps along the way."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*First post in the Luckfox build log: real-time YOLO object detection on a
Luckfox Pico Ultra, a small Rockchip RV1106 board with its own NPU. A project
of its own, separate from the APEX robot build log.*

---

## What Changed Today

The Luckfox Pico Ultra -- a small RV1106 board with a 1 TOPS NPU -- has been
running YOLOv8n on its NPU and streaming a HUD over WiFi for a few weeks. Today it got
a proper interface, and then, unexpectedly, a new operating system.

## A Web Page Instead of a Window

The stream server now serves its own UI from the board, on the same port as
the video, with nothing to install and no internet needed -- plug in the USB
cable, open a browser. A switch flips between the full HUD and plain video with
just the YOLO boxes. A per-session object log lists each detected object once
(detections are matched frame to frame, so a parked car isn't listed eight
times a second) and clears when the viewer disconnects. It stays strictly one
viewer: a second browser takes over, and the first offers a "Take over" button
rather than fighting back. With nobody watching, the pipeline doesn't run at
all.

## Why the Picture Was Black

Testing the UI with the live camera turned up something older: the image was
nearly black, mean brightness about 24 out of 255, so YOLO found nothing.
Nothing on the board was running the camera's auto-exposure. Rockchip ships
that as a separate service plus a tuning file for this exact sensor, and both
were sitting on the board -- built for Luckfox's Buildroot image, so they
couldn't run on the Ubuntu it actually had.

That was the third time the same pattern had bitten this project: an NPU
runtime that had to match its converter version, a hardware encoder whose
userspace and kernel driver didn't agree, and now this. Each one is a vendor
part running outside the vendor stack. So the board moved to Luckfox's own
Buildroot image.

## Leaving Ubuntu Without Burning the Boat

The rule was not to lose the working setup, with only a Mac to build on and no
SD card slot. So before anything was flashed: everything committed, a full
byte-for-byte image of the board's eMMC copied to the Mac and size-checked,
and Rockchip's flashing tool built for macOS and proven on a harmless test
write into unused flash. Ubuntu is one script away, and hasn't been needed.

The SDK builds in an x86 Docker container on Apple Silicon. That surfaced two
real bugs before anything reached the board: GNU Make 4.3's parallel-job
handling kept crashing under emulation (fixed by Make 4.4.1), and the image
came out with every file owned by the build user -- `/etc/shadow` readable by
anyone, setuid bits gone -- caught by inspecting the finished filesystem image,
and fixed by restoring ownership from Buildroot's own records. First boot came
up on the Mac's USB link in nine seconds, with auto-exposure working: mean
brightness went from 24 to 127.

## Hardware JPEG, Two Freezes

Buildroot's JPEG library has no ARM SIMD, which dropped the stream to 5.4fps.
The RV1106 has a hardware JPEG encoder, so the next step was obvious -- and
froze the whole board twice. Once from feeding the encoder RGB instead of the
NV12 Rockchip's own samples use, and once from stopping the server in the
middle of an encode, which deadlocked the driver. The second was only pinned
down by streaming the kernel log to the Mac as it happened. With a clean
shutdown that never interrupts an encoder call, five stop-mid-encode tests in
a row came through fine. A boot guard now drops back to software JPEG if a
boot ever hangs, so a bad experiment can't lock up every boot.

## The Accelerometer, Saved This Time

The MPU-6050 needed its kernel fix ported to the new kernel: enable the I2C
bus, describe the sensor, and let the driver run without an interrupt line,
since only power and data are wired. The original fix from September had only
ever lived in a temporary build folder, so this time it's a patch file in the
repo. Flashed over SSH, it came up first try, and the HUD's accelerometer panel
went from grey to live.

That also unlocked the HUD's tilt instruments, which had been grey placeholders
since they were ported because there was no orientation source. Pitch and roll
now come from the direction of gravity in the accelerometer readings: the
horizon ladder shifts with pitch and rotates with roll, the roll-ring pointer
follows the roll angle, and the P/R boxes show live degrees -- P-33, R-41 with
the board sitting at an angle on the desk -- at no cost to the frame rate. The
compass stays grey: heading isn't something an accelerometer can see, so that
waits for a magnetometer or a gyro.

## The Numbers

Live camera at 960x540, YOLOv8n on the NPU at 640x640:

| | Ubuntu | Buildroot, software JPEG | Buildroot, hardware JPEG |
|---|---|---|---|
| Frame rate | 8.5 fps | 5.4 fps | **8.9 fps** (8.7 with accelerometer) |
| JPEG encode | 26 ms | 83-93 ms | **13 ms** |
| NPU inference | 73 ms | 80 ms | 76 ms |
| CPU use | 45-54% | 68-89% | **40-44%** |
| Free memory | ~95 MB | 135 MB | **135 MB** |
| Camera exposure | none (luma 24/255) | auto (luma 127/255) | auto |

Against Ubuntu, the frame rate gain is modest. The real difference is the rest
of the table: the camera finally sees something to detect, there's 40MB more
memory free, and the hardware encoder took JPEG from 26ms to 13ms. Inference is
now nearly the whole frame budget, which is the right place for the bottleneck
to be on a board bought for its NPU.
