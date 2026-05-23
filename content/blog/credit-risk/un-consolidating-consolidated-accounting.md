---
title: "Un consolidating Consolidated Accounting, or a day trip to the Casino"
date: 2026-03-22T11:16:02Z
draft: false
categories: ["credit-risk"]
tags: [credit-risk, fraud, the Con of Consolidated accounting]
description: "Accounting tricks to be wary of"
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

This is a deep dive into a widely known problem credit. In particular this will cover the root causes of one of the key problems in all its gory details. After this, you should never get caught by this nonsense again. If you do, more fool you.

> "Don't worry, on a consolidated basis the debt service coverage is absolutely fine..."
>
> Foolish words never to be listened to other than in very particular circumstances.

This is of course a post hoc analysis. At the time, it was not so easy to unpick. Which was sort of the point, from the borrowers perspective. Overly complex structures are rarely there for innocent reasons. Sometimes genuine tax reasons for old established REITs that have grown over decades. But in general, they should be at least of mild concern.

This case study requires a *lot* of detail and wider context. Sorry, not sorry. This is how you learn. Now, on to the trip to the Casino. In this case the Casino Group. And a sorry and sordid tale it is, living up to its name.

Shout out here to the two main parties for this seeing the light of day:
1. The excellent series of in depth articles in the FT on this subject.
2. The noted short seller Carson Block. Link to key 2015 paper below.

