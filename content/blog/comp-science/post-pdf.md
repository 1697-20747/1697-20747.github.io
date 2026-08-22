---
title: "Post PDF"
date: 2026-07-19T22:20:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, data-architecture, PDF, XBRL, EBA, banks, future-work]
description: "A placeholder for the point this whole project is quietly waiting for: machine-readable regulatory disclosure making most of the ingestion layer unnecessary."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Seventh post in a series about building a local, offline credit-analysis
pipeline. Start with [Not a Specification](/blog/comp-science/not-a-specification/),
or see the full series list at the bottom of this post.
This one's a placeholder — a marker for where the project goes once a
precondition outside its control is met, not a finished post. Expand later.*

---

## The Placeholder

Almost everything described so far in this series — the metric dictionary,
the verified tiers, the page-citation discipline, Claude Code doing direct
document reads, the entire quality layer — exists to compensate for one
underlying fact: bank disclosure is still mostly published as PDF.

PDF is a rendering format, not a data format. It preserves what a page
looked like, not what the numbers in it mean. Table structure is
reconstructed by guesswork. Units are inconsistent bank to bank, sometimes
page to page. Filenames carry no reliable convention — the same document
type shows up as a differently-dated, differently-named file every single
year, for every bank, which is most of why "identify and correct" has been
the bulk of the actual work in this project so far.

None of that is a permanent condition. It's a consequence of *when* this
was built, not what the problem structurally requires.

## What Changes It

Machine-readable regulatory disclosure already exists and is expanding —
XBRL-tagged filings, structured XLSX templates, and specifically the newer
EBA Pillar 3 disclosure approach, which moves toward standardised,
machine-parseable templates instead of a PDF a human designed to be read.
When the source document already knows which number is CET1 and which unit
it's in, there's no page to read, no column to misalign, no comparative
year to grab by mistake.

The expectation, not yet realised: as more banks and more jurisdictions
move onto genuinely structured formats, the ingestion workload shifts from
*identification and correction* — the bulk of everything this series has
covered — to straightforward, largely mechanical parsing. The ratio of
project effort spent on error handling versus on the actual analytical
work should shift a lot, quickly, once that precondition is met.

This doesn't retire the quality layer described in the [previous
post](/blog/comp-science/antidote-for-large-liar-model/) — a structured
source can still be wrong, still needs cross-checking, still needs a
verified tier. What it retires is the *guessing*: the part of the job that
exists only because a PDF makes you reconstruct structure that a properly
built data file would have handed over directly.

Worth revisiting once enough of the corpus's source documents actually make
that transition.

---

**Previous in the series:** [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
**Next in the series:** [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)

**Update, 2026-08-04:** the quality-layer work didn't stop while this
placeholder waited. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
covers a basic metric that turned out to have never been formally
checked, five real bugs found by finally auditing it properly, and four
more found for free by checking it against the metric next door.

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. **Post PDF** (this post)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
