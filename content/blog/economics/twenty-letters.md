---
title: "Twenty Letters: The Bank of England, the 2% Target, and Seven Years of Missing It"
date: 2026-10-03T00:00:00Z
draft: true
categories: ["economics"]
tags: ["inflation", "CPI", "bank-of-england", "monetary-policy", "M4", "broad-money", "MPC"]
description: "UK prices are up 32% since December 2019, a 4.3% annual compound rate against a 2% target. What the Governor's twenty open letters blamed, what they forecast, and what the money supply was saying all along."
showToc: true
tocopen: true
cover:
  image: "/images/economics/inflation-since-2019-cpi-vs-target.png"
  alt: "UK CPI 12-month rate and cumulative price level vs a 2% compound path, Dec 2019 to Aug 2026"
  caption: "UK CPI vs the 2% target, Dec 2019 – Aug 2026. Source: ONS, own calculation."
---

## Overview

The Bank of England's own inflation calculator puts it plainly: what cost £1,000.00 in 2019 would cost **£1,330.14 in August 2026**, a change of **33.0%**, or **3.83% a year** on average.((Bank of England, [Inflation calculator](https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator), queried 2026-10-03.))

The Bank's remit is a CPI inflation target of **2%**, set by the Chancellor every year. If inflation moves more than 1 percentage point from it in either direction, the Governor has to write an open letter to the Chancellor explaining why, what the Bank is doing about it, and when inflation will come back. Since June 2020 there have been **twenty** of those letters.

This post does three things:

1. Measures the miss properly, from December 2019 (the last pre-Covid print) to August 2026 (the latest ONS release), against what a 2% path would have delivered.
2. Summarises what the twenty letters said: what they blamed, what they forecast, and what happened next.
3. Critiques the explanations, sets the miss against M4 broad money from 2000 onward, and covers the September 2026 MPC meeting's 6–3 split.

---

## The miss, measured

### December 2019 to August 2026

Using the ONS CPI index (series D7BT, 2015 = 100): 108.5 in December 2019, 143.6 in August 2026.((Office for National Statistics, [CPI index 00: all items 2015=100 (D7BT)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23) and [CPI annual rate 00: all items (D7G7)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23), fetched 2026-10-03.))

| Measure | Actual | At 2% target | Gap |
|---|---|---|---|
| Period | Dec 2019 → Aug 2026 (80 months, 6.67 years) | same | |
| Cumulative price rise | **+32.4%** | +14.1% | 2.3× the target path |
| Annualised compound rate | **4.29%** | 2.00% | +2.29pp a year, every year |
| £1,000 at Dec 2019 prices | £1,324 | £1,141 | £183 |
| Price level vs 2% path | | | **16.0% above** |
| Months with CPI inside 1–3% | 26 of 80 | | 33% of the time |
| Months above 3% | 43 of 80 | | |
| Months below 1% | 11 of 80 | | |
| Peak 12-month rate | 11.1% (Oct 2022) | | |

The compound rate is the number that matters. A one-year overshoot can be called a shock. Inflation averaging **more than double** the target, compounded over nearly seven years, is a regime outcome.

The contrast with the previous two decades is stark. From December 1999 to December 2019 UK CPI compounded at **2.03% a year**, and the average 12-month rate over 2000–2019 was **2.04%**. Over twenty years the framework hit its target almost exactly. Over the last seven it has not come close.

### Reconciling with the BoE calculator

My numbers differ slightly from the calculator, and the difference comes down to method:

- **Base.** For past years the calculator uses the calendar-year average CPI. The 2019 average was 107.8, a little below December 2019's 108.5. On that base the rise to August 2026 is 33.2%, close to the calculator's 33.0%.
- **Annualisation.** The calculator's 3.83% only reproduces if the 33% is spread over about 7.7 years (I get 3.81%), which is the same as counting from January 2019. Dividing by 7 years gives 4.18%; measuring from December 2019 gives 4.29%.

So the calculator's "average annual inflation" counts a year of near-target 2019 inflation that came before the problem. That makes 3.83% the *flattering* version of the figure. Measured from the last pre-Covid print, the compound rate is 4.29%.

