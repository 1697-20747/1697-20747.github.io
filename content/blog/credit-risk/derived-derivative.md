---
title: "Derived Derivative"
date: 2026-07-17T09:00:00Z
draft: false
categories: ["credit-risk"]
tags: ["derivatives", "interest-rate-swaps", "PFE", "counterparty-risk", "litigation"]
description: "A Spanish SPV hedged a €1.575bn acquisition loan with stepped 15-year swaps on 12 September 2008 — three days before Lehman collapsed. By 2014 the swaps had produced termination liabilities of roughly €710 million, a scale of move that no pre-crisis PFE or EE model would have flagged as anything but a tail scenario."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

*Marme Inversiones 2007 SL v NatWest Markets Plc and Others* [2019] EWHC 366 (Comm) is the substantive trial judgment behind a jurisdictional skirmish decided three years earlier ([2016] EWHC 1570 (Comm)). Picken J's 2019 judgment is where the real facts live: a Spanish SPV bought Santander's Madrid headquarters in September 2008, hedged the acquisition debt with stepped interest rate swaps three days before Lehman Brothers filed for bankruptcy, and by the time the banks terminated those swaps in November 2014, Marme owed them roughly €710 million.

The case itself is a misrepresentation claim — Marme argued the swaps should be rescinded because RBS had implicitly represented EURIBOR wasn't being manipulated, tied to trader Philippe Moryoussef's later conviction for EURIBOR rigging. Marme lost. Picken J dismissed the claim, the swaps stood, and the termination liabilities stayed on the table. That legal outcome isn't the interesting part for a credit risk post, though — the interesting part is a question the judgment doesn't ask but its own facts answer: what did this hedge look like on day one, and how far did reality diverge from it?

---

## The Deal

Marme Inversiones 2007 SL was incorporated in Spain in November 2007 to buy Ciudad Financiera — Banco Santander's global headquarters complex — under a sale-and-leaseback agreement signed 25 January 2008. Purchase price: €1.9 billion, with Santander leasing the complex back for 40 years at a starting rent of €74.08 million a year (later increased to €82.69 million), subject to annual review.

Completion was repeatedly delayed as financing dragged through the deepening 2008 credit crunch — originally scheduled for 31 March 2008, it slipped six times before finally closing on **12 September 2008**, at a total cost of around €2 billion. Lehman Brothers filed for bankruptcy three days later, on 15 September.

The acquisition was funded by a five-year, €1.575 billion senior loan from a syndicate of eight banks, priced at EURIBOR + 1.6%:

| Lender | Commitment |
|---|---|
| RBS | €366,000,000 |
| HSH Nordbank | €309,000,000 |
| Deutsche Postbank | €200,000,000 |
| Caixa (`la Caixa`) | €200,000,000 |
| Raiffeisen Zentralbank Österreich | €200,000,000 |
| Bayerische Landesbank | €150,000,000 |
| ING Real Estate Finance | €75,000,000 |
| ING Bank NV | €75,000,000 |

The loan agreement required Marme to maintain hedging arrangements with a notional principal at least equal to the outstanding loan balance. Five of the eight lenders — RBS, HSH, Bayern, ING and Caixa — became the actual swap counterparties, between them covering the full €1.575 billion notional.

---

## The Actual Swap Terms

This is where the structure gets interesting, and where my earlier read of this case (based only on the 2016 jurisdictional ruling) was too simple. These weren't plain-vanilla fixed-for-floating swaps.

The five swaps, executed on the morning of 12 September 2008 under standard ISDA Master Agreements, were **stepped** EURIBOR-to-fixed swaps: Marme paid a fixed rate that started low and rose on a pre-agreed annual schedule, in exchange for receiving 3-month EURIBOR. The fixed leg started at **3.3030%** and stepped up annually to a final rate of **6.7635%** by the end of the swap term in August 2023 — a roughly 15-year tenor against a 5-year loan.

