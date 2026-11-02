---
title: "Securitisation 101 — Part 3: Building the Deal"
date: 2026-05-20T07:27:29Z
lastmod: 2026-11-01
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "optimisation", "python", "credit risk"]
series: ["Securitisation 101"]
aliases: ["/blog/comp-science/securitisation-pool-optomiser/"]
description: "From warehouse to tranched deal: pool selection, the frozen static set, rating stresses, capital-stack sizing, a sensitivity cushion, challengers and issuance economics."
summary: "Part 3 of 6: how the model selects the pool, stresses it at each rating level, sizes every class, adds a sensitivity cushion, challenges the result and checks the deal is economic to issue."
ShowToc: true
TocOpen: false
---
<!--more-->

Part 2 covered how the cash moves. This part is about which loans go in, how big each note should be, and whether the deal is worth issuing at all.

Those questions cannot be answered separately. **Credit enhancement and pool selection are one problem**: the pool sets how much enhancement the notes need, and the enhancement, with its cost, decides which loans are worth carrying. Take out the riskiest loans and Class A needs less support; take out too many and the deal is too small or earns too little to pay its costs. So the model loops through four steps until it finds a viable deal:

```
warehouse ─► select & price pool ─► create deal ─► freeze static set ─► stress & tranche ─► viable?
                 ▲                                                                            │
                 └──────────────── no: re-select pool ◄──────────────────────────────────────┘
```

The whole loop runs **as of the issue date**: the pool cut-off plus the usual time to close (80 days, the median in six public UK prime deals). Market data, criteria and deal terms are each taken in the version in force that day, so a deal priced in July 2025 never sees 2026 data. Running an old pool on today's market is still possible, but the build labels it a stale-pool stress.

The engine runs in two modes:
- **dynamic** (the default): select from the warehouse, size the enhancement, and re-select if the deal fails, until it is viable;
- **fixed** (`--fixed-pool`): size the enhancement on exactly the loans given, once. Nothing is filtered, selected or trimmed, and a failure is reported against that pool rather than fixed by changing it. That is the mode for a pool someone else has already chosen.

Which tests run inside that loop is not hard-coded. A master test list, itself an assumption file, says which stresses, sizing methods, gates and reports apply for a jurisdiction and a named run. Mandatory tests (cash conservation, the rating stresses, the optimiser) cannot be switched off, so no one can drop a test to make a deal pass. Every build records the tests it ran.

---

## 1. Selecting the pool

The warehouse (50,000 synthetic loans here) holds more loans than the deal needs. Picking the subset is a combinatorial problem; 20,000 loans give far too many possible pools to try them all.

- **Pre-filter** (`pre_filter.py`): one deterministic pass removes ineligible loans (defaulted, redeemed or repurchased, LTV above the cap, zero balance or rate) and flags concentrations (buy-to-let, interest-only, region). It also checks the pool can pay the notes before any search starts.
- **Search** (`rl_pool_selector.py`): a greedy warm start, then simulated annealing (add / remove / swap loans), rewarding the senior notes and penalising breaches of the concentration caps.
- **In the loop:** the first round takes every eligible loan. If a round fails, the next one searches again with the failure as a penalty: the loans with the highest expected loss after a credit failure, the lowest-yielding after a spread failure.
- **Whole groups only:** loans on the same property or to the same borrower stay together, in or out. A reviewer can also reject loans one by one before the build.

The sample pool is a **seasoned UK prime** pool:
- 5,366 owner-occupied loans, £999.8m, 6 to 84 months old (31 on average);
- 91% of the balance still in a fixed-rate period;
- 0.1% with past adverse credit;
- a regional mix with about a fifth in London and a fifth in the South East.

LTV, loan-to-income and purpose mix are calibrated to BoE MLAR lending data.

---

## 2. Freezing the static set

Before stressing anything, the pool is frozen: the cut-off balances, each loan's calculated credit score and segment, and its PD and LGD inputs. Within a stress run every tranche is treated as issued and fixed; tranches are fixed for good only at issue.

---

## 3. Stressing it

The model uses one **generic calculated credit model**, built from public rating methodology concepts rather than any one agency's:

