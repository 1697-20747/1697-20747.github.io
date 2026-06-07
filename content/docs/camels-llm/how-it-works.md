---
title: "How It Works"
weight: 2
description: "The structured prompting architecture, three grounding mechanisms, and why this approach replaced four rounds of fine-tuning."
summary: "Architecture of the CAMELS analyser — structured prompting against base Qwen with three grounding mechanisms."
---

## The Core Idea

The model is the assembler. The data infrastructure is the substance.

Base Qwen2.5-7B running locally via Ollama is given a system prompt establishing
the analyst role and citation rules. For each CAMELS section a separate prompt
is built containing:

1. **Extracted metrics with page numbers** from the source PDF
2. **Decile context** from a benchmark population of 800+ bank-years
3. **Peer values** from a roster of real bank data, same-region first
4. **The relevant source extract** from the annual report and Pillar 3 PDF
5. **Strict rules** about citation, fabrication, and refusal

The model produces structured CAMELS prose: Assessment, Key Metrics, Analysis,
Peer Context, Key Risks, Rating Agency Commentary.

This is structured prompting, not fine-tuning. Four rounds of QLoRA training
were attempted before this approach won out — see the
[Fine-Tuning Retrospective](../fine-tuning-retrospective/) for the full story.

---

## Three Grounding Mechanisms

### 1. Metric Extraction with Page Tagging

A regex-based extractor (`test_analysis.py`) opens the source PDF via PyMuPDF
and runs metric patterns over every page:

```python
KEY_METRIC_PATTERNS = [
    ("cet1_ratio",     r"CET\s*1\s+(?:ratio|capital ratio)\s*[:\s]+(\d+\.?\d*)\s*%"),
    ("leverage_ratio", r"[Ll]everage\s+ratio\s*[:\s]+(\d+\.?\d*)\s*%"),
    ("rote",           r"[Rr]eturn\s+on\s+[Tt]angible\s+[Ee]quity\s*[:\s]+(\d+\.?\d*)\s*%"),
    ("lcr",            r"[Ll]iquidity\s+[Cc]overage\s+[Rr]atio\s*[:\s]+(\d+\.?\d*)\s*%"),
    # ... etc
]
```

Each match records the value and the page number it came from:

```json
{
  "cet1_ratio":     {"value": 14.0, "source_page": 53,  "source_file": "2025-lbg-annual-report.pdf"},
  "leverage_ratio": {"value": 5.4,  "source_page": 53,  "source_file": "2025-lbg-annual-report.pdf"},
  "rote":           {"value": 22.1, "source_page": 105, "source_file": "2025-lbg-annual-report.pdf"},
  "lcr":            {"value": 145.0,"source_page": 183, "source_file": "2025-lbg-annual-report.pdf"}
}
```

These metrics are injected into every section prompt with their page numbers
inline. The model never has to guess where a figure came from — the page is in
the prompt:

```
EXTRACTED METRICS (subject bank, with global decile context):
  CET1 RATIO: 14.0% [Source: 2025-lbg-annual-report.pdf, p.53]
  LEVERAGE RATIO: 5.4% [Source: 2025-lbg-annual-report.pdf, p.53]
  RETURN ON TANGIBLE EQUITY: 22.1% [Source: 2025-lbg-annual-report.pdf, p.105]
```

The strict prompt rule: never use `[Source: p.XX]` as a placeholder, always cite
a specific page. The model follows this with high reliability.

### 2. Decile Context

A separate script (`build_benchmark_index.py`) walks all processed financial
data and computes population statistics for each metric:

```json
{
  "cet1_ratio": {
    "unit": "%",
    "all": {
      "count":   147,
      "median":  13.6,
      "p10":     11.2,
      "p25":     12.34,
      "p75":     14.50,
      "p90":     14.85,
      "deciles": [11.2, 12.0, 12.5, 13.0, 13.3, 13.6, 14.0, 14.3, 14.6, 14.85]
    },
    "recent": {
      "count":   36,
      "median":  13.6,
      "p10":     12.34,
      "p25":     13.2,
      "p75":     14.5,
      "p90":     14.85,
      "deciles": [12.34, 12.8, 13.2, 13.4, 13.55, 13.6, 14.0, 14.3, 14.5, 14.85]
    }
  }
}
```

At inference time, for each extracted metric, the decile lookup appends the
ranking to the prompt before the model sees it:

```
CET1 RATIO: 14.0% [Source: p.53]  ← 7th decile globally (median: 13.6%, p10: 12.34%, p90: 14.85%; n=36)
```

The model isn't being asked to judge whether 14.0% is good — it's being told
where 14.0% sits in the population and asked to describe what that means.

Regional breakdowns (UK, EU, US, AU, CA) keep currency-incompatible metrics
separate. RWA in GBP isn't compared against RWA in USD.

### 3. Peer Values from Real Bank Data

A peer roster (`build_peer_roster.py`) walks all processed annual report JSONs,
extracts each bank's latest metrics, applies sanity filters (no ROA = 2025.0
from year-leakage, no Tier 1 = 2.33% from regex misfire on a different "2.33%"
on the page), and saves:

```json
{
  "Lloyds Banking Group": {
    "region": "UK", "currency": "GBP", "year": 2025,
    "metrics": {"cet1_ratio": 14.0, "leverage_ratio": 5.4, "rote": 22.1, ...}
  },
  "Barclays": {
    "region": "UK", "currency": "GBP", "year": 2025,
    "metrics": {"cet1_ratio": 14.3, "tier1_ratio": 14.3, "lcr": 170.0, ...}
  },
  "HSBC Holdings": {
    "region": "UK", "currency": "USD", "year": 2025,
    "metrics": {"cet1_ratio": 14.9, "tier1_ratio": 14.9}
  }
}
```

For each CAMELS pillar, `test_analysis.py` finds same-region peers with the
relevant metrics and injects them as a block:

```
PEER VALUES (from peer roster — cite as [Peer roster: <Bank> <Year>]):
  • Barclays [Peer roster: Barclays 2025] (GBP): CET1 14.3%, Tier 1 14.3%
  • HSBC Holdings [Peer roster: HSBC Holdings 2025] (USD): CET1 14.9%
  • NatWest Group [Peer roster: NatWest Group 2024] (GBP): CET1 13.6%
  • ABN AMRO [Peer roster: ABN AMRO 2023] (EUR): CET1 14.3%, Tier 1 14.3%, TotalCap 18.7%
```

Same-region peers always rank above cross-region peers, regardless of how
many metrics they have. UK peers come first for a UK subject bank.

The system prompt rule: use ONLY this peer data, never invent peer values, if
a peer's value for a metric isn't in the block say "not available for this
peer". This eliminates the failure mode where the base model would otherwise
invent plausible-sounding figures like "Barclays statutory profit £4,200m".

---

## Anti-Hallucination Rules

The system prompt is explicit about what is and isn't allowed:

```
STRICT RULES:
1. Every figure from the SUBJECT bank's annual report must cite [Source: p.XX]
   with a SPECIFIC page number from the source extract. Never use [Source: p.XX]
   as a placeholder.
2. For PEER bank figures (from the PEER VALUES block in the prompt), cite as
   [Peer roster: <Bank> <Year>] — never attribute peer values to page numbers
   of the subject bank's report.
3. If data is unavailable, write 'Data not available'. Never fabricate figures.
4. For peer comparisons, use ONLY peer data provided in the prompt. Never invent
   additional peer values or speculate on peer figures not provided.
5. If no peer data block is provided, OMIT the Peer Context section entirely.
6. For rating agency commentary, only state what is actually present in the
   source documents. If no rating agency commentary is in the source, write
   'No rating agency commentary available in source documents'. Never invent
   Moody's, S&P, or Fitch quotes or ratings.
7. Do not invent 'hypothetical peer data', 'industry averages', or
   'sector medians'.
```

Combined with temperature 0.05 and repeat_penalty 1.15, the base Qwen follows
these rules reliably. Where the model doesn't have data, it correctly refuses:

```markdown
#### Rating Agency Commentary:
No rating agency commentary available in source documents.
```

---

## What the Model Has to Learn vs What the Pipeline Provides

This split is the key insight from the project:

**What base Qwen2.5-7B already knows (no training needed):**
- How to follow instructions and produce structured output
- How to write in third-person analyst prose
- Domain vocabulary (CET1, MREL, LCR, NSFR, IRB, Stage 3, IRRBB, MDA threshold)
- Basel III/IV framework, regulatory thresholds
- General financial analysis concepts (capital adequacy, asset quality, etc.)

