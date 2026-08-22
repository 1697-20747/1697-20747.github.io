---
title: "Whose Bank Is This?"
date: 2026-07-19T23:00:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, data-architecture, legal-entity, ring-fenced-banking, scope, banks]
description: "Group and subsidiary are both real, both rated, and easy to conflate. Why this project scopes to group-consolidated only, deliberately, with the architecture already built for the alternative it isn't doing yet."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Eighth post in a series about building a local, offline credit-analysis
pipeline. Start with [Not a Specification](/blog/comp-science/not-a-specification/),
or see the full series at the bottom of this post.*

---

## The Question Nothing Was Asking

A Pillar 3 filing sat in this corpus, correctly formatted, internally
consistent, every number plausible. Thirty-five metrics extracted cleanly.
Nothing about it looked wrong.

It was the wrong bank. Not a different company — the same banking group,
but a ring-fenced retail subsidiary's own disclosure, not the group's. Total
assets off by a factor of five. Every ratio technically real, technically
sourced, technically describing a real regulated entity — just not the one
the corpus intended.

That's a genuinely different failure from anything else this project has
found. A wrong number is caught by checking it against other numbers. A
wrong *document* isn't — the check has to be "is this actually who I think
it is," and nothing in the pipeline was asking that question at all.

## Why the Distinction Is Real, Not Pedantic

Group and subsidiary aren't the same credit story wearing two labels. A
bank holding company and its ring-fenced or otherwise licensed operating
subsidiary are genuinely, separately rated by real rating agencies —
different capital treatment, different regulatory perimeter, and
structural subordination that's real, not theoretical: holdco creditors
typically sit behind opco creditors in a resolution scenario. A lender
exposed to the retail subsidiary specifically has a different credit
position than one exposed to the group, even though both entities share a
name and a logo.

So "which entity is this assessment of" isn't a footnote. It's the same
category of fact as the fiscal year or the reporting currency — the kind
of thing that changes what the rest of the document even means.

## What Was Actually Missing

This project already had a rule about this. The anti-hallucination system
built for the writing phase includes "consolidated group only" — has for
a long time. The rule was correct. It just lived in exactly one place: an
instruction for the model, at the very last step of the pipeline. Nothing
upstream of that ever declared, for a given source document, which entity
it was even *for*. A rule that only constrains the last step can't catch a
wrong entity that entered three steps earlier — which is precisely what
happened, twice, in two unrelated banks, from two different causes (a
wrong file downloaded, and a legal name one word off from the right one).

This is the same lesson the [previous post](/blog/comp-science/antidote-for-large-liar-model/)
already made about hallucination generally: a good instruction is a
backstop, not a strategy. The strategy is a structural check that happens
before the instruction is ever needed.

A related but genuinely different problem turned up while backfilling
legal names across all 60 banks: some banks weren't misidentified, they
*changed*. One restructured into a new holding company partway through the
corpus's history; another renamed itself outright in its most recent
filing year. Same institution, same continuous history, different legal
name depending on which fiscal year you're reading. It's the old question
about a hammer: replace the head, and later replace the handle too — is it
still the same hammer? A credit history is supposed to read as one
continuous track record, and "same bank, different name" isn't the same
failure as "wrong bank entirely" — it doesn't get fixed the same way
either. The answer here was to split the legal name by fiscal year and
record it as a known fact, not force one name across a boundary where the
entity itself changed, and not confuse it with an actual data error.

## The Decision

Scope this project to group-consolidated entities only. Explicitly, not
by default.

Subsidiary-level assessment is a real thing this project could eventually
do, and it isn't being ruled out — it's being deliberately deferred.
Adding it now means researching and ingesting a second tier of filings for
every ring-fenced or otherwise separately-regulated subsidiary across 60
banks, which is a large expansion of scope for a project that already
[decomposed its own work breakdown once](/blog/comp-science/not-a-specification/)
specifically to avoid taking on more than the load-bearing piece required.
Not now.

But "not now" and "not architected for" are different things. The schema
change made alongside this decision adds an explicit scope field to every
filing — which entity, exactly, group or which kind of subsidiary — and a
parent-entity link that's populated for nobody yet, but exists. If a
subsidiary bank is ever added, it plugs into a relationship the schema
already understands, rather than triggering a redesign to make room for a
concept nobody planned for. Build the extension point. Don't build the
extension.

## What Changes in the Output

Every generated credit paper will now state its scope at the top, plainly
— legal entity name, group or subsidiary, and an explicit note when a
subsidiary is out of scope — with the same prominence a rating agency
gives "Issuer: X, senior unsecured." Not a methodology appendix a reader
has to go looking for. The first line.

That's a small change with a specific purpose: a reader shouldn't have to
infer scope from context, or trust that it's correct by default. It should
be a stated fact, checkable the same way every other fact in this pipeline
is checkable — because it's exactly the kind of thing that's easy to get
wrong quietly, and expensive to have gotten wrong without saying so.

---

## References

- [Not a Specification](/blog/comp-science/not-a-specification/) — the work-breakdown discipline this scope decision follows
- [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/) — where the Barclays wrong-entity finding first came up, and the "backstop, not strategy" argument this post extends

---

**Update, 2026-07-22:** the ING Groep finding that motivated this post's
"hammer" section turned out to have a second layer — [Confirmed, Not
Claimed](/blog/comp-science/confirmed-not-claimed/) covers what happened
when this exact entity data was backfilled without being independently
re-checked, and the structural fix (a separate, diffable verification
register) that followed.

---

**Previous in the series:** [Post PDF](/blog/comp-science/post-pdf/)
**Next in the series:** [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. **Whose Bank Is This?** (this post)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
