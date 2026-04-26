---
title: "Interest Rates Are Interesting"
date: 2026-04-03T09:42:06Z
draft: true
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

This going to be one of probably many sessions on interest rates. It is a vast subject, and influences our lives every day no matter how we live our lives. To restate the blinding obvious one more time. I am not an economist, nor am I trained in the dismal sciences. Hopefully I am moderately less than useless at data. Lets see I guess.

---

## Section One

What is an interest rate? Not what you think for a start. Ever *really* read a loan document, one suspects not.

Hey, its just 10.00%. Maybe with a p.a. suffix? Ahhh, no. Sorry, not how the math works.

Interest requires (i) a rate of interest; and (ii) the periodicity in which it is applied. You must have both. *Both* I say!

Lets take the perception of 10.00% More on decimal places, or significant figures, later. 10.00% per annum means what it says on the tin. 10.00%, per annum. So if you borrow or lend $100, at the end of the year you pay or receive $10. Job done. Not. What about if you pay $10, spread over each month. Hey, that's just $1.20, no problem. Wrong again. You need to know the rate of interest, and you need to know the compounding frequency. 10.00% per annum /per annum is not the same thing as 10.00% per annum / per month. See chart below for the compounding difference this makes over longer time frames. Here is 10.00% per annum, compounded at frequence from annual, down to daily, with totals shown.


## Math

### Annual Compounding

$$
A_{\text{annual}} = 1000 \times (1 + 0.10)
$$

$$
A_{\text{annual}} = 1000 \times 1.10 = 1100.00
$$

$$
\text{Interest} = 1100.00 - 1000 = 100.00
$$

---

### Daily Compounding

$$
A_{\text{daily}} = 1000 \times \left(1 + \frac{0.10}{365}\right)^{365}
$$

$$
A_{\text{daily}} \approx 1000 \times 1.105155 = 1105.155
$$

$$
\text{Interest} \approx 1105.155 - 1000 = 105.155
$$

---

### Difference

$$
\Delta = 105.155 - 100.000 = 5.155
$$

| Compounding Type | Final Amount ($) | Interest Earned ($) | Effective Annual Rate | Extra vs Annual ($) |
|------------------|------------------|----------------------|------------------------|----------------------|
| Annual (1×)      | 1100.000         | 100.000              | 10.0000%              | 0.000 |
| Daily (365×)     | 1105.155         | 105.155              | 10.5155%              | 5.155 |


Compounding matters. If you re calculate the interest at 10.00%, every single day, the notional accretor on which you are applying interest rises over time. In dollar terms, more interest. Potentially a lot more in cash terms. Bet you wish you read the loan docs about now.....

Now the above is for constant interest, where the rate of interest is set, and does not change. This is generally known as fixed rate. Interest rates can reference dynamic in interest rates, which can change, or vary. These are know as variable interest rates. This matters, which will be explored in full. In short summary, fixed rates give you certainty. If interest rates rise, you are winning, if interest rates fall, you will feel like you paid too much. Variable rates allow for rates to drop (good for borrowers), or rise (bad for borrowers). There are pros and con's for each. They have their applications. Basically, if you want certainty, you will have to pay for it in some fashion at the moment of entering into a contract. 

Yield, means the effective interest rate at a moment in time, that a bond sells for. Much more on this later. The yield curve then, is the term structure of interest rates, where the interest rate at 0.5 years could be quite different than the interest rate for 10 years, or even 30 years. Again, details matter, more later.

For now lets look at how interest rates have changed over time. Here is a set of statistical analyses for UK interest rates. This means the term structure of rates, or the yield curve, at any point in time, compared over time.

There is a lot going on here, it will explained in good time. This is the shotgun approach common at the start of data analytics (but only the start), where you run a bulk chart pack. Then the idea is you spend a long time thinking about that it all means, what the relationships are, how it reflects IRL reality, etc. Then you re do and tweak the actually meaningful charts.

{{< figure src="/images/economics/01_boxplots.png" caption="Rate distributions by maturity" >}}

{{< figure src="/images/economics/02_histograms.png" caption="Frequency distributions across the yield curve" >}}

{{< figure src="/images/economics/03_steepness_histogram.png" caption="Yield curve steepness frequency" >}}

{{< figure src="/images/economics/04_time_series.png" caption="Interest rate history by maturity" >}}

{{< figure src="/images/economics/05_steepness_time_series.png" caption="Yield curve steepness over time" >}}

{{< figure src="/images/economics/06_correlation_heatmap.png" caption="Rate correlation across maturities" >}}