**What the prompt pipeline injects (so the model doesn't have to guess):**
- Specific metrics with exact page citations from this bank's report
- Decile context from the actual population of bank data
- Real peer values for same-region comparison
- Source extract for the relevant CAMELS section
- Strict rules about citation format and refusal behaviour

**What gets refused (where neither model nor pipeline has data):**
- Rating agency quotes (when no S&P/Moody's/Fitch text is in source)
- Peer figures not in the roster
- Specific numbers absent from the source extract

This split lets a 7B model with 4GB on disk produce analyst-quality output
that beats much larger generic models on this specific task — because the
larger generic models would invent the missing data, and a small focused
model with grounding doesn't have to.

---

## What the Model Produces

For Lloyds Banking Group 2025, Capital Adequacy section:

```markdown
### Assessment: Strong

#### Key Metrics:
- CET1 Ratio: 14.0% [Source: 2025-lbg-annual-report.pdf, p.53] — 7th decile globally
- Total Capital Ratio: 18.9% [Source: 2025-lbg-annual-report.pdf, p.146] — 5th decile
- Leverage Ratio: 5.4% [Source: 2025-lbg-annual-report.pdf, p.53] — 7th decile

#### Analysis:
Lloyds Banking Group demonstrates a strong capital adequacy position with
robust CET1 and total capital ratios that are well above average compared to
global peers. The leverage ratio is also favourable, indicating efficient use
of assets relative to equity.

#### Peer Context:
- Barclays [Peer roster: Barclays 2025] (GBP): CET1 14.3%, Tier 1 14.3%
- HSBC Holdings [Peer roster: HSBC Holdings 2025] (USD): CET1 14.9%
- NatWest Group [Peer roster: NatWest Group 2024] (GBP): CET1 13.6%
- ABN AMRO [Peer roster: ABN AMRO 2023] (EUR): CET1 14.3%, Tier 1 14.3%, TotalCap 18.7%

#### Key Risks:
- Market Risk: While the leverage ratio indicates efficient use of assets,
  market risk could still pose a challenge if rate or currency fluctuations
  impact performance.
- Credit Risk: Strong credit performance and low impairment charge suggest
  good risk management practices.

#### Rating Agency Commentary:
No rating agency commentary available in source documents.
```

Every subject-bank figure cited to a specific page. Every peer figure cited to
the roster. No fabrication. Where data is absent, the section correctly
refuses.

---

## Pipeline Run

A single `test_analysis.py` invocation:

1. Opens the annual report PDF and Pillar 3 PDF via PyMuPDF
2. Extracts metrics with page tagging
3. Classifies each page into CAMELS sections by keyword matching
4. Loads benchmark index and peer roster
5. Identifies subject bank in roster, determines region
6. Builds run folder: `output/<Bank>/<Year>/<YYYYMMDD_HHMMSS>/`
7. Generates Overview (institutional profile + AR highlights) via 2 Ollama calls
8. For each CAMELS pillar:
   a. Gets relevant pages from section index
   b. Gets same-region peers for the pillar
   c. Builds prompt with metrics + decile + peers + source extract + rules
   d. Calls Ollama for analysis
9. Assembles full markdown report
10. Writes audit.json with all source provenance
11. Calls `generate_dashboard.py` to build HTML dashboards
12. Updates `latest` symlink to point to this run

Total time: ~5 minutes on M2 Pro for a typical bank with 300-page annual report
plus 150-page Pillar 3.

---

## Why This Approach Won

After four rounds of QLoRA fine-tuning produced no usable model, the pivot to
structured prompting was forced rather than planned. But once implemented, the
output quality was visibly higher than any of the trained models.

The reasons, in order of importance:

1. **Base Qwen already has the structural and linguistic skills** — instruction
   following, third-person prose, domain vocabulary. The training wasn't
   teaching it anything it didn't already know.

2. **The grounding data is the actual signal** — page citations, decile
   context, peer values. None of these can be reliably stored in 1.4M LoRA
   parameters. They need to be in the prompt at inference time.

3. **Hallucination resistance comes from refusal, not training** — telling the
   model to refuse when data isn't available works. Training the model to
   refuse takes thousands of examples and may still fail.

4. **The data pipeline survives the pivot** — every script written for
   fine-tuning still runs. The benchmark index, peer roster, source extractor,
   and section classifier are all used at inference time.

For the detailed account of what went wrong with fine-tuning, see the
[Fine-Tuning Retrospective](../fine-tuning-retrospective/).

---

[Back to CAMELS LLM docs](..) | [Main blog post](/blog/comp-science/llm-credit-paper-generator/)
