---
title: "Same Shape, Different Paper"
date: 2026-08-23T10:12:33Z
draft: false
categories: ["comp-science"]
tags: [robotics, ros2, raspberry-pi, software-architecture, safety]
description: "Sixth post in the APEX build log. Today: drawing the current ROS 2 architecture as an actual diagram after a paper published the same month turned out to describe the same shape on the same class of hardware -- then walking that one graph through two different operating modes to see what object avoidance actually means in each."
summary: "Drew the current apex_ros architecture as a diagram for the first time, then walked the same graph through two concrete cases -- table-top wander and track following -- to see what changes between modes and what, deliberately, never does."
showToc: true
tocopen: false
cover:
  image: "images/comp-science/apex_ros_architecture.png"
  alt: "apex_ros system architecture diagram: sensors through perception, fusion, world model, and mode selection into planning, arbitrated into control and the vehicle -- with a hazard-response/safety column on the right that bypasses planning entirely with a non-negotiable override"
  caption: "The current apex_ros architecture, drawn in systems-paper style"
---

*Sixth post in a build log for an autonomous RC vehicle project, previously
APEX-DC while it ran DonkeyCar, now just APEX on ROS 2. Previous post: [The
Later That Came
Early](/blog/comp-science/the-later-that-came-early/), or see the full
series at the bottom of this post.*

---

![apex_ros system architecture: sensors through perception, fusion, world model, and mode selection into planning, arbitrated into control and the vehicle -- with a hazard-response/safety column on the right that bypasses planning entirely with a non-negotiable override](/images/comp-science/apex_ros_architecture.png)

## What Changed Today

Every post so far in this series has described the shape of the software in
prose — nodes instead of a loop, a World Model nothing else is allowed to
bypass, a mode selector sitting above the old manual/autonomous/e-stop
switch. Today the shape got drawn instead, for the first time: the diagram
above is the current apex_ros stack, current meaning *as built*, not the
final aspirational version — Stereo Depth and Object Detection are both
labeled "planned" because neither has a real node behind it yet, while
Track Boundary Perception is labeled "built" because it does.

The occasion was a paper that turned up this week — Bonci et al., a ROS 2
architecture for autonomous driving, validated on a 1:10-scale RC platform
on an indoor track, running on a Raspberry Pi 5 or Jetson Orin Nano. Not a
full-size-vehicle paper whose assumptions wouldn't transfer — the same
hardware class and physical scale as this project. It describes almost the
same layered shape this project had already committed to in prose. Having
something to hold the current design up against was reason enough to
finally draw it.

## The Column That Wasn't Copied

The one part of the diagram not drawn in plain grey-on-dark is the column
on the right: Hazard Response FSM and Safety Monitor, reading sensor data
directly rather than through Perception, and overriding Control with a
dashed line that skips Planning entirely. The paper has a name for this —
"decoupled sensor access paths" — and calls it out as a deliberate design
principle: a safety-critical loop should never have to wait on a slower
perception pipeline to get an answer.

Neither of those two boxes was drawn that way *because* of the paper. The
hazard-response trigger has read its sensor directly since it was built, and
the command arbiter has always put a latched safety shutdown ahead of
anything the planner proposes — both decisions made for an ordinary reason,
wanting a stop to actually happen on time. Finding the same principle
already named in an unrelated paper, on unrelated hardware, is the same
thing that happened with [the interface boundary two posts
ago](/blog/comp-science/the-later-that-came-early/) that turned out to be
exactly what ROS 2 wanted anyway — a decision made for one reason turning
out to be the right one for a reason nobody had yet.

## Two Instances of the Same Graph

The diagram is one graph, but which parts of it are actually doing anything
on a given drive depends entirely on which `OperatingMode` the Mode Manager
has selected. Two concrete walk-throughs make that more real than the boxes
alone do.

