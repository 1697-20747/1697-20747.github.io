---
title: "LLM Credit Paper Generator"
date: 2026-05-25T18:02:38Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, LLM, AI, banks, prompt-engineering]
description: "Building a domain-grounded AI bank credit analyst — what worked, what didn't, and why fine-tuning was not the answer."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

*Second post in a series — start with [Not a Specification](/blog/comp-science/not-a-specification/)
for the problem statement this project actually set out to solve.*

This is a project to generate bank credit papers using AI. Easier said than done.
Project teams trying this with off-the-shelf LLMs tend to get stuck in a rut, and
not without reason — generic LLMs do not know what a CAMELS analysis is, do not
know what regulatory thresholds matter, do not cite source pages, and freely
invent peer figures that sound plausible.

The honest version of this story has two acts. The first act was building a
data pipeline and fine-tuning a Qwen2.5-7B model on 6,623 curated training pairs.
The second act was throwing the fine-tuned model away after it failed to
outperform the base model with structured prompting, and shipping the structured
prompting approach instead. The data pipeline survived. The fine-tuning did not.

Both acts have lessons worth writing up.

The assumptions baked in from day one:

1. A financial statement is available to download, presumably in PDF form.
2. A statutory Pillar 3 report exists. PDF or Excel — both bad formats for data.
3. The output is a credit paper. Not what I would design for, but apparently
   what is wanted.
4. Asset class: Financial Institutions.
5. Open data only, open source tooling, runs offline on a Mac.

Key constraints:

- I am decent on machine learning and agents but had never applied any of this
  to LLMs before.
- Open data is essential. More is better.
- Hallucinations to be minimised — every token an LLM generates is a
  hallucination in the strict sense, but this is engineered to minimise them in
  the practical sense.
- Compute constrained. Colab Pro and a Mac mini with 16GB. Not nearly enough.
- I hate post-production, so no fancy formatting. Text-based Markdown as an act
  of rebellion.
- The working version goes on GitHub. If you know what you are doing, the README
  is sufficient.
- Every number in a credit paper compared to population. CET1 is 12.6% — 3rd
  decile amongst the overall population. Comparative analysis baked in from day
  one.
- BYO credit papers. Drop your own analyst papers in `credit_reports/` and they
  become training data.
- Everything open sourced, nothing stolen, ratings principles adhered to.
- CAMELS as the overarching analytical framework.

The language around credit analysis is specific and nuanced. But once you know
it, it is not that hard. A focused model is better suited here than a generic
chatbot. This screams smaller domain-specific model — which is exactly what I
spent two weeks trying to build, before realising that careful prompting of the
base Qwen2.5-7B model with three grounding mechanisms produced better results.

---

## What Actually Ships

After four rounds of fine-tuning experiments (more on those below), the working
production system is:

- **Base Qwen2.5-7B** via Ollama, running locally, no fine-tuning applied
- A system prompt establishing the analyst role and citation rules
- Three grounding mechanisms injected into every prompt:
  1. **Extracted metrics with page numbers** from the source PDF
  2. **Decile context** from a benchmark index built from 800+ bank-years
  3. **Peer values** from a roster of real bank data (UK/EU/US/AU/CA)
- Strict prompt rules preventing peer-figure fabrication and rating-agency-quote
  invention

The output is a CAMELS credit paper with every metric cited to a source page,
every peer comparison using real values from the roster, and a benchmark table
showing the bank's decile position globally. Section-by-section structure with
Assessment / Key Metrics / Analysis / Peer Context / Key Risks / Rating Agency
Commentary.

The data pipeline that was originally built for fine-tuning is still the
project's primary value. The 6,623 training pairs, the benchmark index, the
peer roster, the source extractor — all of it gets used at inference time, just
via prompt injection instead of weight updates.

---

## The Data Problem

The first thing you realise when building a domain-specific bank analyst is
that the data is awful.

The pipeline pulls from six source streams:

**Stream 1 — Annual Reports.** SEC EDGAR has every 10-K for every listed US
bank going back decades, in machine-readable HTML. UK, EU, Australian and
Canadian banks are messier — IR pages with inconsistent formats, date-stamped
filenames that change every year, some banks blocking automated downloads
entirely (HTTP 403). 130+ annual reports in the dataset.

**Stream 2 — Pillar 3 Reports.** The richest source of regulatory capital
data. Published alongside annual reports but inconsistently — some PDF only,
some Excel only, some both, no standard schema. A CET1 ratio reported as
`13.50` in one bank's workbook appears as `0.1350` in another and `1350` (basis
points) in a third. PDF extraction is imprecise by nature.

**Stream 3 — EBA Transparency Exercise.** The European Banking Authority
publishes standardised financial data for 156+ EU banks every year. Gold for
benchmarking — every bank on exactly the same basis. 1,463 records from one
CSV file. This is what good bank data looks like.

