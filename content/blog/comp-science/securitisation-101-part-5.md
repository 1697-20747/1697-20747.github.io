---
title: "Securitisation 101 — Part 5: Credit Enhancement, Mechanism and Design"
date: 2026-11-01T09:00:00Z
lastmod: 2026-11-01
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "credit enhancement", "credit risk", "python"]
series: ["Securitisation 101"]
description: "How the model sizes credit enhancement: the credit model, the scenario grid, the cash-flow waterfall, bisection, the sensitivity cushion, the swap and reserve design, and the checks against public deals."
summary: "Part 5 of 6: the credit enhancement engine step by step, the design choices behind each layer, and how the result compares with recent public UK prime deals."
ShowToc: true
TocOpen: false
cover:
  image: "images/comp-science/ce_engine_process.svg"
  alt: "Credit enhancement calculation engine: inputs, credit model, scenarios, waterfall, bisection, cushion, checks"
  caption: "The credit enhancement engine, with the sample deal's figures"
---
<!--more-->

Part 3 showed where the senior note's size comes out of the build. This part opens up the engine that produces it: what credit enhancement is made of, how each layer is sized, and why the design is what it is.

**Credit enhancement** cannot be separated from the pool it supports. Every loan in the pool changes the enhancement the notes need, and the enhancement decides which loans are worth carrying. In the dynamic mode the engine below sits inside the pool-selection loop: a failed round re-selects the pool and sizes again. In the fixed mode it runs once on a pool already chosen, and reports whether that pool works as it stands.

**Credit enhancement** is everything that stands between a note and a loss: the interest the loans earn above what the deal pays out (excess spread), the cash reserve, and every note below it (subordination). The question the engine answers is how much of that each class needs to survive its rating's stresses without losing a penny.

---

## The engine

![Credit enhancement calculation engine](/images/comp-science/ce_engine_process.svg)

The figures in brackets are from the sample deal: 5,366 loans, £999.8m, selected from a 50,000-loan warehouse, priced on 19 July 2025.

### Inputs, as of the issue date

Every input is a dated data set, and the build takes each one as it stood on the issue date:
- **market data:** the Bank of England OIS curve, Bank Rate, the SONIA–Bank Rate basis, Class A margins and deal terms from public UK prime issues;
- **the static set:** the pool frozen at cut-off, with each loan's score, segment and loss inputs;
- **parameters:** some are published in rating methodologies (house-price falls, forced-sale discounts, costs, asset correlation), some are the model's own estimates (the originator score, the payment shock when a fixed rate ends, the score calibration, the size of the rate stress).

The issue date is not today. It is the pool cut-off plus the time a deal usually takes to close: 80 days, the median in six public UK prime deals. A build on today's market with an old pool is still possible, but it is labelled a **stale-pool stress**, because no deal could issue that way.

### 1. Credit model: the loss to survive

