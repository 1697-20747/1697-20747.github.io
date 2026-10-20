---
title: "Securitisation 101 — Part 2: The Parties and the Waterfall"
date: 2026-05-17T07:13:29Z
lastmod: 2026-10-20
draft: false
categories: ["comp-science"]
tags: [securitisation, tranching, RMBS, mortgages, finance]
series: ["Securitisation 101"]
description: "Who does what in a UK RMBS, and how the cash moves through the revenue and principal waterfalls every month."
summary: "Part 2 of 4: the parties to an RMBS and the priority of payments as the model runs it, with a stress-case month worked through."
ShowToc: false
disableAnchoredHeadings: true
---
<!--more-->

## The parties

![RMBS Entity Roles](/images/comp-science/rmbs_entity_roles.png)

| Party | What it does |
|---|---|
| **Originator** | Makes the loans and sells them to the SPV. It gets its capital back to lend again. In a prime deal it often keeps the first-loss note (risk retention) |
| **Issuer / SPV** | A bankruptcy-remote company that owns the pool and issues the notes. If the originator fails, the pool is protected |
| **Servicer** | Collects borrower payments, handles arrears and repossessions, and reports performance |
| **Trustee** | Holds the security for the noteholders and enforces the documents if anyone breaches them |
| **Cash manager** | Runs the priority of payments each month and manages the reserve |
| **Agent bank / paying agent** | Calculates and pays interest and principal to investors |
| **Swap counterparty** | Swaps the fixed rates on the loans into Bank Rate, so fixed-rate loans can back floating-rate notes |
| **Rating agencies** | Rate the notes at issue and monitor them afterwards |

The cash moves borrower → servicer → SPV → cash manager (the waterfall) → paying agent → investors.

---

## The waterfall

Each month the cash is split into **revenue** (interest) and **principal**, and each runs down its own priority of payments. The model follows a UK prospectus structure:

**Revenue priority of payments**
1. Net swap payment
2. Senior fees (servicer, trustee, cash manager)
3. Class A interest, then each rated class's interest in turn. Each class's interest is followed by a cure of its principal deficiency ledger (PDL), which records losses not yet made good. A class that is not the most senior can defer unpaid interest; it accrues and is paid later.
4. Reserve fund top-up
5. Class Z PDL cure, then Class Z interest
6. Class Z principal, but only once every rated class is repaid
7. Anything left goes to the residual holder (a residual certificate, where the deal has one)

**Principal priority of payments**: scheduled repayments, prepayments, recoveries and PDL cures repay the rated notes sequentially, A first. If revenue falls short, principal can cover it, with the amount debited to the PDL. Class Z is repaid last.

**Credit enhancement**, in the order it absorbs losses:
- excess spread (interest on the loans above what the notes cost);
- the reserve fund;
- subordination (every class below absorbs losses before the class above).

Losses hit Class Z first, then each class upwards. The deal also has an optional call at the step-up date, when the pool is bought back and every note is repaid.

**No cash is created.** The model checks that sources equal uses every month and over the whole life of the deal, against every note. The reserve is paid out at the end, so closing cash is zero.

---

## A stress case, worked through

The [stress-case waterfall](/html/stress_case_waterfall.html) takes the current sample deal and runs the worst of the AAA scenarios: front-loaded defaults, no prepayments, and Bank Rate rising to 9.75%.

| | Month 1 | Month 43 (peak defaults) |
|---|---|---|
| Interest collected | £6.3m | £8.7m |
| Swap receipt (net) | – | £1.7m |
| Senior fees | £0.3m | £0.2m |
| Class A interest | £5.0m | £9.2m |
| Class Z PDL cure | £1.1m | £1.1m |
| Defaults / losses | £0.2m / £0.1m | £7.6m / £2.1m |

Over the life of this scenario, 30.6% of the pool defaults and 8.3% is lost. **Class Z loses all of its £128m. Class A loses nothing**, and that is exactly what it was sized for. Closing cash is £0.00.

The day-1 position is on the [sources and uses](/html/sources_and_uses.html) page.

---

### Securitisation 101 series

**Previous:** [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/) · **Next:** [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. Part 2: The Parties and the Waterfall (this post)
3. [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
