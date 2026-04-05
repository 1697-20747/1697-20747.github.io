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

Now, how do we know this? Because like all good dictums, this one was carved in stone. You can go and see it, in Greek, if you are not convinced. Please research the details yourself, there are many. For our purposes this is a strong edict that attempts to set the maximum price for goods. Using very strong words, effectively an 'or else'. Now in his day Diocletion had some power. But not enough to quash inflation with mere words. Every wanna be tyrant whose crackpot policies has resulted in hyper inflation (hello Venezuela, Turykie, etc, etc).

During what is now called the Crisis of the Third Century, Roman coinage had been greatly debased by the numerous emperors and usurpers who minted their own coins. Gold coins were no longer all gold coins. This is false money creation. In modern parlance, their Treasurers liked to promise spending far above the level that the ability of the economy could sustain. In a way the fraud was a bit more honest back in the day. At least you could test the honesty of the coins yourself.

Regardless the inevitable happened, people did not like taking less (debased) money for their products and goods, so the inevitable increasing prices (inflation spiral) resulted. Then, as is now, its quite hard to talk your way out this dilemma unless you 1. promise to reduce the supply of money; and 2. really (truly) mean it; and 3. people actually believe you. For reference, the death penalty was not enough of a threat to stop the tawdry behavior of coin debasement. In the same way that the death penalty seems not to stop people so inclined to murder people. How things don't change.

Let us cherry pick some actual examples, with some context. First the currency structure, then an example:

aureus – 1600 denarii
argenteus = 100 denarii
follis = 20 denarii
1/4 of follis = 4 denarii

Legumes and grains
Wheat – 100 denarii for about 17 liters

Without agonizing over the math, a denarii comes out (via gold equivalent, using silver to gold ratio) as something like 1 denarius ≈ 0.28 g Au × £123 ≈ £34.4 today. With a healthy level of skepticism on precision here, but good enough. This would price the wheat at £3,400 for 17 litres. A US Bushel is near enough 35 litres. So this prices wheat at £7,100 a bushel. This is of course, if true, insane. Today you can buy a bushel for less than £4.50. Now this was either one hell of an inflation cycle in gold terms, or something is off.

---

## What the CPI Actually Measures

CPI tracks the price of a fixed "basket" of goods over time. The Bureau of Labor Statistics surveys households to determine what goes in the basket, then tracks those prices monthly. All the relevant government entities go about this in variations of themes. They also tinker with substitutions. A conspiracy theorist would be inclined to think that this is to game the result down, while taking decisions that drive inflation higher.

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

Whilst the RPI is fatally flawed, more on that in one moment, it has one very solid advantage if you are a price setter. You get to push your prices higher, every time. The reason that every phone company or indexed biller who could read used the RPI as the inflator is not the pursuit of precision, it was greed, plain and simple. The cherry picked the index that would allow them to charge more, end of. The ONS has a good summary article, note the date of 2018: Shortcomings of the Retail Prices Index as a measure of inflation. Lets refer to their conclusion:

> In 2013, the RPI lost its status as a National Statistic. Our position on the RPI is clear: we do not think it is a good measure of inflation and discourage its use. There are other, better measures available and any use of RPI over these far superior alternatives should be closely scrutinized.

2013 is the date of this comment. Now fast forward to 2026, and guess the measure used to set student loan interest rates? Wait for it..... RPI plus 3%. So the government, using the RPI that the producer of said index has admitted is flawed, still uses it. You can bet your last penny that if RPI was systemically less, it would have died a long time ago. Now what is the impact of this, well its approximately 90bps per annum, compounding up if you are not paying off the loan. Thats not nothing, actually its about (1.009)^{25} or approx 1.251, so a 25% penalty. Now the other problem here is the 3%, that a hefty credit risk premium for government backed loans to student. Now if these are really loans or just punishment devices is a conversation for another day. No one, other than researchers, should be allowed to price from RPI.

![Causes of the difference between the RPI and CPIH inflation rates 2006 to 2018](/images/ons_rpi_cpih_wedge.png)

