---
title: "Securitisation 101 — Part 3: Building the Deal"
date: 2026-05-20T07:27:29Z
lastmod: 2026-10-23
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "optimisation", "python", "credit risk"]
series: ["Securitisation 101"]
aliases: ["/blog/comp-science/securitisation-pool-optomiser/"]
description: "From warehouse to tranched deal: pool selection, the frozen static set, rating stresses, capital-stack sizing, a sensitivity cushion, challengers and issuance economics."
summary: "Part 3 of 4: how the model selects the pool, stresses it at each rating level, sizes every class, adds a sensitivity cushion, challenges the result and checks the deal is economic to issue."
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

Which tests run inside that loop is not hard-coded. A master test list, itself an assumption file, says which stresses, sizing methods, gates and reports apply for a jurisdiction and a named run. Mandatory tests (cash conservation, the rating stresses, the optimiser) cannot be switched off, so no one can drop a test to make a deal pass. Every build records the tests it ran.

---

## 1. Selecting the pool

The warehouse holds more loans than the deal needs. Picking the subset is a combinatorial problem; 20,000 loans give far too many possible pools to try them all.

- **Pre-filter** (`pre_filter.py`): one deterministic pass removes ineligible loans (defaulted, redeemed or repurchased, LTV above the cap, zero balance or rate) and flags concentrations (buy-to-let, interest-only, region). It also checks the pool can pay the notes before any search starts.
- **Search** (`rl_pool_selector.py`): a greedy warm start, then simulated annealing (add / remove / swap loans), rewarding the senior notes and penalising breaches of the concentration caps.
- **In the loop:** the first round takes every eligible loan. If a round fails, the next one searches again with the failure as a penalty: the loans with the highest expected loss after a credit failure, the lowest-yielding after a spread failure.
- **Whole groups only:** loans on the same property or to the same borrower stay together, in or out. A reviewer can also reject loans one by one before the build.

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
- giving **credit coverage**: the stressed loss each rating level must survive. For the sample pool, AAA coverage is 21.1% defaults × 34.1% severity = 7.2% of the pool.

Some loans need more than the published scoring captures. Loans already in arrears at cut-off start closer to default (three times the hazard). Flats and homes worth over £1m fall further in a downturn (10% and 15% more). Regional add-ons, a remortgage effect and a seasoning credit are in place but neutral until calibrated. Each of these is labelled an estimate.

The originator score matters most. It is a judgement from the operational review, on a 1–10 scale where 1–3 is a high-street prime lender. The sample pool is built as prime, so it is set at 2. An earlier version left it at 5 (a near-prime lender), which nearly doubled the expected PD.

Each rating is run through the monthly waterfall under 16 scenarios: defaults front- or back-loaded × four prepayment speeds × Bank Rate up or down.

---

## 4. Sizing the stack

Every class, including Class Z, is sized from the stresses. Each class's attachment is searched by bisection, between the highest level where it loses in its rating's scenarios and the lowest where it does not, down to a floor (Class Z must at least fund the reserve and the day-1 costs). For the sample deal, Class A loses at 7.2% subordination and survives at **7.3%**: that is the stress-test level.

Classes follow the convention of issued UK notes: lettered from the most senior, each one rating category below the class above, with an unrated first-loss Class Z. Ratings are shown as, for example, AAA(sf). Three stacks are built in: prime master trust (A + Z, the default), sequential (A to D + Z) and full sequential (A to F + Z).

### The sensitivity cushion

The stress test assumes the central assumptions are right. The cushion adds room for them being wrong, but only where the model has had to guess. Published parameters (house-price falls, sale discounts, costs, asset correlation) are already in the rating stresses, so they are reported, not cushioned. Each estimate is shocked to its adverse value and the attachment is **re-solved**:

| Estimate (adverse side) | Class A break-even rises by |
|---|---|
| Originator score (+2 points) | 1.0pp |
| Payment shock when a fixed rate ends (+50%) | 0.9pp |
| Score calibration (+8 points) | 0.7pp |
| Size of the rate stress (+25%) | 0.5pp |
| LGD score weight | 0.1pp |

Combined by root-sum-square, that is a **1.6%** cushion, so Class A attaches at **8.9%**. With the 1.5% reserve its enhancement is **10.4%**, close to the public pattern for UK prime master trusts (about 10%). On the pool's own loss distribution, the chance that Class A takes any loss is about 1.6bp, against about 16bp allowed for AAA.

A joint check moves all five estimates together, each by 1/√5 of its shock (the same overall size as one full shock); the cushioned structure passes. Every estimate at full size at once is a reverse stress, reported but never required: Class A would then need 12.9%.

### Challenging the result

The sizing is PD-based: each class must take no loss in its rating's deterministic stresses. Several challengers report beside it.

- **Break-even.** On its worst scenario, Class A first loses when defaults reach 27.2% of the pool (1.29× the AAA rate), or the market value decline reaches 41.2% (1.33×).
- **An EL-based view** sizes each class to a target expected loss instead. It would give Class A only 2.5%, because a thick senior class loses so little when it loses at all. Here the EL view is far less conservative, so it is reported, not used.
- **Monte Carlo.** Correlated paths run through the waterfall, with defaults and house prices driven by one systematic draw, and importance sampling pushes the paths into the AAA tail. Class A never loses, even at 6.3 standard deviations. That is not comfort: it says the behavioural default model is a placeholder far milder than the AAA stress, and the challenger cannot bite until it is calibrated to real performance.
- **Swap termination.** If the swap ended at month 12 and the issuer stayed unhedged through the rates-up scenarios, Class A would need 10.2%, more than it has. Counterparty rules (collateral or replacement on a downgrade) normally remove that risk; the report makes it visible.

### Prepayment

UK borrowers rarely repay inside their fixed rate, because early repayment charges apply, and then most remortgage within a few months of it ending. The model prepays loan by loan on that pattern: low while the charge applies, a spike after the fix ends, then a rate driven by each loan's age and its incentive against today's mortgage rates. The sample pool prepays at about 15% in year 1, 22% in year 2 and 35% as the five-year fixes end.

| Prepayment | Class A WAL (to call / maturity) | Class Z yield |
|---|---|---|
| Slow (half speed) | 3.3 / 4.9 years | 8.0% |
| Base | 2.7 / 3.0 years | 6.5% |
| Fast (×1.75) | 2.3 / 2.3 years | 5.6% |

Slow prepayment extends the senior notes; fast prepayment runs the excess spread off and costs Class Z. Without the call, Class A is repaid by month 130 instead of 61.

### Is it worth issuing?

The swap is struck at the market rate on the issue date. The loans' fixed rates, though, were locked when they went into the warehouse. If Bank Rate rises in between, the swap and the notes cost more while the loans pay the same. The sample deal earns 90bp of excess spread after the swap and can absorb a **1.1pp** rise before it is uneconomic. If a 1pp rise did happen before issue, the deal re-sized on the new rates would need Class A at 8.6%, still inside the 8.9% it has.

A bigger move is an **issuance failure**: the deal is not issued at those terms. The model does not force a fix. It stops and flags it for manual assessment: reprice, hold the loans in the warehouse, or re-select the pool.

On a prime pool, the first-loss note is retained by the issuer. Selling it at a market yield (12% here) does not work: Class Z is paid only from excess spread, and even at a 1,200bp margin it yields 6.7%.

---

### Securitisation 101 series

**Previous:** [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/) · **Next:** [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. Part 3: Building the Deal (this post)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
