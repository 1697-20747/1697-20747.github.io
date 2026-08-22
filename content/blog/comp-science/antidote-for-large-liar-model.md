---
title: "Antidote for Large Liar Model"
date: 2026-07-19T22:00:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, LLM, hallucination, data-architecture, error-handling, banks, Qwen]
description: "Why the ingestion pipeline was designed, from the first line of code, so the LLM writing phase can never become the source of a fact — and what error handling actually means when the failure mode is confident invention, not a crash."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Sixth post in a series about building a local, offline credit-analysis
pipeline. Start with [Not a Specification](/blog/comp-science/not-a-specification/)
for the problem statement, or see the full series at the bottom of this post.*

---

## The Large Liar Model Problem

Ask a base language model to write a bank's credit paper and it will. Fluent
structure, correct-sounding vocabulary, plausible numbers, a confident tone
throughout — and some fraction of those numbers will be invented. Not
maliciously. An LLM doesn't know the difference between recalling a fact and
generating a plausible continuation of a sentence that *looks like* a fact —
that's not a bug in one particular model, it's what the architecture does by
design. Qwen2.5-7B will do it. So will everything else in its weight class.
The earlier post in this series has a real example: asked for peer context
without grounded data, a model invented a specific-sounding figure — a named
bank's statutory profit, quoted to the nearest million — that was simply not
true, delivered with exactly the same confidence as the true numbers around
it.

That's the problem this post is actually about. Not "the model is sometimes
wrong" — every system is sometimes wrong. The specific failure mode is a
system being *confidently, plausibly, undetectably* wrong, which is worse
than an error that announces itself. A crash is cheap to notice. A wrong
number formatted exactly like a right number is not.

For a project whose stated goal is a deterministic assessment of credit
risk — the whole premise laid out in the first post — this isn't a rough
edge to sand down later. An assessment nobody can fully trust isn't a lesser
version of the product. It isn't the product.

## Why "Error Handling" Means Something Different Here

Conventional error handling assumes the failure announces itself: an
exception, a null pointer, a stack trace. You catch it, log it, maybe retry.

Hallucination doesn't throw an exception. It returns 200 OK with a wrong
number formatted identically to a right one. Traditional error handling has
nothing to catch, because nothing failed in the traditional sense — the model
did exactly what it's built to do, which is produce a plausible continuation.
The number just happens not to be true.

So the error handling that actually matters here isn't in the LLM call at
all. It has to happen *before* the model is ever given the opportunity to be
the source of a fact — which means it's not a feature of the writing phase.
It's a property the ingestion pipeline has to have from its very first line
of code, long before any prose gets generated.

## The Antidote, Mechanism by Mechanism

Everything described in the earlier posts in this series turns out, in
retrospect, to be a specific defense against a specific way a model could
end up inventing a fact:

**Grounded extraction only — read, never recall.** Every metric in the
database is tied to a source page and, wherever possible, a direct quote.
Nothing is "known" in the sense a language model knows things. It's looked
up, every time, from a document that still exists and can be re-checked.

**`not_found` is a legitimate answer.** This is probably the single most
important discipline in the whole pipeline, and it's the one most tempting
to skip. A missing fact stays missing. It does not get filled with the most
plausible-looking nearby number. Across this entire corpus, hundreds of
cells are deliberately, permanently `not_found` — not because nobody looked,
but because looking honestly is worth more than a fabricated completeness.
Silence, recorded explicitly, beats invention every time.

But a `not_found` still has to be *earned*, and that's a different
discipline from the one above — not "don't invent a value," but "don't
declare absence until you've actually looked hard enough to mean it." A
real example: three years of M&T Bank's core capital metrics — CET1,
Tier 1, total capital, leverage ratio, RWA, deposits — sat `not_found`,
logged and explained as truncated source files. The files were re-
downloaded fresh from SEC EDGAR to fix it, and turned out to be
byte-identical to what was already on file. Nothing was truncated. The
actual finding, mid-investigation: *"Major finding — the data isn't
missing at all. The table exists, but the bank switched from spelling
out 'Common Equity Tier 1' to using the abbreviation 'CET1' starting
FY2023 — the original entry's grep only searched for the full phrase and
missed it entirely. Let me pull the complete table with full context."*
The table was a clean, complete, correctly-labeled three-entity capital
disclosure, sitting on the page the whole time. Eighteen rows filled once
someone actually looked instead of trusting the stored diagnosis of why
they were missing. Getting `not_found` right doesn't just mean refusing
to guess; it means treating an apparent absence as a claim that needs
checking too, the same as any other extracted fact — including checking
whether the *reason* you were given for the absence is itself true.

**Verified tiers, not blanket trust.** A value that's been through a
first-pass automated extraction and a value a human — now, almost always
Claude Code doing a direct source read — has confirmed by hand are not
treated the same. Anything consuming this data downstream, including a
future prose-generation step, can ask *how sure are we of this specific
number* and get a real answer, not an assumption.

**Insert-and-supersede — wrong facts leave a trail.** A correction never
silently overwrites. The wrong value stays on record, marked superseded,
with the reasoning for the correction attached. A fact that turned out to
be wrong is never allowed to simply disappear as if it had never been
asserted — which matters because a system that can quietly erase its own
mistakes is a system nobody can fully audit.