{{< figure src="/images/economics/inflation-since-2019-cpi-vs-target.png" caption="Top: CPI 12-month rate against the 2% target and the 1–3% band, with each of the 20 Governor's open letters marked. Bottom: actual price level vs a 2% compound path (Dec 2019 = 100), and the running annualised compound rate since Dec 2019 (right axis). Source: ONS D7BT/D7G7, Bank of England; own calculation." >}}

The bottom panel shows why "inflation is back near target" is the wrong way to judge the period. The 12-month rate has been near 3% since 2024, but the **price level** never comes back down. The Bank targets the inflation *rate*, not the price *level*, so the 16% overshoot is permanent: nothing in the framework claws it back. The running compound rate (blue) peaked near 5.7% in mid-2023 and is still 4.3% after six and a half years.

---

## The twenty letters, summarised

All twenty Governor-to-Chancellor letters since 2020 are listed below, with the CPI print that triggered each one and the Bank's own explanation.((Bank of England, [Letters sitemap](https://www.bankofengland.co.uk/sitemap/letters); HM Treasury, [Open letters between the Governor of the Bank of England and the Chancellor of the Exchequer](https://www.gov.uk/government/collections/hmt-open-letters-between-the-governor-of-the-bank-of-england-and-the-chancellor-of-the-exchequer).)) All are signed by Andrew Bailey.

| # | Date | Trigger CPI | Reasons given | Bank's projection | Policy at the time |
|---|---|---|---|---|---|
| 1 | 18 Jun 2020 | 0.8% (Apr 20) | Oil price collapse (~40%), Covid spare capacity, weak clothing/footwear | Rise during 2021; target in ~2 years | Bank Rate 0.1%; QE +£100bn |
| 2 | 17 Sep 2020 | 0.2% (Aug 20) | VAT cut on hospitality, Eat Out to Help Out, oil, slack | Below 1% until around year-end; ~2% in two years | 0.1%; QE £745bn programme |
| 3 | 17 Dec 2020 | 0.3% (Nov 20) | Pandemic demand hit, VAT cut, oil 25% down | ~½% over winter, then "rising quite sharply towards the target" | 0.1%; QE +£150bn to £875bn gilts |
| 4 | 6 May 2021 | 0.4% (Feb 21) | Fuel and energy falls, weak clothing demand | **Temporarily above 2% late 2021**, then back to 2% | 0.1%; no tightening until "clear evidence" slack is gone |
| 5 | 23 Sep 2021 | 3.2% (Aug 21) | Base effects, energy bills, commodities, supply bottlenecks, reopening | Slightly above 4% in Q4 21; cost pressures "transitory" | 0.1%; no change |
| 6 | 16 Dec 2021 | 5.1% (Nov 21) | Supply chains, goods demand, energy (1½pp) | **Peak ~6% in April 2022** | First hike: +0.15pp to 0.25% |
| 7 | 17 Mar 2022 | 5.5% (Jan 22) | Energy and core goods >4/5 of overshoot; used cars; Russia's invasion of Ukraine | **Peak ~8% in Q2 22**, a little above 2% in two years | +0.25pp to 0.75% |
| 8 | 16 Jun 2022 | 9.0% (Apr 22) | Energy and the war, goods rotation, tight labour market, firms' pricing | Slightly above 11% in October | +0.25pp to 1.25% |
| 9 | 22 Sep 2022 | 9.9% (Aug 22) | Energy, food, broadening domestic pressure; labour market "tighter for longer than expected" | Just under 11% in October | +0.5pp to 2.25% |
| 10 | 15 Dec 2022 | 10.7% (Nov 22) | Energy, food at 16.4%, wages ~7%, services 6.3% | Peak passed; below 2% in years 2–3 | +0.5pp to 3.5% |
| 11 | 23 Mar 2023 | 10.4% (Feb 23) | Food at 18%, energy, tight labour market | "Just under 4%" by end-2023 | +0.25pp to 4.25% (same day) |
| 12 | 22 Jun 2023 | 8.7% (May 23) | Services 7.4%, wages 7.6%, second-round effects | Medium term; risks "skewed significantly to the upside" | +0.5pp to 5.0% |
| 13 | 21 Sep 2023 | 6.7% (Aug 23) | External shocks feeding second-round wage and price effects | **2% in Q2 2025** | Held at 5.25%; QT £100bn/yr |
| 14 | 14 Dec 2023 | 4.6% (Oct 23) | As above; services falling faster than expected (airfares) | **2% by end-2025** | Held at 5.25% |
| 15 | 21 Mar 2024 | 3.4% (Feb 24) | Services still 6.1%, wage growth | 2.3% in two years, 1.9% in three | Held at 5.25% |
| 16 | 19 Jun 2025 | 3.4% (May 25) | Energy, water bills, VED, food, employer NICs, packaging regulation | Peak 3.5% in Q3 25; back to target in 2026; rise "temporary" | Held at 4.25% |
| 17 | 18 Sep 2025 | 3.8% (Aug 25) | Food 5.1%, administered prices, services 4.7%, employer NICs | **Peak 4.0% in Sep 25**; falls through 2026 | Held at 4.0%; QT £70bn |
| 18 | 18 Dec 2025 | 3.2% (Nov 25) | Food, administered prices (0.4pp), labour costs | **Close to 2% from April 2026** | −0.25pp to 3.75% |
| 19 | 30 Apr 2026 | 3.3% (Mar 26) | Middle East conflict, Strait of Hormuz, motor fuel, services 4.5% | 3.3% in Q3 26, 1.4pp above February's forecast | Held at 3.75% |
| 20 | 17 Sep 2026 | 3.1% (Aug 26) | Middle East energy shock: petrol 130p→170p, diesel 140p→190p; agricultural commodities +20% | ~3¾% in Q4 26, slightly above 4% early 2027; back towards target through 2027 | Held at 3.75% (6–3 vote) |

