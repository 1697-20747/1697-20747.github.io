---
title: "What the Arduino Was Actually Doing"
date: 2026-08-26T09:45:00Z
draft: false
categories: ["comp-science"]
tags: [robotics, ros2, raspberry-pi, sensors, odometry, hardware]
description: "Seventh post in the APEX build log. Today: a wheel encoder, a return-to-base feature that now has three progressively-less-trusted ways to find its way home, and a reference design that turned out to be doing more than it looked like."
summary: "Added a wheel-speed sensor to close a gap the last post admitted to, and learned that removing a microcontroller means finding a new home for whatever job it was quietly doing."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Seventh post in a build log for an autonomous RC vehicle project,
previously APEX-DC while it ran DonkeyCar, now APEX on ROS 2. Previous
post: [Same Shape, Different
Paper](/blog/comp-science/same-shape-different-paper/), or see the full
series at the bottom of this post.*

---

## What Changed Today

The last few sessions built a way for the car to find its way home
without GPS — this project has never had one — by tracking an orange
traffic cone as a visual beacon. That grew a small hierarchy of
fallbacks, each one trusted a little less than the one before it: seek
the cone directly when it's visible, creep toward its last-known bearing
when it briefly isn't, fall back to a dead-reckoned heading from an IMU
when even that's gone, and only then start driving in a bounded search
circle. The IMU leg came with an explicit admission attached: without a
wheel-speed sensor, that dead reckoning is heading-quality, not
position-quality, and it drifts.

Today closes that gap. The car now has a wheel encoder — two Hall-effect
sensors, one per rear wheel, feeding a second, independent estimate of
how fast the car is actually moving into the same sensor-fusion node the
IMU already feeds. It's built from an existing open design,
[FouadRobotics/Wheel-Encoder-Prototype](https://github.com/FouadRobotics/Wheel-Encoder-Prototype),
with one deliberate change from the original: no Arduino.

## What the Arduino Was Actually Doing

The instruction was simple to state — skip the microcontroller, wire the
sensors straight to the Pi, the same way the distance sensors already
are. The part that took more thought was noticing that "skip the
microcontroller" isn't the same as "delete a part from the diagram." The
reference design's two Hall sensors are bare analog outputs. Its Arduino
wasn't just relaying them over serial — it was reading those analog pins
itself and deciding, in software, when a magnet had actually passed by.
Remove the Arduino, and that decision-making doesn't come along for free;
it just stops happening anywhere at all.

Two things had to move. First, the raw analog reading itself needed
somewhere to land — the Pi has no analog input, so a small I2C
analog-to-digital breakout goes in the Arduino's old spot in the signal
path, without becoming a second microcontroller in its own right. Second,
the actual decision logic — is this reading high enough, adjusted for
this sensor's own baseline, to count as a magnet passing — got ported
into the ROS 2 side as its own small, independently tested piece of
software, doing deliberately the same job the Arduino's loop used to do,
just running somewhere else now.

## The Numbers That Didn't Come Along For The Ride

The reference project had already worked out its own per-sensor baseline
readings from real hardware — two specific numbers, found by running its
own calibration sketch. Copying them over would have been the easy move,
and it would have been wrong: those numbers describe a 10-bit reading on
one specific microcontroller's analog input, and the Pi's replacement ADC
reads at a different resolution entirely. Same logic, different units —
reusing the old numbers wouldn't just be imprecise, it would be measuring
something else's baseline and calling it this one's. Those two constants
are unset placeholders instead, with the encoder node refusing to start
until they're replaced with real measurements off the real hardware.

The same instinct applied to a question the reference project never
actually answered: whether its two sensors are meant to work together to
sense direction, the way a proper quadrature encoder pair does. Nothing
in the original design confirms that, so nothing here assumes it. Each
wheel's sensor reports speed, and only speed — which way the wheel is
turning comes from whatever the car was just told to do, not from the
sensor itself. That's a real gap, not a hidden one: a wheel spinning
opposite to its last command — wheelspin, a stall, a crash — will report
the wrong sign until the command changes. Better to know exactly where
that gap is than to paper over it with an encoder pair that was never
confirmed to support the fancier trick.

## Why It Matters

The interesting failure mode in a hardware port isn't forgetting to wire
a pin — it's forgetting that a part you're deleting was quietly doing two
jobs, and only remembering to replace one of them. The Arduino here was
both a signal path and a decision-maker, and losing sight of the second
role would have shipped a wheel encoder that compiled, ran, and reported
numbers that meant nothing — the same failure this series keeps coming
back to in different clothes, a plausible-looking value standing in for
one anyone actually checked.

---

**Previous in the series:** [Same Shape, Different
Paper](/blog/comp-science/same-shape-different-paper/)
**Next in the series:** [Fast, But Undecoded](/blog/comp-science/fast-but-undecoded/)

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. [Stay On, Then Smooth, Then Fast](/blog/comp-science/stay-on-then-smooth-then-fast/)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
6. [Same Shape, Different Paper](/blog/comp-science/same-shape-different-paper/)
7. **What the Arduino Was Actually Doing** (this post)
8. [Fast, But Undecoded](/blog/comp-science/fast-but-undecoded/)
9. [Locked In, Never Measured](/blog/comp-science/locked-in-never-measured/)
10. [Not Every Pixel Needs an Answer](/blog/comp-science/not-every-pixel-needs-an-answer/)
