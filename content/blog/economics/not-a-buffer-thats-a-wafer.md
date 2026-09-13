---
title: "Not a Buffer, That Is a Wafer: The Lords on the UK Fiscal Outlook"
date: 2026-09-13T00:00:00Z
draft: true
categories: ["economics"]
tags: ["gilts", "yield-curve", "uk-fiscal-policy", "duration", "interest-rates"]
description: "The Lords' 10 September fiscal outlook debate, a current UK gilt discount curve built from today's benchmark yields, and what that curve actually does to the price of a real long gilt sold back in 2013."
showToc: true
tocopen: true
cover:
  image: ""
  alt: ""
  caption: ""
---

## The debate: "not a buffer, that is a wafer"

On 10 September 2026 the House of Lords held a general debate on the UK's fiscal outlook, moved by Lord Bridges of Headley (Conservative).((Parallel Parliament, [Fiscal Outlook, Lords Chamber, 10 September 2026](https://www.parallelparliament.co.uk/lord/lord-bridges-of-headley/debate/2026-09-10/lords/lords-chamber/fiscal-outlook).)) It's worth a read in full, but the short version is that the numbers are not subtle.

Lord Bridges opened with the stock: national debt is nearly £3 trillion, 94% of GDP, up almost £96 billion in the past year, which he called "on an unsustainable path." His most quotable line was about the fiscal headroom the Chancellor is working with — down to roughly £5 billion, which he characterised as "not a buffer; that is a wafer." Fair, and also a genuinely good line, which is presumably why every summary of the debate leads with it, this one included.

The market side of his argument is the more interesting bit for this blog. He pointed out that the UK now has the highest 10-year borrowing costs in the G7, and the fourth-highest among advanced economies globally, and that a recent 30-year gilt sale cleared at the highest borrowing cost seen in almost three decades. Debt servicing is forecast at £110 billion for 2025-26 — 3.5% of national income, more than the education budget and closing in on double the defence budget — rising to £137 billion by 2030-31.

His diagnosis of *why* runs through the usual Opposition lines: higher business taxes and the Employment Rights Act (which he put at roughly £1 billion a year in direct cost) weakening growth, welfare spending up £75 billion a year with health and disability benefits up over a third, and the OBR's own estimate of potential growth stuck at 1.5% a year, with GDP per capita growing at 1.1% — roughly half the pre-financial-crisis trend. Other peers filled in around him: Lord Rooker and Lord Davies on the demographic backdrop, Lord Elliott on welfare dependency, Lord Howell on the fiscal cost of decarbonisation, and Lord Hill on the more general point that somebody in government needs to be honest in public about the trade-offs, rather than just in the OBR's small print. Bridges closed on the classic bond-market threat: defer the hard choices and the market makes them for you, "more painful and more costly" than if a Chancellor had chosen the timing.