Sources for each row: the Governor's letter PDFs on bankofengland.co.uk and gov.uk (listed at the end). One timing quirk: no letters were written between March 2024 and June 2025, because CPI stayed inside the 1–3% band from April 2024 to March 2025.

### What the letters say, by phase

**1. The undershoot (letters 1–4, 2020–21).** Covid, a collapsing oil price, the hospitality VAT cut and Eat Out to Help Out pushed CPI to 0.2%. The response was aggressive: Bank Rate cut to 0.1%, and gilt QE raised by £450bn over 2020, to £875bn. The May 2021 letter already expected inflation to go "temporarily" above 2% later that year, yet it kept the commitment not to tighten until there was "clear evidence" that spare capacity was being eliminated.

**2. "Transitory" (letters 5–6, late 2021).** The September 2021 letter said the Committee's central expectation was that elevated global cost pressures "will prove transitory". CPI was 3.2% and Bank Rate was 0.1%. By December CPI was 5.1% and the first hike was 15 basis points.

**3. War and energy (letters 7–10, 2022).** Russia's invasion of Ukraine became the main explanation. The June 2022 letter made the central defence of the period: "This real economic adjustment is something monetary policy is unable to prevent." The hiking cycle sped up to 50bp moves, but from a starting point of 0.1%.

**4. Persistence (letters 11–15, 2023–24).** The story moved from external shocks to *second-round effects*: wages at 7–8%, services at 6–7%, and a labour market "tighter for longer than expected". Bank Rate peaked at 5.25%. Return-to-target dates were given (Q2 2025, then end-2025), and CPI did briefly touch 2.0% in May–June 2024.

**5. The relapse (letters 16–18, 2025).** Inflation came back without a global shock. The explanations were mostly **domestic and policy-made**: higher water bills and Vehicle Excise Duty, Ofgem cap moves, the April 2025 rise in employer National Insurance Contributions, packaging regulation, and food. Every letter called the rise "temporary".

**6. The Middle East (letters 19–20, 2026).** The conflict from late February 2026, with shipping disruption through the Strait of Hormuz, pushed fuel and gas prices sharply higher. The April 2026 letter's Q3 forecast was 1.4pp above February's. The September letter projects CPI above 4% in early 2027.