{{< figure src="/images/economics/07_rolling_volatility.png" caption="Rolling rate volatility by regime" >}}

{{< figure src="/images/economics/08_fan_chart.png" caption="Projected rate path fan chart" >}}

{{< figure src="/images/economics/09_stats_table.png" caption="Summary statistics across maturities" >}}

<!-- {{< figure src="/images/economics/10_spot_curve_animation.gif" caption="Yield curve shape evolution animated" >}} -->

### Historical Yield Curve in action

I like this little animation, it give you a perspective you don't get from the data. The bottom segment is just the steepness factor. It might not be good for anything other than context, but it is one of my favorite ways of considering interest rate environments over time. You can see from both images that the term structure of rates has really flattened over time. There are two ways of flattening, a stable long term rate with a sharp pick up in the front end of the curve, caused by central banks doing their thing; or just a lower, flatter yield curve.

The Bank Rate is the short end of the curve, this sets near term rates. In theory the long end of the curve is set by the market, who create the term structure of bond yields. But that concept got diluted by central banks discovering Quantitative Easing. This is where the central bank buys the longer end of the curve, thereby suppressing rates. That subject deserves a blog of its own, as its a pseudo fiscal policy framework run by an institution without a mandate for fiscal activity. Actually, that needs a couple of book, not just a post.

<iframe 
  src="/tools/yield_curve_player.html"
  width="100%" 
  height="650" 
  style="border:none;"
  loading="lazy">
</iframe>


The source of this data is the Bank of England. Now sadly its a zip file and no one has thought to put it up accessible via API (go on, please do this is important data for research!), but at least the data is there. Its also quite messy, I will put the combined cleaned up csv file in resources section. But it does the job of showing the changes over time. As at 02 Apr 2026 when I did this. I'll try and update periodically.


