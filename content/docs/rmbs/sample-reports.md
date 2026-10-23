---
title: "Sample Outputs"
weight: 3
description: "Outputs for the current sample deal SYN-RMBS-2025-001: investor report, pitch deck, sources and uses, stress-case waterfall, monthly report."
summary: "Outputs for the current sample deal SYN-RMBS-2025-001."
ShowToc: false
---

All outputs come from one build of the model on the synthetic sample pool (cut-off 30 April 2025). Regenerate them with `./generate_outputs.sh all`.

| Output | What it shows |
|---|---|
| [Investor report](/html/rmbs-investor-report.html) | Pool KPIs, capital structure, credit coverage per note, sensitivity tornado, issuance economics, projected note balances, cash reconciliation, stratifications, loan map and a searchable loan-level table (about 3MB) |
| [Investor pitch deck](/html/rmbs-investor-deck.html) | Highlights, capital structure, pool, stratifications, credit coverage, WAL to call, Class Z, key risks. Arrow keys to move, P to print |
| [Sources and uses](/html/sources_and_uses.html) | Day-1 cash raised from each note against the pool purchase, reserve and costs, reconciled to the penny |
| [Stress-case waterfall](/html/stress_case_waterfall.html) | The worst AAA scenario through the revenue and principal priority of payments, and the loss cascade |
| [Monthly report, payment date 12](/html/rmbs-monthly-report.html) | Note factors, arrears at 30 / 60 / 90+ days, the priority of payments, reserve, triggers and reconciliation for one payment date (SYNTHETIC servicer data) |

Not published here:
- the BoE loan-level tape (a 7MB CSV) and the monthly tape refreshes;
- the draft prospectus skeleton, which holds only data sections.

## Sample deal at a glance

| Item | Value |
|---|---|
| Pool | 9,951 loans, £1,449m, WA rate 5.24%, WA original LTV 72.7% |
| Profile | Prime proxy, new issue: 90% in an introductory fix, 2% past adverse credit, 14% buy-to-let, about a fifth in London |
| Stack | Prime master trust: Class A Notes (AAA(sf), Bank Rate + 70bp) £1,350m; unrated Class Z Notes, first loss, £129m, retained |
| Class A enhancement | 8.9% subordination (7.3% stress test + 1.6% sensitivity cushion on the estimated parameters) + 1.5% reserve = 10.4% (8.7% on the notes basis) |
| AAA credit coverage | 7.2% of pool (21.1% defaults × 34.1% severity); Class A covers it 1.45x; implied chance of any loss about 1.6bp against a 16bp AAA target |
| Break-even | Class A first loses at defaults of 27.2% of the pool (1.29x the AAA rate) or a market value decline of 41.2% (1.33x) |
| Prepayment | About 15% a year in year 1, 22% in year 2, 35% as the five-year fixes end; Class A WAL 2.7 years to the call (3.3 slow, 2.3 fast) |
| Issuance economics | 90bp excess spread after the swap; tolerates a 1.1pp Bank Rate rise between warehouse and issue |

Illustrative only: synthetic loans, public-domain parameters, not an offer of securities and not a rating.
