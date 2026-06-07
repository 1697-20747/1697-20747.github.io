---
title: "Data Sources"
weight: 3
description: "All six data pipelines, bank coverage, and the bank industry data quality problem."
summary: "All six data pipelines, bank coverage, and the bank industry data quality problem."
---

## Coverage Summary

~5,000+ data records from 150+ source documents across US, UK, EU, Australia
and Canada. The data feeds two distinct workflows:

1. **Training data preparation** (legacy) — JSONL pairs for QLoRA fine-tuning
2. **Inference-time grounding** (current) — benchmark index + peer roster
   injected into prompts

The fine-tuning attempt didn't ship — see the
[Fine-Tuning Retrospective](../fine-tuning-retrospective/). The grounding
infrastructure is what actually runs in production.

| Region | Currency | Banks | Years |
|--------|----------|-------|-------|
| UK | GBP | Lloyds, Barclays, HSBC, NatWest, Standard Chartered | 8–10yr |
| EU | EUR | Deutsche Bank, Santander, UniCredit, BNP Paribas, ABN AMRO, Intesa | 4–10yr |
| AU | AUD | ANZ, Westpac, NAB, CBA | 3–5yr |
| CA | CAD | RBC, TD Bank, Scotiabank, BMO, CIBC | 2–10yr |
| US | USD | JPMorgan, BofA, Goldman, Citi, Wells Fargo + FDIC top 100 | 5–10yr |

---

## Annual Reports

SEC EDGAR has every 10-K filing for every listed US bank going back decades,
in machine-readable HTML. The downloader pulls these automatically by CIK
number. UK, EU, Australian and Canadian banks are messier — IR pages with
inconsistent formats, date-stamped filenames that change every year, some
banks blocking automated downloads entirely (HTTP 403), others requiring
JavaScript to render the page before the PDF link appears.

Every major bank required its own bespoke URL pattern. HSBC uses date-stamped
filenames reflecting the results announcement day, not the reporting period
(`250227-annual-report-and-accounts-2024.pdf`). Deutsche Bank stores each
year's report in the following year's folder. NatWest changes the Pillar 3
filename every single year with no discernible pattern. ABN AMRO migrated
their document hosting to a third-party CDN mid-series. These are not edge
cases. This is the norm.

---

## Pillar 3 Reports

The richest source of regulatory capital data. Published alongside annual
reports but in a mix of formats — some banks PDF only, some Excel only, some
both. The Excel files vary enormously in structure, sheet naming, column
layout and unit conventions from bank to bank and year to year within the same
bank. A CET1 ratio that appears as `13.50` in one bank's workbook appears as
`0.1350` in another's and `1350` (basis points) in a third. There is no
standard schema.

Extracting data from PDFs is inherently unreliable. PDF is a presentation
format, not a data format. Tables are reconstructed by layout engines that
make assumptions about column boundaries and row associations that frequently
produce incorrect results — particularly in the dense regulatory capital
tables Pillar 3 reports contain. **Any pipeline that relies on PDF table
extraction for quantitative data must be treated as producing approximate
outputs requiring human validation. This system is no exception.**

---

## EBA Transparency Exercise

The European Banking Authority publishes standardised capital, asset quality,
profitability and liquidity data for 156+ EU/EEA banks every year as a
downloadable CSV. Free, no registration, consistent schema, machine-readable.
This is what good bank data looks like.

The contrast with manually parsed annual report PDFs is stark. The EBA data
takes minutes to download and process. The annual reports take days of URL
hunting, format normalisation, rename scripting, and extraction debugging.
The data content is broadly similar. The accessibility difference is entirely
a function of how the data is published.

---

## FDIC Call Reports

Every US bank files quarterly with the FDIC. They have a public REST API at
`banks.data.fdic.gov`. Top 100 banks by assets, annual periods. The API
documentation has some inconsistencies — several field names in the docs
don't match the actual API response. Once working, it is reliable structured
data.

---

## Rating Agency Methodology

All freely available with registration where required:

| Source | Documents | Content |
|--------|-----------|---------|
| Basel Committee (BIS) | 9 | Capital, LCR, NSFR, leverage, IRRBB, output floor |
| OCC Comptroller's Handbook | 7 | Capital, earnings, liquidity, sensitivity, asset quality |
| EBA Guidelines | 3 | SREP, NPL management, liquidity stress |
| Federal Reserve | 2 | DFAST 2023 + 2024 stress test results |
| IMF | 5 | FSAP technical notes — UK, US, Germany, France, Euro Area |
| PRA | 2 | UK supervisory approach, ICAAP guidance |
| OSFI | 2 | B-20 mortgage underwriting, B-15 model risk (Canada) |
| APRA | 1 | APS 110 Capital Adequacy (Australia) |
| Fitch | 1 | Banks Rating Criteria (free registration) |
| S&P | 1 | Financial Institutions Rating Criteria (free registration) |
| DBRS Morningstar | 1 | Global Banks methodology |

---

## Real Analyst Credit Papers

The gold standard. Real S&P RatingsDirect, Moody's Credit Opinion and Fitch
Rating Report PDFs dropped into `credit_reports/` are extracted automatically.
Banks currently covered: Lloyds Banking Group, Barclays, Deutsche Bank,
Standard Chartered, Santander UK, Citigroup.

Most institutional credit research is paywalled ($500–2,000 per report from
the agencies). What is available freely tends to be older reports, publicly
disclosed rating actions, or reports published by banks on their own IR
pages. If you have access to current research through a Bloomberg or
Refinitiv terminal, adding more papers to `credit_reports/` is the single
highest-leverage improvement you can make.

---

## Benchmark Index — How It's Built

`scripts/build_benchmark_index.py` walks all processed financial data
(annual reports, EBA CSV, FDIC API records) and computes population statistics
for each metric:

- Mean, median
- p10, p25, p75, p90
- Decile breakpoints (10 thresholds covering 0–100th percentile)
- Sample size

Two distributions per metric:
- **all** — every year in the dataset
- **recent** — last 3 years only

Plus regional breakdowns for UK, EU, US, AU, CA where the sample shares a
currency.

The output is `processed/benchmark_index.json`. At inference, `test_analysis.py`
loads it and computes the decile for each extracted subject-bank metric before
calling the LLM.

---

## Peer Roster — How It's Built

`scripts/build_peer_roster.py` walks `processed/financials/*.json` (the
extracted JSONs from each annual report), identifies each bank by filename
prefix, extracts the latest year's metrics, applies sanity filters, and
saves:

```json
{
  "Lloyds Banking Group": {
    "region": "UK", "currency": "GBP", "year": 2025,
    "metrics": {"cet1_ratio": 14.0, "leverage_ratio": 5.4, "rote": 22.1, ...}
  }
}
```

Sanity filters reject obviously-wrong extractions:
- ROA > 5% (rejects "ROA 2025.0" from year-leakage)
- Tier 1 ratio < 5% (rejects regex misfires)
- LCR < 80% or > 250% (out-of-range)
- ... etc

These are extractor bugs that should be fixed at source eventually, but
filtering them out of the roster prevents bad values reaching the prompt.

At inference, `test_analysis.py` loads the roster, identifies the subject bank,
finds same-region peers (UK peers for UK bank — same region always ranks above
cross-region regardless of metric coverage), and injects 3–5 peer banks'
relevant metrics into each section prompt.

---

## The Industry Data Quality Problem

Building this pipeline reveals a genuine gap between what the regulatory
framework requires banks to disclose and the practical accessibility of that
data.

The gap is not in the content — banks do disclose what they are required to
disclose. The gap is entirely in machine-readability. A CET1 ratio is
disclosed in every Pillar 3 report. Getting it into a machine-readable form
requires: finding the IR page, navigating past JavaScript, downloading a PDF,
running a layout engine to reconstruct the table, heuristically identifying
the correct row and column, normalising the units, and validating that the
number makes sense. This process fails often enough that human review is
required for any quantitative use.

**What good would look like:** The EBA transparency exercise demonstrates
the model. 156 banks, consistent schema, annual cadence, free CSV download,
no registration. Extending this to Pillar 3 disclosures at the individual
bank level — a standardised Apache Parquet or JSON schema for the key
quantitative tables, with stable URLs and open download permissions — would
eliminate the extraction problem entirely.

The LEI (Legal Entity Identifier) is already a global standard for bank
identification. Using it as the primary key in filenames and URLs
(`<LEI>_pillar3_<YYYY>.pdf`) would make discovery trivial. The regulatory
framework already mandates the disclosure. The only missing piece is the
format and delivery convention. The EBA, FDIC and Federal Reserve have
shown the way. The industry should follow.

---

[Back to CAMELS LLM docs](..) | [How It Works](../how-it-works/) | [Main blog post](/blog/comp-science/llm-credit-paper-generator/)