Source: https://www.ons.gov.uk/chartimage?uri=/economy/inflationandpriceindices/articles/shortcomingsoftheretailpricesindexasameasureofinflation/2018-03-08/f921bcd3

This begs the question of why, researchers? Actually, there is decent reason. A flawed metric, if calculated using a consistent method, can still inform of relative price changes if held over the long term. It ceases to have absolute value though.

**Other than for research, it should be prohibited for the government or any private entity to use this index to price anything. Those who game it should be fined.**

---


## Key Takeaways

- CPI is a useful approximation, not a precise measure
- Substitution bias causes it to overstate inflation by roughly 0.3–0.5% annually
- Chained CPI is more accurate but adopted slowly for political reasons (it reduces Social Security COLA adjustments)
- Personal inflation varies enormously by income — rent-heavy budgets are hit harder

---

---

## In the long run.... we are all dead.

Thankfully some studious persons at the Bank of England did my homework for me. I should pay them back update this, one day. Even more helpfully, the FRED team made the data usable. The BoE one is kind of a messy excel file.

BoE original file text:

> The Bank of England's three centuries dataset originated from the 2010 Q4 Quarterly Bulletin article 'The UK recession in context — what do three centuries of data tell us?' by Sally Hills, Ryland Thomas and Nicholas Dimsdale, based on an initial set of series for which the authors  were able to obtain permission from the publishers /authors to publish online .   Thanks to the kind co-operation and assistance of many academic  and central bank colleagues the spreadsheet has been updated and extended several times since that point.  The current version 3.1  has been extended further and is now the repository for some of the underlying data behind the recent study 'British Economic Growth 1270-1870' by Steve Broadberry, Bruce Campbell, Alex Klein, Mark Overton and Bas van Leeuwen to whom we are extremely grateful.   This has been included as a standalone section of the database although many series in subsequent sections of the spreadsheet use these estimates in various ways to create series that go up to the present day.   Through the kind permission of Greg Clark, Nick Mayhew and Nuno Palma we have also been allowed to include wage, price and money supply  data stretching back to the C13th.  Some trade data have also been extended back to that time.  So the spreadsheet now contains time series covering three centuries of UK data and nearly seven and a half centuries of data for England.  We are also able  to provide some benchmark  estimates for money, GDP and population  for 1086 thanks to the work of Nick Mayhew and James Walker, so for these series broad comparisons can be made over nearly a thousand years of UK history.  In light of this and for the purposes of future proofing we have renamed (though not renumbered)  the spreadsheet given the time period it now covers.

We should celebrate honest academic work like this. It informs our lives.

![BoE Long Run Inflation](/images/uk_cpi_analysis.png)

Top panel — 546 annual observations from 1270–2016. Blue bars show annual CPI inflation on the left axis; red bars denote deflation years. The coral line traces the cumulative price level on a log-scaled right axis (rebased to 100 at 1270). Six key episodes are annotated with callout arrows (Black Death, Tudor debasement, Civil War, Napoleonic Wars, post-WWI spike, 1970s crisis).

Bottom panel — 97 non-overlapping 5-year periods, each independently rebased to 100. The green histogram shows the frequency distribution of 5-year cumulative inflation outcomes. The purple KDE curve on the right axis draws the implied continuous probability distribution. Reference lines mark zero net inflation (100), the median, and the mean. A stats box shows min/max/std dev and the share of deflationary 5-year periods.

There are a couple of other ways of looking at this data, even as the horizontal format for the distribution is possibly the best. Here are other typical alternatives:

![BoE Long Run Inflation 5 year](/images/boe_5yr_lineplot.png)

and;

![BoE Long Run Inflation 5 year](/images/boe_5yr_hist2d.png)

Some take away thoughts.

Why 5 years? Well, 1 year is not not enough in the main at least in modern developed emerged economies. But there is a case to refer to them as de merging given some on the insanity demonstrated of late. But after 5 years, cumulative inflation starts to bite. This is when you see all the cost of living crisis articles appears. We will test this in a moment. Also, it gives us a 100 or so time series. Enough to be useful.

