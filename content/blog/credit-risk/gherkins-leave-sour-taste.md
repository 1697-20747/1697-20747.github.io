---
title: "Gherkins Leave Sour Taste"
date: 2026-06-07T08:28:14Z
draft: false
categories: ["credit-risk"]
tags: ["real-estate", "currency-risk", "receivership", "structured-finance"]
description: "How London's most desirable office building ended up in receivership — not because the building failed, but because the financing did."
showToc: true
tocopen: false
cover:
  image: "/images/credit-risk/gherkin_img.png"
  alt: "30 St Mary Axe (The Gherkin)"
  caption: "30 St Mary Axe ('The Gherkin'), London"
---


## Overview

If you want a textbook example of an asset-liability mismatch, the Gherkin is it. Not a failing building. Not empty floors. Not even particularly reckless leverage by the standards of 2007. What killed it was a currency bet hiding inside a capital structure — one that got dramatically worse every time the Swiss franc strengthened, which, post-2008, it did with depressing regularity. Well, depressing if you are Swiss watch maker protecting your export market. Helpful is you are Swiss and actually want your wealth protected and your currency not debased. It is all about perspective, really.

This is a story about a £600 million building that was 99% occupied, collecting rent from blue-chip tenants, and still ended up in receivership. The building didn't fail. The financing did.

---

## The Building

30 St Mary Axe — known universally as the Gherkin — was designed by Norman Foster and Partners and built by Skanska. Construction began in 2001 on the former Baltic Exchange site, which the IRA had comprehensively destroyed in a 1992 bomb attack. The building opened in April 2004, 180 metres of aerodynamic glass rising over the City of London, and promptly won the 2003 Emporis Skyscraper Award (the judging committee evidently willing to work ahead of schedule). It cost approximately £138 million to construct, plus around £90 million for the land — so roughly £230 million all-in before any financing costs.

Swiss Re, the Zurich-based reinsurer, commissioned and initially occupied a substantial portion of the building. Having a globally recognisable, credit-worthy anchor tenant on a long lease makes a building extremely attractive as an investment asset. Swiss Re knew what they had built, and priced it accordingly.

---

## The 2007 Acquisition

In early 2007, Swiss Re sold the Gherkin for £600 million — a record price for a City building at the time, and widely considered overpriced even then. The buyers were a joint venture between Germany's IVG Immobilien and British real estate investor Evans Randall, structured as a 50/50 partnership (IVG through its Euroselect 14 fund; Evans Randall through a vehicle called Skyline Investments).

The acquisition was financed by a £396–500 million loan from a consortium of five banks led by Bayerische Landesbank. The exact figure varies by source — £396 million per some reports, closer to £500 million per others — but the direction of travel is clear: heavily leveraged, as was entirely standard at the peak of the pre-crisis property boom. At £600 million purchase price and roughly £400–500 million of debt, you are looking at somewhere between 65–80% LTV. Fine for a trophy asset with strong cash flows. Problematic if your debt starts growing in sterling terms without any additional borrowing.

Swiss Re remained the principal tenant, occupying roughly half the building. Average rents across the 20-odd tenants ran at around £55 per square foot. The building was, as a property, close to perfect.

---

## The Hidden Risk

The financing contained a feature that turned a sensible trade into a slow-motion disaster.

IVG's tranche of the loan — roughly half the debt stack, given the 50/50 ownership — was denominated in Swiss francs rather than sterling. This was not unusual in European property finance in 2007. Swiss franc interest rates were materially lower than sterling rates, so borrowing in CHF reduced the headline interest cost. Property investors across Europe were doing the same thing. The logic was seductive: cheap funding, strong asset, long income, blue-chip tenants. What's not to like?

The problem is straightforward, and someone should have screamed it loudly at the credit committee: the building generates rent in pounds sterling. The debt is in Swiss francs. If the franc appreciates against the pound — which is to say, if sterling weakens — the sterling-equivalent value of the CHF debt goes up, even though no additional money was borrowed.

