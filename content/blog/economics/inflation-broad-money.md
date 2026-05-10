---
title: "Inflation Broad Money"
date: 2026-05-06T19:13:38Z
draft: false
categories: ["economics"]
tags: []
description: "A short summary shown in post listings."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

As Friedman. 

> "“Inflation is always and everywhere a monetary phenomenon, in the sense that it is and can be produced only by a more rapid increase in the quantity of money than in output.”" - Milton Friedman

 Later he clarified that he was referring to episodes of persistent inflation. In the short run, supply shocks can impact the price level.

This post is all about assessing broad money supply on inflation. Just the facts if you please. I am not suggesting exogenous shocks don't matter. The current oil price shock in may 2026 is definitely going to wash a wave of inflation through the west. But I am not assessing this, just the concept of government actions expanding money relating to subsequent inflation.

For a more wider discussion, read what an actual economic thinks. What the hell do I know, I'm just applying some math here. This is a good overview.

[Paul Krugman on wider Inflation](https://paulkrugman.substack.com/p/money-isnt-everything)
---

# Broad Money Supply and Inflation: A Cross-Country Analysis of G20 Economies, 1970–2023

## Abstract

What then is the empirical relationship between broad money supply growth
(M2 or M3, per cent per annum) and consumer price inflation (CPI, per cent per
annum) across nineteen G20 member economies over the period 1970–2023,
comprising 1,026 annual country-year observations. 

Is monetary expansion a necessary, if not always sufficient, condition for sustained inflation?. 
We have date for inflation and broad money going back decades. Lets see.

The pooled Pearson correlation coefficient of r = +0.751 (Spearman ρ = +0.636; OLS R² = 0.564) provides substantial, if
heterogeneous, empirical support. Now this comes with the usual caveats around over simplification. But there is a prima facie hypothesis to be put to the test.

---

## 1. Theoretical Framework

The Quantity Theory of Money, formalised in the equation of exchange
MV = PQ, posits that, under the assumption of constant velocity (V) and
output (Q), a one-per-cent increase in the money stock (M) produces an
equiproportionate increase in the price level (P).

---

## 2. Data and Methodology

### 2.1 Data Sources

Broad money aggregates (M2 or M3, depending on national definition) are
sourced from the IMF International Financial Statistics (IFS, Tables 34–35),
the World Bank Financial Development Database (indicator FM.LBL.BMNY.GD.ZS
and FM.LBL.BMNY.ZG), BIS monetary and credit statistics, and national
central bank publications (Federal Reserve H.6 statistical release; ECB;
Bank of Japan; Bank of England; Bundesbank). Pre-1980 data for emerging
market economies are supplemented from Mitchell (2007) and Reinhart and
Rogoff (2011). CPI inflation series are drawn from the IMF World Economic
Outlook (indicator PCPIPCH), the World Bank (FP.CPI.TOTL.ZG), and the
OECD Main Economic Indicators. All series are calibrated to annual
frequency. Thanks AI for the slog in doing this.

Broad Money is a measure of liquidity within the economy, including    
* cash
* bank deposits
* near-money financial assets

M2 is the measure, roughly, of cash plus savings. It is a narrow measure, retail in nature. You could expect M2 to respond rapidly.

M4 comprises:

* sterling notes and coin
* sterling bank and building society deposits
* certificates of deposit
* short-term bank paper and similar sterling instruments
* certain repo claims and money-market liabilities held by the UK private sector.

But excludes:
* central bank reserves
* government money printing alone

The latter actions will show up in M2 and M4 though.

> The Broad money aggregate M4 is a measure of the quantity UK money supply.
>
> Bank of England   

[M4 Bank of England](https://www.bankofengland.co.uk/statistics/details/further-details-about-m4-data?utm_source=chatgpt.com)

### 2.2 Stationarity

Prior to correlation analysis, Augmented Dickey-Fuller (ADF) tests confirm
that both broad money growth (ADF statistic = −9.73; p < 0.0001) and CPI
inflation (ADF statistic = −9.42; p < 0.0001) are integrated of order zero
— I(0) — in their first-difference (growth-rate) representations. The
analysis is therefore conducted on stationary series, mitigating the risk of
spurious correlation.

In plain english this means regression analysis should provide some meaningful results. This is because before checking whether money growth and inflation move together, we verified the data behave properly statistically. After converting them into growth rates, both series became stable over time, so the correlation results are much more trustworthy.

### 2.3 Lag Structure

Cross-correlations are computed at lags of 0, 1, and 2 years (M2 growth
leading CPI). The optimal lag is selected by maximising |r|. Contemporaneous
correlation is employed for the pooled regression; country-specific best-lag
correlations are reported in the per-country analysis.

### 2.4 Outlier Treatment

Argentina, Brazil, Russia, and Turkey exhibit hyperinflationary or
near-hyperinflationary episodes in which annual CPI inflation and M2 growth
exceed 1,000 per cent. These observations are retained in the correlation
analysis but are capped at 300 per cent in scatter-plot visualisations for
legibility. Their inclusion amplifies the pooled correlation coefficient;
sensitivity analysis excluding these observations yields r = +0.52 and
R² = 0.27, still economically and statistically significant.

Much more on these problem children in other posts.

---

## 3. Empirical Results

### 3.1 Pooled Cross-Country Correlation

Across all 1,026 country-year observations, broad money growth and CPI inflation show a fairly strong positive relationship. The Pearson correlation is +0.751, while the Spearman rank correlation is +0.636, both highly statistically significant (p < 0.0001).

The regression results suggest that, on average, a 1 percentage point increase in broad money growth is associated with roughly a 0.53 percentage point increase in CPI inflation. The model explains about 56% of the variation in inflation across the sample (R² = 0.564), indicating that money growth is an important — though not exclusive — driver of inflation outcomes.

The regression intercept of 1.84% suggests there is also a baseline level of inflation that exists even without strong monetary expansion, likely reflecting structural, demand-side, and supply-side pressures within economies.

Overall, the findings are broadly in line with earlier studies such as Warren McCandless and Weber (1995), and Paul De Grauwe and Magdalena Polan (2005). However, the estimated relationship is weaker than the one-for-one relationship predicted by simple monetary theory, likely because of changes in financial systems and instability in money velocity over time.

Stated otherwise, Milton is looking rather good about now for causation, not just correlation. Not perfect, but decent.

### 3.2 Country-Level Heterogeneity

Significant cross-country variation is observed. The strongest correlations
are recorded for Argentina (r = +0.926 at lag 0), France (r = +0.827 at lag
2), Italy (r = +0.873 at lag 2), Indonesia (r = +0.749 at lag 0), and
Brazil (r = +0.716 at lag 0). In these economies, monetary expansion has
historically been tightly associated with inflationary outcomes, consistent
with fiscal dominance and commodity-price pass-through mechanisms. This is expected, sadly, as interventionist play games with inflation for short term politics. This tyranny has destroyed the long term prosperity of the Lat Am regions.

The weakest associations are found for the United States (best-lag r = +0.367
at lag 2), India (r = +0.234 at lag 2), and Saudi Arabia (r = +0.458 at lag
0). For the United States, this attenuation likely reflects the post-2008
expansion of central bank reserves that remained sequestered within the
banking system rather than entering broad circulation, as well as the secular
decline in monetary velocity (V) associated with quantitative easing. 

This make sense, we intrinsically expect different behaviors from G8 economy's. Lets see if running 8% constant deficits comes back to bite the US as they play currency deflation. As at May 2026, its looking like it might in the midst of the Iran conflict. I'll leave this comment for prosperity's sake and revisit in a year or two's time.

### 3.3 Lag Structure of Monetary Transmission

A pronounced heterogeneity in lag structure is evident between advanced and
emerging market economies. Back to science on this one for a bit, with some greek thrown in. 

> Homogenous milk (if you have ever lived in North America this will resonate), means milk that has been agitated and filtered such that the particles are approximately uniform in size. Homo, from the greek, means same or alike. 

> Heteros, being the alternate greek pre fix, implies some fundamental oppositeness. I can't recall seeing hetero milk for sale in a supermarket, maybe that is just me. Right, back to economics. But before that, economics is also greek, for the management of households.

If only Western governments could manage their house prudently; it seems a forgotten skill. A task, in the Japan Sengoko and later Edo period for the wife, not the Samurai lord. 

Regardless, back to the schisms which are expected:

**Advanced economies** (USA, DEU, GBR, JPN, FRA, ITA, CAN, AUS, KOR) exhibit
peak correlations at lags of 1–2 years, consistent with longer transmission
chains through credit markets, asset prices, and expectations-anchored wage
and price-setting. The United Kingdom achieves its maximum correlation of
r = +0.627 at lag 2; Japan at r = +0.682 at lag 2; Canada at r = +0.675 at
lag 2. This 1–2 year transmission lag accords with the empirical consensus in
the monetary policy literature (Bernanke and Gertler, 1995; Romer and Romer,
2004).

**Emerging market and developing economies** (ARG, BRA, IDN, MEX, TUR, RUS)
exhibit peak correlations at lag 0 or lag 1, reflecting more direct fiscal
monetisation, weaker central bank credibility, less developed financial
intermediation, and a higher proportion of commodity-indexed prices. Brazil
and Argentina both exhibit their highest correlations contemporaneously (lag
0), consistent with near-instantaneous pass-through in high-inflation regimes
where agents rapidly reprice in response to monetary signals.

### 3.4 Broad Money to GDP Ratio: Financial Deepening

The ratio of broad money to nominal GDP — the inverse of monetary velocity —
exhibits a strong upward secular trend across all G20 economies from 1970 to
2023, consistent with the global process of financial deepening and
intermediation. And also pathetic inability to learn from past lessons. Borrow today, who cares about the future?
Not the people who fall prey to this nonsense and vote for it, that's for sure.

Japan's ratio rises from approximately 100 per cent in 1970
to over 320 per cent by 2023; China's from 45 per cent to 245 per cent,
driven by state-directed credit expansion; advanced European economies
converge in the 140–175 per cent range.

A story for later, but Japan is a natural buyer of Japanese debt. This luxury is a concept that the UK is suffering from amnesia on, as the worlds market no longer really needs Gilt. My oh my, the UK needs the marginal buyer now though. Japan Post Bank, for example, holds enormous amounts of Yen. Before the left and MMT advocates get excited about this, you have to have a highly productive export economy to generate surplus cash before you get to this point. Borrowing like a mad person and claiming it will be fine like Japan, is nonsense without all the other aspects.

[JGB Holders](https://www.mof.go.jp/english/policy/jgbs/reference/Others/holdings01.pdf)

This secular trend has material implications for the QTM: a rising M/PQ ratio
implies that monetary expansion is partially absorbed by the demand for money
balances, moderating the inflationary impact of a given rate of M2 growth.
This mechanism — financial deepening as an inflationary buffer — explains in
part why the post-2008 and post-2020 quantitative easing programmes in
advanced economies did not initially generate the inflation predicted by
naive monetarist models.

Perhaps not, but the tensions it brought are bearing fruit now in other ways. QE is not a free ride in my view. That is a whole subject on its own. Funny how when QE drive yields down, the gain in book value on held bonds was not bemoaned. But on exit the enormous accounting 'losses' were decried. Oddly not celebrated as a natural reversion. Free on the way up, everyone else's problem on the way down. This is result of changes in market value as term structure of rates goes back up (bond values down) and the negative carry of paying say 5.00% whilst holding 2% yielding bonds. Same same, its life. Hard to pick a fight with gravity and win in the long run. Please dear government, float us a hundred billion or so, if you please to stay in the game during QT. Such is politics.

QE is the cheats way of playing with the term structure of rates, when your mandate is the short end of the curve. It is pseudo fiscal policy without the framework or electoral mandate for same.

---

## 4. Qualifications and Structural Considerations

### 4.1 Velocity Instability

The Quantity Theory rests on the assumption of stable or predictable velocity
of money circulation (V = PQ/M). The post-1990 era has witnessed significant
velocity decline across G20 economies, driven by financial innovation,
regulatory changes (Basel capital requirements), and the expansion of
non-bank financial intermediation. Unstable velocity attenuates the
contemporaneous money–inflation link and introduces lag uncertainty.

### 4.2 Fiscal Dominance vs. Monetary Orthodoxy

The high correlations observed for Argentina, Brazil, Turkey, and Russia
(particularly in periods of hyperinflation) reflect fiscal dominance — the
subordination of monetary policy to government financing requirements — rather
than conventional monetary transmission. In these episodes, M2 growth was
endogenous (more greek) to fiscal deficits, rendering the causal interpretation
straightforward: fiscal deficits were monetised, directly generating
seigniorage inflation. Yes poor people with no assets, this is the government screwing you over. Whilst lying. Oh, and personally profiting.

### 4.3 Non-Bank Debt and Shadow Credit

A significant limitation of the M2-based analysis is its omission of
non-bank credit creation — shadow banking, corporate bond issuance, and
fintech lending. The "Türkiye problem" (to use a practitioner formulation) is
illustrative: Turkey's inflationary dynamics in 2021–2023 were substantially
driven by credit provision outside the formal M2 aggregate, complicating the
monetary explanation and necessitating a total-credit or debt-service approach
for a complete account. We will continue to explore this to death in other posts. It remains the 'too much' debt problem, its just that now we are arguing over whose debt, not the aggregate.

### 4.4 Endogeneity and Reverse Causality

The OLS regression does not resolve the endogeneity (darn these greeks!) inherent in the
money–inflation relationship. Central banks that target inflation may
accommodate supply shocks by expanding the money supply, creating reverse
causality. Structurally identified vector autoregression (SVAR) models
(Christiano, Eichenbaum and Evans, 1999) are required for causal
identification; the present cross-country OLS is properly interpreted as a
characterisation of correlation, not causation.

---

## Interactive Dashboard

{{< rawhtml >}}
<iframe 
  src="/html/g20_money_inflation.html" 
  width="100%" 
  height="900px" 
  frameborder="0" 
  scrolling="yes"
  style="border: 1px solid #1e2d42; border-radius: 8px;">
</iframe>
{{< /rawhtml >}}

---

---

## 5. Conclusions

The empirical evidence across nineteen G20 economies from 1970 to 2023
provides strong aggregate support for the Quantity Theory of Money: broad
money growth and CPI inflation exhibit a pooled Pearson correlation of +0.751
and an OLS R² of 0.564. However, several structural qualifications attenuate
the theoretical prediction of unit-slope pass-through (β = 0.527 vs. unity),
consistent with the findings of De Grauwe and Polan (2005).

## Interactive Dashboard II
Its a bit easier with just the one series. The one that we began all this with, the UK:

{{< rawhtml >}}
<iframe 
  src="/html/uk_broad_money_vs_inflation_1970_2023.html" 
  width="100%" 
  height="900px" 
  frameborder="0" 
  scrolling="yes"
  style="border: 1px solid #1e2d42; border-radius: 8px;">
</iframe>
{{< /rawhtml >}}

Three principal conclusions emerge:

1. **The money–inflation relationship is regime-dependent.** It is robust and
   contemporaneous in high-inflation emerging market economies characterised
   by fiscal dominance (ARG, BRA, TUR), but attenuated and lagged by 1–2
   years in low-inflation advanced economies with credible, independent central
   banks (USA, DEU, JPN).

2. **Financial deepening moderates monetary pass-through.** The secular rise
   in the broad money-to-GDP ratio absorbs a portion of monetary expansion
   into money-demand rather than inflationary pressure, explaining why
   post-2008 QE in advanced economies was not immediately inflationary. The
   2021–2023 inflationary episode in advanced economies, which coincided with
   extraordinary M2 expansion and supply-side disruptions, represents a
   partial reassertion of the monetary relationship following an extended
   period of suppression.

3. **M2-based analysis is a necessary but insufficient framework.** Total
   credit — including non-bank debt creation — is required for a complete
   account of inflationary dynamics in financially sophisticated economies.
   The monetarist framework remains indispensable but must be integrated with
   credit-cycle and fiscal-sustainability analysis for policy-relevant
   inference.

---

## 6. Data Sources

| Source | Series | URL |
|--------|--------|-----|
| IMF IFS | Money (Table 34), Quasi-Money (Table 35) | data.imf.org |
| IMF WEO | PCPIPCH — CPI inflation % | imf.org/datamapper |
| World Bank | FM.LBL.BMNY.GD.ZS — Broad money % GDP | data.worldbank.org |
| World Bank | FM.LBL.BMNY.ZG — Broad money growth % | data.worldbank.org |
| World Bank | FP.CPI.TOTL.ZG — CPI inflation % | data.worldbank.org |
| BIS | Monetary and credit statistics | bis.org/statistics/money_credit |
| OECD | Main Economic Indicators | stats.oecd.org |

## 7. References

- Friedman, M. & Schwartz, A.J. (1963). *A Monetary History of the United States, 1867–1960*. Princeton University Press.
- McCandless, G.T. & Weber, W.E. (1995). Some Monetary Facts. *Federal Reserve Bank of Minneapolis Quarterly Review*, 19(3), 2–11.
- De Grauwe, P. & Polan, M. (2005). Is Inflation Always and Everywhere a Monetary Phenomenon? *Scandinavian Journal of Economics*, 107(2), 239–259.
- Bernanke, B. & Gertler, M. (1995). Inside the Black Box: The Credit Channel of Monetary Policy Transmission. *Journal of Economic Perspectives*, 9(4), 27–48.
- Teles, P., Uhlig, H. & Valle e Azevedo, J. (2016). Is Quantity Theory Still Alive? *Economic Journal*, 126(591), 442–464.
- Sargent, T.J. & Surico, P. (2011). Two Illustrations of the Quantity Theory of Money. *American Economic Review*, 101(1), 109–128.
- Ha, J., Kose, M.A. & Ohnsorge, F. (2019). *Inflation in Emerging and Developing Economies*. World Bank Group/IMF Working Paper.
- Christiano, L., Eichenbaum, M. & Evans, C. (1999). Monetary Policy Shocks: What Have We Learned and to What End? *Handbook of Macroeconomics*, Vol. 1A.
- Mitchell, B.R. (2007). *International Historical Statistics*. Palgrave Macmillan.
- Reinhart, C.M. & Rogoff, K.S. (2011). From Financial Crash to Debt Crisis. *American Economic Review*, 101(5), 1676–1706.

---

## Key Takeaways

- Point one
- Point two
- Point three

---

## References

- [Source title](https://url.com)
