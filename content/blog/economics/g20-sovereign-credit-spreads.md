---
title: "G20 Sovereign Credit Spreads vs Debt/GDP — Historical Analysis 1970–2023"
date: 2026-05-03
draft: false
categories: ["economics"]
tags: ["sovereign-credit", "debt", "spreads", "G20", "interest-rates"]
description: "Does higher government debt reliably predict higher borrowing costs? 54 years of data across 19 countries says: it depends entirely on who you are."
showToc: true
tocopen: false
---

## Overview

May, 2026. The UK 10 yr Gilt yields have topped 5.00% for the first time since 2008. Now, this is an absolute measure, and therefore a flawed measure in many ways. But democracy still lives on, at least in debt capital markets. The bond Vigilante are voting. And for for the present incumbent Labour government fiscal policies, or IRL lack thereof.

The conventional assumption is straightforward: more debt means higher borrowing costs. The data across G20 countries from 1970 to 2023 tells a more complicated story. The aggregate Pearson correlation between Debt/GDP and sovereign credit spreads is **−0.050** — statistically indistinguishable from zero. R² = 0.0025. Debt/GDP explains less than 0.3% of spread variance.

But please don't get excited please Modern Monetary Theorists (that delusion still needs to die). The turkey's life outlook is not correlated to Christmas either, until such time as it is. Debt still matters. Like falling from great heights, its not the fall that hurts, it is the sudden inevitable stop that does the damage.

> “Annual income twenty pounds, annual expenditure nineteen nineteen and six, result happiness. Annual income twenty pounds, annual expenditure twenty pounds ought and six, result misery.” - Wilkins Micawber, David Copperfield, Charles Dickens, c. 1850. It should be noted he fails to heed his own advice and ends in debtors prison. Take note chancellors of the West who seem unable to ever balance a budget. That means you too Mr Carney, you lack the excuse of not knowing better.

The dashboard below explores why. At least I hope it does. yes, I know its flawed, all such analysis is. USD yields are not such an objective benchmark, but it is good enough for the purpose at hand.

---

## Interactive Dashboard

{{< rawhtml >}}
<iframe 
  src="/html/g20-sovereign-spreads.html" 
  width="100%" 
  height="900px" 
  frameborder="0" 
  scrolling="yes"
  style="border: 1px solid #1e2d42; border-radius: 8px;">
</iframe>
{{< /rawhtml >}}

---

## Key Findings

**1. Sign reversal destroys the aggregate signal.** Advanced economies (Japan, Germany, Australia) show *negative* correlation — debt rises as spreads fall, driven by QE, safe-haven demand, and central bank credibility. Emerging markets show *positive* correlation. These opposing effects cancel in aggregate, producing the near-zero result.

**2. Currency sovereignty matters more than debt levels.** Japan exceeds 250% Debt/GDP with near-zero spreads. Argentina at ~80% faces double-digit spreads. The difference is that Japan borrows in yen; Argentina borrows in dollars.

**3. The global rate cycle dominates.** The Volcker shock, the post-2008 zero-rate era, and the 2022 tightening cycle moved yields across all sovereigns simultaneously, regardless of individual fiscal positions.

**4. Spreads are fast; debt is slow.** Debt/GDP moves 2–5pp per year. Spreads can move 100–500bps in weeks. They are not measuring the same thing on the same timescale.

**5. China is the strongest single-country correlation (r = −0.797)** — rising debt alongside falling spreads as China developed its domestic bond market and accumulated foreign reserves, severing the debt–spread link.

---

### Part 2 — Debt/GDP vs Real GDP Growth

We will return to a deep dive into this subject at a later date. For now, lets see the impact of overall debt contributes to growth. This is an oversimplification. The answer to this question is not nearly this simple as its a multifactor model at play here with many dynamic correlations. It also ignore non state debt, eg the Türkiye problem. So its not total indebtedness, but its a start.

{{< rawhtml >}}
<iframe 
src="/html/g20_debt_gdp_growth_scatter.html" 
width="100%" 
height="900px" 
frameborder="0" 
scrolling="yes"
style="border: 1px solid #1e2d42; border-radius: 8px;">
</iframe>
{{< /rawhtml >}}


**Overall correlation: Pearson r = −0.284 | Spearman ρ = −0.321 | OLS R² = 0.081**