---

## Critique

### 1. Every letter blames something the Bank doesn't control

Across twenty letters the stated causes are almost all exogenous: oil, Covid, VAT, supply chains, war, energy caps, water bills, NICs, food, the Middle East. The Bank's own policy stance is never listed as a cause. The closest any letter comes is September 2022, which accepted that the labour market "has remained tighter for longer than expected a year ago".

That framing is partly fair. A central bank can't stop an energy price spike raising the measured price level in the first round. But the remit does not ask the Bank to stop shocks. It asks the Bank to stop shocks from *persisting*. On that test the record is weak: 54 of 80 months outside the band, and a second, separate overshoot in 2025 with no war to explain it.

### 2. The forecasts in the letters kept missing, mostly in one direction

The letters set the Bank's own test, and the Bank failed it repeatedly:

| Letter | Projection | Outturn |
|---|---|---|
| Sep 2021 | "Slightly above 4%" in Q4 2021, transitory | 4.2%, 5.1%, 5.4% |
| Dec 2021 | Peak ~6% in April 2022 | 9.0% in April, 11.1% in October |
| Mar 2022 | Peak ~8% in Q2 2022 | 9.0–9.4% |
| Sep 2023 | 2% in Q2 2025 | 3.5%, 3.4%, 3.6% in Q2 2025 |
| Jun 2025 | Peak 3.5% in Q3 2025 | 3.8%, 3.8%, 3.8% |
| Dec 2025 | Close to 2% from April 2026 | 2.8% (then a new shock) |

Some calls were right. The June and September 2022 letters got the 11% October peak almost exactly, and the September 2025 letter's 4% peak turned out *too high*. But the big misses were all early and all on the low side, made while policy was being set at 0.1%. A forecasting system that consistently puts inflation back at 2% "at a conventional horizon of around two years" (a phrase repeated in nearly every 2020–22 letter) becomes, in practice, a reason for delay.

