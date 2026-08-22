---
title: "Confirmed, Not Claimed"
date: 2026-07-22T18:00:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, data-architecture, verification, provenance, banks]
description: "A field that says a fact is true and a fact that's actually been checked look identical, right up until they disagree. Why file identity now lives in a separate, independently-built register instead of a column on the record it describes."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Ninth post in a series about building a local, offline credit-analysis
pipeline. Start with [Not a Specification](/blog/comp-science/not-a-specification/),
or see the full series at the bottom of this post.*

---

## Two Days, Wrong, Looking Fine

A filing's entity fields said `legal_entity_name: ING Groep N.V.`,
`entity_scope: group_consolidated`. Both populated. Both plausible. Both
sitting there for two days after being written during a routine backfill.

The actual PDF's own cover page said "ING Bank Annual Report 2021" — a
different, narrower entity than the one the database claimed. Nothing
caught it, because nothing was checking. The backfill that wrote those
fields never re-opened the file to confirm; it just filled in a
reasonable-looking value and moved on, the same way any of the wrong-
entity bugs this project has found started — Truist, NatWest, a Barclays
Pillar 3 report, a Société Générale filing that was secretly a duplicate
of something else entirely. What made this one different is that it was
caught only by accident, because a later pass happened to re-check.

## A Field That Asserts and a Fact That's Been Checked Look the Same

That's the actual lesson, and it's more general than entity names. A
column in a database doesn't carry any information about how sure anyone
is that it's true. `legal_entity_name` populated by a careful direct read
of a cover page, and `legal_entity_name` populated by a bulk backfill that
assumed consistency, render identically. Query the table and you can't
tell which one you're looking at.

This project has run into a version of this before — a `not_found` value
that was genuinely checked and confirmed absent looks exactly like a
`not_found` that nobody's gotten around to yet, unless something separate
is tracking which is which. That's what `qa_classify_gaps.py` exists to
fix for missing values. The ING finding is the same problem, one layer up
— for the *identity* of a source document, not a metric inside it.

## The Fix Is Structural, Not a Reminder to Be Careful

The fix isn't "be more careful during backfills." That's a policy, and
policies are exactly the kind of thing this project's own [anti-
hallucination architecture](/blog/comp-science/antidote-for-large-liar-model/)
already argued against relying on — a rule is a backstop, not a strategy.

The actual fix: a separate table, `file_register`, populated only by
independently opening a file and reading its own stated identity — never
copied from what the main record already claims. Every filing's entity
name, scope, document type, and fiscal year gets a *second*, independently
sourced answer, with the exact cover-page text that produced it. Then the
two get diffed. Agreement means nothing changed. Disagreement is a live
alarm, the moment it exists — not a coincidence discovered two days or two
months later.

The reason this has to be a separate table, not a "verified" checkbox on
the existing one, is the same reason `qa_classify_gaps.py` isn't a column
on `metrics`: a verification layer that lives inside the thing it's
verifying inherits all the same blind spots. If the backfill script had
just added a `verified: true` flag next to the fields it was populating,
it would have marked itself correct with exactly the same confidence it
got the value wrong with.

## The Broader Point

Hallucination isn't only something a language model does. A backfill
script that fills in a plausible value without re-checking the source is
doing the structurally identical thing a language model does when it
completes a sentence with a plausible-sounding number — producing
something that looks like a fact because it's shaped like one, not
because anyone confirmed it. The fix for both is the same: don't trust a
value because it's present and formatted correctly. Trust it because
something independent checked, and can be asked to check again.

---

## Key Takeaways

- A populated field and a confirmed fact are not the same claim, and
  nothing about how a database renders them tells you which one you have.
- Verification that lives inside the record it verifies inherits that
  record's blind spots. It has to be structurally separate to be worth
  anything.
- The fix for "someone might forget to check" is never a reminder. It's
  a system where forgetting to check is visible.

---

## References

- [Not a Specification](/blog/comp-science/not-a-specification/) — the problem statement this whole series works from
- [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/) — the entity-scope question this post is the structural answer to
- [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/) — the anti-hallucination architecture this extends to human/script-driven backfills, not just model output

---

**Previous in the series:** [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
**Next in the series:** [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)

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
9. **Confirmed, Not Claimed** (this post)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
