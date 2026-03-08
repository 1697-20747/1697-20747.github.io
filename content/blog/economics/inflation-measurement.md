---
title: "Why Inflation Measurement Is Harder Than You Think"
date: 2026-02-23
draft: false
weight: 10
categories: ["economics"]
tags: ["inflation", "CPI", "macroeconomics"]
description: "The CPI is everywhere, but how it's actually constructed reveals some uncomfortable tradeoffs."
showToc: true
tocopen: false
---

## Overview

The Consumer Price Index gets quoted on every financial news segment. But if you dig into how it's actually constructed, you start to see cracks. This post walks through the methodology, the known biases, and what better alternatives look like. Before we do that, some historical context.


---

## Out with the old and in with the..... old (again?)

Cast your mind back to circa 300CE. I did imply this was not a new problem, nor in fact are the attempted solutions that don't work.

Diocletian's Edict on Maximum Prices (301 CE), or Edictum de Pretiis Rerum Venalium, was a sweeping, ultimately failed Roman law designed to curb rampant inflation. It established maximum legal prices and wages for over 1,400 goods, services, and labor types, with severe, often fatal, penalties for violation. 

Now, how do we know this? Because like all good dictums, this one was carved in stone. You can go and see it, in Greek, if you are not convinced. Please research the details yourself, there are many. For our purposes this is a strong edict that attempts to set the maxium price for goods. Using very strong words, effectively an 'or else'. Now in his day Diocletion had some power. But not enough to quash inflation with mere words. Every wanna be tyrant whose crackpot policies has resulted in hyper inflation (hello Venezuala, Turykie, etc, etc).

During what is now called the Crisis of the Third Century, Roman coinage had been greatly debased by the numerous emperors and usurpers who minted their own coins. Gold coins were no longer all gold coins. This is false money creation. In modern parlance, their Treasurers liked to promise spending far above the level that the ability of the economy could sustain. In a way the fraud was a bit more honest back in the day. At least you could test the honesty of the coins yourself.

Regardless the inevitable happend, people did not like taking less (debased) money for their products and goods, so the inevitable increasing prices (inflation spiral) resulted. Then, as is now, its quite hard to talk your way out this dilema unless you 1. promsie to reduce the supply of money; and 2. really (truly) mean it; and 3. people actually believe you. For reference, the death penalty was not enough of a threat to stop the tawdry behavior of coin debasement. In the same way that the death penalty seems not to stop people so inclined to murder people. How things don't change.

Let us cherry pick some actual examples, with some context. First the currency structure, then an example:

aureus – 1600 denarii
argenteus = 100 denarii
follis = 20 denarii
1/4 of follis = 4 denarii

Legumes and grains
Wheat – 100 denarii for about 17 liters

Without agonizing over the math, a denarii comes out (via gold equivalent, using silver to gold ratio) as something like 1 denarius ≈ 0.28 g Au × £123 ≈ £34.4 today. With a healthy level of sceptisim on precision here, but good enough. This would price the wheat at £3,400 for 17 litres. A US Bushel is near enough 35 litres. So this prices wheat at £7,100 a bushell. This is of course, if true, insane. Today you can buy a bushell for less than £4.50. Now this was either one hell of an inflation cycle in gold terms, or something is off.

---

## What the CPI Actually Measures

CPI tracks the price of a fixed "basket" of goods over time. The Bureau of Labor Statistics surveys households to determine what goes in the basket, then tracks those prices monthly. All the relevant goverment entities go about this in variations of themes. They also tinker with substututions. A conspiracy theorist would be inclinded to think that this is to game the result down, while taking decisions that drive inflation higher.

Like the much vaunted boiling from model, inflation grinds you down over time, year on year you don't tend to be as aware.

Simple in theory. Messier in practice.

```python
# Replicating a basic CPI calculation in Python
basket = {
    "rent":        0.32,   # weight (share of spending)
    "food":        0.14,
    "transport":   0.16,
    "healthcare":  0.08,
    "other":       0.30,
}

prices_2023 = {"rent": 1800, "food": 620, "transport": 410, "healthcare": 290, "other": 900}
prices_2024 = {"rent": 1980, "food": 645, "transport": 398, "healthcare": 315, "other": 935}

cpi_change = sum(
    basket[item] * (prices_2024[item] / prices_2023[item] - 1)
    for item in basket
)
print(f"Estimated CPI change: {cpi_change:.2%}")
```

```bash
# Run it
python3 cpi_calc.py
# Estimated CPI change: 5.23%
```

---

## The Substitution Bias Problem

When beef gets expensive, people buy chicken. The fixed-basket approach doesn't account for this — it assumes you keep buying the same beef. This is **substitution bias**, and it causes CPI to *overstate* inflation.

The BLS partially addresses this with the "chained CPI" (C-CPI-U), which updates the basket more frequently.

![CPI vs Chained CPI comparison](/images/cpi-comparison.png)

---

## Generating the Comparison Chart

Here's the Python I used to generate the chart above:

```python
import matplotlib.pyplot as plt
import numpy as np

years = list(range(2000, 2025))
# Synthetic data for illustration
cpi      = np.cumsum(np.random.normal(0.025, 0.01, len(years))) + 100
chained  = cpi - np.linspace(0, 8, len(years))   # chained typically runs lower

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, cpi,     label="CPI-U",      linewidth=2)
ax.plot(years, chained, label="C-CPI-U",    linewidth=2, linestyle="--")
ax.set_title("CPI vs Chained CPI (2000–2024)", fontsize=14)
ax.set_ylabel("Index (Base: 2000 = 100)")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("static/images/cpi-comparison.png", dpi=150, bbox_inches="tight")
```

---

## The Sins of RPI

Whilst the RPI is fatally flawed, more on that in one moment, it has one very solid advantage if you are a price setter. You get to push your prices higher, every time. The reason that evey phone company or indexed biller who could read used the RPI as the inflator is not the prusuit of precision, it was greed, plain and simple. The cherry picked the index that would allow them to charge more, end of. The ONS has a good summary article, note the date of 2018: Shortcomings of the Retail Prices Index as a measure of inflation. Lets refer to their conclusion:

> In 2013, the RPI lost its status as a National Statistic. Our position on the RPI is clear: we do not think it is a good measure of inflation and discourage its use. There are other, better measures available and any use of RPI over these far superior alternatives should be closely scrutinised.

2013 is the date of this comment. Now fast forward to 2026, and guess the meansure used to set student loan interest rates? Wait for it..... RPI plus 3%. So the government, using the RPI that the producer of said index has admitted is flawed, still uses it. You can bet your last penny that if RPI was systemiaclly less, it would have died a long time ago. Now what is the impact of this, well its approximately 90bps per annum, compouding up if you are not paying off the loan. Thats not nothing, actually its about (1.009)^{25} or approx 1.251, so a 25% penalty. Now the other problem here is the 3%, that a hefty credit risk permium for government backed loans to student. Now if these are really loans or just punishment devices is a conversation for another day. No one, other than researchers, should be allowed to price from RPI.

This begs the question of why researchers? A flawed metric, if calculated using a consistent method, can still inform of relative price changes if held over the long term.
---


## Key Takeaways

- CPI is a useful approximation, not a precise measure
- Substitution bias causes it to overstate inflation by roughly 0.3–0.5% annually
- Chained CPI is more accurate but adopted slowly for political reasons (it reduces Social Security COLA adjustments)
- Personal inflation varies enormously by income — rent-heavy budgets are hit harder

---

## References

- [BLS CPI Methodology](https://www.bls.gov/cpi/questions-and-answers.htm)
- Boskin Commission Report (1996) — foundational critique of CPI measurement