The Lords Economic Affairs Committee made the same point in November 2023. It said the Bank's forecasts "seldom predict anything other than a return to the two per cent target", and that the "transitory" view held in 2020–21 "was not challenged, at least publicly".((House of Lords Economic Affairs Committee, *Making an independent Bank of England work better*, 27 November 2023, as reported by [Mortgage Solutions](https://www.mortgagesolutions.co.uk/news/2023/11/27/bank-of-england-reform-needed-after-inflation-errors-lords-say/).)) The Bernanke review (April 2024) found shortcomings in the Bank's forecasting infrastructure and made 12 recommendations, all of which the Bank accepted.((Bank of England, [Forecasting for monetary policy making and communication: a review](https://www.bankofengland.co.uk/news/2024/april/forecasting-for-monetary-policy-making-and-communication-a-review), 12 April 2024.))

### 3. The response was asymmetric

When CPI was 1.2–1.8pp *below* target in 2020, the Bank cut to an all-time low and added £450bn of QE within months. When CPI was 1.2pp *above* target in August 2021 and climbing, it waited four months and then moved 15bp. A symmetric target applied asymmetrically produces an upward bias, and that is exactly what the compound rate shows.

### 4. The letters are explanations, not accountability

The letter mechanism is procedural. The Chancellor replies, usually with thanks and confidence in the Bank. Nothing changes as a result: there is no penalty, no review trigger, and no requirement to explain *past* forecast errors as opposed to the current deviation. After twenty letters the format is predictable: a list of causes, a projection that inflation will return to target in the medium term, and a promise that the MPC "stands ready". The Bernanke review fixed forecasting plumbing. It did not change what happens when the Bank misses for seven years.

### 5. The fair counter-arguments

- **Supply shocks.** Most of the 2021–23 overshoot was imported (energy, food, goods). Raising rates hard into a supply shock costs output without changing the first-round price effect. The remit explicitly lets the MPC trade off speed of return against output volatility.
- **Peers missed too.** The Fed and the ECB also called 2021 transitory and also overshot. Bernanke himself noted the Bank's challenges were "hardly unique". The UK's peak (11.1%) was higher, partly because of how the UK's household energy cap passes through.
- **Fiscal and regulated prices.** The 2025 relapse was largely administered prices and the employer NICs rise, which were government decisions the Bank had to absorb.
- **It eventually worked.** Inflation fell from 11.1% to 2.0% in 19 months once rates were at 5%+.

All true. None of it explains why the Bank was still at 0.1% with QE running in late 2021, or why a target that held for twenty years has compounded at more than double its level for seven.

---

## The money was saying it first: M4 broad money, 2000–2026

{{< figure src="/images/economics/inflation-m4-vs-cpi-2000-2026.png" caption="M4 broad money 12-month growth (left axis, BoE LPMVQJW, seasonally adjusted) against CPI 12-month inflation (right axis, ONS D7G7), January 2000 – August 2026. Shaded: GFC and Covid-era QE. Source: Bank of England IADB, ONS; own calculation." >}}

Broad money barely appears in the twenty letters. The chart shows why it should have.((Bank of England, [Interactive Database: LPMAUYN (M4 amounts outstanding, SA) and LPMVQJW (M4 12-month growth, SA)](https://www.bankofengland.co.uk/boeapps/database/), fetched 2026-10-03.))

- **2020–21:** M4 growth jumped from 3.8% (Dec 2019) to a peak of **13.6% in February 2021**, the fastest since the GFC, as QE and Covid lending schemes created deposits. CPI was at 0.4% at the time.
- **20 months later**, CPI peaked at **11.1% (October 2022)**.
- **2023:** M4 *contracted*, down 3.9% year on year by September 2023, as Bank Rate reached 5.25% and QT ran. Disinflation followed through 2024.
- **2026:** M4 growth is back to **4–5%** (5.0% in June, the fastest since late 2022).

Across the full 2000–2026 sample, the correlation between CPI and M4 growth in the *same* month is **−0.20**. Against M4 growth **24 months earlier** it is **+0.41**, the highest of any lag tested between 0 and 36 months. Separately, the M4 *stock* grew **32.1%** from December 2019 to August 2026, almost exactly matching the **32.4%** rise in the CPI index over the same months.

Caveats, because this relationship is not a law:

- **2000–2007:** M4 grew 9–14% a year (9.2% average) while CPI stayed near 2%. Much of that was money held by financial intermediaries, not households, and velocity was falling.
- **2009–2019:** QE did not produce consumer price inflation; M4 growth averaged about 1% over 2010–19.
- The 2020 episode was different because the new money landed with households and firms (furlough, bounce-back loans) at the same time as a supply shock, rather than staying inside the banking system.

So money growth is an indicator, not a mechanism you can set a dial with. But it was a large, public, real-time signal in 2020–21 that a forecasting framework built around output gaps and expectations mostly set aside. I go through the monetarist argument in more depth in [Inflation and Broad Money](/blog/economics/inflation-broad-money/), and the measurement problems in [Why Inflation Measurement Is Harder Than You Think](/blog/economics/inflation-measurement/).

---

## The latest meeting: September 2026, a 6–3 split

At its meeting ending **16 September 2026**, the MPC voted **6–3 to hold Bank Rate at 3.75%**. Three members voted to **raise it by 25bp to 4%**.((Bank of England, [Monetary Policy Summary and minutes, September 2026](https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2026/september-2026), 17 September 2026.))

| Hold at 3.75% (6) | Hike to 4.0% (3) |
|---|---|
| Andrew Bailey (Governor) | Megan Greene |
| Sarah Breeden | Catherine L Mann |
| Swati Dhingra | Huw Pill |
| Clare Lombardelli | |
| Dave Ramsden | |
| Alan Taylor | |

**The backdrop.** Brent was up 36% and UK wholesale gas 78% on July Report levels, at about $106/bbl and 207p/therm. Energy prices are tracking the July *adverse* scenario rather than the central case. CPI is projected at about 3¾% in Q4 2026 and slightly over 4% early in 2027, just as the spring wage round happens. Services inflation has fallen to 3.4% from 4.5% in March, unemployment is 4.9%, and underlying pay growth is estimated at about 3½%.

**The hold camp is not one camp.** It splits into two:

- **Leaning towards a hike (Bailey, Breeden, Lombardelli, Ramsden).** All four say the risks have moved up and that the case for tightening is building. Bailey said that if the conflict persists "it is likely that policy may have to tighten". Lombardelli said the case for raising rates "is building the longer the conflict continues". What holds them back is that indirect energy pass-through has so far been weaker than expected, and there is little evidence yet of second-round effects.
- **Dovish (Dhingra, Taylor).** Both put weight on slack, restrictive financial conditions, and Bank Rate still being well above European peers. Taylor puts neutral at 3%, so 3.75% is already "firmly restrictive". He argues policy should respond to evidence that the shock is spreading "rather than mechanically to volatile ticks in headline energy prices", and he raises the possibility of *easing* if tensions fade.

**The hikers (Greene, Mann, Pill)** make a risk-management case:

- **Slack has already peaked**, given stronger GDP and signs of employment growth. Slack was the main argument for expecting limited second-round effects (Greene).
- **Timing.** The inflation peak in early 2027 lands on the wage-setting round, and energy and food are the prices households notice most (Mann).
- **Asymmetric costs.** Setting policy *as if* second-round effects will be strong and correcting later is cheaper than the reverse. Waiting for definitive evidence "would leave policy behind the curve" (Greene).
- **Signalling.** A hike "sends a clear signal" of commitment amid "the fog of geopolitical conflict" (Pill). Pill also points to wider, slower-moving pressures: weather, fiscal dynamics and the AI build-out.
- **Market pricing** of a prolonged hold before the latest escalation was "hard to square with achieving the 2% target" (Mann).

**QT was unanimous.** The MPC voted to run the remaining £488bn gilt stock down to **zero by the end of 2034**, at an average £46bn a year (£20bn of active sales plus maturities). It also explored implementing sales through HM Treasury and the DMO.

**Reading the split against the twenty letters.** This is the first time in the episode that the argument inside the MPC is mainly about **the cost of being late**. The hikers are effectively arguing the critique above: waiting for proof of persistence is how 2021 happened. The majority's reply, through Taylor, is that this time policy is already restrictive and slack is real, which was not true at 0.1% in 2021. Both sides can be right on the facts. What 2021–2026 shows is that the Bank has paid more for waiting too long than for moving too early.

---

## Conclusion

- **The miss:** +32.4% on prices in 80 months, 4.29% a year compounded against 2.00%, and a price level 16% above the target path that the framework will never claw back.
- **The letters:** twenty explanations, almost all citing external shocks, with return-to-target projections that missed repeatedly and mostly on the low side, worst in 2021 when policy was at its loosest.
- **The money:** M4 growth peaked about 20 months before CPI and contracted before the disinflation. Over this cycle it was a better early warning than the Bank's forecasts, although its record over 2000–2019 is too mixed to treat it as a rule.
- **Now:** CPI has been at or above 3% in 13 of the last 18 months and is heading for 4% again, and three of nine MPC members want to move before the evidence is complete. On the 2021 record, that is the lesson the remit letters never quite admit to.

---

### Sources

- Bank of England — [Inflation calculator](https://www.bankofengland.co.uk/monetary-policy/inflation/inflation-calculator)
- Office for National Statistics — [CPI index D7BT](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23), [CPI annual rate D7G7](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23)
- Bank of England — [Interactive Database](https://www.bankofengland.co.uk/boeapps/database/) (LPMAUYN, LPMVQJW)
- Bank of England — [Inflation and the 2% target](https://www.bankofengland.co.uk/monetary-policy/inflation); [letters sitemap](https://www.bankofengland.co.uk/sitemap/letters)
- Governor's letters to the Chancellor: [Jun 2020](https://www.bankofengland.co.uk/-/media/boe/files/letter/2020/governor-cpi-letter-june-2020.pdf), [Sep 2020](https://www.bankofengland.co.uk/-/media/boe/files/letter/2020/governor-cpi-letter-september-2020.pdf), [Dec 2020](https://www.bankofengland.co.uk/-/media/boe/files/letter/2020/governor-cpi-letter-december-2020.pdf), [May 2021](https://www.bankofengland.co.uk/-/media/boe/files/letter/2021/may/governor-cpi-letter-may-2021.pdf), [Sep 2021](https://www.bankofengland.co.uk/-/media/boe/files/letter/2021/september/governor-cpi-letter-september-2021.pdf), [Dec 2021](https://www.bankofengland.co.uk/-/media/boe/files/letter/2021/governor-cpi-letter-december-2021.pdf), [Mar 2022](https://www.bankofengland.co.uk/-/media/boe/files/letter/2022/march/governor-cpi-letter-march-2022.pdf), [Jun 2022](https://www.bankofengland.co.uk/-/media/boe/files/letter/2022/june/governor-cpi-letter-june-2022.pdf), [Sep 2022](https://www.bankofengland.co.uk/-/media/boe/files/letter/2022/september/governor-cpi-letter-september-2022.pdf), [Dec 2022](https://www.bankofengland.co.uk/-/media/boe/files/letter/2022/december/governor-cpi-letter-december-2022.pdf), [Mar 2023](https://assets.publishing.service.gov.uk/media/641c40325155a2000c6ad51b/Open_CPI_Letter_-_March_2023_-_23_March.pdf), [Jun 2023](https://assets.publishing.service.gov.uk/media/64942c3fde86820013bc8c25/CPI_open_letter_-_June_2023_-_Final_22062023_0845.pdf), [Sep 2023](https://www.bankofengland.co.uk/-/media/boe/files/letter/2023/governor-cpi-inflation-letter-september-2023.pdf), [Dec 2023](https://www.bankofengland.co.uk/-/media/boe/files/letter/2023/governor-cpi-inflation-letter-december-2023.pdf), [Mar 2024](https://www.bankofengland.co.uk/-/media/boe/files/letter/2024/governor-cpi-inflation-letter-march-2024.pdf), [Jun 2025](https://www.bankofengland.co.uk/-/media/boe/files/letter/2025/governor-cpi-inflation-letter-june-2025.pdf), [Sep 2025](https://www.bankofengland.co.uk/-/media/boe/files/letter/2025/governor-cpi-inflation-letter-september-2025.pdf), [Dec 2025](https://www.bankofengland.co.uk/-/media/boe/files/letter/2025/governor-cpi-inflation-letter-december-2025.pdf), [Apr 2026](https://www.bankofengland.co.uk/-/media/boe/files/letter/2026/governor-cpi-inflation-letter-april-2026.pdf), [Sep 2026](https://www.bankofengland.co.uk/-/media/boe/files/letter/2026/governor-cpi-inflation-letter-september)
- Bank of England — [Monetary Policy Summary and minutes, September 2026](https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2026/september-2026)
- Bank of England — [Bernanke review of forecasting](https://www.bankofengland.co.uk/news/2024/april/forecasting-for-monetary-policy-making-and-communication-a-review)
- House of Lords Economic Affairs Committee — *Making an independent Bank of England work better* (Nov 2023), via [Mortgage Solutions](https://www.mortgagesolutions.co.uk/news/2023/11/27/bank-of-england-reform-needed-after-inflation-errors-lords-say/)

*Data and script: `static/data/economics/uk_cpi_m4_monthly_1999-2026.csv`, `static/data/economics/inflation_since_2019_charts.py`.*

*Editorial note (draft): (1) The letter summaries come from automated reads of each PDF. Spot-check the quoted phrases and forecast numbers against the originals before publishing, especially the forecast-miss table. (2) The Lords committee quotes are taken from press coverage, not the report itself; swap in the parliamentary link. (3) QE totals for 2020 are from the letters (gilts only). (4) The 24-month M4 lead correlation is a full-sample statistic and is unstable across sub-periods (see caveats). Set to draft pending review.*
