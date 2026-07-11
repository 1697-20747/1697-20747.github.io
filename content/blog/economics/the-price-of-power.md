---
title: "The Price of Power"
date: 2026-06-15T00:00:00Z
draft: false
categories: ["economics"]
tags: ["energy", "UK", "GDP", "deindustrialisation", "industrial-policy"]
description: "UK industrial electricity prices are the highest in the developed world. UK productivity growth is among the lowest in the G7. This post asks whether the two are connected, does the data, and finds the answer is: probably, but not in the way you might think."
showToc: true
tocopen: false
---

## Overview

I have relied on AI for the numbers here, again because the data is not news here. The answer is known. Electricity production, volumes thereof, have collapsed in the UK in recent decades. Given more power is generally a good thing, this is odd as policy choice. If you think power is a bad thing, push your car home from the supermarket for say 20 kilometre's with the engine (electric or petrol) off. Once a week for each shop. Even better, clear 5 acres of wheat, and thresh the grain, all without a combine. Energy still bad? Thought not.


 Critique as you will. I have no objection to renewable power, quite the opposite. At what cost is the point. I am less convinced that covering prime farmland with solar panels is a good idea though. I have a bias to what works, and not committing industrial suicide. Putting aside the rhetoric, here is the exam question: Does high power prices and/or power availability correlate to industry and economic growth? Is Net Zero, the current UK legislative implementation not the concept, a net gain or net cost to date?

UK industrial electricity prices in 2023 stood at 25.85p/kWh — the highest of any country in the 28-nation IEA dataset. The US equivalent was 7.9p/kWh. Germany, often cited as Europe's industrial powerhouse, paid 17.71p/kWh. France, with its nuclear-heavy grid, paid 17.84p/kWh. The UK pays 3.3 times more than the US and 46% more than the IEA median.

Meanwhile, UK real GDP per capita grew at an average of 1.35% annually between 2000 and 2010, and at 0.87% annually between 2011 and 2023 — a deceleration of approximately half a percentage point per year. The US, over the same periods, went from 0.94% to 1.40%. GDP growth in the UK's own peer group went up. The UK's went down. This is what systemic decline into oblivion looks like from up close.

This post sets out the data, runs the correlations, reviews the literature, and tries to say something honest about what the numbers actually show.

---

## The Data

All data used in this analysis is from publicly available sources:

- **GDP per capita growth** (real, constant 2015 USD): World Bank WDI / OECD.Stat
- **Industrial electricity prices**: UK BEIS/DESNZ Energy Trends Table 5.3.1 and IEA Energy Prices Statistics 2024, all prices in pence per kWh including taxes
- **Industrial gas prices**: UK BEIS/DESNZ Energy Trends Table 5.7.1 / IEA Energy Prices Statistics
- **UK electricity generation (total TWh)**: BEIS/DESNZ Digest of UK Energy Statistics (DUKES) Table 5.6 / DUKES 5.1.3 long-run series
- **UK population**: ONS mid-year population estimates
- **Manufacturing value added % GDP**: World Bank WDI

The interactive dashboard below shows all series. The data covers 2000–2023 for prices and GDP, 2000–2022 for manufacturing.

{{< rawhtml >}}
<iframe src="/html/energy-gdp-dashboard.html" width="100%" height="1800px" frameborder="0" style="border-radius:8px; margin: 1.5rem 0;"></iframe>
{{< /rawhtml >}}

---

## What the Numbers Show

**The electricity price trajectory is stark.** In 2000, UK industrial electricity prices were broadly comparable to the US and slightly below France and Germany. By 2010 a gap had opened. By 2023 the gap had become a chasm. The UK price increased 515% in nominal terms between 2000 and 2023. The US price increased 72% over the same period.

Crucially, this is not explained by gas prices. UK industrial gas prices in 2023 were 5.58p/kWh — approximately 7% below the IEA median and below both France and Germany. The outlier is the US and Canada, where shale gas keeps prices around five to six times lower than the UK. But within Europe, UK gas prices are unremarkable. The premium is in electricity. The electricity-to-gas price ratio in the UK is approximately 6:1. In France it is 2.5:1. In Germany 3:1.

David Turver, who writes the most granular public analysis of UK energy prices, puts it plainly: it cannot be gas prices driving electricity prices so much higher in the UK than elsewhere. The culprits are the network and policy cost components layered onto the electricity price — grid reinforcement, balancing costs, Contracts for Difference obligations, and the legacy of a generation fleet that has been restructured rapidly away from cheap baseload toward a higher-cost mix without an adequate plan for the system costs that entails.