[Bank of England – What are interest rates?](https://www.bankofengland.co.uk/explainers/what-are-interest-rates)

[Bank of England - Historical rates zip files](https://www.bankofengland.co.uk/statistics/yield-curves)

---

## Price vs Yield, what is going on?

Maths eventually, but as usual it is important to really understand the principles first. As a comp science lecturer once advised me, the two most important tools in programming at 1. pencil; and 2. paper. In other words do always think it through.

* Scenario A: $100 bond, pays interest of 6.00% pa semi, 10 year tenor, 3 yrs TTM. All dates even forget accrued interest.
* Scenario B: $100 bond, pays interest of 2.5% pa semi, 15 year tenor, 3 yrs TTM. All dates even forget accrued interest.
* Macro: at time t =0, or now, the 3 year zero coupon rates for 3 years is 4.00%. It just is, don't ask why. Same compound period.

Which bond is par? Which bond is more valuable than the other? How do you know FV?

Bond A pays 6.00% interest. Prevailing rates are 4.00% to TTM point. Is 6 better than 4? Yes. So you would expect this to me more valuable, and trade above par. In an efficient market, other than credit risk it would earn you the all in equivalent YTM of 4.00% yield.

Bond B pays 2.5% cash. Interest rates are higher than that in the market. This sounds like a losing deal. Why would you pay full price for that? You wouldn't.

You get the idea now. When doing this, or fixed rate loans, or especially derivatives like swaps, always try and keep in your head if the trade is in the money or out of the money, and who is which, and WHY.


Par, from the latin, means equal, like, well-matched, or even. Specifically in our case it means that the equal part is that the bond, fair valued, trades at ratio of notional to price of 100c in the dollar. So if the bond notional was say $100,000,000.00; then the purchase price would be $100,000,000.00 at that moment in time.

Now, other than potentially for about one second on the day of issuance, bonds don't really ever trade at par. At large notionals, there is always at least a small difference in price as yield curve at moment issued will never be exactly repeated. This is the same as saying that no bond will ever practically trade at par once issued. Probably.

Time to talk a little dirty now... eeew, no not like that! Clean versus dirty prices can be quite confusing if you just look at the math. What is really going on is that you are not always going to be paying cash for a bond on a coupon date, or the exact date you receive interest payment. Lets say its a semi annual coupon bond, for argument sake 01 Jan and 01 Jun. If you buy it, for whatever reason in October 01, no interest for you until January. Now if the seller does not adjust for the accrued interest that they would have been due to receive from Jun 01 to Oct 01, you are getting free money. Financial markets, for all their many sins, are pretty good about not letting such things happen. So you have to adjust for this in the price, hence 'clean' versus 'dirty' pricing. Dirty is what you pay for is how to remember. You want to know clean price for value, you need dirty price as that is what you settle on, being the full valuation of future payments, adjusted for accrued interest.

## Clean vs Dirty Price in Bond Valuation

### Key Idea
- **Dirty Price (Full Price)** = Actual price paid for a bond  
- **Clean Price (Quoted Price)** = Price excluding accrued interest  

\[
\text{Dirty Price} = \text{Clean Price} + \text{Accrued Interest}
\]

---

## Accrued Interest

Between coupon dates, interest accrues linearly:

\[
\text{Accrued Interest} = C \times \frac{t}{T}
\]

Where:
- \( C \) = coupon payment per period  
- \( t \) = days since last coupon  
- \( T \) = total days in coupon period  

---

## Bond Pricing (Dirty Price)

The full (dirty) price is the present value of future cash flows:

\[
P_{\text{dirty}} = \sum_{i=1}^{n} \frac{C}{(1+y)^i} + \frac{F}{(1+y)^n}
\]

Where:
- \( C \) = coupon  
- \( F \) = face value  
- \( y \) = yield per period  
- \( n \) = number of periods  

---

## Clean Price

\[
P_{\text{clean}} = P_{\text{dirty}} - \text{Accrued Interest}
\]

---

## Intuition

- Coupons are paid periodically, but **interest accrues daily**
- When you buy a bond between coupon dates:
  - Seller has earned part of the next coupon
  - Buyer compensates via **accrued interest**
- Markets quote **clean price** to remove this time effect

---

## Example

Assume:
- Coupon = 5 annually
- 90 days into a 180-day period

\[
\text{Accrued Interest} = 5 \times \frac{90}{180} = 2.5
\]

If:
\[
P_{\text{clean}} = 98
\]

Then:
\[
P_{\text{dirty}} = 98 + 2.5 = 100.5
\]

---

## Summary

| Concept        | Formula                                      | Meaning |
|----------------|----------------------------------------------|--------|
| Dirty Price    | \( P_{\text{clean}} + AI \)                  | Actual transaction price |
| Clean Price    | \( P_{\text{dirty}} - AI \)                  | Quoted market price |
| Accrued Interest | \( C \times \frac{t}{T} \)                | Earned coupon since last payment |

---

## Key Takeaway

- **Dirty price = economic value**
- **Clean price = market convention**
- The difference is purely **timing of coupon accrual**

---

### Fixed Income Taxonomy:

| Term                     | Meaning                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| Time to Maturity (TTM)   | Remaining life of the bond                                              |
| Maturity                 | The final date when principal is repaid                                 |
| Remaining Term           | Synonym for TTM                                                         |
| Tenor                    | Term at issuance; sometimes used loosely for remaining maturity         |
| Face Value (Par)         | Amount repaid at maturity (typically 100 or 1,000)                      |
| Coupon Rate              | Annual interest rate paid on face value                                 |
| Coupon                   | Periodic interest payment (Coupon Rate × Face Value)                    |
| Yield to Maturity (YTM)  | Internal rate of return assuming bond held to maturity                  |
| Current Yield            | Annual coupon divided by current market price                           |
| Clean Price              | Bond price excluding accrued interest                                   |
| Dirty Price              | Bond price including accrued interest (actual transaction price)        |
| Accrued Interest         | Interest earned since last coupon payment                               |
| Fair Value               | Theoretical price based on discounted future cash flows                 |
| Market Price             | Price at which the bond is currently trading                            |
| Discount                 | When bond trades below par                                              |
| Premium                  | When bond trades above par                                              |
| Duration                 | Weighted average time of cash flows; measure of interest rate sensitivity|
| Modified Duration        | Price sensitivity to a change in yield                                  |
| Convexity                | Measure of curvature in price–yield relationship                        |
| Yield                    | General return measure (can refer to YTM, current yield, etc.)          |
| Spot Rate                | Yield for a zero-coupon bond at a specific maturity                     |
| Forward Rate             | Implied future interest rate derived from spot rates                    |
| Credit Spread            | Yield difference vs a risk-free benchmark                               |
| Default Risk             | Risk that issuer fails to make payments                                 |
| Liquidity Risk           | Risk of not being able to trade without price impact                    |
| Call Option              | Issuer’s right to redeem bond early                                     |
| Put Option               | Holder’s right to sell bond back early                                  |
| Callable Bond            | Bond with embedded call option                                          |
| Puttable Bond            | Bond with embedded put option                                           |
| Zero-Coupon Bond         | Bond with no coupons; issued at discount                                |
| Floating Rate Note (FRN) | Bond with variable coupon linked to a benchmark rate                    |


## Key Takeaways

- Point one
- Point two
- Point three

---

## References

- add csv file here at some point, cleaned version.