Per rating level, a **generic calculated credit model** turns the pool into a stressed loss:
- each loan's credit score gives a pool PD;
- a Vasicek model turns that into the default rate a rating must withstand (the default probability the rating allows over the pool's life);
- each loan's severity comes from the market value decline, the forced-sale discount, costs and floors.

For AAA on the sample pool: **19.3% defaults × 34.1% severity = 6.6% of the pool**. That is the credit coverage. It is a static number, though, and a deal does not lose its money all at once.

### 2. Scenario grid: when and how the loss arrives

Each rating is run through 16 deterministic scenarios:
- defaults front-loaded or back-loaded;
- prepayment at 0%, 5%, 10% or 20% a year;
- Bank Rate stressed up or down.

The stressed Bank Rate moves the variable-rate loans, the swap and the notes. **Fixed loan rates never reprice**: a borrower on a five-year fix pays the same rate whatever happens to Bank Rate, and the model never pretends otherwise.

### 3. The waterfall: where enhancement is actually used

Every scenario runs loan by loan, month by month, through the full revenue and principal priorities of payments (Part 2), for a candidate set of note sizes. This is where the three layers of enhancement do their work, in order:
1. **Excess spread** absorbs losses first, every month, by curing the principal deficiency ledgers.
2. **The reserve** covers senior shortfalls when revenue falls short.
3. **Subordination** takes what is left: losses are written off from the bottom class up.

Sources equal uses in every month of every scenario. A deal that only works because cash appeared from nowhere would fail that check.

### 4. Bisection: the smallest class that survives

Each class's attachment (the share of the pool below it) is searched by bisection: the lowest level where the class takes no loss in any of its rating's 16 scenarios. There is one floor: Class Z must at least fund the reserve and the day-1 costs.

For the sample deal, Class A survives every AAA scenario at **7.0%**. That is the stress-test attachment. The scenario that binds is front-loaded defaults with 20% prepayment and Bank Rate rising.

### 5. The sensitivity cushion

The stress test assumes the central assumptions are right. The cushion allows for them being wrong, but only where the model has had to estimate. Published parameters are already in the stresses, so they are not cushioned twice. Each estimate is moved to its adverse value and the attachment is **re-solved**:

| Estimate (adverse side) | Class A attachment rises by |
|---|---|
| Originator score (+2 points) | 1.7pp |
| Payment shock when a fixed rate ends | 1.5pp |
| Score calibration (+8 points) | 1.2pp |
| Size of the rate stress (+25%) | 0.7pp |
| LGD score weight | 0.1pp |

Combined by root-sum-square, the cushion is **2.66pp**, so Class A attaches at **9.7%**. With the 1.5% reserve, its enhancement is **11.2%**, 1.70 times its AAA credit coverage.

Moving all five estimates together, each by 1/√5 of its shock, is the joint check; the cushioned structure passes it. All five at full size at once is the reverse stress: Class A would then need 13.6%. That is reported, never required.

---

## Design choices

### Why size on scenarios, not on one number

Credit coverage says how much the pool loses. It does not say whether the deal can carry that loss, which depends on when defaults come, how fast the good loans prepay (taking their excess spread with them), and what rates do to the swap and the notes. The cash-flow scenarios answer that. The static coverage is reported beside them as a cross-check.

### Why the cushion covers estimates only

A cushion on everything would count the published parameters twice. A cushion on nothing would treat a guess the same as a published figure. Here the cushion is driven by the four estimates no methodology publishes, which is also where real data would help most.

### The reserve: sized at closing, then amortising

The reserve starts at 1.5% of the pool, inside the 1.37–2.0% of recent standalone prime deals. It then amortises with the rated notes, at its closing ratio, as long as arrears and losses stay low (90+ day arrears under 3%, cumulative losses under 1%, no shortfall on the senior class). If a condition fails, it stops amortising and holds its level. That follows the public deals. A fixed reserve would have been more generous to the notes than the market is.

The reserve is funded by Class Z, the retained first-loss note. When reserve cash is released, it first repays Class Z for the reserve it funded, ahead of any residual to the originator. Public deals do the same with the subordinated loan that funds their reserve.

### The swap: hedging duration, not copying a schedule

The fixed-rate loans pay a fixed coupon until their fix ends, while the notes pay floating. One pay-fixed amortising swap hedges that, designed from first principles:
- its notional schedule, fixed at issue, is the **expected fixed-rate balance**: scheduled repayments plus the engine's own prepayment, which does not depend on rates while early repayment charges apply;
- so its rate sensitivity matches the exposure's month by month in the base case;
- it is struck at the OIS par rate for that schedule (3.648% here, against a 4.25% Bank Rate).

Prepayment away from the base case leaves it over- or under-hedged. The model reports a hedge ratio, the swap's rate sensitivity over the exposure's: 0.97 at half-speed prepayment, 1.00 at base, 1.04 at 1.75 times.

The alternative, a notional that tracks the actual fixed balance, is what the public prime deals use. The worst AAA cases show the difference, measured as Class Z's loss as a share of the pool:

| Worst AAA case | Scheduled swap | Tracking notional |
|---|---|---|
| Bank Rate up | 4.07% | 5.80% |
| Bank Rate down | 4.05% | 3.31% |

With the schedule, the up and down cases come out almost equal. In the stresses, defaults and fast prepayment leave the deal over-hedged, which earns when rates rise and costs about as much when they fall. The tracking notional is lopsided: it removes the down-case cost but leaves the up case 2.5pp worse.

One exclusion matters: **swap termination payments for mark-to-market differences are excluded from the stress analysis.** If the swap ends early, it simply stops, and neither side pays a break cost. A separate stress ends the swap at month 12 with no replacement; Class A would then need 9.8%.

### Class Z: the first-loss note, index flat

Class Z is retained by the originator and pays the index flat: no margin. That is how the retained first-loss notes in three public prime deals are priced. The originator's return is the residual, not a coupon on Class Z. An earlier version paid a 500bp margin, a placeholder that matched neither prime practice nor the roughly 800bp a sold specialist Class Z pays. The margin made no difference to the rated notes, because Class Z interest ranks below all of them. It only split the originator's return between Class Z and the residual.

---

## Challenging the number

The sizing rule is strict: no loss in any deterministic scenario. Several challengers report beside it, and none of them can loosen it:
- **Break-even.** On its worst scenario, Class A first loses when defaults reach 30.9% of the pool (1.60 times the AAA rate), or the market value decline reaches 49.2% (1.59 times).
- **EL view.** Sizing to a target expected loss instead would give Class A only 2.0%. A thick senior class loses so little when it loses at all that an EL target barely binds.
- **Implied chance of loss.** On the pool's own loss distribution, the chance that Class A takes any loss is about 0.8bp, against about 20bp allowed for AAA.
- **Stress-to-expected ratio.** The AAA loss is 21 times the base-case expected loss, well above the 5–10 times seen in public criteria. That says the base-case default model is a placeholder: too benign, not too harsh.
- **Monte Carlo.** A correlated simulation with importance sampling exists, but it is off in the standard run. It cannot bite until the behavioural model is calibrated to real performance.
- **Rate move before issue.** If Bank Rate rose 1pp between the warehouse and issue, the stress-test attachment would rise to 7.3%, still inside the 9.7% Class A has.

---

## Against the market

The build checks its own terms against public UK prime deals issued on or before its issue date. It flags anything outside the observed range, without failing the build. Like for like, the comparison has to be against the pool, not the notes: here Class Z also funds the reserve and costs, while in the public deals a separate subordinated loan does.

| Term | Sample deal | Public prime deals |
|---|---|---|
| Class A share of the pool | 92.0% | 91.4–92.0% |
| Enhancement at closing (subordination + reserve) | 9.5% | 10.0% |
| Reserve at closing | 1.5% of the pool | 1.37–2.0% |
| Step-up | 2.0 times the margin at month 60 | 2.0 times at 58–60 months |
| Class Z margin | index flat | index flat |

The sample deal comes out slightly **thinner** than the market, not thicker: 9.5% enhancement against 10.0%. That is the kind of gap a rating agency would ask about. The sensitivity cushion is the first place to look, along with the placeholder default model behind it. Replicating a published agency approach is the next step on the roadmap.

On a specialist deal the terms differ: margins step up 1.5 times rather than twice, payments are monthly, costs are funded by excess-spread notes, there is no general reserve, and the originator retains a vertical slice. The engine compares a build only with deals of its own sector.

---

### Securitisation 101 series

**Previous:** [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/) · **Next:** [Part 6: The Bank of England Data Tape](/blog/comp-science/securitisation-101-part-6/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
5. Part 5: Credit Enhancement, Mechanism and Design (this post)
6. [Part 6: The Bank of England Data Tape](/blog/comp-science/securitisation-101-part-6/)