**Table-top first, because it's the mode furthest along.** Track Boundary
Perception has nothing to look at — no track exists on an open table — and
stays exactly as idle as Stereo Depth and Object Detection already are. The
live path runs almost entirely through the safety column and one module the
simplified diagram above doesn't break out on its own: the table-top wander
controller, which steers toward whichever side has more ToF clearance,
brakes using the same Collision Avoidance logic the Planning row shows, and
— when steering alone can't clear an obstacle — hands off to a bounded
three-point-turn. All of it sits underneath one unconditional rule: the
instant the Hazard Response FSM's edge-drop trigger fires, everything else
yields, no exceptions. That's not aspirational for this mode — it's the one
part of the whole stack that's been confirmed running end to end on the
actual Pi 5, mock ToF sensor and all.

**Track is the newer, less complete instance.** Track Boundary Perception is
the live path here: an HSV threshold and a polynomial fit on the Pi Camera
feed, projected onto the ground plane, become the first real numbers World
Model's track synthesis has ever populated — centerline and curvature, both
computed, not guessed. Path Planner (pure pursuit against that centerline)
and Speed Planner (graduated braking off the same curvature) are the
Planning-row boxes that actually mean something in this mode, and the
safety column's track instantiation watches lateral offset from the fitted
centerline instead of a ToF edge-jump — same FSM shape, a different trigger
plugged in, exactly the "shared, reusable" state machine the design called
for from the start. What track mode doesn't have yet, honestly: the command
arbiter's mode-to-producer mapping was never finished for it, so none of
this is actually wired through to the vehicle end to end the way table-top's
path is.

## Object Avoidance, Both Ways

Object avoidance isn't its own box in the diagram above — it's Collision
Avoidance, the same module, doing two different jobs depending which
instance of the graph is running.

In table-top mode it's the middle layer of a three-layer stack, in strict
priority order every tick: the Hazard Response FSM's edge-drop trigger
always wins, unconditionally, whatever else is happening; underneath that,
Collision Avoidance estimates closing rate off consecutive ToF readings and
ramps braking the same continuous, two-threshold way Speed Planner ramps
corner braking, rather than a hard on/off stop; and underneath *that*, when
an obstacle sits too close for any steering angle to clear it geometrically,
a bounded three-point-turn takes over — reverse, reorient, recheck, and if
it still can't clear after a fixed number of cycles, stop and ask for help
rather than resume driving into something a direct measurement just said
was still blocked.

Track mode uses the same Collision Avoidance module for the same job — time
to collision off a fused object's closing speed — but deliberately doesn't
get the three-point-turn option. A track has a lane; a car in it gets
braked for, not reversed away from, and an off-track departure is what the
FSM's track instantiation is already for, a completely separate hazard from
an obstacle sitting in the lane. The two never merge into one detector —
they arrive at the command arbiter as two independent inputs, each tunable
and testable on its own, and neither gets to skip the arbiter's fixed
order: latched safety shutdown first, hazard state second, whatever the
planner proposed third. That ladder is the actual invariant across every
mode in the diagram — what changes between table-top and track is which
trigger sits at each rung, never whether a rung gets skipped.

## Why It Matters

A diagram is cheap to get wrong in a way that looks right — clean boxes and
confident arrows for a design that doesn't actually hang together. Walking
it through two real modes instead of leaving it as one static picture is
what tells you whether it's actually one architecture or just two separate
systems sharing a page: here, the same Collision Avoidance module, the same
FSM shape, and the same arbiter priority order show up in both walk-throughs
doing recognizably the same job with a different trigger wired in — which is
the part worth having drawn in the first place.

---

**Previous in the series:** [The Later That Came
Early](/blog/comp-science/the-later-that-came-early/)
**Next in the series:** [What the Arduino Was Actually Doing](/blog/comp-science/what-the-arduino-was-actually-doing/)

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
10. [Not Every Pixel Needs an Answer](/blog/comp-science/not-every-pixel-needs-an-answer/)
11. [The Vendor Stack Was the Fix](/blog/comp-science/the-vendor-stack-was-the-fix/)
