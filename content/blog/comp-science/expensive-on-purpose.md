---
title: "Expensive On Purpose"
date: 2026-09-12T09:00:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, LLM, AI, agents, data-architecture, verification, on-prem, Qwen]
description: "Verifying one bank's worth of metrics against real source documents cost about half a million tokens. A more efficient reading method barely moved that number. Here's why the cost is the point, not a bug — and why it might belong on a local model instead of a metered API."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Two Numbers

Closing out UBS's remaining metric gaps in the [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
project's verification database — 199 missing cells, each one requiring a
real page number and a real quote from a real filing before it could be
written — cost about 486,000 tokens across 251 tool calls. A comparable pass
on MUFG, 339 cells plus a full re-confirmation of which document belonged to
which fiscal year, cost about 483,000 tokens across 238 calls.

Those numbers are almost identical, which is itself the interesting part.
Between the two runs, the extraction method changed: instead of printing
full PDF pages into the model's own context — an expensive habit, since
every page printed stays in the transcript for the rest of that session,
and a 500-page filing has a lot of pages — the second run dumped each PDF's
text to a scratch file once and grepped small snippets out of it as needed.
That change measurably improved how much got done per token: roughly 40%
more gaps closed for a comparable spend. It did not meaningfully reduce the
total. The token floor for this kind of work turned out to be set by how
much primary material genuinely has to be read and reasoned over, not by
how efficiently that material gets rendered into a prompt.

That raises the obvious question: why does verifying a spreadsheet's worth
of numbers cost this much, and is it actually worth it?

## What a Keyword Match Cannot See

