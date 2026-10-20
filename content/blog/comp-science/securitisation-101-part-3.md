---
title: "Securitisation 101 — Part 3: Building the Deal"
date: 2026-05-20T07:27:29Z
lastmod: 2026-10-20
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

- **Pre-filter** (`pre_filter.py`): one deterministic pass removes ineligible loans (defaulted, redeemed or repurchased, LTV above the cap, zero balance or rate) and flags concentrations (buy-to-let, interest-only, region). It also checks the pool can pay the notes before any search starts.
- **Search** (`rl_pool_selector.py`): a greedy warm start, then simulated annealing (add / remove / swap loans), rewarding the senior notes and penalising breaches of the concentration caps.
- **In the loop:** the first round takes every eligible loan. If a round fails, the next one searches again with the failure as a penalty: the loans with the highest expected loss after a credit failure, the lowest-yielding after a spread failure.
- **Whole groups only:** loans on the same property or to the same borrower stay together, in or out.

Simulated annealing needs no training data and every step is visible, which matters when there is no corpus of past warehouse pools to learn from.

The sample pool is built to look like a **UK prime new issue**:
- loans 3–30 months old (17 months on average);
- 90% of the balance still in an introductory fix;
- only 2% with past adverse credit;
- a regional mix with about a fifth in London.

LTV, loan-to-income and purpose mix are calibrated to BoE MLAR lending data.

---

## 2. Freezing the static set

Before stressing anything, the pool is frozen: the cut-off balances, each loan's calculated credit score and segment, and its PD and LGD inputs. Within a stress run every tranche is treated as issued and fixed; tranches are fixed for good only at issue.

---

## 3. Stressing it

The model uses one **generic calculated credit model**, built from public rating methodology concepts rather than any one agency's:

- a credit score per loan → a pool PD → a rating-level default rate (a Vasicek model, at the default probability a rating allows over the pool's life);
- times loss severity per loan (house-price falls, forced-sale discount, costs, with floors);
- giving **credit coverage**: the stressed loss each rating level must survive. For the sample pool, AAA coverage is 21.0% defaults × 33.7% severity = 7.1% of the pool.

The originator score matters here. It is a judgement from the operational review, on a 1–10 scale where 1–3 is a high-street prime lender. The sample pool is built as prime, so it is set at 2. An earlier version left it at 5 (a near-prime lender), which nearly doubled the expected PD, from 2.6% to 4.7%.

Each rating is run through the monthly waterfall under 16 scenarios: defaults front- or back-loaded × four prepayment speeds × Bank Rate up or down. There are blank slots for actual rating-agency approaches, so the generic model can be benchmarked against each one later.

The intelligent next step is to reverse engineer each rating agency's approach from its published criteria. Each optimised pool could then be smoke-tested against every agency's process before issue, challenging the pool and structure before proceeding. That is not covered in this project; the slots are there for it.

---

## 4. Sizing the stack

Every class, including Class Z, is sized from the stresses. Each class's attachment is searched by bisection, between the highest level where it loses in its rating's scenarios and the lowest where it does not, down to a floor (Class Z must at least fund the reserve and the day-1 costs). For the sample deal, Class A loses at 7.1% subordination and survives at **7.2%**: that is the stress-test level.

An earlier version stopped too soon. If the starting structure passed, the search never went lower, because Class Z, which is repaid from revenue, is never repaid in the harshest scenario, and its whole balance fed back as the "requirement". The requirement simply equalled the starting size. The search now always tests downwards.

Classes follow the convention of issued UK notes: lettered from the most senior, each one rating category below the class above, with an unrated first-loss Class Z. Ratings are shown as, for example, AAA(sf). Three stack designs are built in:

- **Prime master trust** (default): Class A (AAA) over a first-loss Class Z. The Class Z note, retained by the originator, plus the reserve is all of Class A's credit enhancement.
- **Sequential**: Classes A (AAA), B (AA), C (A) and D (BBB) over Class Z, with minimum sizes so the mezzanine notes can actually be sold.
- **Full sequential**: Classes A to F (AAA down to B) over Class Z, as on issued UK specialist deals.

### The sensitivity cushion

The stress test assumes the central assumptions are right. The sensitivity step adds room for them being wrong, but only where the model has had to guess:

- **In the cushion:** the estimated parameters, which no methodology publishes (score calibration, originator score, the payment shock when a fixed rate ends, the LGD score weight and the size of the rate stress).
- **Reported only:** the published parameters (house-price falls, sale discounts, costs, recovery lag, asset correlation, prepayment speeds). The rating stresses already apply them at each rating level, so cushioning them again would count them twice. Market inputs and deal terms are reported only too.

Each estimate is shocked to its adverse value and the attachment is **re-solved**: the bisection runs again under the shocked assumption. The rises combine by root-sum-square, treating the estimates as independent:

| Estimate (adverse side) | Class A break-even rises by |
|---|---|
| Originator score (+2 points) | 1.0pp |
| Payment shock when a fixed rate ends (+50%) | 0.9pp |
| Score calibration (+8 points) | 0.7pp |
| Size of the rate stress (+25%) | 0.5pp |
| LGD score weight | 0.1pp |

That gives a cushion of **1.6%**, so Class A attaches at **8.8%**. With the 1.5% reserve its enhancement is **10.3%**, close to the public pattern for UK prime master trusts (about 10%). On the pool's own loss distribution, the chance that Class A takes any loss is about 1.6bp, against about 16bp allowed for AAA: roughly ten times inside the target.

The ranking also says which real data to chase first: the operational review, then real reversion behaviour.

**Joint check.** The cushion assumes the estimates are independent, so the model tests that too. It moves all five together, each by 1/√5 of its shock, which is the same overall size as one full shock in root-sum-square terms. If the cushioned structure loses there, the estimates compound more than the cushion assumes.

**Reverse stress.** Every estimate at its full adverse value at once is far more remote than the AAA stress the structure is sized to. It is reported, never required. It shows how fragile the deal is at the extreme: expected PD doubles, defaults reach about half the pool, and Class A's interest at the stressed Bank Rate is paid out of its own principal for years.

### Is it worth issuing?

The swap is struck at the market rate on the issue date. The loans' fixed rates, though, were locked when they went into the warehouse. If Bank Rate rises in between, the swap and the notes cost more while the loans pay the same. The sample deal earns 89bp of excess spread after the swap and can absorb a **1.1pp** rise before it is uneconomic.

A bigger move is an **issuance failure**: the deal is not issued at those terms. The model does not force a fix. It stops and flags it for manual assessment: reprice, hold the loans in the warehouse, or re-select the pool. This is a real path under a very adverse market shift.

---

### Securitisation 101 series

**Previous:** [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/) · **Next:** [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. Part 3: Building the Deal (this post)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
