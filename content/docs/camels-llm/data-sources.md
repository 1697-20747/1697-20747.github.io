---
title: "Data Sources"
weight: 3
description: "All six data pipelines, bank coverage, and the bank industry data quality problem."
summary: "All six data pipelines, bank coverage, and the bank industry data quality problem."
---

## Coverage Summary

~5,000 training pairs from 150+ source documents across the US, UK, EU, Australia and Canada.

| Region | Currency | Banks | Years |
|--------|----------|-------|-------|
| UK | GBP | Lloyds, Barclays, HSBC, NatWest, Standard Chartered | 8–10yr |
| EU | EUR | Deutsche Bank, Santander, UniCredit, BNP Paribas, ABN AMRO, Intesa | 4–10yr |
| AU | AUD | ANZ, Westpac, NAB, CBA | 3–5yr |
| CA | CAD | RBC, TD Bank, Scotiabank, BMO, CIBC | 2–10yr |
| US | USD | JPMorgan, BofA, Goldman, Citi, Wells Fargo + FDIC top 100 | 5–10yr |

---

## Annual Reports

SEC EDGAR has every 10-K filing for every listed US bank going back decades, in machine-readable HTML. The downloader pulls these automatically by CIK number. UK, EU, Australian and Canadian banks are messier — IR pages with inconsistent formats, date-stamped filenames that change every year, some banks blocking automated downloads entirely (HTTP 403), others requiring JavaScript to render the page before the PDF link appears.

Every major bank required its own bespoke URL pattern. HSBC uses date-stamped filenames reflecting the results announcement day, not the reporting period (`250227-annual-report-and-accounts-2024.pdf`). Deutsche Bank stores each year's report in the following year's folder. NatWest changes the Pillar 3 filename every single year with no discernible pattern. ABN AMRO migrated their document hosting to a third-party CDN mid-series. These are not edge cases. This is the norm.

---

## Pillar 3 Reports

The richest source of regulatory capital data. Published alongside annual reports but in a mix of formats — some banks PDF only, some Excel only, some both. The Excel files vary enormously in structure, sheet naming, column layout and unit conventions from bank to bank and year to year within the same bank. A CET1 ratio that appears as `13.50` in one bank's workbook appears as `0.1350` in another's and `1350` (basis points) in a third. There is no standard schema.

Extracting data from PDFs is inherently unreliable. PDF is a presentation format, not a data format. Tables are reconstructed by layout engines that make assumptions about column boundaries and row associations that frequently produce incorrect results — particularly in the dense regulatory capital tables Pillar 3 reports contain. Any pipeline that relies on PDF table extraction for quantitative data must be treated as producing approximate outputs requiring human validation. This system is no exception.

---

## EBA Transparency Exercise

The European Banking Authority publishes standardised capital, asset quality, profitability and liquidity data for 156+ EU/EEA banks every year as a downloadable CSV. Free, no registration, consistent schema, machine-readable. This is what good bank data looks like. 1,463 training pairs from one file.

The contrast with manually parsed annual report PDFs is stark. The EBA data takes minutes to download and process. The annual reports take days of URL hunting, format normalisation, rename scripting, and extraction debugging. The data content is broadly similar. The accessibility difference is entirely a function of how the data is published.

---

## FDIC Call Reports

Every US bank files quarterly with the FDIC. They have a public REST API at `banks.data.fdic.gov`. Top 100 banks by assets, annual periods. The API documentation lies — several field names in the docs do not match the actual API response. You have to debug it against the live endpoint. Once working, it is reliable structured data. 935 pairs.

---

## Rating Agency Methodology

All freely available with registration where required:

| Source | Documents | Content |
|--------|-----------|---------|
| Basel Committee (BIS) | 9 | Capital, LCR, NSFR, leverage, IRRBB, core principles, output floor |
| OCC Comptroller's Handbook | 7 | Capital, earnings, liquidity, sensitivity, asset quality, credit risk rating |
| EBA Guidelines | 3 | SREP, NPL management, liquidity stress |
| Federal Reserve | 2 | DFAST 2023 + 2024 stress test results |
| IMF | 5 | FSAP technical notes — UK, US, Germany, France, Euro Area |
| PRA | 2 | UK supervisory approach, ICAAP guidance |
| OSFI | 2 | B-20 mortgage underwriting, B-15 model risk (Canada) |
| APRA | 1 | APS 110 Capital Adequacy (Australia) |
| Fitch | 1 | Banks Rating Criteria (free registration) |
| S&P | 1 | Financial Institutions Rating Criteria (free registration) |
| DBRS Morningstar | 1 | Global Banks and Banking Organisations methodology |
| Moody's | 1 | Banks — Argentina supplement (global framework valid) |

---

## Real Analyst Credit Papers

The gold standard. Real S&P RatingsDirect, Moody's Credit Opinion and Fitch Rating Report PDFs dropped into `credit_reports/` are extracted automatically. Banks currently covered: Lloyds Banking Group, Barclays, Deutsche Bank, Standard Chartered, Santander UK, Citigroup. 196 pairs, weighted 2x in training.

Most institutional credit research is paywalled ($500–2,000 per report from the agencies). What is available freely tends to be older reports, publicly disclosed rating actions, or reports published by banks on their own IR pages. If you have access to current research through a Bloomberg or Refinitiv terminal, adding more papers to `credit_reports/` is the single highest-leverage improvement you can make to the training data.

---

## The Industry Data Quality Problem

Building this pipeline reveals a genuine gap between what the regulatory framework requires banks to disclose and the practical accessibility of that data.

The gap is not in the content — banks do disclose what they are required to disclose. The gap is entirely in machine-readability. A CET1 ratio is disclosed in every Pillar 3 report. Getting it into a machine-readable form requires: finding the IR page, navigating past JavaScript, downloading a PDF, running a layout engine to reconstruct the table, heuristically identifying the correct row and column, normalising the units, and validating that the number makes sense. This process fails often enough that human review is required for any quantitative use.

**What good would look like:** The EBA transparency exercise demonstrates the model. 156 banks, consistent schema, annual cadence, free CSV download, no registration. Extending this to Pillar 3 disclosures at the individual bank level — a standardised Apache Parquet or JSON schema for the key quantitative tables, with stable URLs and open download permissions — would eliminate the extraction problem entirely.

The LEI (Legal Entity Identifier) is already a global standard for bank identification. Using it as the primary key in filenames and URLs (`<LEI>_pillar3_<YYYY>.pdf`) would make discovery trivial. The regulatory framework already mandates the disclosure. The only missing piece is the format and delivery convention. The EBA, FDIC and Federal Reserve have shown the way. The industry should follow.

---

[Back to CAMELS LLM docs](..) | [Training pairs](../training-pairs/) | [Main blog post](/blog/comp-science/llm-credit-paper-generator/)
