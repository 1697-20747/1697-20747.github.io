---
title: "How Training Pairs Work"
weight: 2
description: "How raw financial data becomes LLM training examples, and how Qwen2.5-7B is fine-tuned on them."
summary: "How raw financial data becomes LLM training examples, and how Qwen2.5-7B is fine-tuned on them."
---

## The Core Idea

A training pair is an example of the behaviour you want the model to learn. Nothing more. The model reads thousands of examples and learns to reproduce the pattern. The quality and diversity of those examples determines the quality of the output.

For a credit analysis model the behaviour is: given extracted financial data with source page numbers, write a structured CAMELS analysis with regulatory context, peer comparison, and cited figures. The model needs to learn the domain language, the correct regulatory thresholds, when to say "data not available" rather than fabricating, and exactly how to cite page numbers.

None of this requires a fundamentally different kind of model. It requires examples.

---

## Anatomy of a Training Pair

Every pair has three parts in the standard instruction-following format. Here is a simplified real example:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a senior credit analyst specialising in bank credit analysis using the CAMELS framework. Every numerical claim must cite a source as [Source: p.XX]. If data is unavailable write 'Data not available' — never fabricate figures. Structure responses with: Assessment (Strong/Adequate/Weak/Critical), Key Metrics, Analysis, Peer Context, Key Risks, and source citations."
    },
    {
      "role": "user",
      "content": "Bank: Lloyds Banking Group\nYear: 2025\n\nTASK: Analyse the Capital Adequacy section.\n\nKEY METRICS:\n  CET1 RATIO: 14.0% [Source: p.53]\n    <- 7th decile globally (median: 13.8%, p10: 10.5%, p90: 14.2%; n=847)\n  LEVERAGE RATIO: 5.4% [Source: p.53]\n\nTEXT CONTENT:\n[Page 53]\nThe Group's CET1 ratio was 14.0% at 31 December 2025..."
    },
    {
      "role": "assistant",
      "content": "## Capital Adequacy (C)\n\n**Assessment: Strong**\n\n### Key Metrics\n- CET1 ratio: 14.0% [Source: p.53] — 7th decile globally, 950bp above the 4.5% Pillar 1 minimum\n- Leverage ratio: 5.4% [Source: p.53] — 175bp above the 3.25% UK minimum\n\n### Analysis\nLloyds maintains a strong capital position with a CET1 ratio of 14.0% [Source: p.53], comfortably above both regulatory minimums and internal targets...\n\n### Peer Context\nAt the 7th decile globally (median: 13.8%), Lloyds is positioned above the peer median. Among UK peers the ratio is broadly in line with Barclays (13.8%) and above NatWest (13.6%).\n\n### Key Risks\n- Basel IV output floor (72.5% by 2030) — management estimate of 30-40bp CET1 headwind\n- Ongoing share buyback programme creates downward pressure"
    }
  ]
}
```

The system message stays constant across all pairs — it defines the model's identity, citation rules, and output format. The user message contains the task, extracted metrics with benchmark decile context, and source text. The assistant message is the target response the model learns to produce.

---

## Six Training Pipelines

The dataset is built from six separate pipelines, each producing a different type of pair.

### Pipeline A — Financial Statements

The largest pipeline. For each annual report section (capital adequacy, asset quality, earnings etc.), the extractor pulls relevant pages and tables from the source PDF, runs metric extraction to find key ratios with page numbers, looks up each metric in the benchmark index to get decile context, and builds a user prompt containing all of this.

The assistant response starts as a template — structurally correct but with placeholder language. A one-time quality upgrade pass via the Claude Haiku API rewrites each template into proper analyst prose. Cost: under $10 for the full run. Fully resumable — saves progress after every API call.

**What Haiku does here:** reads the extracted financial data and writes an analyst-quality response. It is a data writer, not an inference model. Once the training data is written, Haiku plays no further role. All inference at deployment time is handled by Qwen.

### Pipeline B — Rating Agency Methodology

Chunks from Basel Committee standards, OCC Comptroller's Handbook, EBA SREP guidelines, Fitch/S&P/Moody's methodology documents, OSFI and APRA prudential standards. These teach the model the analytical framework and regulatory thresholds — what the Basel III minimum actually is, how the buffer stack works, what rating agencies look for in a liquidity assessment.

Each chunk is paired with a user question about the relevant CAMELS pillar and an assistant response that contextualises the excerpt analytically rather than just reproducing it.

### Pipeline C — Gold Credit Papers (2x weight)

Real analyst credit papers from S&P, Moody's and Fitch, extracted from PDF or DOCX files. These are the highest-quality training signal in the dataset. Each paper is split into CAMELS sections and paired with structured prompts. Included at 2x weight — every gold pair appears twice in the shuffled training file.

**Why 2x:** the gold papers set the quality standard. The model should see more examples of correct output than approximate output. Doubling the weight costs nothing computationally and measurably improves output style.

### Pipeline D — EBA Transparency Exercise

156 EU/EEA banks, 2019–2025, standardised CSV data published annually by the European Banking Authority. 1,463 pairs. The best single source in the dataset because every bank is on exactly the same basis — no extraction errors, no unit ambiguity, consistent schema. This is what good bank data looks like. The industry should take note.

### Pipeline E — FDIC Call Reports

Top 100 US banks by assets via the FDIC BankFind REST API. Annual periods. Tier 1 ratio, net charge-off rate, ROA, NIM, efficiency ratio, loan-to-deposit ratio. 935 pairs. Structured data, no PDF extraction, reliable figures.

### Pipeline F — Overview Pairs

One pair per annual report covering the institutional profile paragraph and Annual Review highlights paragraph. Each pair is built by Claude Haiku reading the first pages of the annual report and writing analyst-quality two-paragraph summaries. These teach the model a specific subtask — synthesising factual background into tight, cited, third-person prose — that the CAMELS section pairs do not cover.

---

## Quality Tiers

Not all pairs are equal. The training file contains four quality tiers:

| Tier | Source | Count |
|------|--------|-------|
| Gold (2x weight) | Real S&P/Moody's/Fitch reports | ~392 |
| Upgraded | Annual report sections, Haiku-written responses | ~1,200 |
| Structured | EBA + FDIC data, rule-based responses | ~2,400 |
| Analytical | Rating agency methodology, contextualised excerpts | ~1,400 |

The gold pairs set the standard. The upgraded pairs have the right structure and prose. The structured pairs have perfect data but simpler language. The analytical pairs teach framework knowledge. Together they cover the full range of what a credit analyst needs to know and how they need to write.

---

## The Interface to Qwen Training

After the training file is built and quality-fixed, training is a single command on Apple Silicon:

```bash
python -m mlx_lm lora \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --train \
  --data training_data/ \
  --config lora_config.yaml \
  --iters 600