None of this is new territory for this blog — the G20 sovereign-spreads post earlier this year covered the "vigilantes are voting" side of the story((See this blog's earlier piece on [G20 sovereign credit spreads](/blog/economics/g20-sovereign-credit-spreads/).)) — but a debate this gilt-market-heavy is a good excuse to actually look at what today's curve is pricing, and then do something Lord Bridges didn't: pick one real bond and show what "the highest borrowing costs in three decades" has done to it in cash terms.

## The curve itself

Here's the UK gilt curve as it stood on 11 September 2026, benchmark yields from 1 month out to 30 years.((Trading Economics, [United Kingdom Government Bond Yield](https://tradingeconomics.com/united-kingdom/government-bond-yield), accessed 13 September 2026.)) The top panel is the par yield curve; the bottom panel converts it into a discount factor curve — the price today of £1 received at each future date, which is the actual "discount curve" the title promised.

{{< figure src="/images/economics/fiscal-outlook-discount-curve.png" caption="UK gilt par yield curve and implied discount factors, 11 September 2026" >}}

The shape matches Bridges' framing precisely: short rates around 3.85–4.9%, and a long end that keeps climbing all the way to 30 years (5.91%) rather than flattening or inverting the way a "normal" curve eventually would. That persistent long-end premium — the market wanting more compensation the further out it lends to the UK government — is exactly the "term premium" story behind his "highest 30-year borrowing cost in almost three decades" line. £1 due in 10 years is worth about 59p today; £1 due in 30 years is worth about 17p. That second number is doing a lot of the work in "debt servicing to £137 billion by 2030-31" — every pound the DMO borrows long-dated from here gets discounted (from the buyer's side) and compounded (from the taxpayer's side) at close to 6%, not the 3–4% that was on offer for most of the 2010s.

One methodological note, in the spirit of flagging simplifications rather than pretending they don't exist: this is a *par* yield curve, not a bootstrapped zero curve. I've fitted it with a monotone (PCHIP) interpolation and then used the fitted par yield at each maturity as a proxy for the zero rate, discounting semi-annually. For a curve this smooth the difference between a proper bootstrapped zero curve and this shortcut is small — a few basis points at most maturities — but it's a shortcut, not a bootstrap, and a trading desk would not accept it as one.

## Finding an actual 3% gilt to reprice

The brief was to find a real UK gilt issued at a 3.00% coupon and reprice it off the curve above. Worth being upfront about what I actually found: **there is no conventional gilt currently in issue with an exact 3.00% coupon.** I checked the DMO's own gilts-in-issue data, the DMO's historic auction records, and three separate market data aggregators (giltsyield.com, the GILT Calculator, and Hargreaves Lansdown's gilt price list); the coupon ladder currently runs …2.5%, 3.25%, 3.5%, 3.75%… with nothing sitting on 3.00% exactly.((Cross-checked against [giltsyield.com's conventional gilts in issue](https://giltsyield.com/bond/) and [Hargreaves Lansdown's UK gilt price list](https://www.hl.co.uk/shares/corporate-bonds-gilts/bond-prices/uk-gilts).))

The closest real, currently-trading gilt is the **3¼% Treasury Gilt 2044** (ISIN GB00B84Z9V04, maturing 22 January 2044). It's a better match than the coupon alone suggests: the DMO first auctioned it on 16 May 2013, £2.5 billion nominal, at an average accepted price of £99.18 and an average accepted yield of **3.293%**((UK Debt Management Office, [3¼% Treasury Gilt 2044 — prospectus](https://www.dmo.gov.uk/media/cvgjgbmf/prosp070513.pdf); [16 May 2013 auction result](https://dmo.gov.uk/media/0gldljeu/160513conventional.pdf).)) — near enough par, and near enough a 3.00% yield, that it's a fair stand-in for "a gilt priced at 3%" even though the coupon printed on the certificate is a quarter-point higher. So: a real gilt, sold into a real 3-ish-per-cent world in 2013, thirty-one years to maturity at issue, now sitting with 17.4 years left to run. That's about as clean a "before" snapshot as the market offers for this exercise.

## What the curve does to it

Discount the 3¼% 2044's remaining cash flows — 35 semi-annual coupons of £1.625 per £100 nominal plus the £100 redemption, from 13 September 2026 to 22 January 2044 — using the curve above, and the result is:

| | 2013 issue | 13 Sep 2026, off today's curve |
|---|---|---|
| Price (per £100 nominal) | £99.18 | £73.47 clean / £73.94 dirty |
| Equivalent flat yield | 3.29% | 5.67% |
| Years to maturity | 31.0 | 17.4 |

A gilt sold at essentially par in 2013 is worth about £73.47 clean today — a fall of roughly 26 points, or about a quarter of face value, holding no default risk whatsoever. That's just the arithmetic of duration: nothing about the UK's credit quality has to move for a long-dated, fixed-coupon bond to lose a quarter of its value when the yield it's discounted at rises by 2.4 percentage points. It's the mechanical flip side of Lord Bridges' complaint. Higher gilt yields are bad for the Treasury's future borrowing costs, as he said; they are equally bad, right now, for anyone still holding the gilts the Treasury sold years ago at the old, lower rate — pension funds and insurers holding exactly this kind of paper for liability-matching among them.

## Zooming in: duration in one picture

The chart below takes that same 3¼% Treasury Gilt 2044 (issued 16 May 2013) and zooms the yield axis to the 3.00%–7.00% range specifically, plotting price against a flat (parallel) yield shock rather than the full curve, so the duration effect is isolated and visible as one clean line. A second line, on the right-hand axis, adds the total return an actual buy-and-hold investor would have realised: buy at the 2013 auction, hold through to today, sell at whatever price the yield on the x-axis implies, and add back every coupon actually collected along the way.

{{< figure src="/images/economics/fiscal-outlook-2044-gilt-repricing.png" caption="Price impact of rising yields on the 3¼% Treasury Gilt 2044, zoomed to the 3.00%–7.00% range, with total return since the 2013 purchase on the right-hand axis" >}}

The straight dashed line is a linear reference between the 2013 issue point and today's curve-implied point — the bond's actual price/yield line sits very slightly *above* that straight line across the whole range, which is convexity doing what convexity does (bond prices are a convex, not linear, function of yield — losses on the way up are a little smaller than a straight-line duration estimate implies, gains on the way down a little bigger). At this gilt's current yield, its Macaulay duration works out to about 12.5 years and modified duration to about 12.2. Rule of thumb: for every extra 100 basis points of yield, expect roughly a 12% price move in the opposite direction near current levels, tapering slightly as you move up the curve, which is exactly what the chart shows — steep, and very nearly straight, but not quite.

The total return line is the more human way of reading the same picture. Someone who bought this gilt at auction in May 2013 and sold it today, off the current curve, would have collected 27 semi-annual coupons of £1.625 along the way — £43.875 per £100 nominal, undiscounted — against a capital loss of about £25.71 (£99.18 down to £73.94 dirty). Net that out and the cumulative total return over 13.3 years is only about **19%**, which annualises to roughly **1.3% a year** — nominal, well before inflation, on a bond with a 3¼% coupon. That's the whole story of this post in one number: the coupon income was real, but the price decline nearly wiped it out, purely because yields backed up. Sell instead at the 3.00% end of the chart's range and total return jumps to about 49% (an investor who'd been lucky enough to sell before yields rose); sell at the 7.00% end and it falls to about 8%. Same bond, same coupons received, wildly different outcome depending entirely on where the curve happens to sit on the day you sell — which is duration risk stated as plainly as it gets.

Put in Lord Bridges' terms: the same market mechanism that produces "the highest 30-year borrowing cost in almost three decades" for new issuance is, cash-flow for cash-flow, the reason a 2013-vintage gilt has spent thirteen years paying a coupon and still barely broken even in nominal total-return terms. It's one curve, doing both things at once.

## The caveats, because they matter

A few things worth being explicit about before anyone treats these numbers as more precise than they are:

- The par-curve-as-zero-curve shortcut noted above. A proper OIS- or gilt-bootstrapped zero curve would move these prices by a handful of basis points, not by anything that changes the story.
- Day counts use a simple actual/365 approximation rather than the gilt market's actual actual/actual convention; again, a rounding-level effect at these maturities.
- The zoomed chart uses a *flat* yield shock applied to one bond's own cash flows, which is standard practice for showing duration/convexity in isolation, but is not the same exercise as re-pricing the bond off a *shifted curve* (which is what the first chart's discounting actually does). The two are consistent with each other at the two marked points by construction, but they answer slightly different questions — flat-yield sensitivity versus curve-consistent valuation — and shouldn't be blended.
- "Closest available gilt to a 3.00% coupon" is doing real work in this post. The 3¼% Treasury Gilt 2044 is a genuine, currently-traded instrument with a real DMO auction history, not a hypothetical — but it is a quarter-point off the brief's exact 3.00% figure, because that exact coupon doesn't currently exist in the gilt market. Better to say so than to quietly round.
- The total return figures simply sum the 27 coupons actually paid since 2013 — no reinvestment, no compounding, and no accrued-interest adjustment at either the 2013 purchase or the assumed sale. A real total-return calculation (reinvesting each coupon at prevailing short rates) would land a little differently, most likely a bit lower given how low reinvestment rates were for much of 2013–2021 — but not enough to change the headline: a decade-plus of holding a 3¼% gilt through this rate cycle has produced a nominal return closer to a savings account than to the coupon rate printed on the certificate.

---

### Sources

- Parallel Parliament — [Fiscal Outlook, Lords Chamber, 10 September 2026](https://www.parallelparliament.co.uk/lord/lord-bridges-of-headley/debate/2026-09-10/lords/lords-chamber/fiscal-outlook)
- Trading Economics — [United Kingdom Government Bond Yield](https://tradingeconomics.com/united-kingdom/government-bond-yield)
- UK Debt Management Office — [3¼% Treasury Gilt 2044 prospectus](https://www.dmo.gov.uk/media/cvgjgbmf/prosp070513.pdf)
- UK Debt Management Office — [16 May 2013 auction result, 3¼% Treasury Gilt 2044](https://dmo.gov.uk/media/0gldljeu/160513conventional.pdf)
- giltsyield.com — [Conventional gilts in issue](https://giltsyield.com/bond/)
- Hargreaves Lansdown — [UK gilt price list](https://www.hl.co.uk/shares/corporate-bonds-gilts/bond-prices/uk-gilts)

*Editorial note (draft): all pricing/duration figures above are author calculations from publicly published curve and auction data, not a market data terminal — worth a spot-check of the coupon-date assumptions (22 Jan/22 Jul) and the current benchmark yields against a second source (e.g. the DMO's own daily gilt prices) before this goes live. Set to draft pending review.*
