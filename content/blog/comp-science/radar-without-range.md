---
title: "Radar Without Range"
date: 2026-08-08T09:12:51Z
draft: true
categories: ["comp-science"]
tags: [robotics, computer-vision, donkeycar, raspberry-pi, stereo-vision, dashboards]
description: "First post in a build log for APEX-DC, an autonomous RC vehicle project. Today: turning a single-camera live stream into a dashboard with two HUD-overlay feeds, a live object table, and two top-down maps — one of them deliberately not to scale."
summary: "Extended a single-camera live stream into a four-panel dashboard, and drew a hard line between a measured position and a guessed one."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*This is the first post in a build log for APEX-DC, an autonomous RC
vehicle project running DonkeyCar on a Raspberry Pi 5. Hardware just
arrived and testing is starting for real, so this series will track what
gets built and, more importantly, why — see the full series list at the
bottom of this post.*

---

## What Changed Today

The project has two cameras: a Raspberry Pi Camera Module 3 Wide on a
Hailo-8 AI accelerator, and a Luxonis OAK-D with its own on-device stereo
depth pipeline. Up to today there was a live web stream for one camera at
a time. Today that became a single dashboard with four panels: both
cameras' HUD-overlay video feeds side by side, a live rolling table of
every tracked object (class, confidence, distance, age), and two top-down
2D maps showing detected objects relative to the vehicle's center.

## Why It's Two Maps, Not One

The interesting decision wasn't the plumbing — it was what to do about the
fact that only one of the two cameras can actually measure distance.

The OAK-D has a real stereo pair, so its map plots genuine measured
positions with real distance rings. The CSI camera behind the Hailo-8 has
no stereo pair at all — it can tell you an object's *angle*, never its
distance. The tempting shortcut is to fake a reasonable-looking distance
so both maps look the same. That's exactly the kind of number that looks
fine right up until someone trusts it.

Instead, the CSI panel places every detection on a fixed ring at the
correct angle and marks it explicitly as distance-unknown — a bearing-only
"radar" view rather than a real position. Nothing on that panel implies
precision it doesn't have.

## Why It Matters

This is a testing tool going into real hardware bring-up, not a demo.
Every reading on it needs to be trustworthy on its own terms — including
being honest about which readings are measurements and which are just
angles. Getting that distinction right on day one, before either camera
has produced a single real frame, is cheaper than un-teaching a bad habit
later.

---

**Previous in the series:** — this is the first post
**Next in the series:** [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)

---

## Full Series

1. **Radar Without Range** (this post)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
