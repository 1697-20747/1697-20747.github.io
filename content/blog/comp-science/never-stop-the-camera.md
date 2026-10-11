---
title: "Never Stop the Camera"
date: 2026-10-11T20:47:00Z
draft: false
categories: ["comp-science"]
tags: [embedded-linux, luckfox, rv1106, buildroot, computer-vision, debugging, reliability]
description: "Second post in the Luckfox build log. The detection board kept hanging, so the fix had to rest on evidence: crash logs that survive a reset, register dumps from the moment of failure, and A/B tests by the hundred."
summary: "The Luckfox board hung about once in every few dozen app restarts. A watchdog supervisor caught the moment of failure: the eMMC controller's DMA stalls fetching its first descriptor about 5.5 s after the camera stream restarts. The fix is architectural: start the camera once and never stop it. 100 of 100 restarts clean, 3 hours continuous, 14 fps."
showToc: true
tocopen: false
---

*Second post in the Luckfox build log (the first is
[The Vendor Stack Was the Fix]({{< relref "the-vendor-stack-was-the-fix.md" >}})):
real-time YOLO object detection on a Luckfox Pico Ultra, a small Rockchip RV1106
board with its own NPU.*

---

## The Rule

After the move to Buildroot, the board ran well until it didn't. Every so often
it simply hung: no video, no SSH, and only a power cycle would bring it back.
For this one the rule was to fix nothing until the evidence said what to fix.

## Making a Hang Leave Evidence

A hung board tells you nothing, so the first job was making it talk.

- **A supervisor that owns the watchdog.** A small static, memory-locked
  process now owns the hardware watchdog. It kicks the watchdog only while the
  stream server's heartbeat is fresh and a test write to storage completes.
- **A crash log that survives the reset.** When either check fails, it dumps
  every task's kernel stack and the eMMC controller's registers into ramoops,
  memory that survives a warm reset. Then it stops kicking. The board resets
  itself in about 45 seconds, and the crash log is waiting on the next boot.
- **A test that triggers it on demand.** A stress script restarts the app over
  and over, waits out each self-reset and collects the logs.

## What the Logs Said

Every hang looked the same. About 5.5 seconds after the camera stream came back
on, the eMMC stopped completing writes. The kernel re-initialised the card,
which didn't help, and the filesystem journal aborted.

The register dump narrowed it to one step:

```
IDSTS   0x00004000   DMA state: reading descriptor, no error bits
DSCADDR 0x0f612000   == DBADDR: still the FIRST descriptor
BUFADDR 0x00000000   never got as far as a data buffer
STATUS  0x0000cd06   FIFO empty, card idle
```

The eMMC controller's built-in DMA engine had asked main memory for its first
descriptor, and the read never came back. That rules out a worn card, a
bad driver timeout and a clock change; clock rates were also sampled across a
restart and didn't move. It's a memory read stuck somewhere inside the chip,
and it only happened when Rockchip's camera tuning service (3A, for auto
exposure and white balance) was running.

## A/B, by the Dozen

| Configuration | Restarts | Hangs |
|---|---|---|
| 3A service left running across camera restarts | ~55 | 8 |
| No 3A at all (but black, untuned images) | 30 | 0 |
| Fresh 3A service before every camera restart | ~33 | 1 |
| Rockchip's own capture API with 3A in-process | 2 | 1 |
| Kernel patch: camera register writes wait for eMMC idle | 40 | 1 |
| **Camera stream started once at boot, never stopped** | **100** | **0** |

Rockchip's kernel already contains a workaround for an RV1106 conflict between
the camera blocks and the SD controller. It's enabled only for the SD-card
slot, and only on the first silicon revision. This chip is revision 1, and its
eMMC never had the workaround. Extending it to the eMMC reduced the hang rate
but didn't remove it, so whatever the closed-source 3A code does 5.5 seconds in
is still a question for Rockchip. A report with the logs is going to the vendor.

The pattern was clear even before the cause was: every hang followed a camera
*restart*, and the first start after boot had never failed.

## The Fix: Never Stop the Camera

A new 250-line daemon, `yolo_camd`, opens the camera once at boot and never
stops the stream. It shares its four capture buffers with the detection server
as DMA-BUF file descriptors over a Unix socket. Each frame, the server borrows
the newest buffer, converts it and hands it back, with no copies. The server
can crash, be redeployed or be restarted at will; the camera never notices.

- **Restart test:** 100 of 100 server restarts clean, with one camera
  stream start for the whole run.
- **Continuous run:** 3 hours with a video viewer and a navigation client
  attached. No resets, frame rate between 13.1 and 14.1 fps, free memory flat
  at 126-128 MB.
- **No speed cost:** video holds at 13.9 fps.

If anything does go wrong, the supervisor still resets the board within a
minute and keeps the evidence.

## Numbers Since the Last Post

| | Last post | Now |
|---|---|---|
| Video with HUD | 8.9 fps | **13.9-14.7 fps** |
| Navigation only | 10.3 Hz | **15 Hz** |
| JPEG encode | 13 ms (hardware) / 27 ms (software) | 27 ms (software) / **12 ms (hardware)** |
| Hang rate on app restart | about 1 in 7 | **0 in 100** |

The frame rate gain came from a three-stage pipeline, so capture, inference and
drawing overlap instead of taking turns.

Hardware JPEG, which "froze the board" in the last post, is back. On the stable
base it passed 50 of 50 restarts, each one tearing down Rockchip's media stack
while the camera kept running. So the earlier freeze was most likely the same
camera-restart hang all along.

| | Software JPEG | Hardware JPEG |
|---|---|---|
| JPEG encode | 29 ms | 12 ms |
| CPU use | 100% | 75% |
| Video with HUD | 13.9 fps | 14.7 fps |

The frame rate barely moves because the NPU is now the bottleneck. The real win is
a quarter of the CPU back.
