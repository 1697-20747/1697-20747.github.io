---
title: "Adding the 61st Bank"
date: 2026-07-19T20:30:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, claude-code, LLM, data-architecture, sqlite, agentic-workflows, banks]
description: "How this project's bank-ingestion pipeline has changed since May, what Claude Code actually does in it now, and what happens end to end when a new bank gets added."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

This is the fifth post in an accidental series about building a local, offline
credit-analysis pipeline. The [first post](/blog/comp-science/not-a-specification/)
laid out the actual problem statement — why "write a bank's credit paper" was
an aspiration, not a specification, and why the metrics layer turned out to be
the load-bearing piece. The [second](/blog/comp-science/llm-credit-paper-generator/)
was about the fine-tuning journey and why structured prompting beat a trained
model. The [third](/blog/comp-science/one-metric-three-rulebooks/) was about
one specific architectural bug — a metric that couldn't exist under a given
accounting regime, and what it takes to stop rediscovering the same fact one
bank at a time.

This one is different. It's not about a bug. It's about how the actual
ingestion process — the thing that turns a bank's PDF filings into rows in a
database — has quietly become a completely different kind of system since May,
and what genuinely happens now when a new bank gets added.

The short version: it used to be regex over PDF text. It's now Claude Code
reading source documents the way an analyst would, cross-validating what it
finds against a database it already partly trusts, and writing its own
findings into a table designed specifically so the next session doesn't have
to rediscover them. The corpus currently stands at 60 banks. This post is
about what happens for the 61st.

---

## The Beginning: Regex and Hope

The first version of this pipeline, described in the earlier post, worked like
this: a script opened a PDF, ran regular expressions over the extracted text
looking for patterns like "CET1 ratio... (\d+\.\d+)%", and tagged whatever
matched with the page number it came from. It worked well enough to build a
benchmark index and a peer roster for prompt injection, which was the actual
goal at the time — the metrics themselves were inputs to something else, not
the product.

That approach has a ceiling, and the ceiling is lower than it looks. A regex
that matches "CET1 ratio... 14.0%" also matches "the regulatory minimum CET1
ratio... 4.5%" if the sentence shapes are similar enough, and it has no way to
know the two numbers mean opposite things. It matches the first plausible
percentage near the right words, which means it will happily grab a
prior-year comparative column instead of the current year, or a subsidiary
entity's figure instead of the consolidated one, or — in one memorable case
this month — an exact duplicate of a completely different metric's value that
happened to be sitting one column over.

None of these failures look like failures. They look like data. A wrong
number in a spreadsheet doesn't raise an exception. It just sits there,
plausible, until something downstream notices it doesn't add up — and
"downstream" here means CET1 exceeding Tier 1 capital, which is
mathematically impossible under every capital framework this corpus covers,
sitting quietly in the database for weeks before anyone asked whether the
ordering held.

## What Changed

The corpus grew from a benchmarking input to the actual product: a golden-
source SQLite database, one row per (bank, fiscal year, metric), with a
fixed dictionary of 43 metric keys and a deliberately strict set of rules
about how a row is allowed to change.

The rules that matter most:

**Insert-and-supersede, not update-and-overwrite.** A correction never
overwrites a row. It inserts a new one and marks the old row as superseded.
The wrong value doesn't disappear — it becomes a historical record of having
been wrong, with the correction's reasoning attached. This turns out to
matter enormously for catching a whole *class* of bug later, which I'll get
to.

**A four-tier verification system.** Every row carries a `verified` level:
0 for a first-pass automated extraction, up through 2 for a value someone —
now, almost always Claude Code — has read from the actual source document
and cross-validated by hand. Higher tiers are protected: an automated sweep
is not allowed to overwrite a `verified=2` row, only flag a conflict for a
human to look at.

**One write path.** Every insert in the database goes through a single
shared function, `safe_upsert.py`. This sounds like a small thing. It
stopped being small the day a supersede-ordering bug — two nearly-
simultaneous writes racing each other — corrupted several banks' data before
anyone noticed the pattern. Centralising the write path was the fix, and it's
been the *only* write path since.

**A durable memory for findings, not just data.** Alongside the metrics
table sits `architecture_feedback` — a table, not a comment, not a Slack
message, not a paragraph in someone's head. Every time a bug pattern gets
confirmed (not guessed at — confirmed, with a source read), it gets logged
here: what it looks like, how many rows it affects, whether it's fixed.
Fifty-eight entries exist in that table right now. It is, genuinely, the
project's memory of its own mistakes.

## What Claude Code Actually Does

The honest answer is: it reads. Not "runs an extraction script" — reads,
the way a junior analyst would, page by page, and then does the parts of the
job that used to require a human specifically because they require judgment,
not pattern-matching.