**Two sources have to agree.** Where the same fact is reported
independently in an annual report and a Pillar 3 filing, both get checked
against each other. Disagreement doesn't get silently resolved by trusting
whichever document was read first — it gets surfaced as a finding. This is
the same instinct as requiring two independent sources for a claim before
trusting it: a single source, however confident-looking, is still one
source.

That check assumes both documents are actually *for the same thing*, which
isn't always true. One bank's Pillar 3 filing turned out, on inspection of
its own cover page, to belong to a ring-fenced retail subsidiary — not the
group the corpus intended. Every one of the 35 metrics pulled from that file
was real, correctly extracted, internally consistent — and quietly
describing the wrong legal entity, at a fraction of the group's actual
scale. The cross-document check only flagged 2 of the 35, because the other
33 had no annual-report figure to disagree with; the other 33 would have
sat there, plausible and wrong, indefinitely. The fix wasn't a value
correction, it was re-sourcing the actual group-level document — a reminder
that "the number is wrong" and "the document is wrong" are different
failures, and a check built to catch the first won't reliably catch the
second.

**Numbers still have to make sense together, not just look right alone.**
CET1 can never exceed Tier 1 capital. That's not a business rule, it's
arithmetic — and it's caught several real errors in this corpus that
individually looked completely plausible. A number can pass every
formatting check and still be wrong; checking it against the *other*
numbers around it catches what checking it in isolation can't.

**Nothing gets corrected without a second opinion.** Every proposed
correction in this pipeline — whatever found it, automated sweep or Claude
Code source read — gets compiled into a review list with the exact source
quote, and gets an explicit approval before it's written. No automated
process is allowed to trust its own conclusion enough to skip that step, no
matter how confident the match looks.

**The pipeline keeps a memory of how it's been wrong before.** A confirmed
bug pattern gets logged permanently, not fixed once and forgotten. Fifty-
eight distinct findings exist in that record as of this series' most recent
post — which means the system doesn't just get corrected, it gets
structurally harder to make the *same* mistake again, because the next
person or process checking a suspicious value can query what's already
been found rather than rediscovering it from nothing.

**Even "we removed a wrong number" gets checked.** The newest piece of this
architecture exists because retracting a bad value and never following up
on it produces exactly the same silence as a genuinely undisclosed fact —
indistinguishable from the outside, which makes it its own quiet failure
mode. A dedicated check now exists specifically to make sure a retraction
was actually followed by a real answer, not just an absence.

## The Last Line of Defense, Not the First

The earlier post in this series already described the system prompt rules
the writing-phase model follows: cite every figure to a page, cite every
peer value to the roster, never invent a peer figure, write "data not
available" rather than fabricate. Those rules matter. But they're the *last*
line of defense, not the first — a backstop for a model that, by the time it
sees a prompt, has already been handed nothing but checked, sourced,
cross-validated facts. The instruction "don't fabricate" is far more
reliable when the model is never actually put in a position where
fabricating would be the easy path, because there's no gap in the provided
facts for a plausible invention to fill.

That's the actual antidote. Not a better prompt asking the model to be
honest — a pipeline built so the model is structurally never the party
being trusted for a fact in the first place. By the time Qwen, or whatever
model eventually gets the DAPT treatment mentioned in the first post, is
asked to write a sentence, every number in that sentence is already true.
Its job is explaining a fact someone else already checked, not recalling
one from its own weights.

## Why This Matters at Commercial Level

A hobby project can tolerate an occasionally wrong number. A credit
assessment that's going to inform an actual decision cannot — a
confidently wrong CET1 ratio is not a rounding error, it's a materially
wrong risk conclusion delivered with false authority. The bar for "good
enough" is different once the output is meant to be relied on rather than
admired.

Which is really the whole point of everything described in this series so
far: build the part that has to be certain first, make uncertainty a
first-class, visible state rather than something that gets papered over,
and only then let a language model anywhere near the sentence-writing part
of the job — where its actual strength is composing fluent, well-structured
prose around facts, not supplying the facts themselves.

---

## Key Takeaways

- Hallucination doesn't throw an exception. The error handling that matters
  has to happen before generation, not around it.
- `not_found`, recorded honestly, is worth more than a plausible guess. A
  visible gap is a fact. A filled gap that shouldn't have been filled is a
  liability wearing a fact's clothes.
- A number that looks right in isolation can still be wrong. Check it
  against the other numbers around it, not just against its own formatting.
- Never let a process approve its own correction. A second check, with the
  source quote attached, is cheap insurance against a confident mistake.
- Remembering how a system has been wrong before is what stops it from
  being wrong the same way twice.
- The prompt-level anti-fabrication rules are a backstop, not the strategy.
  The strategy is not giving the model the opportunity to fabricate in the
  first place.

---

## References

- [Not a Specification](/blog/comp-science/not-a-specification/) — the problem statement this whole series works from
- [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/) — the fine-tuning journey, and the invented-peer-figure example referenced above
- [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/) — the accounting-regime bug that started the shift toward durable, queryable memory
- [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/) — what the ingestion pipeline described here actually looks like in practice

---

**Update, 2026-07-19:** [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
takes the Barclays wrong-entity finding mentioned above and follows it
somewhere new — group vs. subsidiary as a scope question, not a data-
quality one, and the deliberate decision to defer subsidiary-level
assessment while building the architecture to support it later.

---

**Previous in the series:** [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
**Next in the series:** [Post PDF](/blog/comp-science/post-pdf/)

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. **Antidote for Large Liar Model** (this post)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