```

Or on Google Colab Pro (A100) via the provided notebook — set `MAX_SEQ = 4096` in Cell 1.

**What the training loop does:**

Each iteration takes one batch of training pairs. The model is shown the system and user messages and asked to predict the tokens of the assistant response one by one. For each predicted token, the loss is computed (cross-entropy between predicted probability and actual token). Gradients flow backward and update the LoRA adapter weights. The base model stays frozen throughout.

After training, the adapter weights encode the domain knowledge — CAMELS structure, citation discipline, assessment language, regulatory thresholds, peer comparison framing, and refusal behaviour when data is absent.

**What LoRA adapters are:**

Instead of updating all 7.6 billion parameters — which would require 30–60GB of memory — QLoRA freezes the base model and trains tiny adapter matrices injected into specific layers. This project's adapters have 1.4 million trainable parameters out of 7.6 billion total. That is 0.019%. The trained adapter file is 7MB. The base model is 4GB. They combine at inference time.

**Sequence length is the critical hyperparameter.** At 512 tokens (Mac training), most training pairs are truncated — the model never sees the complete peer comparison or refusal sections. At 4,096 tokens (Colab A100), every pair is seen in full. This is the single biggest quality improvement available — more than model size, more than dataset size.

**Validation loss** is computed on a held-out eval set (10% of data) every 25 iterations. Starting at 3.14, ending at 0.876 after three Mac training rounds. Target after Colab Pro training at 4,096 tokens is ~0.5–0.6.

---

## What the Model Learns

After training the model has internalised:

- **Domain vocabulary** — CET1, MREL, LCR, NSFR, IRB, Stage 3, IRRBB, CCyB, G-SIB surcharge, MDA threshold — and what each means analytically
- **Regulatory thresholds** — Basel III minimums, UK PRA requirements, ECB expectations, OSFI Canadian standards, APRA Australian standards — and how to frame proximity to each
- **Citation discipline** — every figure needs `[Source: p.XX]`, and when data is absent the correct answer is "Data not available" not a fabricated figure
- **Assessment language** — Strong/Adequate/Weak/Critical with the specific criteria each rating agency uses
- **Benchmark context** — the decile ranking is pre-computed and injected into the prompt; the model learns to incorporate it into narrative prose
- **Overview writing** — institutional profile and annual review highlight paragraphs in tight, factual, cited prose

---

## After Training: Deployment

The trained adapter is merged back into the base model, re-quantised to 4-bit, and deployed via Ollama. From that point everything runs locally:

```bash
.venv/bin/python3 test_analysis.py \
  --pdf financials/2025-lbg-annual-report.pdf \
  --pillar3 pillar3/lloyds_banking_group_2025_pillar3.pdf \
  --bank "Lloyds Banking Group"

open output/Lloyds_Banking_Group/2025/dashboard.html
open output/Lloyds_Banking_Group/2025/dashboard_regional.html
```

No API calls. No internet. No data leaving the machine. Qwen handles all eight sections of every credit paper — institutional profile, AR highlights, and six CAMELS pillars — entirely locally.

---

[Back to CAMELS LLM docs](..) | [Main blog post](/blog/comp-science/llm-credit-paper-generator/)