Renewable power at the stand alone unit cost are undoubtedly becoming cheaper. But delivered to the user across the tansmission and distribution network power prices are rising, in spite of the uplift in the renewable component. This is a pay more get less model.

**The GDP comparison is less clean but suggestive.** Looking at the two-period comparison (2000–2010 vs 2011–2023):

| Country | Elec price rise | GDP growth 00–10 | GDP growth 11–23 | Delta |
|---------|----------------|-----------------|-----------------|-------|
| UK | +127% | 1.35% | 0.87% | −0.49pp |
| USA | +29% | 0.94% | 1.40% | +0.46pp |
| Germany | +100% | 0.82% | 1.02% | +0.20pp |
| France | +109% | 1.31% | 1.07% | −0.24pp |
| Japan | +42% | 0.85% | 0.55% | −0.31pp |
| Canada | +61% | 1.33% | 0.98% | −0.34pp |

The country with the smallest electricity price increase (USA) showed the largest improvement in GDP growth. The country with the largest electricity price increase (UK) showed the largest deterioration. This is consistent with the hypothesis. It is not proof of it.

---

## Statistical Analysis

The bilateral contemporaneous correlation between annual electricity price changes and annual GDP growth is statistically significant for only one country in the sample: South Korea (r=−0.53, p=0.008). For the UK specifically, r=+0.09 (p=0.67) — essentially zero. The lagged correlation (electricity price in year t−1 vs GDP growth in year t) is similarly weak for most countries.

This does not mean there is no relationship. It means the relationship does not operate at the annual frequency. This is consistent with what the academic literature would predict.

The relevant mechanism is not: high electricity prices this year cause low GDP growth next year. The relevant mechanism is: persistently high electricity prices make energy-intensive production uneconomic over a period of years, cause investment to relocate to lower-cost jurisdictions, reduce the capital stock in tradable manufacturing sectors, and thereby suppress productivity growth in the medium term. This is a structural effect operating over a five to twenty year horizon, not a year-to-year cyclical one.

---

## What the Literature Says

The most directly relevant study is Burke and Mizrahi (2022) in *Energy Economics*, which uses mean-group panel estimates for 18 OECD countries over 1960–2016. Their finding: a 10% increase in energy prices dampens economic growth by approximately 0.15 percentage points on average, with larger effects in more energy-intensive economies.

Applying that coefficient mechanically to the UK's 515% nominal electricity price increase since 2000 — discounted roughly for inflation and non-linearity — gives a back-of-envelope growth drag on the order of 0.3–0.5 percentage points annually over the period. The actual UK growth deceleration versus peers is approximately 0.5 percentage points. The magnitudes are in the right ballpark, though this kind of arithmetic attribution is illustrative rather than rigorous.

A 2024 study using machine learning methods on UK-specific data found strong positive correlation between energy prices and GDP levels — which sounds counterintuitive until you realise the causation likely runs in both directions. GDP growth increases energy demand which pushes up prices; high prices also suppress energy-intensive activity. The cross-country panel studies are better designed to isolate the causal direction.

The EU-level literature (Tugcu et al., PMC 2023) found no robust strong correlation between energy consumption and GDP across EU member states — but this conflates energy consumption with energy prices, and the relevant channel for the UK hypothesis is prices affecting investment decisions, not volumes.

---

## The Manufacturing Story

The most compelling evidence for structural damage is in the manufacturing data, which does not require statistical inference — it is simply a fact.

UK manufacturing as a share of GDP fell from 15.5% in 2000 to 9.6% in 2022. This is a 38% decline in relative terms. Over the same period:

- Germany held manufacturing value added above 22% of GDP throughout
- South Korea held above 27%
- The USA, also deindustrialising, fell from 14.8% to 11.4% — a smaller proportional decline than the UK

Energy-intensive industries — steel, aluminium, ceramics, glass, paper, industrial chemicals — are where high electricity prices bite hardest. The UK's remaining industrial base in these sectors has faced sustained cost disadvantage relative to US, Asian, and even some European competitors. The Stellantis van plant in Luton, whose closure in 2024 was linked explicitly to energy cost competitiveness by the company itself, is a recent visible example of a trend running for two decades.

