---
title: "Not a Buffer, That Is a Wafer: The Lords on the UK Fiscal Outlook"
date: 2026-09-13T00:00:00Z
draft: true
categories: ["economics"]
tags: ["gilts", "yield-curve", "uk-fiscal-policy", "duration", "interest-rates"]
description: "The Lords' 10 September fiscal outlook debate, a current UK gilt discount curve built from today's benchmark yields, and how the same rate volatility split one real gilt's realised return — capital, interest, and inflation-adjusted — eight different ways across its 2023 issuance tranches."
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

None of this is new territory for this blog — the G20 sovereign-spreads post earlier this year covered the "vigilantes are voting" side of the story((See this blog's earlier piece on [G20 sovereign credit spreads](/blog/economics/g20-sovereign-credit-spreads/).)) — but a debate this gilt-market-heavy is a good excuse to actually look at what today's curve is pricing, and then do something Lord Bridges didn't: pick one real bond and show what borrowing-cost volatility does to an actual buyer, in cash terms, split into what came from interest and what came from capital.

## The curve itself

Here's the UK gilt curve as it stood on 11 September 2026, benchmark yields from 1 month out to 30 years.((Trading Economics, [United Kingdom Government Bond Yield](https://tradingeconomics.com/united-kingdom/government-bond-yield), accessed 13 September 2026.)) The top panel is the par yield curve; the bottom panel converts it into a discount factor curve — the price today of £1 received at each future date, which is the actual "discount curve" the title promised.

{{< figure src="/images/economics/fiscal-outlook-discount-curve.png" caption="UK gilt par yield curve and implied discount factors, 11 September 2026" >}}

The shape matches Bridges' framing precisely: short rates around 3.85–4.9%, and a long end that keeps climbing all the way to 30 years (5.91%) rather than flattening or inverting the way a "normal" curve eventually would. That persistent long-end premium — the market wanting more compensation the further out it lends to the UK government — is exactly the "term premium" story behind his "highest 30-year borrowing cost in almost three decades" line. £1 due in 10 years is worth about 59p today; £1 due in 30 years is worth about 17p. That second number is doing a lot of the work in "debt servicing to £137 billion by 2030-31" — every pound the DMO borrows long-dated from here gets discounted (from the buyer's side) and compounded (from the taxpayer's side) at close to 6%, not the 3–4% that was on offer for most of the 2010s.

One methodological note, in the spirit of flagging simplifications rather than pretending they don't exist: this is a *par* yield curve, not a bootstrapped zero curve. I've fitted it with a monotone (PCHIP) interpolation and then used the fitted par yield at each maturity as a proxy for the zero rate, discounting semi-annually. For a curve this smooth the difference between a proper bootstrapped zero curve and this shortcut is small — a few basis points at most maturities — but it's a shortcut, not a bootstrap, and a trading desk would not accept it as one.

## Finding an actual 3% gilt — and a better story than planned

The original brief here was to find a real UK gilt issued at a 3.00% coupon and reprice it off the curve above. Worth being upfront: **there is no conventional gilt currently in issue with an exact 3.00% coupon** — I checked the DMO's own gilts-in-issue data and several market aggregators, and the coupon ladder runs …2.5%, 3.25%, 3.5%, 3.75%… with nothing sitting on exactly 3.00%.((Cross-checked against [giltsyield.com's conventional gilts in issue](https://giltsyield.com/bond/) and [Hargreaves Lansdown's UK gilt price list](https://www.hl.co.uk/shares/corporate-bonds-gilts/bond-prices/uk-gilts).)) A closer look at the DMO's full **Gilt Issuance History** (report D2.1E)((UK Debt Management Office, [Gilt Issuance History, report D2.1E](https://www.dmo.gov.uk/data/pdfdatareport?reportCode=D2.1E), data as of 13 September 2026.)) turned up something more useful than a coupon-matching exercise: the **3½% Treasury Gilt 2025** (ISIN GB00BPCJD880).

This gilt is a real curiosity for exactly the reason this post needs. It was issued in eight separate "outright" auction tranches through 2023, one of the most volatile years UK short rates have had in decades — the Bank of England was still hiking through most of it. Because the coupon (3.5%) was fixed at first issuance and every subsequent tranche was a reopening of the *same* stock, the price moved instead of the coupon: from £99.65 at the first tranche (18 January 2023, yield 3.633% — about as close to "issued at 3%" as this exercise is going to get) down to £95.38 at the cheapest tranche (6 July 2023, yield 5.668%), before recovering to £98.10 by the last full tranche (30 November 2023, yield 4.553%).((All issue prices, yields and nominal amounts from the DMO Gilt Issuance History, report D2.1E; tranche dates and amounts cross-checked against individual DMO auction results, e.g. [16 May 2013-style press notices](https://www.dmo.gov.uk/media/gfwhnbjv/pr100123a.pdf) for the pattern.)) And unlike the 3¼% 2044 gilt this post originally reached for, this one has already run its full course: it redeemed at par on **22 October 2025**((UK Debt Management Office, [3½% Treasury Gilt 2025 prospectus](https://www.dmo.gov.uk/media/5cdl1wbx/prosp100123a.pdf) — coupon dates 22 April/22 October, maturity 22 October 2025.)) — before today's valuation date, so there's no "current curve" left to discount it against. What there is instead is a complete, realised outcome for every single buyer, which turns out to be a better vehicle for the total-return question than a hypothetical sale ever was.

## One gilt, eight entry points

Every buyer of this gilt, whichever of the eight tranches they bought into, received the same 3.5% coupon and the same £100 par redemption on the same day. The only thing that varied was the price — and therefore the yield — they paid to get in. That means the entire dispersion in outcomes below is pure interest-rate-timing risk, with nothing else contaminating it: no credit risk (it's a gilt), no call risk (none), no reinvestment-rate risk in the coupon calculation (excluded by design, see caveats).

{{< figure src="/images/economics/fiscal-outlook-2025-gilt-tranche-returns.png" caption="Realised nominal return, split into capital and interest, versus CPI-real return, by 2023 issuance tranche of the 3½% Treasury Gilt 2025 (GB00BPCJD880)" >}}

Splitting total return into its two components makes the mechanism obvious. **Capital return** — how much of the redemption gain came from buying below par — ranged from a negligible 0.35% (the January tranche, bought almost at par) to 4.84% (the July tranche, bought at the worst point of the year for prices). **Interest received** — coupons actually paid from purchase to redemption, simply summed — ranged from 7.14% (the shortest-held, November tranche) to 10.67% (the March tranche, which had the most coupon dates left to collect). Add the two together and total nominal return across the eight tranches ranges from **9.1%** to **14.0%** over holding periods of 1.9 to 2.8 years — a real spread, on the same bond, driven entirely by which week of 2023 an investor happened to buy in.

Then adjust for inflation, with the issue date of each tranche as the reference point, as it should be: deflate each tranche's nominal total return by the change in ONS CPI (all items, 2015=100) from that tranche's own issue month to October 2025 (139.8).((Office for National Statistics, [CPI Index 00: All Items 2015=100](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23).)) Real returns compress the spread further in cash terms but *widen* it in relative terms: the January 2023 tranche — bought when CPI was still at 126.4, near the top of the post-2021 inflation surge — earned essentially nothing in real terms, **0.3%** over 2.76 years. The July 2023 tranche, bought cheaper and after more of that inflation had already passed, earned **6.8%** real over a shorter, 2.3-year hold. Same coupon, same redemption, same issuer — a real-return gap of six and a half percentage points, purely from entry timing into a volatile issuance year.

## What this has to do with Lord Bridges

This is the same mechanism as the debate itself, just running the film from a different angle. Lord Bridges' complaint is about the *government's* cost of borrowing rising as gilt yields climb — the highest G7 10-year cost, the worst 30-year auction in three decades. The 2025 gilt's tranche history shows the same rate volatility from the *lender's* side: eight ordinary auctions in one year producing an entry-yield range of over 200 basis points (3.63% to 5.67%), and a realised real-return range of over 6.5 percentage points depending on which auction an investor turned up to. Nobody's credit judgement was wrong in either direction — the UK didn't get any more or less creditworthy between January and July 2023 — the entire spread is the yield curve moving under everyone's feet in real time, which is exactly the instability Bridges was describing from the Treasury's side of the same ledger.

The curve chart further up remains the live, forward-looking version of the same story: it's not being used to reprice this particular gilt (which has nothing left to reprice), but it's the same curve mechanism, doing to today's new issuance exactly what 2023's curve did to the 2025 gilt's buyers.

## The caveats, because they matter

A few things worth being explicit about before anyone treats these numbers as more precise than they are:

- Interest is simply summed, not reinvested or compounded. A true total-return calculation would reinvest each coupon at prevailing short rates as it was received; given how sharply short rates moved in 2023–25, that would shift the figures a little (most likely down slightly, since much of the reinvestment window sat in a falling-rates 2024–25), but not enough to change which tranches did better or worse relative to each other.
- No accrued-interest adjustment is made at purchase or at redemption; all figures are on a clean-price, full-coupon basis.
- Real returns use ONS CPI (all items, 2015=100) as the deflator, with each tranche's own issue month as the base — not a single common start date — per how this section frames the comparison. RPI or CPIH would give slightly different numbers; CPI is the Bank of England's own target measure, which is the more defensible choice for a UK rates post.
- The final £365 million tap of this gilt (16 July 2024) is excluded from the tranche table: the DMO's issuance history records its nominal amount but not a separately published clean price or yield, so a capital-return figure for it can't be built from this dataset alone.
- The curve chart earlier in this post (11 September 2026) and the tranche-return chart are not the same exercise stitched together — the first is a live, forward-looking valuation curve; the second is a closed, backward-looking realised-return history for a gilt that has already redeemed. They share a theme (rate volatility) and a market (UK gilts), not a single calculation.

---

### Sources

- Parallel Parliament — [Fiscal Outlook, Lords Chamber, 10 September 2026](https://www.parallelparliament.co.uk/lord/lord-bridges-of-headley/debate/2026-09-10/lords/lords-chamber/fiscal-outlook)
- Trading Economics — [United Kingdom Government Bond Yield](https://tradingeconomics.com/united-kingdom/government-bond-yield)
- UK Debt Management Office — [Gilt Issuance History, report D2.1E](https://www.dmo.gov.uk/data/pdfdatareport?reportCode=D2.1E)
- UK Debt Management Office — [3½% Treasury Gilt 2025 prospectus](https://www.dmo.gov.uk/media/5cdl1wbx/prosp100123a.pdf)
- Office for National Statistics — [CPI Index 00: All Items 2015=100](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23)
- giltsyield.com — [Conventional gilts in issue](https://giltsyield.com/bond/)
- Hargreaves Lansdown — [UK gilt price list](https://www.hl.co.uk/shares/corporate-bonds-gilts/bond-prices/uk-gilts)

*Editorial note (draft): all return/inflation-adjustment figures above are author calculations from the DMO's published issuance history and ONS's published CPI series, not a market data terminal — worth a spot-check of the per-tranche coupon-count assumptions and the CPI index values against the ONS series directly before this goes live. Set to draft pending review.*
