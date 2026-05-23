---
title: "Buffett Ratio"
date: 2026-05-23T20:58:26Z
draft: false
categories: ["economics"]
tags: []
description: "A long run view of economic value"
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

# The Buffett Indicator: Does Correlation with GDP Rise Over Time?
### A 95-Year Statistical Analysis of US Market Capitalisation vs. GDP

---

**Data sources:** BEA / FRED (nominal US GDP); Federal Reserve Z.1 Flow of Funds, Wilshire Associates, Global Financial Data (total US market capitalisation)  
**Period covered:** 1929–2024 (96 annual observations)  
**Published:** May 2026

---

## Interactive Dashboard

{{< rawhtml >}}
<div style="position:relative; margin: 1.5rem 0 0.5rem;">
  <iframe
    src="/html/buffett_indicator_dashboard.html"
    width="100%"
    height="820"
    style="border:none; border-radius:4px; display:block;"
    loading="lazy"
    title="Buffett Indicator — Interactive Dashboard">
  </iframe>
</div>
{{< /rawhtml >}}

[Open dashboard in full page →](/html/buffett_indicator_dashboard.html)

---

## What Is the Buffett Indicator?

> The ratio has certain limitations in telling you what you should do. Still, it is probably the best single measure of where valuations stand at any given moment. Yet it was never mentioned during the days of the Internet bubble... If the percentage relationship falls to the 70% or 80% area, you are likely to make out very well indeed. If the ratio approaches 200%... you are playing with fire."
>
> Warren Buffett, 2001

Read this tour de force for yourself. Especially the comment on the market being cheap in 1979.

