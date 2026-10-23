---
title: "Securitisation 101 — Part 4: Outputs, Assumptions and Limits"
date: 2026-05-20T07:28:00Z
lastmod: 2026-10-23
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "reporting", "python", "data"]
series: ["Securitisation 101"]
aliases: ["/blog/comp-science/securitisation-pool-optomiser-part-2/"]
description: "What the model produces (BoE tape, investor report, pitch deck, draft prospectus), what is still a placeholder, and the limits of a public-data build."
summary: "Part 4 of 4: the outputs generated on command for the sample deal, the assumptions that matter most, and what needs real data."
ShowToc: true
TocOpen: false
---
<!--more-->

## Outputs, on command

Once the deal is built, each output is generated on its own with `./generate_outputs.sh <what>`, all from the same build:

| Command | Output | Sample deal |
|---|---|---|
| `tape` | BoE loan-level data tape (CSV, TXT or single-sheet XLSX) and cover sheet. Header = BoE field codes only; validated before it is written | 9,951 loans × the template fields |
| `investor` | Investor report: one dynamic page with asset-level detail | [open](/html/rmbs-investor-report.html) |
| `deck` | Investor pitch deck (HTML slides; arrow keys, P to print) | [open](/html/rmbs-investor-deck.html) |
| `sources` | Day-1 sources and uses | [open](/html/sources_and_uses.html) |
| `waterfall` | Stress-case waterfall | [open](/html/stress_case_waterfall.html) |
| `prospectus` | **Draft skeleton only**: the data-driven sections (capital structure, full priorities of payments, eligibility criteria, triggers, enhancement, break-even, WAL and prepayment tables, stratifications), with every legal section left for counsel | – |
| `monthly` | Monthly reporting, one pack per payment date from the servicer's performance file (synthetic here) | [month 12](/html/rmbs-monthly-report.html) |

The investor report covers:
- pool KPIs and the capital structure, with ratings shown the UK way (AAA(sf), unrated Class Z);
- credit coverage per note, and each note's implied chance of loss against its rating's target;
- the sensitivity tornado, the joint check and the reverse stress;
- issuance economics;
- projected note balances;
- the life-of-deal cash reconciliation;
- stratification charts;
- a loan map;
- a sortable, searchable table of all 9,951 loans.

Every output carries a run footer: the run id, code version, a hash of the configuration and of the data, the seed, the pool fingerprint and the test run, so any figure can be traced back to the build that made it.

It is about 3MB, because the loan-level data is in the page:

<iframe src="/html/rmbs-investor-report.html" loading="lazy" width="100%" height="900" style="border:1px solid #333;border-radius:8px"></iframe>

### Through the life of the deal

Each month the servicer's performance file (defaults, prepayments, losses, interest, arrears) drives the waterfall for that month; later months are projected. Each payment date gets:
- the investor pack, which checks itself line by line and reconciles to the penny;
- an HTML report with note factors, arrears at 30, 60 and 90+ days, the priority of payments, the reserve and the triggers;
- a refreshed BoE tape with its cover sheet, a data-quality report and the changes since last month.

There is no real servicer data here, so the sample uses a synthetic file and says so on every page. After 12 months the pool is £1,173m, Class A has paid down to 79% of its face, and every month reconciles.

### A console to drive it

A local web console runs the whole thing without the command line:
- an executive dashboard;
- a status flow from ingestion to redemption, with the history of every run;
- an exceptions list (issuance failures, breaches, failed checks, flags);
- control pages to run the build, the outputs and the monthly reporting;
- the manual review queue, where a reviewer accepts or rejects loans one by one;
- an assumptions editor that saves each change as a new, checked version.

It runs on the user's own machine only, behind a login, with every action written to an audit log.

---

## Assumptions are placeholders

Every behavioural, market and structural assumption is a placeholder: plausible, public-average, and documented in an assumptions register with the real input that should replace it. The sensitivity tornado from Part 3 says which matter most for the senior notes:

1. the originator score (an operational review input);
2. the payment shock when a fixed rate ends;
3. the score calibration.

All three are estimates no methodology publishes, and they make up most of the sensitivity cushion. Those are the first places to put real data.

Every critical number sits in its own data set, grouped as market data, calibrations, published methodology parameters or the model's own estimates. Each set carries its source, as-of date, status and owner. A data register lists them with a fingerprint of each, the build records which ones it used, and a check fails the build if anything is unreferenced or undocumented. Where no as-of date was ever recorded, the register says so rather than guessing.

**Calibrated to public data:** BoE Bank Rate, HM Land Registry house prices (including the range of regional falls, from -15% to -27%, behind the house-price shock), and BoE mortgage lending statistics (MLAR) for LTV, loan-to-income and purpose mix. Public-average note margins and costs are used too. Comparable deals are used only as unnamed ranges: no transaction, rating agency or lender is named.

---

## Limits

- **Synthetic pool.** The loans are realistic but made up. A real warehouse tape replaces them.
- **Not an agency model.** The generic credit model uses public rating concepts; slots for actual agency approaches are left blank for benchmarking later.
- **Not modelled:** a CCC-rated class (no public parameters for it), two agencies' ratings side by side (one calculated model, by design) and multiple master-trust series. The legal prospectus stays with counsel.
- **The synthetic servicer file and tape refresh.** Monthly reporting works end to end, but on made-up performance; a real servicer's loan-level file replaces it.
- **The behavioural model is benign.** The Monte Carlo challenger cannot bite until defaults, prepayments and recoveries are calibrated to real history.
- **Do not use in production.** See Part 1: the last 10% needs real data, judgement and an independent review.

What needs real data now, in order: an operational review of the originator (the originator score), a performance history to calibrate defaults, prepayments and recoveries, the Bank of England's SONIA curve and market note spreads on the issue date, and real deals to validate against.

---

## References

- Bank of England, *Loan-level data: reporting template for residential mortgage pools* (2024)
- Bank of England / FCA, *Mortgage Lenders and Administrators Statistics* (MLAR)
- HM Land Registry, *UK House Price Index*
- ONS / APCP-T(21)07, lenders' formula for mortgage repayments
- National Audit Office, *Introduction to Asset-Backed Securities* (2016)
- Published rating-agency RMBS methodologies and credit enhancement primers (public domain; not named)
- A public UK RMBS prospectus (structure and note terms only; not named or quoted)

---

### Securitisation 101 series

**Previous:** [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)
4. Part 4: Outputs, Assumptions and Limits (this post)