This is currency risk. It is not exotic. It is GCSE economics. You borrow in a currency you don't earn in, and you have taken a leveraged directional FX bet whether you intended to or not.

The chart below shows what GBP/CHF looked like across the 20 years prior to the 2007 deal. Each fan arm tracks how the exchange rate moved over successive 5-year windows, indexed to 100 at the start of each period.

{{< rawhtml >}}
<script>
window.addEventListener('message', function(e) {
  if (e.data && e.data.iframeHeight) {
    var iframes = document.querySelectorAll('iframe');
    for (var i = 0; i < iframes.length; i++) {
      try {
        if (iframes[i].contentWindow === e.source) {
          iframes[i].style.height = (e.data.iframeHeight + 4) + 'px';
          break;
        }
      } catch(x) {}
    }
  }
});
</script>
<iframe src="/html/gbpchf-fan-chart.html" width="100%" height="200" style="border:none; background:#0f1117;" scrolling="no"></iframe>
{{< /rawhtml >}}

The fan is not pointing uniformly in one direction. But look at the 1992–1997 window: sterling fell about 25% against the franc at one point (Black Wednesday 1992 is baked into that chart whether the labels say so or not), before recovering. The 1997–2002 window saw relatively stable rates as carry trades flourished. By 2002–2007, the rate was sitting at a moderately comfortable 2.4 CHF per pound — up from the low 2.2s of 2003–2004. The franc looked weak. Swiss rates were low. The deal looked cheap to finance.

What the fan chart tells you, if you're paying attention, is that GBP/CHF is not a stable pair. It has historically moved a lot. Over a 7-year horizon (the likely hold period of the deal), you were not buying insurance against FX movement by failing to hedge — you were simply hoping the risk didn't materialise. In 2007, with the Swiss franc near multi-year lows, that was not a small hope.

---

## What Went Wrong

After the global financial crisis erupted in 2008, the Swiss franc did what it always does in a crisis: it went up. Investors flooded into safe-haven assets, and CHF is about as safe-haven as currencies get. By 2009, GBP/CHF had moved from 2.4 to around 1.7 — a roughly 30% sterling depreciation against the franc in two years. By 2011, during the height of the European sovereign debt crisis, it had reached approximately 1.4 — a CHF appreciation of around 60–65% from the 2007 level.

The effect on the IVG tranche of the debt was mechanical and brutal. If you borrowed CHF equivalent to, say, £200 million at 2.4, and the rate moved to 1.6, the same CHF obligation now costs you £300 million in sterling terms. The building hasn't changed. The rent hasn't changed. You just owe £100 million more than you thought you did.

The chart below shows the full GBP/CHF trajectory from 2005 to 2015, with key events marked.

{{< rawhtml >}}
<iframe src="/html/gbpchf-line-chart.html" width="100%" height="200" style="border:none; background:#0f1117;" scrolling="no"></iframe>
{{< /rawhtml >}}

---

## Quantifying the Risk: PFE at 99th Percentile

Potential Future Exposure (PFE) is the standard credit risk tool for asking: *how bad could this get, at a given confidence level, over a given horizon?* For an unhedged CHF liability on a sterling-income asset, the calculation is straightforward — and the answer is uncomfortable.

Using the historical GBP/CHF annual volatility derived from 1987–2007 data (σ ≈ 7.6% per annum) and a lognormal model with zero drift (the conservative assumption — no assumed trend), the 99th percentile worst-case increase in the sterling equivalent of the CHF debt builds as follows over a five-year horizon:

{{< rawhtml >}}
<iframe src="/html/gbpchf-pfe-chart.html" width="100%" height="200" style="border:none; background:#0f1117;" scrolling="no"></iframe>
{{< /rawhtml >}}