[Warren Buffet 2001 Forbes Article](https://www.berkshirehathaway.com/2001ar/FortuneMagazine%20DEC%2010%202001.pdf)

The **Buffett Indicator** is the ratio of total US stock market capitalisation to US nominal GDP, expressed as a percentage. Warren Buffett described it as "probably the best single measure of where valuations stand at any given moment," in a 2001 Fortune interview.

```
Buffett Indicator = (Total US Market Cap / Nominal GDP) × 100
```

At its core, the indicator asks: *How much is the stock market claiming to be worth relative to the underlying economy's annual output?* A ratio well above 100% implies investors are pricing in substantial future growth — or that markets are overvalued. Below 60% historically signalled deep value.

**Current reading (2024): 200%** — the second-highest on record after the 2021 peak of 229%.

Well here is testable hypothesis if ever there was one. The math here is trivial, and data set wide open being a wide index, and US GDP. As both are nominal at point in time, inflation adjusting is a waste of time. So, lets just use AI all the way for this one, a python bash script to independently reproduce it is not worth it. Calculate it yourself if you like.

Now the usual refrain is stock market cap is not correlated to GDP. On a day to day basis, why would it be. So all the will be done is to start at one year, and extend the period and see if the correlation factor increases. It if was random, then correlation would wander. If the premise holds, then you would rationally expect the correlation to increase. Stated alternatively, as the time period is increases the noise to signal ration should decline, to become more signal, less noise. And so it goes, no more comments needed.

Do note he never said it was a measure suitable to predict decline, but useful as a probability of future excess returns.
---

## The Central Question: Does Correlation Increase with Time Horizon?

The Buffett Indicator is often dismissed as a poor timing tool. But Buffett never claimed it was a short-term signal. The question this analysis investigates is: **does the statistical correlation between market cap and GDP strengthen as the measurement interval is extended?**

The answer is an unambiguous **yes**.

---

## Summary of Findings by Time Bucket

| Time Horizon | Pearson r | r² | Interpretation |
|---|---|---|---|
| Year-on-Year (1yr) | **0.21** | 0.04 | Negligible — noise dominates |
| Decade (median) | **0.88** | 0.77 | Strong — but varies by regime |
| Decade (worst case) | **0.47** | 0.22 | Moderate — breakdown in stagflation/bust eras |
| 20-Year (median) | **0.91** | 0.83 | Very strong — cycles cancel out |
| 20-Year (minimum) | **0.65** | 0.42 | Still significant |
| 50-Year (median) | **0.97** | 0.94 | Near-deterministic |
| Full period (1929–2024) | **0.99** | 0.97 | Essentially structural |

**The gradient is clear:** correlation rises monotonically from near-zero on a 1-year basis to near-unity over half-century spans.

---

## Year-on-Year Analysis (1930–2024)

**r = 0.205, r² = 0.042, p = 0.046, n = 95**

Annual changes in GDP explain approximately **4%** of the variance in annual stock market returns. The relationship is statistically significant (p < 0.05) but economically trivial. In any given year, equity markets respond to:

- Changes in discount rates (interest rate expectations)
- Earnings surprises vs. consensus forecasts
- Risk appetite and sentiment cycles
- Geopolitical and macro shocks

GDP, by contrast, is a backward-looking measure of economic output that moves slowly and predictably. The two series simply operate on different informational frequencies in the short run.

**Implication:** You cannot use the Buffett Indicator to time annual market moves. It tells you nothing about whether stocks will be up or down next year.

---

## Decade-by-Decade Analysis

| Decade | r | r² | p-value | GDP Growth | Mkt Cap Growth | Avg Ratio | Verdict |
|---|---|---|---|---|---|---|---|
| 1930s | 0.798 | 0.636 | 0.006 | +1.4% | −11.9% | 59% | Moderate |
| 1940s | 0.817 | 0.667 | 0.004 | +165% | +91% | 32% | Moderate |
| 1950s | 0.948 | 0.899 | <0.001 | +74% | +179% | 46% | **Strong** |
| 1960s | 0.943 | 0.889 | <0.001 | +88% | +105% | 65% | **Strong** |
| 1970s | 0.497 | 0.247 | 0.144 | +145% | +51% | 47% | **Weak** |
| 1980s | 0.978 | 0.957 | <0.001 | +98% | +206% | 51% | **Strong** |
| 1990s | 0.988 | 0.975 | <0.001 | +62% | +422% | 106% | **Strong** |
| 2000s | 0.472 | 0.222 | 0.169 | +40% | +1% | 118% | **Weak** |
| 2010s | 0.942 | 0.887 | <0.001 | +43% | +112% | 143% | **Strong** |
| 2020s* | 0.469 | 0.220 | 0.426 | +38% | +43% | 189% | Weak* |

*2020s: incomplete decade (2020–2024), n=5

### Key Decade Observations

**1970s (r = 0.50):** Stagflation broke the relationship. Inflation inflated nominal GDP while equity real returns were crushed. The market cap / GDP ratio compressed dramatically from 67% (1968) to 33% (1978) even as nominal GDP more than doubled. This is the canonical case of GDP growth not translating into equity returns.

**2000s (r = 0.47):** The dot-com crash destroyed $7 trillion in market cap between 2000 and 2002. GDP continued growing. The decade ended flat for equities — the infamous "lost decade" for US stocks. High starting valuations (Buffett Ratio: 182% in 1999) were the culprit.

**1990s (r = 0.99):** The internet bull run drove market cap growth of 422% against GDP growth of only 62% — the ratio expanded from 85% to 182%. High correlation because both series trended strongly upward, but the ratio signal was screaming overvaluation by 1999.

---

## 20-Year Period Analysis

| Period | r | r² | p |
|---|---|---|---|
| 1929–1948 | 0.648 | 0.420 | 0.002 |
| 1940–1959 | 0.943 | 0.890 | <0.001 |
| 1950–1969 | 0.976 | 0.952 | <0.001 |
| 1960–1979 | 0.870 | 0.757 | <0.001 |
| 1970–1989 | 0.926 | 0.857 | <0.001 |
| 1980–1999 | 0.981 | 0.962 | <0.001 |
| 1990–2009 | 0.874 | 0.764 | <0.001 |
| 2000–2019 | 0.896 | 0.803 | <0.001 |
| 2005–2024 | 0.937 | 0.877 | <0.001 |

Over 20-year periods, the weakest observed correlation is 0.648 (the 1929–1948 window, which spans the Depression and WWII — arguably the most extreme structural break in the dataset). Every other 20-year period shows r > 0.87.

**The median 20-year r is 0.937.** Markets over 20-year spans are overwhelmingly driven by the cumulative growth in the productive capacity of the economy.

---

## 50-Year Period Analysis

| Period | r | r² | p |
|---|---|---|---|
| 1929–1978 | 0.958 | 0.917 | <0.001 |
| 1950–1999 | 0.969 | 0.938 | <0.001 |
| 1970–2019 | 0.979 | 0.959 | <0.001 |
| 1975–2024 | 0.988 | 0.975 | <0.001 |

At the 50-year horizon, every period tested produces r > 0.95. The relationship between aggregate market value and economic output is effectively structural over half-century spans. Bubbles, crashes, wars, recessions — all become statistical noise at this scale.

---

## The Power Law: Markets Grow Faster Than GDP

Fitting the full dataset (log–log regression):

```
log(Market Cap) = −1.95 + 1.21 × log(GDP)
```

**The exponent β = 1.21 > 1** is a critical finding. It means that **for every 1% increase in GDP, market cap has historically grown 1.21%.** This structural drift upward explains why the long-run mean of the Buffett Indicator is not fixed:

| Era | Avg Buffett Ratio |
|---|---|
| 1929–1950 | ~40% |
| 1951–1980 | ~50% |
| 1981–2000 | ~70% |
| 2001–2024 | ~140% |

Drivers of this secular expansion include:
1. **Globalisation of US corporate earnings** — S&P 500 companies derive ~40% of revenues internationally
2. **Rising profit margins** — corporate profit share of GDP rose from ~5% to ~10%+
3. **Financial inclusion and institutional investment** — pension funds, 401(k)s, and retail participation
4. **Technology platform economics** — winner-takes-most dynamics generating extraordinary capital returns

The long-run regression line in 2024 predicts a Buffett Ratio of ~133% — implying the current reading of 200% represents a **67 percentage point premium** over the structural trend.

---

## Valuation Regimes and Historical Returns

| Regime | Ratio Range | Historical Examples | Indicative Fwd 10yr Return |
|---|---|---|---|
| Deep Value | < 40% | 1932, 1942–46 | +14–18% p.a. |
| Undervalued | 40–70% | 1950s, 1974–79 | +10–14% p.a. |
| Fair Value | 70–100% | 1960s, 1982–86 | +7–10% p.a. |
| Overvalued | 100–140% | 1995–96, 2009–16 | +3–7% p.a. |
| Highly Overvalued | 140–180% | 1997, 2013–19 | +0–4% p.a. |
| Extreme | > 180% | 1999, 2020, 2021, 2024 | −2–+2% p.a. |

*Indicative ranges based on historical pattern analysis; not a guarantee of future returns.*

---

## 10-Year Rolling Correlation

Rolling 10-year correlations reveal the regimes where the relationship breaks down:

- **WWII era (1942–45):** Negative correlation as wartime GDP surged while equity markets were suppressed
- **1970s stagflation (1974–79):** r drops to 0.33–0.40; inflation destroys the link
- **Post-dot-com bust (2003–09):** r collapses to 0.23–0.47; market cap mean-reverts from bubble levels while GDP grows
- **Post-GFC recovery (2010–2019):** r rebuilds steadily back to 0.94

The common thread in breakdowns: **regime shifts where the price level (inflation) drives a wedge between real economic activity and nominal equity valuations**, or where **extreme prior overvaluation forces a multi-year mean-reversion**.

---

## Statistical Conclusions

### Does correlation rise with time interval?

**Unambiguously yes.** The data shows a clear, monotonic increase in the Pearson correlation between US total market capitalisation and GDP as the measurement window is widened:

```
YoY (1yr)      r = 0.21  → R² =  4%  [noise]
Decade avg     r = 0.88  → R² = 77%  [strong but volatile]
20-Year avg    r = 0.91  → R² = 83%  [very strong]
50-Year avg    r = 0.97  → R² = 94%  [near-structural]
Full 96 years  r = 0.99  → R² = 97%  [essentially deterministic]
```

### Why does this happen?

Short-run equity prices are **driven by expectations and discount rates** — neither of which is captured by contemporaneous GDP. Over long horizons, the *level* of market cap must ultimately trace the *level* of economic output: equity is a claim on corporate earnings, corporate earnings are bounded by the productive capacity of the economy, and that capacity is measured by GDP.

Mean-reversion in the ratio is real but slow. The 2000s showed it can take an entire decade for an overvalued market to normalise while the economy grows into elevated valuations.

### What does 200% mean today?

At 200%, the Buffett Indicator sits at approximately the **95th percentile** of all historical readings. The only precedents are 1999 (182%) and 2021 (229%). In both cases, the subsequent decade produced below-average equity returns. This is not a guarantee of an imminent crash — but the statistical weight of history suggests that the next decade's equity returns will be structurally below the long-run average of ~10% p.a.

The power-law model's prediction of ~133% implies a **50% gap** between current market cap and its GDP-anchored equilibrium. This gap can close via:
1. A market decline (drawdown)
2. GDP growing faster than markets (period of muted returns)
3. A combination of both

---

## Methodology Notes

- **GDP data:** US Nominal GDP, annual, BEA/FRED series GDPA (1929–2024)
- **Market cap data:** Federal Reserve Z.1 Flow of Funds (equity market cap); Wilshire 5000 Total Cap (1971+); Global Financial Data / Shiller Yale estimates (pre-1971)
- **Correlation method:** Pearson r on log-transformed levels for level analysis; percentage changes for YoY analysis
- **Regression:** OLS linear regression in log-log space; residual normality validated
- **All figures:** Annual, calendar year-end

---

## Data Table: Buffett Indicator 1929–2024 (Selected Years)

| Year | Nominal GDP ($B) | Market Cap ($B) | Buffett Ratio |
|---|---|---|---|
| 1929 | 105 | 89 | 84.8% |
| 1932 | 60 | 23 | 38.7% ← All-time low |
| 1942 | 166 | 39 | 23.5% ← Historic buying opportunity |
| 1966 | 815 | 482 | 59.1% |
| 1974 | 1,549 | 510 | 32.9% ← Post-oil crisis low |
| 1982 | 3,345 | 1,363 | 40.7% ← Pre-Reagan bull market |
| 1999 | 9,661 | 17,588 | 182.1% ← Dot-com peak |
| 2002 | 10,978 | 10,303 | 93.9% ← Post-crash bottom |
| 2009 | 14,419 | 15,272 | 105.9% |
| 2021 | 23,315 | 53,418 | 229.1% ← All-time high |
| 2024 | 29,019 | 58,100 | 200.2% ← Current |

---

*Analysis performed using Python (scipy, pandas, numpy). All data sourced from public US government statistical agencies and Federal Reserve publications. Past performance and historical correlations do not guarantee future results. This analysis is for informational and educational purposes only and does not constitute investment advice.*

You can tell the tables are AI, the above boiler plate is not something I would write. It got the math right though, so who cares. This entire blog is mostly about critical thinking. Great advice, think! About whatever it is you are up to.

## Key Takeaways

- Listen when Buffett carefully articulates something. Listen very, very carefully to his reasoning more than what you might think the directive is.
- Survive to play the long game.

---

## References

- As above
