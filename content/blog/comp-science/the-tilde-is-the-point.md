---
title: "The Tilde Is the Point"
date: 2026-08-08T16:20:00Z
draft: true
categories: ["comp-science"]
tags: [robotics, computer-vision, donkeycar, raspberry-pi, monocular-vision, hud]
description: "Second post in the APEX-DC build log. Today: a distance estimate for the one camera that can't actually measure distance — and why the number is printed with a tilde in front of it."
summary: "Added a monocular distance estimate to the Pi camera's HUD, and made sure it can never be mistaken for a real measurement."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Second post in a build log for APEX-DC, an autonomous RC vehicle project
running DonkeyCar on a Raspberry Pi 5. Previous post: [Radar Without
Range](/blog/comp-science/radar-without-range/), or see the full series
at the bottom of this post.*

---

## What Changed Today

The last post drew a hard line: the Pi Camera Module 3 Wide, behind the
Hailo-8 accelerator, has no stereo pair, so it gets no distance — only a
bearing. That line hasn't moved. What changed today is that the camera
now offers a distance estimate anyway, using a different trick: given an
object's class and how wide it looks in the frame, and a table of how
wide that class of object usually is in real life, geometry gives you a
rough range. It's the same "known object size" method the project's own
geometry module had already named, months ago, as a deliberately
unattempted option.

Alongside it: the on-screen instrument HUD got smaller and less
obstructive (the artificial horizon and its readout boxes were
overpowering the actual video underneath them), and each tracked object
now gets a small crosshair marking its center.

## Why the Tilde

The new distance number shows up in the HUD as `~1.2m` — tilde, then the
figure. The OAK-D's real stereo-measured distance, when it's available,
shows as `1.2m` with no tilde, and always wins if both exist for the same
object.

That's not a formatting choice, it's the whole point of the post. A
monocular size-based estimate is a genuinely different, less reliable
kind of number than a stereo measurement — it depends on an object being
roughly the size its class usually is, which is a good bet for a coffee
mug and a bad one for a dog. Printing both the same way would let a
*guess* sit on screen wearing the same clothes as a *measurement*, which
is exactly the failure mode the last post was about avoiding for the
top-down maps. The tilde is a small, permanent reminder of which one
you're looking at.

## Why It Matters

None of this is precision for its own sake. This HUD exists to be
trusted while real hardware bring-up is happening — every number on it
gets looked at and, sooner or later, acted on. A guessed distance is
still useful; a guessed distance silently dressed up as a measured one is
a bug waiting for someone to lean on it. Marking the difference costs one
character.

---

**Previous in the series:** [Radar Without Range](/blog/comp-science/radar-without-range/)
**Next in the series:** [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. **The Tilde Is the Point** (this post)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