**Stream 4 — FDIC Call Reports.** Every US bank files quarterly with the
FDIC. Public REST API. Top 100 banks by assets. 935 records.

**Stream 5 — Rating Agency Methodology.** Fitch, S&P, DBRS Morningstar
methodologies. Basel Committee full suite (9 documents), OCC Comptroller's
Handbook (7 volumes), FDIC examination manuals, EBA SREP guidelines, PRA
supervisory statements, OSFI and APRA prudential standards.

**Stream 6 — Real Analyst Credit Papers.** The gold standard. Real S&P,
Moody's and Fitch credit reports dropped into `credit_reports/` and extracted
automatically.

This data feeds two distinct workflows. The first was training data
preparation — turning extracted material into JSONL pairs for QLoRA training.
The second was inference-time data — building a benchmark index and peer
roster for prompt injection. The second turned out to matter more.

---

## The Fine-Tuning Story (Acts 1–4)

For anyone who has not done this before, here's roughly what fine-tuning means
in this context. The base Qwen2.5-7B is a 7-billion parameter language model
trained by Alibaba on a large general corpus. It knows how to follow
instructions, write structured text, and reason. It knows the word CET1. It
does not know what a good CAMELS analysis looks like, the correct regulatory
thresholds for UK banks specifically, how to cite page numbers from a source
document, or when to refuse to fabricate data.

Fine-tuning is the process of nudging those 7 billion parameters to do those
things. QLoRA does it cheaply by freezing the base model and training small
"adapter" matrices — about 0.02% of total parameters. The trained adapter is a
7MB file that combines with the 4GB base model at inference time.

**Round 1 (Mac MLX, 1,737 pairs, 512 tokens):** worked. Validation loss
3.14 → 1.30. Limited by sequence length — most training pairs got truncated.

**Round 2 (Mac MLX, 3,832 pairs, 512 tokens):** worked. Loss 2.53 → 1.07.
Better data, same constraint.

**Round 3 (Mac MLX, 3,832 pairs, 512 tokens):** worked. Loss → 0.876. Deployed
briefly. Output was structurally correct but with fabricated peer comparisons
and invented rating agency quotes.

**Round 4 (Colab Pro A100, 6,623 pairs, 4,096 tokens):** trained successfully
to loss 0.75 — the best loss of all four runs. **Then everything went wrong.**

The Unsloth save in Cell 7 produced a hybrid file: 154MB of safetensors that
were neither a clean LoRA delta (~7MB) nor a full merged model (~15GB). GGUF
conversion in Colab filled the 112GB disk and crashed. Conversion on Mac
required using a base model the adapter wasn't trained against (the unsloth
4-bit variant needs bitsandbytes, which is Linux/CUDA only). The merge ran but
produced a model that had lost the base Qwen's instruction-following without
gaining the trained behaviour.

The deployed Round 4 model was worse than the base model with a system prompt.
On the same task — analyse Lloyds 2025 Capital Adequacy — the trained model
produced repetition loops, echoed back the prompt template, and inserted
fabricated `[Source: Official Regulatory Reports]` placeholders. The base
Qwen, given the same task with the same source extract, produced clean
analyst prose with specific page citations and structured sections.