This is essential reading for any serious equity analyst or credit analyst. Put yourselves back in the moment it was published. Read it many times, take note on the critical thinking deployed within.
[When Genius Fails](https://muddywatersresearch.com/research/co/mw-is-short-groupe-casino/)

But, before we go there, you need to familiarize yourself in great details with accounting frameworks. Read it, I mean every word of it until you can apply it:
[IFRS 10 Consolidated Accounting](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/)

Digested all that lot?

Lets start with Muddy Waters, source report above:

> The basic problem with Casino is that its financial statements are literally meaningless to understanding the company’s (poor) health. It has about half the EBITDA its financials show, but almost all of the debt. For the LTM period, it appears as though Casino has EBITDA of €2.6 billion. However, its true economic ownership (“proportional”) EBITDA really is only €1.4 billion. To eliminate the income inflation of financial engineering, EBITDA likely should be further adjusted downward by approximately €165 million to €1.2 billion.
>
> While Casino’s financials overstate EBITDA by an estimated 100%, the portrayal of the debt is much more accurate. Casino’s real net debt is approximately 93% of the amount shown in the consolidated financials. The deleveraging “plan” is clearly shambolic. The press release read that the shown on the consolidated financials. In other words, while Casino’s chairman wrote in the 2014 annual report Casino’s balance sheet was “strong” and its leverage ratio was a conservative 1.8x, a leverage calculation based on debt and EBITDA actually owned by Casino, along with estimated adjustments to offset financial engineering profits, results in a leverage ratio at that time of 6.1x. (Note the substantial deterioration in our estimated leverage ratio since then.)

The rest of this post is going to posthumously unpick the how of the above, in excruciating detail. We will rely on facts from Group Casino financial reports, and leave the speculation of motive to others. But the FT covered it nicely, so no need to add to the noise. You can look up the credit rating agencies reports from this time yourself. They have taken their beating on this name already. If you think they can learn, go read the Enron post. Seems they can't.

For this we can just focus on one element, being the GPA holding. Unpicking that is enough. For this, I have copies of the GPA and Group Casino financials referenced below. The rest is links.

## Share price as evidence

First a moan. Capital markets rely on facts, and those facts being available. There seems to be a trend now where historical stock prices are being increasingly put behind pay walls, even for API access. This is a disgrace at the industry level, especially for stale historical data. Regulators take not, market participants should be obligated to provide historical data in open source format. Or better, the mandate be set federally and a common funded statistical service be established to provide quality curated data. The cost of this is minimal. ANother example is fallen angels, try getting historic data on survival rates for companies over the last century, i.e. de listed or bought out companies. Capital markets cannot thrive in the absence of high quality, open sourced data.

Here is the share price chart. This took far too much work, because of the above. The chart is self evident of the results. We know who was telling the truth now. Again stating that at the time is was not so easy as the post hoc analysis permits. The web sites block scrapers and API calls (damn them!). To solve this I ran a bash script to call up yfinance API and run in venv environment, this dumped data in csv file. The only drama being data set cuts of at 2000. I really wanted to show the massive decline from GPA purchase back in 1994 onwards. it should not be this hard. 

> Regulators do something useful please and mandate good quality curated open source public historical data sets. It cannot be that hard. Or government mandate ONS to do it. It would cost peanuts!

### Casino Share Price Chart (2000-2026)

![Groupe Casino (CO.PA) Share Price History 2000-2026](/images/credit-risk/casino_share_price_chart_1994_2026.png)

**Chart Overview:**
This chart visualizes Groupe Casino's dramatic decline from a €380 peak in July 2014 to €0.24 in May 2026. Key inflection points include:

- **2000-2014**: Gradual appreciation (€4 → €380)
- **2014 Peak**: €380 (14-year high, Rallye leverage peak)
- **2015-2022**: Structural deterioration (-86% from peak)
- **2023-2024**: Accelerated collapse (-99.9%)
- **2026**: Share trading at €0.24 (penny stock territory)

The secondary axis shows estimated market capitalization in billions of euros, illustrating how the company's enterprise value contracted from ~€80B (2014) to near-zero by 2026.

**Key Events Marked:**
- 2000: Dot-com crash recovery
- 2008: Financial crisis impact
- 2014: Leverage-driven peak
- 2015: Rallye acquisition consequences
- 2020: COVID-19 disruption
- 2022: Covenant pressure mounting
- 2023: Retail store closure crisis
- 2024: Restructuring/bankruptcy proceedings

**Data Source:** Yahoo Finance (CO.PA), 2000-2026 daily closing prices (6,780 trading days)

**Note:** Data is euro-denominated from 2000 onwards. Pre-2000 (1994-1999) historical data in French Francs is not available in modern financial databases.

FT and Muddy Waters 1: Groupe Casino nil points. That is the score of what was a very hard fought contest. More on that later. Probably in the psychology section!


Side note, then companies remove the share price chart from their web site, you kind of know things are grim. They meet the obligations with the number, but strip the hsitorical aspects.

# Casino Guichard Perrachon SA (EPA:CO) — Status as of May 16, 2026

## Overview

As of May 16, 2026, Casino Guichard Perrachon is navigating a period of financial stabilization following a major restructuring.

The group is now primarily focused on:
- French urban convenience retail:
  - Monoprix
  - Franprix
- Digital commerce:
  - Cdiscount

---

# Market Performance & Snapshot

Casino shares have remained highly volatile.

While the stock closed at **€0.22** on May 15, 2026, it declined **15.38%** in the latest trading session.

| Metric | Value (May 15/16, 2026) |
|---|---|
| Last Price | €0.22 |
| Market Capitalization | ~€90.13 million |
| 52-Week High | €0.7565 |
| 52-Week Low | €0.1490 |
| Trading Volume | 980,445 |
| EPS (TTM) | -€1.36 |

---

# Financial Highlights

The group’s FY2025 and Q1 2026 results showed improving operating profitability despite continued net losses.

| Financial Category | FY2025 Performance | Q1 2026 Performance |
|---|---|---|
| Net Sales | €8.26bn (-2.5% YoY) | ~€1.9bn (estimated) |
| Adjusted EBITDA | €655m (+13.7% YoY) | €110.1m (+10.4% YoY) |
| Trading Profit | €64m (vs -€49m in 2024) | Not explicitly reported |
| Consolidated Net Loss | -€402m | Not explicitly reported |
| Liquidity | €1.002bn (Dec 31 2025) | €0.8bn (Mar 31 2026) |

---

# Summary of Recent Activity

## Operational Recovery

The group’s **“Renouveau 2028”** turnaround plan has contributed to:
- positive like-for-like sales growth,
- improved profitability in core urban retail formats.

Monoprix remained a key earnings driver, with:
- adjusted EBITDA increasing 15.7% in Q1 2026.

---

## Debt & Restructuring

As of late March 2026:

| Item | Amount |
|---|---|
| Net Debt | ~€1.5bn |
| Liquidity | ~€0.8bn |

Casino also secured:
- an extension from creditors for operational financing through May 28, 2026,
- while seeking a broader refinancing agreement targeted for end-June 2026.

---

#
---

# Overall Position

Casino appears to be:
- operationally stabilizing,
- materially smaller than historically,
- still highly leveraged,
- and reliant on ongoing creditor support during restructuring negotiations.
---

# GPA: Economic ownership vs voting control

GPA, for you North American readers, does not mean grade point average in this context. GPA is a Latin American retailer.



> GPA, formerly Grupo Pão de Açúcar, is one of Brazil’s largest food retailers, founded in São Paulo in 1948 by Valentim Diniz. The company operates more than 800 stores across supermarket and convenience formats including Pão de Açúcar and Extra. GPA generated roughly R$19.1 billion (US$3.7 billion) in 2025 revenue. French retailer Groupe Casino acquired a stake in 1999, gained control in 2012, and later reduced ownership during its restructuring. Casino now holds about 20–22.5% of GPA after relinquishing control in 2024. 

GPA is what it is, we won't really get into it that much. How GPA was reflected in Group Casino accounts is the task at hand. In particular *why* is where we are aiming at here. This is because GPA historically had a dual-class share structure that created a **significant mismatch between economic ownership and voting control** for Casino.

Groupe Casino first acquired a stake in the Brazilian retail group GPA in 1999, when it purchased a 26% share of the company's capital. The exact financial price paid for this initial 1999 acquisition is not widely detailed. Over the following years, Groupe Casino significantly expanded its position in GPA, eventually becoming the sole controlling shareholder alongside the Diniz family in 2012.

Refer foreign exchange reserving discussion later. For now consider that GPA operates in Latin America, with assets and thus revenues in Brazilan Real and Columbian Peso's. This is neither good, nor necessarily bad. However the following FX charts highlights some of the challenges arising out of this investment. You cannot hedge for ever. No matter how you cut it, this cycle of purchase and reinvestment would have been economically damaging. Even if you adjust for purchase power as you chase the decline, at some point you need the FX rates to stop the decline, or ideally reverse. This aspect is intrinsic to the story of the Group Casino. Carrying these economics hits in the debt stack is a part of the overall decline of Group Casino.

---
title: "EUR Exchange Rate Decline"
date: 2026-05-16
---

## Currency Depreciation Analysis

The Brazilian Real and Colombian Peso have experienced significant depreciation against the Euro since 1999.

{{< eur-chart >}}

### Key Findings

- BRL lost 83% of value
- COP lost 81% of value
- Steepest declines post-2008
---

# 1. Core distinction

| Concept | Meaning |
|---|---|
| Economic ownership | Share of profits, dividends, and net assets economically owned |
| Voting control | Ability to direct strategy, appoint management, and control board decisions |

At GPA, these diverged materially.

---

# 2. Approximate structure (2018–2020)

| Item | Approximate Level |
|---|---|
| Casino economic ownership in GPA | ~41% |
| Casino voting control in GPA | ~99% of voting rights (via Segisor/control structure) |
| Minority economic ownership | ~59% |
| Effective managerial control | Casino |

The divergence arose from dual-class share structures and control vehicles.

Divisional split:

| Segment | Metric | 2017 | 2018 | 2018 % of Total |
|---|---|---:|---:|---:|
| France Retail | Net Sales (€m) | 18,799 | 19,061 | 49.9% |
| France Retail | EBITDA (€m) | 882 | 914 | 48.9% |
| France Retail | Trading Profit (€m) | 536 | 579 | 46.4% |
| E-Commerce (Cdiscount) | GMV (€m) | 3,304 | 3,646 | 9.6% |
| E-Commerce (Cdiscount) | EBITDA (€m) | (10) | 19 | 1.0% |
| Latam Retail | Net Sales (€m) | 16,782 | 15,577 | 40.8% |
| Latam Retail | EBITDA (€m) | 1,029 | 932 | 49.9% |
| Latam Retail | Trading Profit (€m) | 713 | 644 | 51.6% |
| **Total** | **Net Sales (€m)** | **38,885** | **38,284** | **100%** |
| **Total** | **EBITDA (€m)** | **1,901** | **1,865** | **100%** |
| **Total** | **Trading Profit (€m)** | **1,249** | **1,242** | **100%** |

From this we can observe that roughly 50% of the business is Latam, or offshore. With, presumably a hefty component of FX buried in those numbers. We don't have to look this up, its enough to be able to conclude just from the region and a basic understanding of Latam FX history. In this case we are talking about Brazilian Real and Columbian Peso. With presumable USD exposure though conversion. Native currency is EUR.
---
## Debt stack

Straight from financial statements:

> Most of the Group's debt is carried by Casino, Guichard-Perrachon and is not secured by collateral or any secured assets. Financing is managed by the Corporate Finance department. The main subsidiaries (GPA, Monoprix and Éxito) also have their own financing facilities, which are not secured by collateral or any security interests in assets and are not guaranteed by Casino (except for GPA loans granted by BNDES totalling €8 million as at 31 December2018 that are secured by assets).

Group accounts pg 106.

Now keep in mind the divisional split. Most debt at top co in France, but roughly half of operating assets and thus cash on other side of the world.

| Covenant Ratio | Threshold | Debt Facilities Subject to Covenant | Test Frequency | Ratio at 31 Dec 2018 |
|---|---|---|---|---:|
| Consolidated Net Debt (i) / Consolidated EBITDA (iii) | < 3.5x | €1.2bn syndicated credit line | Annually | 2.74x |
| Consolidated Net Debt (i) / Consolidated EBITDA (iii) | < 3.7x | €350m bilateral credit lines | Annually | 2.74x |
| Consolidated Net Debt (ii) / Consolidated EBITDA (iii) | < 3.5x | €50m bilateral credit line | Annually | 1.84x |
| Consolidated Net Debt (ii) / Consolidated EBITDA (iii) | < 3.5x | USD 750m syndicated credit line | Annually | 1.84x |
| Consolidated Net Debt (ii) / Consolidated EBITDA (iii) | < 3.5x | €40m bilateral credit line | Annually | 1.84x |

(i) Net debt as defined in the loan agreements may differ from net debt presented in the consolidated financial statements
(Note 11.2). It corresponds to borrowings and financial liabilities including hedging instruments with a negative fair value, less (i)
cash and cash equivalents, (ii) financial assets held for cash management purposes and short-term financial investments,
(iii) derivatives with a positive fair value classified as hedges of debt and (iv) financial assets arising from a significant disposal
of non-current assets.
(ii) For these facilities, the definition of net debt includes the net assets held for sale attributable to owners of the parent.
(iii) EBITDA (earnings before interest, taxes, depreciation and amortisation) corresponds to trading profit plus recurring net
depreciation and amortisation expense.

## Embedded FX

| Country | Owners of Parent 1 Jan 2018 | Movement 2018 | Owners of Parent 31 Dec 2018 | Non-Controlling Interests 1 Jan 2018 | Movement 2018 | Non-Controlling Interests 31 Dec 2018 | Total 31 Dec 2018 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Brazil | (1,571) | (280) | (1,852) | (2,492) | (418) | (2,909) | (4,761) |
| Argentina | (156) | (20) | (175) | (13) | (2) | (15) | (190) |
| Colombia | (282) | (15) | (296) | (320) | (34) | (355) | (651) |
| Uruguay | (17) | (17) | (34) | (31) | (15) | (46) | (80) |
| United States | 19 | - | 20 | 1 | - | 1 | 20 |
| Poland | 17 | (4) | 13 | - | - | - | 14 |
| Indian Ocean | (8) | (1) | (9) | (3) | - | (3) | (12) |
| Hong Kong | 1 | - | 1 | - | - | - | 1 |
| **Total Foreign Currency Translation Reserves** | **(1,997)** | **(335)** | **(2,332)** | **(2,858)** | **(468)** | **(3,326)** | **(5,658)** |

Key points:

* Assets and liabilities of subsidiaries in Brazil, Colombia, Argentina and other countries are carried in local currency on subsidiary balance sheets.
* When consolidated into Casino’s EUR reporting currency, exchange-rate movements change the EUR-equivalent carrying value.
* Depreciation of local currencies against the euro creates negative translation reserves.
* These movements are recorded in equity through OCI (Other Comprehensive Income), not directly through EBITDA or trading profit.

The large negative reserve for Brazil indicates substantial BRL depreciation versus EUR over time, materially reducing the euro-denominated carrying value of Casino’s Brazilian assets despite underlying local-currency operations remaining intact.

Economically:

* local operations may still perform strongly in BRL terms,
* while reported EUR net assets decline materially.

This creates a disconnect between:

* operational performance in local currency,
* and consolidated EUR balance sheet valuations.

The negative carry is EUR5.6bn. We can debate free cash flow generation (and I will), noting that Group Casino must distrubte to carry on debt service across the debt stack. Realistically, unless FX reverses, it would take something like the better part of 10 years to generate surplus cash to unwind the negative carry. To get back to zero, not to profit, to fill the hole of carried losses. Tp suggest that this is only problematic is a huge understatement. Any credit analysis that does not dig into is likely fatally flawed.

> There are embedded hedge arrangements supporting EUR balance sheet values that cannot last for ever, and or they have taken a bath on valuation in EUR over a long time. Either way, that is an amount of pain that will one day arrive. Does not make Latam assets 'bad', but does mean they are bad value in EUR terms over the long run.
> Under ceteris paribus conditions going forward, being flat relative FX rates, this negative carry is going to have to be unwound. The source of value to unwind this can only be operational cash flow in the long run, or asset disposals in the medium term. The absence of discussion in the accounts of this aspect reflects poorly.
> Yes under disclosure the purported facts are there. But the consequences are avoided, presumably deliberately.

---
# 3. Why this matters economically

Casino:
- did NOT own most of GPA economically,
- BUT fully controlled decision-making.

➡️ Result: GPA was **fully consolidated** in Casino accounts.

---

## Ill iquidity....

From the 2018 accounts, verbatim:

> As at 31 December 2018, Casino in France(2) had €5 billion in liquidity, composed of a gross cash position of €2.1 billion and confirmed undrawn lines of credit of €2.9 billion with an average maturity of 2.4 years that easily cover upcoming debt repayments. Casino Group consolidated net debt stood at €3.4 billion at year-end 2018 versus €4.1 billion at year-end 2017. For Casino in France(2), net debt came to €2.7 billion at year-end 2018, versus €3.7 billion at year-end 2017, due to the impact of the asset disposal plan. Free cash flow from continuing operations amounted to €1.2 billion before dividends and financial expenses.

2018 Group Accounts, pg 6. Footnote 2 reads:

> (2) Casino Group holding company scope, including the French businesses and the wholly-owned holding companies.

Lets assume the facts are just that, but explode them past the intended implication.



# 4. IFRS accounting consequence

Under IFRS 10:

> Control → full consolidation, regardless of ownership %

Therefore Casino reported:
- 100% of GPA revenue,
- 100% of EBITDA,
- 100% of debt,
- 100% of assets and liabilities,

then deducted **non-controlling interests (NCI)** below net income.

---

# 5. Simplified accounting comparison

## A. Actual consolidated reporting (control basis)

| Line item | Treatment |
|---|---|
| Revenue | 100% of GPA included |
| EBITDA | 100% included |
| Debt | 100% consolidated |
| Net income | Full, then NCI deducted |
| Minority interest | Substantial deduction |

---

## B. If no control (pure economic ownership only)

If Casino only held ~41% with no control:

| Line item | Treatment |
|---|---|
| Revenue | Not consolidated |
| EBITDA | Not consolidated |
| Debt | Not included |
| Net income | Equity-accounted share only |

➡️ GPA becomes a **single-line investment**, not a full subsidiary.

---

# 6. Pro forma illustrative impact (high level)

## Actual consolidated view

| Item | Approximate |
|---|---|
| Casino group revenue | ~€34bn |
| GPA contribution included | ~€13bn |
| Debt | Fully consolidated |
| Scale | Large global retail group |

---

## Pro forma (no control, equity method only)

| Item | Approximate |
|---|---|
| Revenue reported | ~€21bn (reduced scope) |
| EBITDA | materially lower |
| Debt | removed from consolidation |
| Income | only share of GPA earnings |

---

# 7. Key analytical distortion

| Factor | Effect |
|---|---|
| Control vs ownership mismatch | Inflated scale of group |
| Full consolidation of partially owned assets | Larger balance sheet |
| Minority interests | Large earnings deduction line |
| Debt inclusion | Higher apparent leverage |

---

# 8. Why investors focused on this structure

The structure created tension between:

### Positive
- Strategic control of Latin American retail empire
- Consolidated scale benefits
- Cash flow access via upstream dividends

### Negative
- Economic ownership significantly lower than reported scale suggests
- High leverage at holding-company level
- Dependence on subsidiaries not fully owned economically

---

# 9. Structural evolution driver

Over time:
- governance reforms in Brazil (e.g. Novo Mercado standards),
- market pressure for simplification,
- asset disposals and restructuring,

reduced the usefulness of dual-class control structures.

---

# 10. Bottom line

The GPA structure allowed Casino to:

- control ~99% of voting power,
- while owning ~41% economically,

leading to:
- full consolidation under IFRS,
- materially larger reported scale than economic ownership alone would imply,
- and significant minority interest adjustments below net income.

This, presumably purposeful structuring device enabled Group Casino to report headline revenue and EBITDA that was simply never present at the French entity level. Why? To make consolidated debt service metrics look far better than op cash flow would suggest.

# The gory details

## Detailed Analysis: Deconsolidation & Muddy Waters Comparison

For a detailed forensic analysis comparing Casino's 2018 consolidated figures to actual cash available at the parent company level, and how this validates Muddy Waters' 2015 short thesis:

**[→ Read: 2018 Financial Reality - Deconsolidated Cash Analysis vs. Muddy Waters](./casino_2018_vs_muddy_waters_inclusion.md)**

This deep dive reveals:
- How €36.6B consolidated revenue translates to only €4.3B actual cash revenue (-88% adjustment)
- How €1.87B consolidated EBITDA becomes €22M parent-level cash EBITDA (-99% adjustment)  
- Why the parent company's 0.26x DSCR made restructuring inevitable
- Point-by-point validation of Muddy Waters' 2015 thesis through 2024 outcomes

---

## Key Takeaways

- Unless you face a borrower group with a full General Security Agreement that features top co debt and fully secured subsidiaries with no debt and neg pledge on subsidiary indebtedness; you should:
- Identify the economic value generating assets. 
- Break the structure down to match where the key operating assets are broadly contained in logical accounting groups.
- Look very hard for lock up mechanisms.
- Consolidate into economic groupings.
- Run debt analysis on deconsolidated basis and test assumptions buried in consolidated accounts.

Now, if it all pans out, and there are no key structural issues then you can stop and go back to overall consolidation approach. But you can't assume this to be the case until you know.

This is a lot of work, an AD, D and supervising MD. Full time for something like 6 weeks minimum. Its a lot cheaper than losing your shirt though.......

Newplan excel is another poster child for what not to do. That is a story for another day.

---

## References

- [GPA 2018](https://url.com)
- [Group Casino 2018]