- a credit score per loan → a pool PD → a rating-level default rate (a Vasicek model, at the default probability a rating allows over the pool's life);
- times loss severity per loan (house-price falls, forced-sale discount, costs, with floors);
- giving **credit coverage**: the stressed loss each rating level must survive. For the sample pool, AAA coverage is 19.3% defaults × 34.1% severity = 6.6% of the pool.

Some loans need more than the published scoring captures. Loans already in arrears at cut-off start closer to default (three times the hazard). Flats and homes worth over £1m fall further in a downturn (10% and 15% more). Regional add-ons, a remortgage effect and a seasoning credit are in place but neutral until calibrated. Each of these is labelled an estimate.

The originator score matters most. It is a judgement from the operational review, on a 1–10 scale where 1–3 is a high-street prime lender. The sample pool is prime, so it is set at 2. An earlier version left it at 5 (a near-prime lender), which nearly doubled the expected PD.

Each rating is run through the monthly waterfall under 16 scenarios: defaults front- or back-loaded × four prepayment speeds × Bank Rate up or down.

---

## 4. Sizing the stack

Every class, including Class Z, is sized from the stresses. Each class's attachment is searched by bisection: the lowest level where it takes no loss in any of its rating's scenarios, down to a floor (Class Z must at least fund the reserve and the day-1 costs). For the sample deal, Class A survives every AAA scenario at **7.0%**: that is the stress-test level.

Classes follow the convention of issued UK notes: lettered from the most senior, each one rating category below the class above, with an unrated first-loss Class Z. Ratings are shown as, for example, AAA(sf). Three stacks are built in: prime master trust (A + Z, the default), sequential (A to D + Z) and full sequential (A to F + Z).

A sensitivity cushion is added for the estimated parameters (the originator score, the payment shock when a fixed rate ends, the score calibration and the size of the rate stress). Each is moved to its adverse value and the attachment re-solved, and the rises are combined by root-sum-square: **+2.66pp**, so Class A attaches at **9.7%**. With the 1.5% reserve its enhancement is **11.2%**, 1.70 times its AAA stressed loss.

Challengers report beside the result and never loosen it: break-even defaults (30.9% of the pool, 1.60 times the AAA rate), an EL-based view (2.0%), the implied chance of loss (about 0.8bp against 20bp for AAA), a swap that ends at month 12 (Class A would need 9.8%) and a joint move of every estimate (passes). The build then compares its terms with public UK prime deals issued by the same date.

**[Part 5](/blog/comp-science/securitisation-101-part-5/) covers the credit enhancement engine step by step**: the credit model, the scenario grid, the waterfall, bisection, the cushion, the reserve and swap design, and the comparison with the market.

### Prepayment

UK borrowers rarely repay inside their fixed rate, because early repayment charges apply, and then most remortgage within a few months of it ending. The model prepays loan by loan on that pattern: low while the charge applies, a spike after the fix ends, then a rate driven by each loan's age and its incentive against current mortgage rates. The sample pool prepays at about 24% a year over five years (13.5% at half speed, 35.8% at 1.75 times).

| Prepayment | Class A WAL (to call / maturity) | Class Z yield to call |
|---|---|---|
| Slow (half speed) | 3.1 / 5.7 years | 3.1% |
| Base | 2.3 / 2.8 years | 3.1% |
| Fast (×1.75) | 1.8 / 1.8 years | 3.1% |

Slow prepayment extends the senior notes. Class Z's yield barely moves: it pays the index flat, and the originator's return is the residual rather than a Class Z coupon. Without the call, Class A is repaid by month 177 instead of 61.

### Is it worth issuing?

The swap is struck at the market rate on the issue date: the OIS par rate for its notional schedule, 3.648% against a 4.25% Bank Rate on 19 July 2025. The loans' fixed rates, though, were locked when they went into the warehouse. If rates rise in between, the swap costs more while the loans pay the same. The sample deal earns 83bp of excess spread after the swap and can absorb a **1.0pp** rise before it is uneconomic. If a 1pp rise did happen before issue, the stress-test attachment would rise to 7.3%, still inside the 9.7% Class A has.

A bigger move is an **issuance failure**: the deal is not issued at those terms. The model does not force a fix. It stops and flags it for manual assessment: reprice, hold the loans in the warehouse, or re-select the pool. Priced on today's market (a 2-year swap rate about 1pp higher), the same April 2025 pool would be one: excess spread after the swap would be about £1.0m a year negative.

On a prime pool, the first-loss note is retained by the issuer at the index flat, as in public prime deals.

---

### Securitisation 101 series

**Previous:** [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/) · **Next:** [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. Part 3: Building the Deal (this post)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
5. [Part 5: Credit Enhancement, Mechanism and Design](/blog/comp-science/securitisation-101-part-5/)
6. [Part 6: The Bank of England Data Tape](/blog/comp-science/securitisation-101-part-6/)