The debt–growth relationship is statistically significant (p < 0.0001) but
economically modest: debt/GDP explains roughly 8% of growth variance. This is
directionally consistent with Reinhart & Rogoff (2010), though far weaker than
their headline finding, and the causal interpretation remains contested. Hence the comments about much more work to be done.

**16 of 19 G20 countries show negative country-level correlations**, with 11
significant at p < 0.05. The three exceptions — India (+0.218), Russia (+0.070),
and Argentina (+0.044) — reflect country-specific structural dynamics that
override the general pattern.

**Strongest negative correlations:** Japan (r = −0.626), Brazil (−0.571),
South Korea (−0.458), and Mexico (−0.423). Each experienced debt build-ups that
coincided with meaningful growth slowdowns.

**Why the aggregate is still only −0.28:**

- **Reverse causality dominates.** Low growth *causes* debt to rise via automatic
  stabilisers and stimulus spending at least as much as high debt *causes* slow
  growth. Panel OLS cannot separate these directions.
- **Debt level and growth regime do not align in time.** South Korea carried
  moderate debt *and* double-digit growth simultaneously in the 1970s–80s. The
  trajectory of debt and the composition of spending matter more than any
  point-in-time ratio. Türkiye carriers lower state debt, but insane levels of inflation as a result of other influences.
- **Productive investment confounds the signal.** Public debt accumulated through
  infrastructure or human capital investment can raise both the debt level and
  future growth simultaneously, attenuating the negative relationship.
- **No clean Reinhart-Rogoff threshold.** The purported 90% debt/GDP tipping
  point is not visible as a discrete nonlinear break in this data. Growth declines
  gradually across the debt distribution rather than collapsing at a single level.

  More and better data. Job for another day.

---

### Data Sources

| Source | Series | Coverage |
|--------|--------|----------|
| IMF World Economic Outlook | `GGXWDG_NGDP` — gross govt debt (% GDP) | 1980–2023 |
| World Bank | `GC.DOD.TOTL.GD.ZS` — central govt debt (% GDP) | 1990–2023 |
| Abbas et al. (2010), IMF WP/10/245 | Historical public debt database | 1970–2009 |
| OECD.Stat | `IRLT` — 10-year benchmark yields | 1970–2023 |
| FRED, St. Louis Fed | `DGS10` — US 10-year Treasury | 1970–2023 |
| BIS | Long-term interest rate statistics | 1970–2023 |
| World Bank | `NY.GDP.MKTP.KD.ZG` — real GDP growth | 1970–2023 |
| IMF WEO | `NGDP_RPCH` — real GDP growth | 1980–2023 |

---

### Key References

- Reinhart, C. & Rogoff, K. (2010). *Growth in a Time of Debt.* American Economic
  Review, 100(2), 573–578.
- Reinhart, C., Rogoff, K. & Savastano, M. (2003). *Debt Intolerance.* Brookings
  Papers on Economic Activity, 1, 1–74.
- Abbas, S.A. et al. (2010). *A Historical Public Debt Database.* IMF Working
  Paper WP/10/245.
- Gourinchas, P-O. & Rey, H. (2007). *From World Banker to World Venture
  Capitalist.* NBER Working Paper 11563.
- Herndon, T., Ash, M. & Pollin, R. (2014). *Does High Public Debt Consistently
  Stifle Economic Growth?* Cambridge Journal of Economics, 38(2), 257–279.
  *(The replication study that identified errors in Reinhart & Rogoff.)*

---

## Data Sources

- World Bank: Central Government Debt (% GDP) — GC.DOD.TOTL.GD.ZS
- IMF WEO: General Government Gross Debt — GGXWDG_NGDP
- OECD.Stat: Long-term interest rates (10-year benchmark)
- FRED: DGS10 — 10-Year US Treasury Constant Maturity
- Abbas et al. (2010): IMF WP/10/245 — A Historical Public Debt Database

---

## Key Takeaways

- 100% debt to GDP is not the end, just look at the US. but it marks the start of the beginning of the end.
- If you can't run minor operating suprpluses outside of recessions, it because you don't want to.
- There are less natural buyers of the UK gilts now perhaps than in the past. The UK needs the marginal buyer to be there.
- The 100% threshold marks the point where you are starting to walk down the road to perdition. It, budget reform and fiscal control only gets harder.
- The UK has been there in the past in the 1970's, which led to the rise of Thatcherite reforms. So if you are on the left and hate that, all the reason to control the budget.
- A small surplus is not Austerity, its Sanity. It a prepayment on future options.

---

## References

- [Source title](https://url.com)