A stepped structure like this is usually there to solve an affordability problem: it keeps early debt service low enough to clear a covenant (Marme's Senior Loan carried a minimum Interest Cover Ratio of 105%) on the assumption that rental income and/or rates would grow into the higher steps later. It is, in effect, a bet that the cost of the hedge can be deferred into a future that looks like a continuation of the present. In September 2008, "the present" was EURIBOR sitting comfortably above 4%. Within a year, it wasn't.

---

## What Actually Happened

EURIBOR collapsed through 2008–2009 as the ECB slashed rates in response to the financial crisis, stayed low through the European sovereign debt crisis, and went negative by 2015. Marme's fixed leg, meanwhile, was doing the opposite — stepping up every year, exactly as scheduled, regardless of what was happening to the rate it was meant to offset.

The two curves moving in opposite directions is the entire loss mechanism. A swap that started at a manageable 3.3% fixed cost against a still-buoyant EURIBOR turned, within a year or two, into a fixed cost climbing toward 6.76% against a floating leg approaching zero. Marme defaulted on the underlying senior loan at its 12 September 2013 maturity, entered Spanish insolvency proceedings on 4 March 2014, and stopped paying under the swaps from May 2014.

Between November and December 2014, the banks terminated their swaps and issued statements of the sums due:

| Counterparty | Termination amount |
|---|---|
| RBS | €223,721,576.00 |
| HSH Nordbank | €199,249,545.25 |
| Bayerische Landesbank | €129,049,794.94 |
| Caixa | €91,375,814.79 |
| ING | €67,294,554.15 |
| **Total** | **≈€710,691,285** |

Call it roughly 45% of original loan notional, plus default interest, generated by an instrument whose entire purpose was to protect Marme from rate volatility.

---

## What Are EE and PFE?

Two terms are doing a lot of work in this post, so it's worth being precise about what they mean before using them.

When a bank enters a derivative — a swap, in this case — with a counterparty, it's exposed to that counterparty's credit risk for the life of the trade. If Marme defaults while the swap has a positive value *to the bank* (i.e. Marme owes the bank money to unwind it), the bank stands to lose whatever that value is. If the swap has a negative value to the bank at the point of default, the bank generally loses nothing from the derivative itself — it just loses a hedge it now has to replace. So counterparty credit exposure on a swap is not the notional, and it's not fixed — it's the *positive* mark-to-market, and it changes every day as rates move.

Because nobody knows in advance what rates will do, banks don't model a single number. They model a distribution of possible future exposures, usually by simulating thousands of possible rate paths from trade date to maturity and revaluing the swap along each one. Two summary statistics get pulled out of that distribution at each future date:

- **Expected Exposure (EE)** — the *average* positive exposure across all simulated paths at a given future date. This is the number that feeds into everyday capital and pricing calculations (it's the building block of CVA — credit valuation adjustment).
- **Potential Future Exposure (PFE)** — a *high percentile* (typically 95th or 99th) of exposure across the same simulated paths. This is the "how bad could this plausibly get" number, used for setting counterparty credit limits.

Both are forward-looking distributions built at trade inception, calibrated to how volatile the underlying rate has historically been. Neither is a prediction of what will happen — they're a description of the range of what's *statistically plausible*, given the model's assumptions about volatility and mean reversion. That last part matters enormously, because it means EE and PFE are only ever as good as the assumption that the future will look statistically like the past used to calibrate them.

---

## Calculating EE and PFE at Execution

No pre-crisis PFE or EE model from any of the five banks has been published, so what follows is a reconstruction — built from scratch, using only information available on 12 September 2008 — of what a competent desk's exposure model would plausibly have produced. It is not a claim about the banks' actual figures, but the methodology is a standard one and the inputs are the real ones from the judgment.

**The model.** 3-month EURIBOR is simulated as a Vasicek short-rate process — a common, simple choice for this kind of illustration — mean-reverting toward a long-run level, calibrated as follows:

- Starting rate: 4.96% (actual 3M EURIBOR in early September 2008)
- Long-run mean: 4.5% (broadly where EURIBOR had sat for the preceding several years)
- Annual volatility: 110bp (consistent with realised EUR short-rate volatility pre-crisis)
- Mean-reversion speed: a moderate pull back toward the long-run level over several years

At each future date, the swap is revalued: Marme's stepped fixed leg (3.3030% rising to 6.7635%) against the simulated floating leg, on the full €1.575 billion notional, discounted back to present value. Because the model is linear in the simulated rate, the exposure at each date is itself normally distributed, which makes EE and PFE at every point on the curve calculable in closed form rather than needing a full path-by-path simulation.

{{< rawhtml >}}
<script>
window.addEventListener('message', function(e) {
  if (e.data && e.data.iframeHeight) {
    var iframes = document.querySelectorAll('iframe');
    for (var i = 0; i < iframes.length; i++) {
      try {
        if (iframes[i].contentWindow === e.source) {
          iframes[i].style.height = (e.data.iframeHeight + 4) + 'px';
          break;
        }
      } catch(x) {}
    }
  }
});
</script>
<iframe src="/html/marme-swap-pfe-chart.html" width="100%" height="200" style="border:none; background:#0f1117;" scrolling="no"></iframe>
{{< /rawhtml >}}

**The result.** Expected Exposure peaks at around **€152 million** (year 7), reflecting the modest average positive value the swap was expected to accumulate for the banks as the fixed leg stepped up over time. The 99th percentile PFE peaks higher and earlier, at around **€526 million** (year 4) — the "one-in-a-hundred" scenario a 2008-vintage model would have flagged as the worst plausible outcome across the swap's entire 15-year life.

The actual termination liability in November 2014 — roughly **€710.7 million**, six years into the trade — exceeds not just the modelled EE and PFE *at that point in the swap's life*, but the single highest PFE the model produces at *any* point across the full 15 years. There is no percentile on this curve, at any tenor, that the actual outcome sits inside.

---

## How Rare Was €710.7 Million?

Saying the actual outcome exceeded PFE99 tells you it was outside the 99th percentile — but not by how much. It's worth reverse-engineering the actual number back into the model's own terms: what percentile does €710.7 million correspond to, how many standard deviations is that, and what does a move of that size imply about how often you'd expect to see one?

At t = 6.15 years (the point of termination), the modelled exposure distribution has a mean of €137.7 million and a standard deviation of €155.6 million. Plugging in the actual €710.7 million:

```
z = (710.7 − 137.7) / 155.6 ≈ 3.68 standard deviations
```

A 3.68-sigma move on a normal distribution sits at roughly the **99.9885th percentile** — a tail (upper-side) probability of about **0.0115%**, or **1 in 8,657**.

That's the number worth sitting with. Not "outside the 99th percentile" — outside the 99.99th. The model's own 99th percentile PFE (€526 million, at its peak) was already the single most extreme number it produced across the swap's entire 15-year life. The actual outcome clears that bar by roughly 35%, and sits nearly a full extra order of magnitude further out in probability terms — 1-in-100 versus 1-in-8,657.

**Turning that into a timeframe.** If you treat the 1-in-8,657 tail probability the way market commentators loosely treat sigma events after the fact — as if it were a per-day draw probability — then a 1-in-8,657 event should turn up, on average, only once every **8,657 days**, or about **23.7 years**. Marme's swaps needed roughly **2,246 days** — about 6.15 years — to produce it. On this framing, the actual outcome arrived nearly four times faster than the model's own tail would suggest it should.

This is the same loose device Goldman Sachs' then-CFO David Viniar reached for in August 2007, telling the *Financial Times* that the bank was "seeing things that were 25-standard deviation moves, several days in a row" as two of its hedge funds lost a quarter of their value in a week. It's not a rigorous return-period calculation — the underlying quantity is a single point-in-time percentile of a distribution built once at trade inception, not a repeatable daily draw, so treating 1/p as a day-count is a deliberately crude device rather than a statistically defensible one. But it's the same crude device the market itself reaches for whenever it wants to convey just how far outside "plausible" an outcome turned out to be. By that yardstick, this one was a long way outside — nowhere near Viniar's 25 sigma, but a genuine multi-sigma miss all the same.

---

## Was the Model Wrong, or Was the World Different?

A 3.68-sigma outcome raises an obvious question: was the volatility assumption simply too low, and if so, by how much? And does an outcome this rare mean the actual post-2008 rate distribution just wasn't normal?

**The volatility question first, because it has a clean answer.** Because modelled exposure is linear in the simulated rate, it's straightforward to solve backward: what annual volatility would the model have needed to assume for €710.7 million to land on a specific percentile, instead of deep in the tail?

| Target percentile | Required annual vol | vs. the 110bp modelled |
|---|---|---|
| 99th | 174bp | 1.58× |
| 99.9th | 131bp | 1.19× |
| 95th | 246bp | 2.24× |

To make €710.7 million an unremarkable 99th-percentile event, the model would have needed to assume EURIBOR volatility of 174bp a year rather than 110bp — a 58% understatement. To reduce it all the way to a 95th-percentile event, volatility would need to be assumed at 246bp a year, more than double what was modelled and closer to equity-crisis-era volatility than anything seen in EUR short rates before 2008. Neither figure is a plausible input for a pre-crisis desk to have used. Under-calibration alone doesn't close a gap this size.

**The normality question is more interesting, and the answer is more specific than a flat yes or no.** A single 3.68-sigma draw doesn't, by itself, disprove that the underlying process was normal — 1-in-8,657 still means the outcome was *possible* under the model, just very unlikely. One data point is weak evidence against a distribution. So it's worth checking whether a fatter-tailed distribution — the standard fix when Gaussian models understate real-world extremes — would rescue this one:

| Distribution | Tail probability of an equivalent move | Rarity |
|---|---|---|
| Normal | 0.0115% | 1-in-8,657 |
| Student-t, 30 df | 0.032% | 1-in-3,131 |
| Student-t, 15 df | 0.063% | 1-in-1,576 |
| Student-t, 8 df | 0.140% | 1-in-717 |
| Student-t, 5 df | 0.254% | 1-in-393 |
| Student-t, 4 df | 0.324% | 1-in-309 |
| Student-t, 3 df | 0.390% | 1-in-256 |

Even an aggressively fat-tailed Student-t with 3 degrees of freedom — well beyond what's typically used for interest rate models, and fatter than most equity return models — only brings the rarity down to about 1-in-256. A more defensible fat-tail assumption for short rates (8–15 degrees of freedom) still leaves the outcome at 1-in-700 to 1-in-1,600. Fatter tails help, but nowhere near enough to make €710.7 million look like a normal feature of the distribution rather than an outlier.

This isn't a new complaint. Benoit Mandelbrot spent much of his career, starting with a 1963 study of cotton prices, building the empirical case that financial markets simply don't move the way Gaussian models assume — that price changes cluster into calm and turbulent periods rather than arriving as steady, independent increments, and that the tails of real market distributions are far fatter than a normal curve predicts. His argument, laid out at length in *The (Mis)Behavior of Markets* (2004, with Richard L. Hudson), was that finance had borrowed a mathematics of smooth, well-behaved randomness to describe a phenomenon that is neither smooth nor well-behaved — and that the gap between the two shows up, reliably, as exactly this kind of "impossible" outcome. None of that argument depended on 2008 happening — it's a criticism of the modelling framework itself, made decades before this swap was priced.

**So what actually broke.** Not the shape of the distribution — the assumption that there was a single, fixed distribution to begin with. A Vasicek process assumes the short rate reverts, indefinitely, toward the same long-run mean with the same volatility: a *stationary* process you can validly sample from at any point over the swap's 15-year life. What happened from late 2008 onward wasn't an extreme draw from that process. It was the process being replaced. The ECB didn't let EURIBOR wander into a low-tail outcome; it deliberately pinned policy rates near zero for years, as an act of policy, then held them there through a second crisis. That's a **regime change**, not a tail event — the parameters governing the process shifted after inception, rather than an unlikely value being drawn from the original, unchanged process.

Nassim Nicholas Taleb makes essentially this distinction in *The Black Swan* (2007), and puts it more sharply than a risk model can: "history does not crawl, it jumps." A stationary stochastic process, however carefully calibrated, describes crawling — small, continuous, mean-reverting wobbles around a stable centre. What actually moved EURIBOR from 5% to zero wasn't a long walk along that kind of path; it was a jump to a different one, imposed from outside the model by policymakers responding to a crisis the model had no term for.

The distinction matters because it identifies which fix doesn't work. A fatter-tailed distribution still assumes one time-invariant process governing the whole horizon; it just spreads more probability into the extremes of that single process. It doesn't capture a scenario where the *mean itself* moves and stays moved for a decade. That needs a regime-switching or structural-break model, not a fatter tail bolted onto the same stationary assumption. Which, in plainer terms, is just the earlier point again from a different angle: the model was built to answer a volatility question, and the crisis asked a different one — what happens when the policy regime itself changes — that no fixed-parameter distribution, however fat-tailed, is built to answer.

---

## The Valuation Gap

There's a second, quieter data point on valuation in the same judgment, distinct from anything a PFE model would capture. In its damages claim (pursued as an alternative to rescission), Marme argued that had it known about the EURIBOR conduct issues, it would have negotiated differently — either avoiding the swaps altogether via a payment-in-kind loan structure (Marme's counterfactual: **€996 million** better off) or negotiating a 50bp discount across the transaction including 10bp off the swaps (**€29.5 million** better off). Those two counterfactuals sit almost forty times apart, which says something on its own: Marme's own litigated position implies that removing the swap structure entirely was worth roughly thirty-four times more than a modest pricing concession on it. Whatever else is disputed in this case, both sides agree the swaps — not the loan, not the price paid for the building — were where the money was lost.

---

## The Credit Lesson

None of this makes the swaps a mis-sale by itself. Hedging floating-rate debt with a pay-fixed instrument is standard practice, and the court ultimately rejected Marme's argument that it had been misled into the trade. But the structure itself deserves scrutiny independent of the misrepresentation claim: a 15-year hedge against a 5-year loan, with a fixed rate deliberately stepped up over time to make an interest cover covenant work in year one, struck three days before the largest financial crisis in a generation.

Stepped structures defer cost by design. That's the whole point of them — they trade a manageable number today for a larger number tomorrow, on the assumption that tomorrow looks enough like today for the plan to hold. When tomorrow instead looks like a decade of near-zero rates, the deferred cost doesn't shrink to meet reality. It just arrives late, on schedule, exactly as contracted — which is what a fixed leg is supposed to do, and precisely why deferring the pain of a hedge into an uncertain future is a risk decision, not a pricing detail.

---

## Key Facts

| Item | Detail |
|---|---|
| Asset | Ciudad Financiera, Madrid (Santander HQ) |
| Purchase price | €1.9 billion |
| Total completion cost | ~€2.0 billion |
| Senior loan | €1.575 billion, 5-year term, EURIBOR + 1.6%, 8-bank syndicate |
| Swap counterparties | RBS, HSH Nordbank, BayernLB, ING, Caixa |
| Swap structure | Marme pays stepped fixed / receives 3M EURIBOR |
| Fixed rate | 3.3030% → 6.7635% (annual step-up) |
| Swap tenor | ~15 years (to August 2023) |
| Trade date | 12 September 2008 |
| Lehman bankruptcy | 15 September 2008 (3 days later) |
| Marme loan default | 12 September 2013 |
| Marme insolvency (concurso) | 4 March 2014 |
| Swap termination | November–December 2014 |
| Termination liability | ≈€710.7 million + default interest |
| Modelled EE at execution (peak) | ≈€152 million (year 7) |
| Modelled 99th percentile PFE at execution (peak) | ≈€526 million (year 4) |
| Actual outcome expressed as z-score (t=6.15y) | ≈3.68 standard deviations |
| Actual outcome as implied percentile | ≈99.9885th (≈1-in-8,657) |
| Implied vol needed for actual = 99th pctile | 174bp/yr (1.58× modelled) |
| Actual vs peak modelled PFE 99th | actual exceeds peak PFE 99th by ~35% |
| Marme's damages counterfactuals | €996m (PIK structure) / €29.5m (swap discount) |
| Trial outcome (2019) | Marme's misrepresentation/rescission claims dismissed |

---

## References

- [Marme Inversiones 2007 SL v NatWest Markets Plc & Ors [2019] EWHC 366 (Comm)](https://caselaw.nationalarchives.gov.uk/ewhc/comm/2019/366) — The National Archives, Find Case Law. Primary source for all deal, loan syndicate, swap, termination and damages-counterfactual figures.
- [Marme Inversiones 2007 SL v Royal Bank of Scotland plc and Others [2016] EWHC 1570 (Comm)](https://www.judiciary.uk/wp-content/uploads/2016/06/marme-v-rbs-and-others-20160629.pdf) — the earlier jurisdictional ruling referenced in the Overview.
- [Historical Euribor rates by year — euribor-rates.eu](https://www.euribor-rates.eu/en/euribor-rates-by-year/) — source for the 3-month EURIBOR levels used to calibrate the model's starting rate (September 2008) and to describe the rate's path to zero and negative territory through 2015.
- [David Viniar, Wikipedia](https://en.wikipedia.org/wiki/David_Viniar) — for the "25 standard deviation moves" quote, originally reported in the *Financial Times*, 13 August 2007.
- Nassim Nicholas Taleb, *The Black Swan: The Impact of the Highly Improbable* (Random House, 2007) — for the "history does not crawl, it jumps" quote.
- Benoit Mandelbrot and Richard L. Hudson, *The (Mis)Behavior of Markets: A Fractal View of Financial Turbulence* (Basic Books, 2004).

*Methodology note: the EE/PFE modelling in this post (Vasicek short-rate simulation, closed-form exposure percentiles, and the Student-t sensitivity check) is my own construction for this piece, built on the disclosed swap terms above — not a reproduction of any bank's internal model, which has never been published.*