At five years, the 99th percentile PFE is approximately 51% of the original sterling notional. That is: in a 1-in-100 scenario, a £200 million CHF debt tranche grows to approximately £300 million in sterling terms — purely through exchange rate movement, with no additional borrowing.

The red line is the actual outcome. By 2009 (Year 2), reality had already exceeded the 99th percentile model. By 2011 (Year 4), GBP/CHF had reached approximately 1.42 — implying a 69% increase in the sterling value of the CHF liability. The model's five-year 99th percentile was ~51%. The actual four-year outcome was ~69%. A once-in-a-hundred-years event arrived in four years.

> "Consider a turkey that is fed every day. Every single feeding will firm up the bird's belief that it is the general rule of life to be fed every day by friendly members of the human race. On the Wednesday before Thanksgiving, something unexpected will happen to the turkey. It will incur a revision of belief."
> — Nassim Nicholas Taleb, *The Black Swan* (2007)

The twenty years of GBP/CHF data used to calibrate σ contained Black Wednesday, a period of franc weakness during the carry trade era, and a modest appreciation cycle through the early 2000s. What it did not contain was a synchronised global financial crisis followed immediately by a European sovereign debt crisis — two sequential safe-haven flights into CHF, compounding each other over four years. The historical sample was not wrong. It was simply a sample — one path through a distribution whose tails were wider than the data suggested. Taleb's point is not that models are useless. It is that the past, by definition, cannot show you what has not yet happened.

This is not a criticism of the model. Models are approximations. The point is that even a simple, well-parameterised PFE calculation at the time of the 2007 deal would have shown that the unhedged CHF exposure was capable of adding tens or hundreds of millions of pounds to the liability stack in a stress scenario. Whether that analysis was done, and what was done with the result, is a separate question.

The loan first defaulted in 2009. By the time receivers were appointed five years later, the IVG tranche's sterling value had inflated to the point where IVG's LTV covenant — 67% — had been obliterated, with actual LTV reportedly running above 90%. The building was not to blame. The pound was.

---

## Why It Took Five Years to Resolve

The obvious question: if the loan defaulted in 2009, why did it take until 2014 for receivers to be appointed?

Several compounding factors. First, the loan was complex — multi-currency capital structures do not restructure easily, particularly when the two equity owners have materially different interests. Evans Randall's equity was in sterling. IVG's tranche was the one blowing up in franc terms. This asymmetry made a consensual solution extremely difficult. Evans Randall repeatedly stated it had equity ready to inject but could not agree terms because of IVG's position. IVG, meanwhile, filed for insolvency in Germany in 2013 under the weight of broader portfolio problems — not just the Gherkin.

Second, the SNB threw more petrol on the fire. In September 2011, the Swiss National Bank imposed a floor of 1.20 on EUR/CHF to prevent further franc appreciation against the euro. This had a knock-on effect stabilising GBP/CHF somewhat, but the damage was largely done. The LTV had already blown through covenants. The debt had already grown by 60%+ in sterling terms.

Third, lenders were reluctant to pull the trigger. Deloitte's appointment in April 2014 came only after five-plus years of uncured defaults — Neville Kahn of Deloitte described the lenders as having been "reluctant to appoint a receiver but felt they had no choice." This is the polite way of saying that appointing a receiver on a £600 million trophy asset in the heart of the City, occupied by Swiss Re and 19 other tenants, is a decision you triple-check before making. The PR optics of putting one of London's most famous buildings into receivership are not ideal. But math eventually wins.

---

## The Sale

Deloitte ran a global marketing process from mid-2014. Over 200 parties reportedly reviewed the opportunity. This should not surprise anyone — a fully-let, iconic, City-of-London office building in a rising market, on offer at a distressed-seller price, is not something that sits unsold.

In November 2014, the Safra Group — the Brazilian-Lebanese financial conglomerate controlled by Joseph Safra — acquired the building for a price reported at approximately **£726 million**. This was roughly 21% above the 2007 purchase price of £600 million. The sale repaid senior lenders in full. The equity, of course, was gone.