A few real examples from the last few days, because abstractions are less
convincing than specifics:

A capital-ratio correction for one Japanese bank's Pillar 3 report turned
out to unmask a second, live bug in the same table — its Tier 1 ratio wasn't
just wrong, it was an *exact duplicate* of the (also wrong) CET1 figure from
one column over. Not a similar number. The identical figure, copied across
two different metric fields. A regex has no concept of "this number appears
twice where it shouldn't" unless someone tells it to check for exactly that
shape of mistake in advance. A read catches it because a read notices the
table has two rows with the same value and asks why.

A UK bank's per-year figures looked internally consistent for two
consecutive fiscal years — large, plausible, in the right range — until a
direct read confirmed they were both the *prior* year's comparative column,
carried forward twice. The bug wasn't a bad number. It was the right number,
attached to the wrong year, two years running.

A custody bank's own capital table turned out to report two different legal
entities side by side — the consolidated group and a subsidiary bank — each
further split by two different regulatory calculation approaches, giving
eight numeric columns for what looked, from a distance, like a single row of
figures. Confirming the correct column required cross-matching the *prior*
year's already-verified figure against the table first, to establish which
column was which, before trusting the adjacent year.

And one Japanese bank's Pillar 3 filing for a specific fiscal year turned
out, on inspection, not to be a Pillar 3 filing at all — it was a byte-level
duplicate of the same bank's annual report, misnamed. The genuine Pillar 3
report for that year was never ingested, because nothing about the file
itself looked wrong. It had the right filename. It just wasn't the right
document.

None of these are things a pattern-matcher finds by getting better at
patterns. They're things a reader finds by noticing that something doesn't
add up and going to look. That's the actual shift: extraction used to be the
whole job. Now it's the easy part. The hard part — and the part Claude Code
is doing now that nothing did before — is treating every extracted figure as
a claim that needs checking against something else before it's trusted.

## Walkthrough: Ingesting Bank #61

So, concretely — what happens when a new bank joins the corpus?

**1. It gets a roster entry.** `bank_roster.csv` records the bank's name,
jurisdiction, reporting currency, and fiscal year-end. This is the single
source of truth for "which banks are actually in scope" — everything else
checks against it, which matters more than it sounds like it should (more on
that below).

**2. Source documents get acquired.** Usually three document types per
fiscal year: the annual report, a Pillar 3 (regulatory capital) disclosure
where the jurisdiction requires one, and — for US filers — the 10-K directly
from SEC EDGAR. Multiple documents per bank per year exist specifically so
they can be cross-checked against each other later, not just for redundancy.

**3. A Claude Code session works the bank, not a script.** Following a
written protocol (`CLAUDE_CODE_METRICS_PROMPT.md`), the session opens each
source document and works through the fixed 43-metric dictionary, reading
the actual tables rather than pattern-matching text. Every extracted value
gets a page citation and, where meaningful, a direct quote — genuinely
`not_found` where a metric isn't disclosed, never a guess dressed up as a
number.

**4. Everything writes at `verified=1` through the shared path.**
`safe_upsert.py`, no exceptions, no direct `INSERT`. If the bank already has
sparse or partially-wrong data from an earlier pass, the new extraction
supersedes it — the old rows don't vanish, they become history.

**5. The bank gets a status.** `bank_progress` tracks each bank as
`in_progress`, `done`, or — this matters — `needs_review`, for anything that
can't be resolved without a human decision. One bank in this corpus sat at
`needs_review` for weeks: every one of its ten supposed 10-K filings turned
out, on inspection, to belong to an entirely different company in an
unrelated industry. Not a metrics bug. A sourcing bug, at the most basic
level possible — the wrong company's filings, cover to cover. The eventual
decision was to drop the bank from scope rather than re-source it, which
meant something this project's own conventions don't normally allow: an
actual `DELETE`, not a supersede, because there was no genuine data
underneath to preserve. Ten filings, 360 metric rows, gone, with a backup
taken first and a written record of exactly why.

**6. Quality checks run automatically, and again by hand where they flag
something.** More on this below — but the short version is that a corpus-
wide script check happens after every ingestion, and anything it flags gets
a second, deliberate read-and-decide pass, never an automatic overwrite.