As to take aways, there is strong bias to the upside. We might not like inflation, but the people making the spending and borrowing decisions sure seem to. Inflation is to the upside. It if was random, it would be neutral. There is a skew. Which we will get to later.

Data: Bank of England, Consumer Price Inflation in the United Kingdom [CPIIUKA], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/CPIIUKA, March 27, 2026.

Now, lets go to somewhere a little crazier, and we do try and unpick some of the why. Destination Türkiye:

---

## Türkiye Deep Dive

First the data:

![Türkiye Long Run Inflation](/images/turkey_uk.png)

Key additions visible in the updated chart

UK now runs to 2024, showing the 2022 post-COVID spike of 7.9% (UK's highest since 1991) alongside Türkiye's simultaneous 72.3% — same global shock, dramatically different magnitudes
The histogram now captures the full matched sample (65 years each, 1960–2024) making the distributional comparison statistically fair
The source notes box at the bottom explicitly documents the data lineage, splice rationale, and FRED series codes for both countries.

Read that again until you understand the point of this. 7.9% (UK) alongside Türkiye's simultaneous 72.3% — same global shock. That is a withering inflation number, that will surely impoverish anyone who does not hold inflation proof assets. Which is everyone who is poor, or holds cash. This is insanity and delusion rolled into failed economic and fiscal policy.

A quick note, I stitched these data sets together using AI, in this case Claude. All data is as specified. csv files below if you want to check it. It saved an enormous amount of time of writing methods, and left me more time for pondering. I guess that is the point.

If inflation is bad in the UK, and it is, it is a whole world of pain worse for the poor (figurative and in this case literal) souls in Türkiye. Or Türkiye. Take your pick, no offense meant either way.

### The Governor Revolving Door

Since 2016, several Governors of the Central Bank of the Republic of Türkiye (CBRT) have been dismissed from their positions via presidential decree, often following public disagreements with President Erdoğan over interest rate policies. 
Here is the list of governors since 2016, with notes on those forced to resign or dismissed:

* Fatih Karahan: 3 February 2024 – Present
Appointed following the resignation of his predecessor NY Times.
Hafize Gaye Erkan: 9 June 2023 – 2 February 2024
Resigned: Officially requested to be "pardoned from her duties" Reuters.
Reason: She cited a "reputation assassination campaign" against her family, though her departure was formalised by a presidential decree "removing" her from office after she posted her resignation YetkinReport.
* Şahap Kavcıoğlu: 20 March 2021 – 8 June 2023
Replaced: Moved to head the Banking Regulation and Supervision Agency (BDDK) via presidential decree Central Banking. A former lawmaker for the ruling AK Party (AKP). Unlike many of his predecessors, he was a vocal supporter of Erdoğan's unorthodox economic view that high interest rates cause inflation.
Unlike his predecessors, he aligned with the President's unorthodox view that high interest rates cause inflation The New Arab.
* Naci Ağbal: 7 November 2020 – 20 March 2021
Forced to Resign/Dismissed: Removed by presidential decree. A former Finance Minister and a long-time member of the AK Party. Despite his party ties, he was dismissed after four months for implementing orthodox rate hikes that clashed with Erdoğan's preferences.
Reason: His dismissal came just two days after he implemented a sharp 200-basis-point interest rate hike to 19% to combat inflation.
* Murat Uysal: 6 July 2019 – 7 November 2020
Forced to Resign/Dismissed: Removed by presidential decree Al Jazeera.
Reason: He was replaced as the Turkish lira hit record lows against the US dollar Al Jazeera.
* Murat Çetinkaya: 19 April 2016 – 6 July 2019
Forced to Resign/Dismissed: Removed by presidential decree CNBC.
Reason: He reportedly refused to resign voluntarily after resisting government pressure to cut interest rates to boost growth.

There is a lot to unpack here. A lot. Eventually we will get to how cutting rates boots growth and lowers inflation. Shocker, it doesn't. But if you want to keep your job, the lesson here is don't raise rates. No matter what. If you have to fore an employee, it might be a them problem. Maybe, even then less times than you think. If you have to fire that many people on balance your starting assumption should be that you have a 'you' problem.

> There are no poor soldiers. Only poor officers. - Napoleon (maybe).

> "In the British Army, there are no good battalions and no bad battalions, no good regiments and no bad regiments. There are only good and bad officers." - General Slim. Defeat into Victory is an account of the retaking of Burma by Allied forces during the Second World War by the British Field Marshal William Slim. (definitely)

Pick either one, the point is the same. Skilled workers don't blame their tools for the own incompetence. The employee's ain't the problem here one suspects.

The above list is evidence enough that there is no such thing as independent monetary policy as applied to Türkiye. Not even the pretense of any. So for all those clamouring with resentment about the BoE and Fed, be very careful what you wish for. Aligned delusions is likely a recipe for economic disaster. This is not to say that there is no case for the extent of independence, such as central banker deep love of Quantitative Easing running as proxy fiscal policy by people not voted or expressly empowered to do so as a pseudo treasury function.

Key factor: Erdogan is openly averse to high interest rates, claiming high rates cause inflation, which stands in opposition to mainstream economic theory. And sanity for that matter. Lets hear it from the man himself:

> "I have always opposed the distorted system that deepens inequalities, disrupts income justice, and turns billions of people into the slaves of a handful of capitalists. I oppose it again. I have often said that, no matter what, we cannot view as legitimate interest rates and an economic system based on interest rates,"...

> "I will continue to voice my longing for an interest rate-free economy from now on too. We will not turn back from our battle for the economic order based on interest rates to change,"....

> "We are determined to implement our economic programme, with which we have made noteworthy progress over the past two years, until it reaches its goals,".....

[Ergodan May 2025 Speaking at a Global Islamic Economy Summit in Istanbul](https://www.reuters.com/world/middle-east/Türkiyes-erdogan-repeats-opposition-interest-rates-says-economic-plan-continue-2025-05-30/)

Our chart pack so far suggests that the above is bonkers nonsense. If it were true, then inflation would not have run so hot. There appears directionally opposite causality to the theory embedded in the above statements. But lets dig into that accusation.

Add lira to dollar chart
Add inflation and interest rate chart
add real gdp per population growth

Keeping rates artificially low (more on how low later) has most likely contributed to the rise in domestic inflation. In some manner, if Türkiye wanted to be the world champion in domestic inflation, this is a decent path to follow. Argentina and/or Venezuela will most likely be very happy to hand over the championship cup.

The challenge we face in this situation is that the alternative cannot be examined, or even known. This is akin to saying that, ceteris paribus, the UK is worse off after Brexit. Ceteris paribus translates from latin literally as all (things) equal. Ceteris = the rest/others/remaining. The phrase 'et cetera' should spring to mind here, the root is the same. Paribus = equal/peer/companion. The phrase in full means everything else is assumed to be held constant. Which of course in a complex system is impossible. Easy to say, hard to prove. Very, very hard if you set aside your ideology.

At this point we can conclude that each of the UK and Türkiye has suffered bouts of inflation. Türkiye has experienced far higher levels on inflation. From here, we will apply all the diagnostic tools available to see if we can diagnose the primary root causes of inflation in Türkiye.




---

## References

- [BLS CPI Methodology](https://www.bls.gov/cpi/questions-and-answers.htm)
- Boskin Commission Report (1996) — foundational critique of CPI measurement
- https://fred.stlouisfed.org/series/CPIIUKA
- [Bank of England Data set]https://www.bankofengland.co.uk/statistics/research-datasets
- [Shortcomings of the RPI] https://www.ons.gov.uk/economy/inflationandpriceindices/articles/shortcomingsoftheretailpricesindexasameasureofinflation/2018-03-08#:~:text=In%202013%2C%20the%20RPI%20lost,alternatives%20should%20be%20closely%20scrutinised.
- [BoE data 5 year buckets](/data/boe_5yr_indexed_series.csv)