The irony is complete: the building appreciated in value over the seven years of the default. The property market, the building, the tenants — all fine. The equity holders just lost everything because of a currency bet they may not have fully appreciated they were making.

---

## The Credit Lesson

The structuring logic in 2007 was not irrational on its face. Cheap CHF funding was genuinely cheaper than sterling funding. Property investors across Europe were running the same trade. Some of them got lucky.

The Gherkin sponsors did not. The franc moved the wrong way by more than most models would have suggested was probable, in a very short period of time, during a once-in-a-generation financial crisis. That is not, in itself, unusual. Crises are characterised by assets moving further and faster than pre-crisis models predicted. The question is whether you were hedged for it.

In this case: no. IVG's tranche was apparently unhedged. The 20-year fan chart above shows that GBP/CHF had moved by 20–30% in previous 5-year periods. Borrowing in CHF against a sterling asset without a hedge is simply borrowing more than you think you are — the additional debt is just contingent on an FX move you have not been paid to take.

| Item | Currency |
|------|----------|
| Property value | GBP |
| Rental income | GBP |
| IVG debt tranche | CHF |
| Evans Randall equity | GBP |

The asset-liability mismatch sits in row 3. That's the whole story.

Lenders and equity sponsors in real estate — or anywhere — must analyse not just the quality of the collateral but the currency denomination of every liability in the stack. A sterling-income building financed partly in Swiss francs is not 65% LTV. It's 65% LTV plus a leveraged long-CHF short-GBP position, sized at whatever the CHF debt tranche happens to be.

The Gherkin did not default because it was overbuilt, overleveraged in the traditional sense, vacant, or obsolete. It defaulted because part of its debt got materially larger in sterling terms while the income stayed constant in sterling terms. Foreign exchange risk, dressed up as a funding cost saving, became the dominant driver of the credit outcome.

Buildings don't bankrupt themselves. Capital structures do.

---

## Key Timeline

| Date | Event |
|------|-------|
| 1992 | IRA bombing destroys the Baltic Exchange site |
| 2001 | Construction begins (Foster + Partners / Skanska) |
| April 2004 | Building opens; Swiss Re primary tenant |
| February 2007 | Swiss Re sells Gherkin for £600m to IVG / Evans Randall JV |
| 2007–2008 | CHF begins appreciating against GBP |
| 2008–2009 | Global financial crisis accelerates CHF safe-haven inflows |
| 2009 | Loan enters default |
| 2011 | EUR/ERM sovereign crisis; GBP/CHF reaches ~1.42 |
| 2013 | IVG Immobilien files for insolvency in Germany |
| April 2014 | Deloitte appointed joint receivers |
| November 2014 | Safra Group acquires building for ~£726m; senior lenders repaid in full |

---

## References

- [Reuters — Gherkin sold to Safra Group, Nov 2014](https://www.yahoo.com/news/londons-gherkin-tower-sold-brazilian-billionaire-080815281--sector.html)
- [City AM — Gherkin sold: Safra Group buys 30 St Mary Axe](https://www.cityam.com/gherkin-sold-safra-group-buy-one-of-city-londons-tallest-buildings-30-st-mary-axe/)
- [IPE — Gherkin up for sale in wake of IVG receivership](https://www.ipe.com/main-navigation/londons-gherkin-tower-up-for-sale-in-wake-of-ivg-receivership/10002632.article)
- [Management Today — Gherkin in a pickle](https://www.managementtoday.co.uk/gherkin-pickle-londons-favourite-skyscraper-gone-receivership/article/1291458)
- [Wikipedia — 30 St Mary Axe](https://en.wikipedia.org/wiki/The_Gherkin)
- [UBC Pacific Exchange Rate Service — IMF/IFS GBP/CHF annual data](https://fx.sauder.ubc.ca/etc/GBPpages.pdf)
