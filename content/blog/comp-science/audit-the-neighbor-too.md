---
title: "Audit the Neighbor Too"
date: 2026-08-04T09:00:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, data-architecture, verification, provenance, banks, deposits]
description: "A metric in active use across 34 banks had never been formally checked. Auditing it properly caught five real bugs. Cross-checking it against the metric next door caught four more, for free."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Tenth post in a series about building a local, offline credit-analysis
pipeline. Start with [Not a Specification](/blog/comp-science/not-a-specification/),
or see [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
for the verification argument this post turns out to be a second instance
of — one layer down, in a metric's value instead of a document's identity.*

---

## In Use, Never Checked

`total_deposits_bn` had been sitting in the corpus for a while — 361 rows
across 34 banks, most written `verified=1` by an early bulk-extraction
pass, most with no `source_page` or `source_quote` at all. It had simply
never been added to the schema files (`SANITY_RANGES`, the metric
dictionary, the data dictionary) that every other metric goes through
before being trusted. A basic bank number, present, plausible-looking,
never the subject of its own dedicated audit.

That's exactly the shape of problem the [previous
post](/blog/comp-science/confirmed-not-claimed/) described: a populated
field and a confirmed fact render identically. Nothing about `verified=1`
told anyone whether the value had actually been checked.

## Five Ways It Was Wrong

Formalizing the schema, then independently re-verifying all 637 rows
against source across all 60 banks, found five distinct, real bug shapes
— not citation upgrades on numbers that were already right:

1. **Customer-only mislabeling** — NAB, Lloyds, NatWest, Santander,
   Société Générale: an early pass captured "customer deposits" and
   missed a separate bank/wholesale line entirely. Deltas of +2% to +25%.
2. **Average vs. period-end** — Northern Trust, Synchrony Financial:
   sourced from an MD&A "average deposits" schedule instead of the actual
   balance-sheet figure.
3. **Wrong item folded in** — Pinnacle Financial (a repo line summed in
   by mistake); UniCredit, a compound case where debt securities were
   wrongly included *and* real bank deposits were wrongly excluded at the
   same time, so the error's sign flips across the decade instead of
   sitting at a constant bias.
4. **Restated-comparative trap** — CBA, Royal Bank of Canada, de
   Volksbank: a later filing's restated comparative column used instead
   of the figure as originally filed.
5. **Unit error** — Wintrust Financial, all ten years written 1,000x too
   large.

None of these were caught by the corpus's bounds checks, because bounds
checks only catch a number that's implausible on its own. All five were
plausible. They were just wrong.

## Then the Neighbor Lit Up Too

`total_assets_bn` was already fully in the schema — this wasn't a
formalization gap. But while closing out deposits, cross-checking the
deposits-to-assets ratio bank by bank surfaced four more real bugs sitting
in that metric too: Barclays (a UK-segment sub-total grabbed instead of
the group-consolidated total, three years, ~5x too small), SMFG (a value
stored with unit `%`, which makes no sense for a balance-sheet figure),
Société Générale (a ~10x error flagged back in July and never actually
fixed until it turned up again here), and de Volksbank (smaller misreads
plus another restated-comparative case).

None of those four were found by auditing `total_assets_bn` directly.
They fell out of checking it *against something else that should agree
with it*. That's the actual reusable idea here: once one metric has been
properly, independently re-verified, checking it against a structurally
related neighbor is nearly free and catches a different class of bug than
either metric's own bounds check ever could — because two numbers that
should stay in a sane ratio to each other, and don't, is a signal that
exists nowhere else.

`total_assets_bn` is next up for the same full treatment deposits just
got. Applying it to its own neighbor — `rwa_bn`, the metric it's the
denominator for — is the obvious next check once that's done.

---

## Key Takeaways

- A field marked `verified` and a field that's actually been checked are
  not the same claim — whether the field is a document's identity or a
  metric's value.
- A number can sit in active, corpus-wide use for a long time without
  ever having been the direct subject of its own audit.
- Once a metric is properly audited, cross-check it against a related
  one. It's cheap, and it catches bugs the metric's own bounds check
  structurally cannot.

---

## References

- [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/) — the verification-register argument this post is a second instance of
- [Not a Specification](/blog/comp-science/not-a-specification/) — the problem statement this whole series works from

---

**Previous in the series:** [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
**Next in the series:** — this is the latest post

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. **Audit the Neighbor Too** (this post)
