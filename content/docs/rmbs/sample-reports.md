---
title: "Sample Outputs"
weight: 3
description: "Outputs for the current sample deal SYN-RMBS-2025-001: investor report, pitch deck, sources and uses, stress-case waterfall, monthly report."
summary: "Outputs for the current sample deal SYN-RMBS-2025-001."
ShowToc: false
---

All outputs come from one build of the model on the synthetic sample pool (cut-off 30 April 2025, issue date 19 July 2025). Regenerate them with `./generate_outputs.sh all`.

| Output | What it shows |
|---|---|
| [Investor report](/html/rmbs-investor-report.html) | Pool KPIs, capital structure, credit coverage per note, sensitivity tornado, issuance economics, projected note balances, cash reconciliation, stratifications, loan map and a searchable loan-level table (about 3MB) |
| [Investor pitch deck](/html/rmbs-investor-deck.html) | Highlights, capital structure, pool, stratifications, credit coverage, WAL to call, Class Z, key risks. Arrow keys to move, P to print |
| [Sources and uses](/html/sources_and_uses.html) | Day-1 cash raised from each note against the pool purchase, reserve and costs, reconciled to the penny |
| [Stress-case waterfall](/html/stress_case_waterfall.html) | The worst AAA scenario through the revenue and principal priority of payments, and the loss cascade |
| [Monthly report, payment date 12](/html/rmbs-monthly-report.html) | Note factors, arrears at 30 / 60 / 90+ days, the priority of payments, reserve, triggers and reconciliation for one payment date (SYNTHETIC servicer data) |

Not published here:
- the BoE loan-level tape (a 4MB CSV), its post-generation test report and the monthly tape refreshes;
- the draft prospectus skeleton, which holds only data sections.

## Sample deal at a glance

| Item | Value |
|---|---|
| Pool | 5,366 owner-occupied loans, £999.8m, WA rate 4.82%, WA original LTV 75.2%; selected from a 50,000-loan warehouse |
| Profile | Prime proxy, seasoned: 91% in a fixed-rate period, 0.1% past adverse credit, 31 months on average, about a fifth in London |
| Dates | Cut-off 30 April 2025; priced as of the issue date, 19 July 2025 (cut-off plus 80 days) |
| Stack | Prime master trust: Class A Notes (AAA(sf), Bank Rate + 50bp) £923.2m; unrated Class Z Notes, first loss, £97.0m, retained, index flat |
| Class A enhancement | 9.7% subordination (7.0% stress test + 2.66% sensitivity cushion) + 1.5% amortising reserve = 11.2%; against the pool, 92.0% Class A and 9.5% enhancement at closing (public prime deals: 91.4–92.0% and 10.0%) |
| AAA credit coverage | 6.6% of pool (19.3% defaults × 34.1% severity); Class A covers it 1.70x; implied chance of any loss about 0.8bp against a 20bp AAA target |
| Break-even | Class A first loses at defaults of 30.9% of the pool (1.60x the AAA rate) or a market value decline of 49.2% (1.59x) |
| Swap | One amortising swap on the expected fixed-rate balance, £912m, 3.648%; hedge ratio 0.97 / 1.00 / 1.04 at slow / base / fast prepayment |
| Prepayment | About 24% a year over five years; Class A WAL 2.3 years to the call (3.1 slow, 1.8 fast) |
| Issuance economics | 83bp excess spread after the swap; tolerates a 1.0pp rate rise between warehouse and issue |
| BoE tape | 5,366 loans × 233 fields; read back and tested: 27 rules, 29 checks, all pass |

Illustrative only: synthetic loans, public-domain parameters, not an offer of securities and not a rating.
