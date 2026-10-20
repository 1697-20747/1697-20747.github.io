---
title: "Securitisation 101 — Part 4: Outputs, Assumptions and Limits"
date: 2026-05-20T07:28:00Z
lastmod: 2026-10-20
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
| `prospectus` | **Draft skeleton only**: the data-driven sections (capital structure, priority of payments, WAL tables, stratifications), with every legal section left for counsel | – |
| `monthly` | Ongoing monthly reporting: **placeholder**, not built yet | – |

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

Every output carries a run footer: the run id, code version, a hash of the configuration, the seed and the pool fingerprint, so any figure can be traced back to the build that made it.

It is about 3MB, because the loan-level data is in the page:

<iframe src="/html/rmbs-investor-report.html" loading="lazy" width="100%" height="900" style="border:1px solid #333;border-radius:8px"></iframe>

---

## Assumptions are placeholders

Every behavioural, market and structural assumption is a placeholder: plausible, public-average, and documented in an assumptions register with the real input that should replace it. The sensitivity tornado from Part 3 says which matter most for the senior notes:

1. the originator score (an operational review input);
2. the payment shock when a fixed rate ends;
3. the score calibration.

All three are estimates no methodology publishes, and they make up most of the sensitivity cushion. Those are the first places to put real data.

**Calibrated to public data:** BoE Bank Rate, HM Land Registry house prices, and BoE mortgage lending statistics (MLAR) for LTV, loan-to-income and purpose mix. Public-average note margins and costs are used too. Comparable deals are used only as unnamed ranges: no transaction, rating agency or lender is named.

---

## Limits

- **Synthetic pool.** The loans are realistic but made up. A real warehouse tape replaces them.
- **Not an agency model.** The generic credit model uses public rating concepts; slots for actual agency approaches are left blank for benchmarking later.
- **Not modelled yet:** liquidity reserve, excess-spread notes, a CCC-rated class, a switch from sequential to pro-rata principal, quarterly SONIA payment dates, master-trust revolving periods.
- **Prospectus and monthly reporting** are placeholders.
- **Do not use in production.** See Part 1: the last 10% needs real data, judgement and an independent review.

What can still be improved without real data: completing the structure (the items above), more loan-level adjustments (arrears at cut-off, flats versus houses, regional house-price falls), more sensitivity work (break-even per class, path stability, a cap on how far the payment shock can lift defaults) and filling in the monthly reporting.

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
