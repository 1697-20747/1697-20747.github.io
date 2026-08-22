---
title: "From Static Overlay to Object Oriented Widget HUD"
date: 2026-08-09T13:52:28Z
draft: true
categories: ["comp-science"]
tags: [robotics, computer-vision, donkeycar, raspberry-pi, software-architecture, hud]
description: "Third post in the APEX-DC build log. Today: the on-screen instrument HUD stopped being one 1,000-line file and became a package of independent widgets bound to a grid — and why that made a two-line fix out of what would have been a rewrite."
summary: "Split a monolithic HUD-drawing module into standalone widgets bound to explicit screen locations, then watched the payoff show up immediately when two of those widgets started overlapping."
showToc: true
tocopen: false
cover:
  image: "images/comp-science/apex_hud_widget_grid.png"
  alt: "APEX-DC HUD showing the widget-based instrument overlay: crosshair, roll ring, compass tape, accelerometer, and tracked-object boxes"
  caption: "The HUD as of this post — every element below is its own widget bound to a Bounds box"
---

*Third post in a build log for APEX-DC, an autonomous RC vehicle project
running DonkeyCar on a Raspberry Pi 5. Previous post: [The Tilde Is the
Point](/blog/comp-science/the-tilde-is-the-point/), or see the full series
at the bottom of this post.*

---

![The APEX-DC HUD as of this post — crosshair, roll ring, compass tape, accelerometer, and tracked-object boxes, each its own widget](/images/comp-science/apex_hud_widget_grid.png)

## What Changed Today

The instrument HUD — steering/throttle readout, artificial horizon, roll
ring, compass tape, speed and altitude tapes, the works — had grown into
one module with a private drawing function per element, each one reaching
into the raw frame size and picking its own pixel offsets by hand. It
worked, but every new element (this project has added an accelerometer
gauge, a lap counter, a path minimap, a session timer over the last few
posts) meant more hand-tuned constants in a file that already had a lot
of them.

That module is gone now. In its place: a small package where every HUD
element is its own class with a `draw()` method, and every one of them is
constructed with a `Bounds` — an explicit box on the frame it's allowed to
draw in, plus a scale. A separate, much smaller file just lists which
widgets exist and which `Bounds` each one gets. Moving an element, resizing
it, or adding a new one is a change to that one list, not a hunt through
someone else's drawing code.

## Why the Grid Mattered Within a Day

The proof wasn't the refactor itself — it was what happened right after
it. The roll ring (a small tick-marked arc showing bank angle) had been
tuned so its pointer dipped down to touch the frame's centerline at level
roll. That looked fine until the center reticle got a redesign and grew
enough that the two started overlapping.

Before the refactor, fixing that meant finding every place the ring's
position depended on a hardcoded fraction of the frame and hoping nothing
else assumed the old numbers. After it, the ring's entire position comes
from one shared function computing its center and radius from its own
`Bounds` — so "move the ring above the reticle instead of into it" was a
one-line change to where that center sits, done once, correct everywhere
the ring is drawn. A handful of other changes landed the same way over the
next few passes — a smaller accelerometer gauge tucked into the actual
corner of the frame instead of a cell that happened to overlap the speed
tape, transparent instrument backgrounds instead of solid fills, a compass
tape recolored without touching its own heading indicator — each one
scoped to exactly the file for that one widget.

## Why It Matters

None of this changes what the HUD shows. It changes how much a small
request costs to act on. A project like this one gets a steady stream of
"move that," "shrink this," "these two are colliding now" — the kind of
notes that show up only once you can actually see the thing rendered. A
structure where each of those is a bounded, independent change is the
difference between iterating on the HUD daily and dreading opening that
file at all.

---

**Previous in the series:** [The Tilde Is the
Point](/blog/comp-science/the-tilde-is-the-point/)
**Next in the series:** [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. **From Static Overlay to Object Oriented Widget HUD** (this post)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