Germany managed to maintain its industrial base despite high electricity prices in part because large industrial users there had access to various exemptions, relief schemes, and long-term power purchase agreements that buffered the headline price. UK policy has been less consistent in protecting energy-intensive industries from grid and policy cost levies.

---

## UK Electricity Generation: Volume and Per Capita

Separate from the price question is the volume question. How much electricity is the UK actually generating, and what does that look like per head of population?

Total UK electricity generation peaked at 398 TWh in 2005. By 2023 it had fallen to 293 TWh — a decline of 26.4% from the peak. In per capita terms the picture is more striking: generation peaked at 6,525 kWh per person in 2005 and fell to 4,315 kWh per person in 2023, a decline of 33.9%.

To put that in context: per capita electricity generation in 2023 (4,315 kWh/person) is below the level recorded in 1993 (5,569 kWh/person). The UK has added approximately 10 million people to its population since 1993 while generating less total electricity. That is an unusual trajectory for a developed economy.

The standard explanation is efficiency — better-insulated buildings, LED lighting, more efficient appliances, and the shift from energy-intensive manufacturing to services. This is partially true. But it is also a description of deindustrialisation and demand destruction dressed up in more neutral language. An economy generating 34% less electricity per capita than it did twenty years ago is not obviously one that has restructured toward higher-value activity. It may simply be one that has priced energy-intensive activity offshore.

The DUKES data from BEIS is the authoritative source here, derived from metered generation at power stations. The 3,239 kWh/person average consumption figure cited in some sources refers to final consumption at the meter, which excludes transmission and distribution losses, own-use at power stations, and industrial direct consumption. Generation is the correct measure for assessing productive capacity.

---

## The Honest Answer

The bilateral time-series correlation is weak. You cannot look at the year-to-year numbers and conclude that high electricity prices caused low GDP growth in any given year.

But the structural picture is coherent and the two-period comparison is suggestive. The UK experienced the largest electricity price increase among advanced economies over the period and the largest growth deceleration relative to peers. The mechanism — energy costs rendering energy-intensive tradable production uneconomic, accelerating deindustrialisation, and suppressing the manufacturing productivity channel — is theoretically grounded and consistent with the observed data.

The hypothesis is not that energy prices are the sole or primary cause of UK underperformance. Brexit, planning constraints, underinvestment in infrastructure, a financial services bias in industrial policy, and demographic factors all play roles. But high energy prices are a plausible contributory factor that has been underweighted in the standard economic commentary, possibly because the effect is diffuse, structural, and slow-moving rather than acute and visible.

The OECD's March 2026 interim outlook downgraded UK growth by 0.5 percentage points for 2026 — the largest downgrade of any G20 economy. It cited, among other factors, energy price pressure. The UK's industrial electricity prices remained the highest in Europe as of early 2025.

The price of power is high, and not getting lower any time soon. The question is whether we have fully accounted for what it costs. Heating is now the luxury of the upper middle class. It is aspirational to not be cold in winter in the UK. This is madness.

---

## Technical Notes

Statistical analysis conducted in Python using SciPy. Pearson correlation coefficients and p-values are reported. Statistical significance threshold p<0.05 (two-tailed). The 2020 observation is excluded from all period-average calculations due to COVID distortion but is shown in time-series charts. Electricity prices converted to pence per kWh from local currency at annual average exchange rates where applicable. All prices include taxes as reported in IEA and BEIS source data.

---

## References

- Burke, P.J. & Mizrahi, B.H. (2022). "How energy prices shape OECD economic growth: Panel evidence from multiple decades." *Energy Economics*.
- David Turver (2024). "UK Industrial Electricity Prices Highest in the World." Substack.
- David Turver (2025). "High UK Electricity Prices Continue into 2025." Substack.
- Deloitte (2023). UK Industrial Energy Prices: International Competitiveness.
- House of Lords Library (2025). "Electricity prices in Great Britain."
- IEA (2024). Energy Prices 2024. International Energy Agency, Paris.
- OECD (2026). Interim Economic Outlook, March 2026.
- Tugcu, C.T. et al. (2023). "Ambivalent changes in the correlation of energy consumption and economic growth in the EU (2010–2019)." *PMC / Energies*.
- UK BEIS/DESNZ. Energy Trends, Tables 5.3.1 and 5.7.1. Various years.
- World Bank (2024). World Development Indicators. data.worldbank.org.