**7. The coverage report updates.** A per-metric snapshot of what fraction
of (bank × year) cells actually have real data, broken out by metric —
because "60 banks ingested" says nothing about whether any given metric is
actually well covered. Some metrics never will be, for structural reasons
(a Stage 3 credit-impaired-loan ratio genuinely cannot exist on a US bank's
balance sheet — that's the subject of the second post in this series), and
the coverage report is deliberately built to distinguish "not disclosed"
from "not found yet," which turns out to be one of the harder distinctions
to get an automated system to make correctly.

## The Quality Layer

There isn't one QA script. There's a small suite, each one built because a
specific *shape* of mistake got found and someone decided it deserved a
permanent check rather than a one-time fix:

- **Ordering checks** — CET1 ≤ Tier 1 ≤ Total Capital must hold for every
  bank-year. It's not a business rule so much as arithmetic; if it's
  violated, something upstream is definitely wrong, even if it's not obvious
  what yet.
- **Range checks** — every metric has a plausible band. Ratios outside
  [0, 100] where the definition demands a percentage, capital ratios outside
  historically observed extremes, and so on. Not every flag is a bug — some
  are genuine outliers a real bank actually reported — but every flag gets
  looked at rather than dismissed.
- **Cross-tier conflict detection** — catches automated writes trying to
  clobber a value a human already verified.
- **Cross-document reconciliation** — the same metric, sourced independently
  from the annual report and the Pillar 3 filing, should agree. When it
  doesn't, that's either a genuine restatement between the two documents or
  an extraction error, and the check exists specifically to surface the
  disagreement rather than silently trust whichever document got read first.
- **A dictionary sync check** — the human-readable documentation and the
  machine-readable metric definitions live in two different files by
  necessity (one's prose, one's structured data), and nothing stops them
  drifting apart except a script that diffs them.

The newest addition to that list exists because of a mistake the *quality
layer itself* made. A retraction — a value correctly removed for being
wrong — is supposed to get re-investigated and either replaced with a real
figure or confirmed as a genuine gap. It turned out a value could be
retracted and then just... sit there, `not_found`, indistinguishable from a
metric that was checked and genuinely isn't disclosed. The consistency
checker reported "zero violations" for banks that, on closer inspection,
still had real, findable data sitting unclaimed. That's not a data bug. It's
a blind spot in the thing meant to catch data bugs — arguably worse, because
it looks exactly like success. The fix was a new script, purpose-built to
walk every retraction back to its source and ask whether it was actually
followed up on. It found roughly two hundred rows in that state on its first
run. Most have since been resolved; the tool itself is now a permanent part
of the suite, because the failure mode it catches wasn't a one-off.

## What's Actually Different in Practice

Before: a bug got fixed once, in the row where it was noticed, and quietly
recurred everywhere else the same pattern existed — sometimes for months,
sometimes never noticed at all.

Now: a bug found in one bank triggers a question — "does this pattern exist
anywhere else?" — and that question gets an actual answer, corpus-wide, not
a guess. Confirmed patterns get a permanent record. Some get their own
purpose-built script. The corpus isn't just bigger than it was in May. It's
built to notice its own mistakes in a way the regex version structurally
couldn't, because a pattern-matcher has no concept of "this looks right but
let me check it against something else" — and that's the entire job now.

It's still not finished. A handful of banks file through a document
platform whose HTML silently drops content in a way nothing currently
catches — no error, just less text than there should be, which is the worst
kind of failure because it doesn't announce itself. That's the next thing on
the list.

---

## Key Takeaways

- Extraction that looks successful and extraction that's actually correct
  are different claims. A regex match is confirmation the pattern fired, not
  confirmation the number is right.
- The failures that cost the most are the ones that don't look like
  failures — a plausible wrong number sits in a spreadsheet indefinitely
  until something forces a cross-check.
- Insert-and-supersede isn't bureaucracy. Keeping the wrong value on record,
  not just the correction, is what makes a whole later class of bug
  detectable at all.
- A durable, queryable record of confirmed findings is worth more than the
  individual fixes — it's the difference between fixing a bug once and
  fixing it, quietly, thirty separate times without noticing it's the same
  bug.
- A QA layer can have its own blind spots, and finding one is a genuine
  result, not an embarrassment — it's the system getting more honest about
  what it doesn't know, which is the whole point of having the layer.
- The hardest part of building this was never getting a model to extract
  numbers. It was building a structure where being wrong is cheap to notice
  and expensive to leave uncorrected.

---

## References

- [Not a Specification](/blog/comp-science/not-a-specification/) — the problem statement this whole series works from
- [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/) — the fine-tuning journey and why structured prompting won
- [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/) — the accounting-regime bug that started the shift toward durable, queryable memory
- [Qwen2.5 Model Family](https://huggingface.co/Qwen)
- [Claude Code](https://claude.com/claude-code)

---

**Update, 2026-07-19:** [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
takes everything described above and asks the question directly: why was it
built this way, specifically to stop the eventual prose-writing LLM from ever
becoming the source of a fact.

---

**Previous in the series:** [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/)
**Next in the series:** [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. **Adding the 61st Bank** (this post)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