The project's original extraction pipeline — the regex-based `extract_pdf()`
engine documented in the [main README](https://github.com/1697-20747/llm_credit_paper) —
is a reasonable, well-tuned piece of prescriptive code. It knows to skip
segment tables, collapse joined table cells, reject forward-looking targets,
and pick the most frequently repeated value as the authoritative one. It is
also, structurally, unable to catch an entire category of error, because
every fix it has ever needed came from the same root cause: a keyword
matched, so the code assumed the match meant what it looked like it meant.

Three real examples surfaced during the verification pass this post is
based on, none of them findable by any regex:

**The wrong document, for eleven years.** MUFG's `annual_report` field
pointed at the bank's "Integrated Report" — a strategy and governance
publication with no financial statements — for every fiscal year from 2015
to 2025. The extraction pipeline pulled plausible-looking numbers out of it
anyway, because an ESG report about a bank still contains numbers, and some
of them happen to look like the numbers you'd expect. Nothing in a
pattern-matching pipeline asks "is this the right document" — it asks "does
this pattern match," and both questions can have different answers on the
same page.

**A missing line item, for years, in plain sight.** NatWest's total
deposits figure was quietly short an entire balance-sheet line — "Deposits
by banks" — because "Customer accounts" alone matched the keyword and
returned a number that looked complete. It wasn't wrong in the sense of
being a bad extraction of the wrong text; it was a correct extraction of
the wrong scope. A person reading the liabilities section would notice
there were two deposit lines above the total. A keyword search has no
concept of "above the total."

**A number filed under the wrong name, provably.** A Basel Pillar 3
disclosure read "G-SIB/D-SIB additional requirement: 1.5%," and that value
had been stored as a supervisory add-on that only exists in EU and UK
capital frameworks — not in Japan's. Catching this took reconciling the
same regulatory-minimum formula across five separate fiscal years and
noticing there was no room left in any of them for an extra 1.5 percentage
points. A regex has no formula. It has no other years to check the formula
against. It has a string and a pattern, and both matched.

None of these are pattern-matching bugs in the sense of a bad regex that
could be fixed with a better regex. They are questions about what a number
*means* — the right document, the right scope, the right label — and
answering that requires actually reading the source and reasoning about it,
every single time. That is why it's expensive. It isn't expensive because
the task is being done inefficiently; it's expensive because judgment is
being applied to every cell instead of a keyword match, and judgment,
delivered at scale by something that can also read a 500-page PDF start to
finish, does not come for free.

## The Honest Accounting

It would be a cleaner story if the fix for the cost were purely technical —
read the document more cleverly, and the bill drops. That is partially
true: dumping full pages into a running transcript is wasteful in a
specific, avoidable way, because every page printed gets re-paid for on
every subsequent step of that session. Extracting once to a file and
grepping the parts you actually need avoids that particular tax.

But the MUFG-vs-UBS comparison shows the honest limit of that fix. Same
order of magnitude in tokens, meaningfully more work delivered — not a
collapse in absolute cost. Once the wasteful rendering is fixed, what's
left is the actual floor: a document has to be opened, a table has to be
found, a number has to be checked against its neighbours and its prior
years, and a citation has to be real. There isn't a clever prompting trick
that makes that step free, because the step *is* the value being produced.
A cheaper version of it is a version that skips some of the checking, and a
version that skips the checking is a version that reproduces exactly the
bugs described above.

## Why Spend It Anyway

The case for paying this cost isn't that it's cheap — it demonstrably
isn't — it's that the alternative has been quietly failing for years at a
time without anyone knowing, which is a worse kind of expensive. A
`rwa_bn` value that repeats identically across five different fiscal years
for the same bank isn't caught by a sanity-range check, because each
individual value is perfectly plausible on its own. It's only caught by
someone — or something — noticing that five *different* years produced the
*same* number, which requires holding several years in mind and comparing
them, not scanning one page at a time.

What makes it safe to spend this kind of judgment liberally, rather than
carefully rationing it, is the write discipline sitting underneath: every
confirmed value in the database is `verified >= 2` and immutable — insert a
new row and mark the old one superseded, never update or delete in place.
An agent with a wrong idea about a number can't silently overwrite a
correct one; it has to hold the wrong idea for human review instead. That
single constraint is what turns "let an LLM read the actual documents and
form a judgment about every cell" from a reckless idea into a workable one.
Expensive judgment, applied everywhere, backed by a schema that makes it
impossible for a bad judgment to quietly win.

## The On-Prem Case

The [first post in this project's original series](/blog/comp-science/llm-credit-paper-generator/)
runs a 7-billion-parameter Qwen2.5 model locally, on a Mac, for the actual
job of *writing* a credit paper — turning already-verified numbers into
analyst prose. That's a task that rewards a strong single model with good
judgment about tone and structure, and the post's own conclusion was that
careful prompting of a small base model beat a fine-tuned version of the
same model outright.

The *ingestion and verification* workload this post is about has a
different shape, and it's worth asking whether that different shape wants
a different kind of model.

Writing a credit paper needs, once, a coherent piece of prose from a
capable model. Verifying a bank's worth of metrics needs, hundreds of
times, the same small set of moves: open a document, find a number, check
it against a rule or a neighbouring year, cite it exactly or refuse. It's
repetitive, well-specified, and self-checking by construction — the
insert-and-supersede schema and the tiered review discipline (write freely
when nothing is uncertain; hold for a human the moment something touches a
protected value or genuinely disagrees with itself) mean that a wrong
answer from the model doesn't corrupt anything. It either fails a
consistency check, fails a cross-document check, or gets parked for review.
The safety here comes from the *harness*, not from the raw intelligence of
whatever sits inside it.

That's exactly the profile that stops looking wasteful on a metered
frontier API and starts looking like a good fit for something bigger than
Qwen2.5-7B but still local — a 32B-class open-weight model, run on owned
hardware, at effectively zero marginal cost per token once the machine is
paid for. Half a million tokens per bank, times sixty banks, times however
many correction rounds a corpus this large eventually needs, is a real,
recurring dollar figure against a hosted API. Against local compute it's
electricity and time. And because the harness — not the model — is doing
the work of catching mistakes, you can afford to spend those free tokens
liberally: re-read a filing twice, cross-check a formula across every year
instead of just the one in question, run the same cell through the
extraction step more than once and compare. None of that is affordable to
do twice on a metered bill. All of it is nearly free once the hardware is
already running.

The honest caveat is that the *hardest* calls in this dataset — reconciling
a formula across five years to prove a value is mislabeled, or noticing
that a hedge notional jumping 60x in a single year isn't a plausible trend
for a systemically important bank — plausibly still benefit from a stronger
model's raw reasoning. The sensible design probably isn't "replace the
frontier model with a local one," it's an extension of the tiered review
discipline the project already has: a local model doing the high-volume
reading and citation grind, escalating to a stronger model — or straight to
a human — exactly when something doesn't reconcile. Cheap model, expensive
model, human, in that order, instead of just write-freely-or-hold-for-a-human
in two tiers. The infrastructure for that (the hold queue, the audit log,
the immutable-once-verified schema) already exists; it just doesn't yet
route by confidence to more than one model.

## What This Series Is

This is the first post in a second series about this project — separate
from the [original series](/blog/comp-science/llm-credit-paper-generator/),
which covers the credit-paper generator itself: the fine-tuning experiments,
the grounding mechanisms, the anti-fabrication rules. This series is about
the less glamorous half of the same project — the operational reality of
running a large, agentic, document-heavy verification pipeline against sixty
banks' worth of real filings, the specific bug shapes that only show up at
that scale, and the infrastructure decisions (insert-and-supersede, tiered
review, a verification layer that's structurally separate from the record it
verifies) that make spending this much computation on data quality
survivable rather than reckless. More entries to follow as the corpus grows.

---

**Previous in the series:** — this is the first post
**Next in the series:** — to be written

---

## Full Series

1. **Expensive On Purpose** (this post)

---

*See also, from the project's original series:* [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/),
[Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/), and
[Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/) — all
about the same verification database this post's token-cost numbers came
from.
