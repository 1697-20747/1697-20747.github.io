---
title: "Not a Specification"
date: 2026-07-19T21:15:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, LLM, project-management, work-breakdown-structure, DAPT, banks]
description: "The brief was 'write a bank's credit paper.' That's aspiration, not a specification. This is the outline of what the real problem turned out to be, and the path it set."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*This is the first post in a series about building a local, offline
credit-analysis pipeline — written last, but the part that should be read
first. See the full series list at the bottom of this post. This one's
short deliberately — an outline, not a full post. It matters more than its
length suggests, so it'll get expanded later.*

---

## The Brief Wasn't the Problem

"Write a bank's credit paper" is a sentence, not a specification. It names an
output without naming a single one of the decisions that produce it. It's an
aspiration — the kind of brief that sounds achievable right up until you try
to decompose it into things a machine could actually do deterministically.

So the first real work wasn't extraction, or prompting, or fine-tuning. It
was a work breakdown: what does "write a credit paper" actually decompose
into, and which of those pieces are load-bearing?

## The Actual Decomposition

Four distinct sub-problems, not one:

1. **Curated, high-quality credit metrics.** CET1, leverage, NIM, coverage
   ratios — the raw facts a credit assessment stands on. Not "a number was
   extracted somewhere." A number that's correct, sourced, comparable
   across banks and years, and — a dimension the original brief didn't
   even name — for a single, precisely identified legal entity, not
   whichever document with the right numbers on it happened to get
   downloaded.
2. **Quantitative peer assessment.** Where does this bank actually sit
   against comparable institutions — same region, same currency, same
   reporting basis? A ratio in isolation says nothing. A ratio at the 7th
   decile of its real peer group says something.
3. **Qualitative determination.** The judgment layer — is this bank's
   capital position strong, adequate, or weak, and why. This is where
   analyst reasoning actually lives, and it's the one piece that can't be
   fully deterministic by nature.
4. **Assembly into readable prose.** Everything above means nothing to a
   reader until it's written up in the register a credit paper is actually
   expected to read in.

That last clause in step 1 — legal entity as its own dimension of "correct"
— isn't something the original decomposition got right on paper. It's
something that only became visible by building the thing and finding a
real document, months later, that was internally consistent, correctly
sourced, and simply *of the wrong company*. A specification written in
advance can name the categories of correctness it can already imagine.
The rest — the ones you didn't think to ask about — show up as bugs, get
fixed, and get folded back into what "the problem" actually meant all
along. That loop is the real work.

## Which One Is Load-Bearing

A critical read of that list says: 1 is the foundation everything else
depends on, and it's also the one nobody was taking seriously.

If step 3's judgment is well-reasoned but step 1's inputs are wrong, the
output is confident and wrong — the worst combination, because it doesn't
look wrong. Get step 4 right — fluent, well-structured prose — over
ungrounded numbers, and you've built a very convincing way to be
confidently incorrect. This is, more or less, exactly what a base LLM does
if you ask it to "write a credit paper" without giving it anything to stand
on: plausible structure, invented figures, no way to tell the difference
from the outside.

So the decomposition reordered the project. Step 1 stopped being
infrastructure in service of step 4 and became the actual project. Steps
2–4 are downstream of it, not parallel to it.

## Why PDFs Forced the Issue

The naive version of step 1 — pull numbers out of filings — runs straight
into the fact that bank disclosures are not a standardised format. A CET1
ratio is `13.50` in one bank's table, `0.1350` in another's, `1350` (basis
points) in a third. Annual report, Pillar 3, and 10-K each report a
different subset of metrics, sometimes disagree with each other, and are
each formatted by a different team with different conventions across 60
different institutions and up to ten years of history apiece.

You cannot skip past that mess to step 4 by getting a better prompt. The
mess *is* step 1's actual content. Which is what forced a curated metric
dictionary and a real database — a fixed set of metric definitions, one row
per bank/year/metric, explicit units, explicit source pages, explicit
verification tiers — instead of treating extraction as a disposable
preprocessing step. The rest of this series is largely the story of
building and hardening that database.

## The Path So Far

Roughly: an early fine-tuning attempt tried to teach a model the whole job
at once, including judgment and prose — and lost to plain structured
prompting over well-grounded data, because grounding turned out to matter
more than training (post two). Building genuinely trustworthy grounding
turned into its own long project — a metrics database with an increasingly
serious quality layer, culminating in Claude Code doing the actual reading
and cross-checking that step 1 requires (posts three and four).

## What's Expected Next: DAPT for Prose

Step 1 is the hard part, and it's most of what's been built. Step 4 —
prose quality, register, the specific idiom a credit paper is expected to
read in — is the part still expected to benefit from domain-adaptive
pretraining (DAPT): not to teach the model facts (those come from grounded
injection, same as now, non-negotiable), but to teach it *how a credit
analyst writes*, sentence by sentence, once the facts underneath are
trustworthy enough that improving the prose is a safe thing to spend effort
on.

That's a deliberate ordering, not an oversight — you don't refine the
writing style of a document whose facts you don't trust yet. This is next.

---

**Previous in the series:** — this is the first post
**Next in the series:** [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)

---

## Full Series

1. **Not a Specification** (this post)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