[The full retrospective is in FINE_TUNING_RETROSPECTIVE.md in the repo.](https://github.com/1697-20747/llm_credit_paper/blob/main/FINE_TUNING_RETROSPECTIVE.md)

---

## What Worked Instead: Structured Prompting + Three Grounding Mechanisms

When you stop trying to make the model do everything from learned behaviour and
start handing it the relevant facts at inference time, the output gets a lot
better.

**Mechanism 1 — Extracted metrics with page tagging.**

A script (`test_analysis.py`) opens the PDF, runs regex over every page to find
CET1 ratio, leverage, RoTE, LCR, NSFR, total capital ratio, etc., and tags each
match with its source page number. The model never has to guess where a figure
comes from — the page is in the prompt:

```
EXTRACTED METRICS (subject bank, with global decile context):
  CET1 RATIO: 14.0% [Source: 2025-lbg-annual-report.pdf, p.53]  ← 7th decile globally...
  LEVERAGE RATIO: 5.4% [Source: 2025-lbg-annual-report.pdf, p.53]  ← 7th decile...
  ROTE: 22.1% [Source: 2025-lbg-annual-report.pdf, p.105]  ← 10th decile globally...
```

The strict prompt rule: never use `[Source: p.XX]` as a placeholder, always cite
a specific page.

**Mechanism 2 — Decile context from benchmark index.**

A separate script (`build_benchmark_index.py`) walks all processed financial
data and computes percentile thresholds for each metric, both global and per
region. At inference time the metric lookup appends the decile to the prompt
before the model sees it. The model isn't being asked "is this CET1 ratio
good?" — it's being told "this is in the 7th decile" and asked to describe
what that means.

**Mechanism 3 — Peer values from real bank data.**

A peer roster (`build_peer_roster.py`) extracts each bank's latest metrics
from processed annual reports, applies sanity filters (no ROA = 2025.0 from
year-leakage, no Tier 1 = 2.33% from regex misfire), and saves a JSON file
mapping bank → region → currency → latest metrics.

At inference time the script finds same-region peers, picks those with the
most relevant data for the pillar being analysed, and injects them as a block:

```
PEER VALUES (from peer roster — cite as [Peer roster: <Bank> <Year>]):
  • Barclays [Peer roster: Barclays 2025] (GBP): CET1 14.3%, Tier 1 14.3%
  • HSBC Holdings [Peer roster: HSBC Holdings 2025] (USD): CET1 14.9%
  • NatWest Group [Peer roster: NatWest Group 2024] (GBP): CET1 13.6%
```

The system prompt rule: use ONLY this peer data, never invent peer values, if a
peer's value isn't in the block say "not available for this peer".

This eliminates the fabrication mode where the base model would otherwise invent
plausible-sounding numbers like "Barclays' statutory profit of £4,200m" that
look real but aren't.

---

## Strict Anti-Fabrication Rules

Beyond the three grounding mechanisms, the system prompt has explicit rules for
behaviour when data isn't available:

1. Every subject-bank figure must cite `[Source: p.XX]` with a specific page
2. Every peer figure must cite `[Peer roster: <Bank> <Year>]` — never attribute
   peer values to page numbers of the subject bank's report
3. If data is unavailable, write "Data not available" — never fabricate
4. Never invent additional peer values beyond what's provided
5. If no peer data block is provided, omit the Peer Context section entirely
6. For rating agency commentary, only state what is in source documents. If
   none, write "No rating agency commentary available in source documents".
7. Never invent "hypothetical peer data", "industry averages", or "sector
   medians"

The model follows these rules with high reliability at temperature 0.05 and
repeat_penalty 1.15.

---

## What the Output Looks Like

For Lloyds Banking Group 2025 (the test bank used throughout development), the
Capital Adequacy section comes out like this:

```
### Assessment: Strong

#### Key Metrics:
- CET1 Ratio: 14.0% [Source: 2025-lbg-annual-report.pdf, p.53] — 7th decile globally
- Total Capital Ratio: 18.9% [Source: 2025-lbg-annual-report.pdf, p.146] — 5th decile
- Leverage Ratio: 5.4% [Source: 2025-lbg-annual-report.pdf, p.53] — 7th decile

#### Analysis:
Lloyds Banking Group demonstrates a strong capital adequacy position with
robust CET1 and total capital ratios that are well above average compared to
global peers...

#### Peer Context:
- Barclays [Peer roster: Barclays 2025]: CET1 14.3%, Tier 1 14.3%
- HSBC Holdings [Peer roster: HSBC Holdings 2025]: CET1 14.9%
- NatWest Group [Peer roster: NatWest Group 2024]: CET1 13.6%
- ABN AMRO [Peer roster: ABN AMRO 2023]: CET1 14.3%, Tier 1 14.3%, TotalCap 18.7%

Lloyds Banking Group's CET1 ratio is slightly lower than Barclays and HSBC,
but higher than NatWest and Scotiabank.

#### Key Risks:
- Market Risk: While the leverage ratio indicates efficient use of assets...
- Credit Risk: Strong credit performance and low impairment charge suggest...

#### Rating Agency Commentary:
No rating agency commentary available in source documents.
```

Every figure cited. Every peer real. No fabrication. The "Rating Agency
Commentary" line is the model correctly refusing to invent quotes because no
S&P/Moody's/Fitch text was in the source.

---

## The Benchmark Index

The benchmark index is built from all processed financial data — annual
reports, EBA transparency CSV, FDIC Call Reports. For each metric: mean,
median, p10, p25, p75, p90, full decile breakpoints. Global distributions plus
regional breakdowns for UK, EU, US, AU, CA where the sample shares a currency.

GBP figures aren't comparable to USD figures, so regional distributions are
kept separate. The regional dashboard automatically uses the correct
currency-matched peer group.

The decile context appears at the top of every generated credit paper:

| Metric | Value | Global Decile | Median | p10–p90 |
|--------|-------|---------------|--------|---------|
| CET1 Ratio | 14.0% [p.53] | **7th** | 13.6% | 12.34–14.85% |
| Leverage Ratio | 5.4% [p.53] | **7th** | 5.0% | 4.4–5.8% |
| RoTE | 22.1% [p.105] | **10th** | 10.4% | 8.2–13.3% |
| LCR | 145.0% [p.183] | **7th** | 141.0% | 130.3–167.3% |

The benchmark improves as more data is added. With FDIC, EBA, and processed
annual reports included it covers 800+ bank-years across five currency
regions.

---

## The Compute Story

16GB of unified memory on an M2 Pro. This is the constraint everything else
bends around.

For inference: Qwen2.5-7B in 4-bit quantisation loads in 4GB via Ollama and
runs fine. The full pipeline (extract PDF → build prompts → call model 8 times
for the 8 sections → assemble report → render dashboards) takes about 5
minutes for a typical bank.

For training: this is where Colab Pro was needed. The Mac can train at 512
token context with a small dataset. The full 4,096-token training that
produced the highest loss number required A100. And the higher loss number
didn't translate to better output, which was the surprising lesson.

If you want to retry fine-tuning, do it on Vast.ai or RunPod, not Colab.
Detailed reasoning in the retrospective document.

---

## What's Left

The system works end to end. Annual report PDF in → credit paper out, benchmark
table included, every figure cited to a source page, every peer comparison
using real values from the roster.

What remains:

- **More peers in the roster.** Currently 15 banks with sanity-filtered metrics.
  Adding more major banks (HSBC subsidiaries, UK challengers, EU savings banks)
  would improve peer context for those analyses.

- **Better Pillar 3 integration.** Currently extracts top-level RWA and
  liquidity ratios. The full Pillar 3 contains rich IRB / SA / market /
  operational breakdowns that the current pipeline doesn't capture.

- **Real rating agency commentary injection.** When a bank has an S&P or Fitch
  report in `credit_reports/`, the relevant section text should be injected
  into the Rating Agency Commentary prompt instead of relying on the model to
  fall back to "No rating agency commentary available".

- **Round 5 fine-tuning attempt** (optional). With the lessons from Round 4 —
  proper Cell 7 save method, training on Vast.ai not Colab, explicit refusal
  pairs in the data, validation against base model before declaring success.

Code is at [github.com/1697-20747/llm_credit_paper](https://github.com/1697-20747/llm_credit_paper). Apache 2.0.

Technical documentation: [/docs/camels-llm/](/docs/camels-llm/)

---

## Key Takeaways

- **Structured prompting with explicit data injection beats naive fine-tuning**
  for domain tasks with clear formats and external data sources. The model
  becomes an assembler; the data infrastructure becomes the substance.

- **Training loss is not output quality.** Round 4 had the best loss and was
  the worst deployed model. Always evaluate against a held-out task end-to-end,
  not against a metric.

- **The data pipeline is the real value.** A benchmark index, peer roster, and
  metric extractor with page tagging are useful infrastructure regardless of
  what model consumes them. The 6,623 training pairs that were built for
  fine-tuning are still used — just via prompt injection instead of weight
  updates.

- **Colab is unsuitable for serious training work.** Idle timeouts, disk
  limits, credential failures, opaque save formats. For any training run >30
  minutes use Vast.ai or RunPod instead.

- **Mac is fine for everything except the training step itself.** Extraction,
  GGUF conversion, merging, quantisation, inference, evaluation, dashboard
  rendering — all run cleanly on Apple Silicon.

- **Anti-hallucination is architectural, not stylistic.** Telling the model
  "don't fabricate" doesn't work. Pre-extracting the facts, structuring the
  prompt around them, and having explicit rules about behaviour when data is
  absent — does work.

- **Cite everything. Refuse when you can't.** This is the most important rule
  for any LLM application that touches real-world data. Mine cites every
  subject-bank figure to a specific page and every peer figure to a roster
  entry. Where data is absent, it says so.

---

## References

- [FDIC BankFind API](https://banks.data.fdic.gov/api/)
- [EBA EU-wide Transparency Exercise](https://www.eba.europa.eu/eu-wide-transparency-exercise-0)
- [BIS Basel Committee Publications](https://www.bis.org/bcbs/publications.htm)
- [OCC Comptroller's Handbook](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/index-comptrollers-handbook.html)
- [Qwen2.5 Model Family](https://huggingface.co/Qwen)
- [Ollama](https://ollama.com)
- [Unsloth — Fast LLM Fine-tuning](https://github.com/unslothai/unsloth)
- [Technical Documentation](/docs/camels-llm/)
- [Fine-Tuning Retrospective](https://github.com/1697-20747/llm_credit_paper/blob/main/FINE_TUNING_RETROSPECTIVE.md)
- [Project Repository](https://github.com/1697-20747/llm_credit_paper)

---

**Update, 2026-07-19:** two follow-ups since this post. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/) covers a specific architectural bug that pushed the project toward durable, queryable memory instead of one-off fixes. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/) covers what the whole pipeline looks like now — Claude Code doing the actual ingestion work, not just consuming pre-extracted metrics.

---

**Previous in the series:** [Not a Specification](/blog/comp-science/not-a-specification/)
**Next in the series:** [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. **LLM Credit Paper Generator** (this post)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
