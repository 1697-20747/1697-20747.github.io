---
title: "The Later That Came Early"
date: 2026-08-22T09:00:00Z
draft: true
categories: ["comp-science"]
tags: [robotics, donkeycar, ros2, raspberry-pi, software-architecture]
description: "Fifth post in the APEX build log (formerly APEX-DC). Today: the whole software stack moves off DonkeyCar and onto ROS 2 -- earlier than planned -- and why the swap was cheap because of a decision made months ago."
summary: "Left DonkeySim behind for ROS 2, kept the old codebase untouched as reference, and traded one drive loop for a small graph of independent nodes."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Fifth post in a build log for an autonomous RC vehicle project, previously
called APEX-DC while it ran DonkeyCar on a Raspberry Pi 5 — from here on
just APEX, for reasons that will be obvious by the end of this post.
Previous post: [Stay On, Then Smooth, Then
Fast](/blog/comp-science/stay-on-then-smooth-then-fast/), or see the full
series at the bottom of this post.*

---

## What Changed Today

Last post ended with a look past DonkeySim, filed under "later": once
there was an actual car rather than a simulated one, the plan was to move
the whole stack onto ROS 2, the standard framework most real robotics
projects are built on. That "later" even had a prior ruling on the books
saying not yet — finish proving the DonkeyCar stack on real hardware
first, then port. That ruling got overridden this week. Not because the
DonkeyCar stack finished proving itself — the chassis still isn't even
bought — but because waiting for it stopped being the necessary
precondition it looked like, and there was no rule saying the port had to
come after real-hardware validation rather than instead of it.

So: the project now runs on ROS 2 (Humble) as its primary line. The old
DonkeyCar codebase isn't deleted or migrated piecemeal — it's kept
exactly as it is, untouched, as the reference for every hardware
decision, safety rule, and convention that already proved out on it. The
new codebase ports those over, rebuilt in ROS 2's idioms — nodes, topics,
launch files, parameters — instead of DonkeyCar's parts-and-loop model.
Nothing about *why* those decisions were made gets re-litigated; only
*how* they're expressed changes.

## Why the Port Was Cheap to Say Yes To

The "later, not now" reasoning last post gave for waiting was real:
porting a design that's still changing every week means re-doing the
port every time it changes. What made saying yes to doing it now cheap,
rather than reckless, is a decision made months earlier that had nothing
to do with ROS 2 at all — hardware was always kept behind swappable
interfaces rather than hard-wired into whatever was driving the car that
week. A camera, a distance sensor, a battery monitor: each one already
had a clean boundary between "the thing that reads real hardware" and
"the thing that uses the reading," specifically so a piece could be
swapped or mocked without rewriting what depended on it.

That boundary turns out to be exactly the boundary ROS 2 wants drawn
anyway — a node publishing on a topic instead of a Python object handing
back a value. Porting a codebase that already drew that line in the
right place is a much smaller job than porting one that didn't, which is
the actual reason "wait until hardware validates it" stopped being
necessary rather than merely inconvenient.

## From One Loop to Many Nodes

DonkeyCar's shape is one vehicle loop: a list of parts, each read and
written once per tick, in order, inside a single process. ROS 2's shape
is a graph of independent nodes talking over topics, each running on its
own — and that difference is the real architectural change underneath
the port, not just a new set of import statements.

The new stack is laid out sensors-in, perception-out: a stereo camera
pair for measured depth, a Pi Camera plus an AI accelerator for what an
object *is* rather than how far away it is — the exact measured-vs-guessed
distinction the second post in this series drew, now running as two
separate ROS 2 nodes instead of two code paths in one loop. A fusion node
combines the two into a single tracked object with a real position.
Nothing downstream is allowed to read a raw camera topic directly —
everything goes through a World Model node instead, the one authoritative
record of what the car currently believes about its surroundings.
Planning and control read only from that, never from a sensor directly,
which is what makes it possible to swap a sensor later without touching
the planner at all.

Sitting above all of that is a small state machine deciding which
autonomous behavior is even allowed to run — a manual/autonomous/e-stop
switch underneath, and a second selector on top of it for *which*
autonomous job: circling a track, racing one, navigating point-to-point,
or free-roaming a bounded space with no track at all. DonkeyCar never
needed that second layer because it only ever did the one job.

## Why It Matters

The interesting thing about today isn't the framework swap — frameworks
get swapped. It's that the "later" from last post arrived early without
turning into a rewrite, and the reason is boring on purpose: an interface
boundary drawn for an unrelated reason (being able to mock hardware that
hadn't arrived yet) turned out to be the same boundary a much bigger
architectural change needed later. That's usually what a good boundary
actually buys — not that you never have to change anything, but that the
change you didn't plan for still has somewhere to land.

---

**Previous in the series:** [Stay On, Then Smooth, Then
Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
**Next in the series:** — to be written

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. **The Later That Came Early** (this post)
