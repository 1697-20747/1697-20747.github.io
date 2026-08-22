---
title: "Stay On, Then Smooth, Then Fast"
date: 2026-08-14T08:29:03Z
draft: true
categories: ["comp-science"]
tags: [robotics, donkeycar, raspberry-pi, reinforcement-learning, simulation, ros2]
description: "Fourth post in a build log for APEX-DC, an autonomous RC vehicle project. Today: reshaping the reinforcement-learning reward so staying on the track always outranks driving smoothly or driving fast, and a look ahead at where the software might go next."
summary: "Reordered the driving reward so staying on the track always wins, added partial credit for correcting before a hard boundary crossing, and looked past today's simulator toward a possible future framework."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Fourth post in a build log for APEX-DC, an autonomous RC vehicle project
running DonkeyCar on a Raspberry Pi 5. Previous post: [From Static
Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/),
or see the full series at the bottom of this post.*

---

## What Changed Today

Training doesn't happen on the real car yet — there's no chassis wired
up to drive on. It happens in DonkeySim, the free virtual test track
that ships alongside DonkeyCar: a small Unity application that renders a
track, drops a simulated version of the car onto it, and reports back
camera frames and a reward every step. A training algorithm can drive
thousands of virtual laps, crash as often as it likes, and reset
instantly, all before any of it risks a real vehicle.

Up to now, that reward was one blended number: something like "how
centered are you, times how fast are you going." It's a reasonable
starting point, but it has an obvious flaw — a policy chasing that
number can learn that clipping the outside edge of a corner at speed
scores better than a slower, cleaner line, right up until it clips too
much and goes off entirely. Today's change replaces that single number
with an explicit order of priorities: stay on the track, then drive
smoothly, then go fast — in that order, not blended together.

## Stay On, Then Smooth, Then Fast

The three priorities aren't three weights added together — they're a
strict order, and a flat reward number can't really express "never trade
priority one for priority two," only "priority one is usually worth
more." So the actual enforcement mechanism is blunter and more reliable
than any weight could be: going off the track — or coming close enough
to be judged off it — ends the simulated lap immediately, forfeiting
every point of reward the rest of that lap would have earned. That's
what makes "stay on" genuinely outrank the other two in practice, not
just on paper. Smoothness (penalizing sudden steering changes) and speed
come after, each worth a fraction of what staying on the track is worth,
so the policy has no incentive to trade a boundary violation for a
faster corner.

Speed also got a second change: it's now capped, not just weighted.
Going faster than a conservative threshold earns no extra reward at all,
so the only way to raise the score is to hold speed near that cap
through corners rather than in short straight-line bursts — closer to
"drive an efficient line" than "drive as fast as possible."

## A Softer Line Before the Hard One

One more change, smaller but with a real effect on what gets learned:
there used to be exactly one boundary, and crossing it ended the lap
with nothing in between — a policy that drifted right up to the edge
and caught itself got treated identically to one that sailed straight
through. Now there's a second, softer boundary just inside the real one.
Drifting into that inner zone costs a small, shrinking penalty that gets
smaller the more the car corrects — so catching a drift early is now
something the policy is actually rewarded for, not just something that
happens to avoid a worse outcome. It's a small piece of the much bigger
question of how the car should behave once it's already lost the track
entirely, which is still an open problem being worked out separately.

## Track Mode, For Now

All of this reward shaping only teaches one job: stay on an empty track,
as well as possible. It doesn't know objects exist. A separate piece of
the software already watches for obstacles and can nudge the car around
one — built and tested against a simulated obstacle — but it runs as its
own decision layer at drive time, after the trained policy has already
proposed a direction, rather than being folded into this reward. Racing
another car on the same track is further out still. The plan is
deliberately staged: get "stay on the track" solid on its own first,
then add each further capability as its own layer rather than asking one
reward function to learn everything at once.

## Looking Past DonkeySim

Everything above runs entirely inside DonkeySim, which is the right tool
for this stage — free resets, no risk to a real, owned vehicle, fast
iteration. But DonkeySim is also a fairly small, DonkeyCar-specific
world. Longer term, once there's an actual working car rather than a
simulated one, there's a case for moving the whole software stack onto
ROS2 — the standard, much more general framework most real robotics
projects (including ones with multiple robots, or far more sensors than
this one currently has) are built on. That's a deliberate "later," not a
"now": porting a design that's still changing every week would mean
re-doing the port every time it changes, and the current codebase is
already structured — hardware kept behind swappable interfaces rather
than hard-wired in — to make that move cheaper once there's something
proven worth moving.

## Why It Matters

A reward function is a set of instructions written in a language that
can't say "never," only "usually worth more" — get that translation
wrong and the policy will find the exact loophole you didn't mean to
leave. Turning "stay on the track" from one ingredient in a blended
score into something that actually ends the lap when violated is what
makes that instruction mean what it's supposed to mean, instead of
something a fast enough policy can trade away.

---

**Previous in the series:** [From Static Overlay to Object Oriented
Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
**Next in the series:** [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)

---

## Full Series

1. [Radar Without Range](/blog/comp-science/radar-without-range/)
2. [The Tilde Is the Point](/blog/comp-science/the-tilde-is-the-point/)
3. [From Static Overlay to Object Oriented Widget HUD](/blog/comp-science/from-static-overlay-to-object-oriented-widget-hud/)
4. **Stay On, Then Smooth, Then Fast** (this post)
5. [The Later That Came Early](/blog/comp-science/the-later-that-came-early/)
