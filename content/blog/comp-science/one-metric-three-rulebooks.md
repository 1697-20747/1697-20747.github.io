---
title: "One Metric, Three Rulebooks"
date: 2026-07-11T16:20:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, data-architecture, sqlite, IFRS9, CECL, banks]
description: "Why a Stage 3 ratio can't exist on a US bank's balance sheet, and what to do architecturally once you notice a whole class of bug shaped like that."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## The Problem

I'm building a 59-bank credit-analysis corpus — UK, EU, US, Australian, Canadian, Swiss, Japanese — with a fixed set of metric keys per bank per year: CET1 ratio, leverage, NIM, and so on. One of those keys is `stage3_ratio`, the IFRS9 "Stage 3" credit-impaired loan ratio.

A correction came through on a US bank: `stage3_ratio` had a real number sitting in it — 1.12% — except it wasn't a Stage 3 ratio at all. It was that bank's allowance-for-credit-losses coverage ratio, extracted by a pattern that matched on the shape of the sentence rather than the accounting concept behind it. Fixed the row, moved on.

Except the fix was too narrow. IFRS9's Stage 1/2/3 classification is an IASB standard. US banks report under US GAAP, which has never had staging — not under the old incurred-loss model, and not under CECL, which replaced it in 2020. There is no fiscal year, no filing, no future correction pass in which a US bank will ever have a real Stage 3 ratio. It's not a gap waiting to be filled. It's not there because the concept doesn't exist under that accounting regime.

That's a different kind of problem than a bad regex. A regex bug gets fixed once. This one was going to get *rediscovered* — once per US bank, about thirty times, each time looking like a fresh correction note instead of the same fact restated. The knowledge that "this metric structurally can't exist here" was living in one row's free-text notes field. Nothing in the schema knew it.

## The Solution

The fix wasn't a bigger regex. It was making the accounting regime a queryable fact instead of a fact re-derived by search every time.

A few pieces:

**Reused existing infrastructure instead of building new infrastructure.** The project already had a table for exactly this shape of problem — bank-level facts that are true for a date range and explain *why* a metric is missing (originally built for things like Fed Tailoring categories: some US banks are exempt from LCR/NSFR disclosure entirely). Accounting regime is the same shape of fact. It just needed a new category value, not a new table.

**Made the metric dictionary regime-aware.** Every metric key now optionally declares which accounting regimes it applies under, and which regimes are a *permanent* structural gap rather than a temporary one. That distinction matters — a permanent gap should never be searched for again; a temporary one should keep being searched until it's found.

**Seeded it in bulk, not per-bank.** This is the part that actually closes the loop. Unlike a bank's regulatory exemption category, which genuinely has to be discovered per bank by reading a filing, accounting regime is public and knowable in advance for every bank at once — IFRS9 adopted worldwide in 2018, CECL phased in for US filers in 2020. So instead of waiting for the pipeline to rediscover "no staging under US GAAP" thirty separate times, it gets asserted once, for all 59 banks, in a single pass.

**Kept every write reversible and dry-run by default.** Nothing here touches the live database automatically. The scripts print what they'd do; a human reviews it; only then does `--execute` write anything, and even then existing verified data is protected — if a value already trusted by a human conflicts with what the sweep would write, it gets flagged for review instead of overwritten.

The unplanned bonus: while researching exactly which regime each bank falls under, it turned out two banks I'd been treating as a matched pair — grouped under the same region, same general assumptions — actually report under *different* accounting bases entirely. One's filings are US GAAP; the other's are IFRS. Nobody had checked, because they'd never needed correcting before. Which is really the whole lesson: the bug that costs you isn't the one you're actively chasing, it's the assumption sitting quietly a few rows up that nobody's had a reason to question yet.

## Update: splitting the metric itself

The regime-awareness above tells the pipeline *when* a metric can't exist. It doesn't stop the original bug from recurring in a quieter form: the metric key that started this whole thing — call it the ECL coverage ratio, allowance divided by gross loans — was still one key doing double duty. An IFRS9 bank's figure and a CECL bank's figure would sit under the identical name, numerically similar, methodologically not the same thing at all. IFRS9's version is a staged calculation — 12 months of expected loss for performing loans, lifetime for anything watch-listed or worse. CECL's version is lifetime-expected-loss from day one, no staging, a genuinely different measurement philosophy that happens to land in a similar range.

Same shape of mistake as the original bug, just one level more subtle: not "wrong regime entirely" but "right general idea, wrong specific rulebook," quietly averaged together under one name.

Decision: split it in two, one key per regulation — the original name kept for the IFRS9 version, since "expected credit loss" is IFRS9's own term; a new, deliberately differently-worded key for the CECL version, borrowing CECL's own vocabulary ("allowance for credit losses") instead of reusing IFRS9 language for a non-IFRS9 concept. The naming itself is doing some of the work here — if the two keys don't share a word, nobody skims past the distinction by accident.

One thing deliberately left out: the older US accounting regime CECL replaced, which also produces an allowance-coverage figure, doesn't get a third key. Two rulebooks were named, so two keys got built. The older figures aren't deleted or force-fitted into either new bucket — they're flagged as unhomed, visibly, so the gap is a decision waiting to be made rather than a silent loss.

And because a live pipeline had already been extracting values under the old single key for months, resolving this on paper wasn't enough — existing rows needed sorting by which regulation actually produced them, correctly-keyed ones left alone, wrongly-keyed ones moved. Anything already trusted by a human doesn't get moved automatically either, on the theory that re-labelling what a number *means* is a bigger action than correcting what it *says*, and deserves a second look rather than a script's confidence.

## Key Takeaways

- A structural gap and a temporary gap look identical in a single row. They should never be handled by the same code path.
- If a fact is knowable in advance for every entity in your dataset, don't let your pipeline rediscover it one entity at a time.
- Reuse the table shape you already have before reaching for a new one — "effective-dated fact explaining a gap" was already solved here, just for a different category.
- The pair you never re-checked is exactly where the next surprise lives.
- "Numerically comparable" and "the same metric" are different claims. A shared name asserts the second one whether you meant to or not.
- When you leave a gap deliberately, say so in the same place someone would look for the answer — a flagged gap is a decision; a silent one is a future bug report.
