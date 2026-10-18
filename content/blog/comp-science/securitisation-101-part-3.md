---
title: "Securitisation 101 — Part 3: Building the Deal"
date: 2026-05-20T07:27:29Z
lastmod: 2026-10-18
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "optimisation", "python", "credit risk"]
series: ["Securitisation 101"]
aliases: ["/blog/comp-science/securitisation-pool-optomiser/"]
description: "From warehouse to tranched deal: pool selection, the frozen static set, rating stresses, capital-stack sizing, a sensitivity cushion and issuance economics."
summary: "Part 3 of 4: how the model selects the pool, stresses it at each rating level, sizes every class, adds a sensitivity cushion and checks the deal is economic to issue."
ShowToc: true
TocOpen: false
---
<!--more-->

Part 2 covered how the cash moves. This part is about how big each note should be, and whether the deal is worth issuing at all. The model loops through four steps until it finds a viable deal:

```
warehouse ─► select & price pool ─► create deal ─► freeze static set ─► stress & tranche ─► viable?
                 ▲                                                                            │
                 └──────────────── no: re-select pool ◄──────────────────────────────────────┘
```

---

## 1. Selecting the pool

The warehouse holds more loans than the deal needs. Picking the subset is a combinatorial problem; 20,000 loans give far too many possible pools to try them all.

- **Pre-filter** (`pre_filter.py`): one deterministic pass removes ineligible loans (in default, LTV above the cap, score below the floor). It also checks the pool can pay the notes before any search starts.
- **Search** (`rl_pool_selector.py`): a greedy warm start, then simulated annealing (add / remove / swap loans), rewarding Class A size and penalising constraint breaches. A sources-and-uses imbalance is penalised hardest, so an invalid pool is never accepted.

Simulated annealing needs no training data and every step is visible, which matters when there is no corpus of past warehouse pools to learn from.

The sample pool is built to look like a **UK prime new issue**:
- loans 3–30 months old (17 months on average);
- 90% of the balance still in an introductory fix;
- only 2% with past adverse credit;
- a regional mix with about a fifth in London.

LTV, loan-to-income and purpose mix are calibrated to BoE MLAR lending data. Getting this right matters: an earlier version left too many loans on reversion rates, and the credit model rightly penalised it.

---

## 2. Freezing the static set

Before stressing anything, the pool is frozen: the cut-off balances, each loan's calculated credit score and segment, and its PD and LGD inputs. Within a stress run every tranche is treated as issued and fixed; tranches are fixed for good only at issue.

---

## 3. Stressing it

The model uses one **generic calculated credit model**, built from public rating methodology concepts rather than any one agency's:

- a credit score per loan → a pool PD → a rating-level default rate (a Vasicek model, at the default probability a rating allows over the pool's life);
- times loss severity per loan (house-price falls, forced-sale discount, costs, with floors);
- giving **credit coverage**: the stressed loss each rating level must survive. For the sample pool, AAA coverage is 26.5% defaults × 33.9% severity = 9.0% of the pool.

Each rating is run through the monthly waterfall under 16 scenarios: defaults front- or back-loaded × four prepayment speeds × Bank Rate up or down. There are blank slots for actual rating-agency approaches, so the generic model can be benchmarked against each one later.

---

## 4. Sizing the stack

Every class, including Class Z, is sized from the stresses. Each class's attachment point is searched between "loses in its rating's scenarios" and "does not lose" until the stack settles. Two stack designs are built in:

- **Prime master trust** (default): Class A over a first-loss Class Z. The Class Z note, retained by the originator, plus the reserve is all of Class A's credit enhancement.
- **Sequential mezzanine**: Classes A, B, C and D over Class Z, with minimum sizes so the mezzanine notes can actually be sold.

### The sensitivity cushion

The stress test assumes the central assumptions are right. The sensitivity step adds room for them being wrong. Each of 15 assumptions is shocked low and high at the fixed structure, and the stress test is re-run each time. Each class's adverse changes combine into a cushion, which is added to its attachment.

For the sample deal, the stress test needs 10.3% subordination under Class A. The cushion adds 2.6%, giving **12.9%**. The biggest drivers:

| Assumption (adverse side) | Class A loss at the fixed structure |
|---|---|
| Payment shock when a fixed rate ends (+50%) | 1.8% of pool |
| Originator score (+2 points) | 1.8% |
| Asset correlation (+20%) | 0.5% |

That ranking also says which real data to chase first.

### Is it worth issuing?

The swap is struck at the market rate on the issue date. The loans' fixed rates, though, were locked when they went into the warehouse. If Bank Rate rises in between, the swap and the notes cost more while the loans pay the same. The sample deal earns 108bp of excess spread after the swap and can absorb a **1.4pp** rise before it is uneconomic.

A bigger move is an **issuance failure**: the deal is not issued at those terms. The model does not force a fix. It stops and flags it for manual assessment: reprice, hold the loans in the warehouse, or re-select the pool. This is a real path under a very adverse market shift.

---

### Securitisation 101 series

**Previous:** [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/) · **Next:** [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. Part 3: Building the Deal (this post)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
