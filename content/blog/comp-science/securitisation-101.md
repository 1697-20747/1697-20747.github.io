---
title: "Securitisation 101 — Part 1: What It Is, and Why the Data Comes First"
date: 2026-05-17T07:13:28Z
lastmod: 2026-10-20
draft: false
categories: ["comp-science"]
tags: [securitisation, tranching, RMBS, mortgages, finance]
series: ["Securitisation 101"]
description: "What securitisation is, how a UK RMBS is generated end to end from a warehouse of loans, and a worked sample deal."
summary: "Part 1 of 4: securitisation in plain terms, the cradle-to-grave process, and a worked sample deal from the current model."
ShowToc: false
disableAnchoredHeadings: true
cover:
  image: "images/comp-science/rmbs_legal_structure.png"
  alt: "RMBS legal structure and mortgage transfer flow"
  caption: "Legal structure of the current sample deal: mortgages transfer to the SPV, which issues the notes"
---
<!--more-->

## Overview

This is about the dark art of securitisation (securitization?!): what it is, the concepts behind it, and how it works in real life.

A few notes before we proceed:
- It is based on real processes and actual credit concepts, done at scale.
- The data set is made up, of course, but the loans are realistic: a synthetic pool built to look like a UK prime new issue.
- The loan data follows the Bank of England loan-level template, and the model produces a BoE-compliant data tape.
- The code generates the pool, projects every loan month by month, runs the cash through the waterfall, stress-tests it at each rating level and sizes the notes. It then produces the reporting.
- Everything runs from stand-alone bash and Python scripts from the command line, with no IDE needed.
- Key assumptions live in stand-alone config files and are read in as needed. Change them and the model still works.
- These are big data sets and CSV is a poor choice, so the main tables use Apache Parquet (fast on the Monte Carlo and stress runs).

⚠️ **Warning:** the model is complex but realistic. It uses public data sets (interest rates, house prices, BoE lending statistics) and adopts rating agency concepts from public-domain methodologies. It does not replicate any particular agency's approach; it is a sensible average. **Do not use it in a production environment.** The last 10% needs real data and the use of brain cells. Your assumptions and mine will not be the same, and that is part of the last 10%.

Think about getting a loan, the end-to-end process and all the data it generates. Now multiply by 10,000. That gives you a sense of the scale. Securitisation is a very data-rich environment and an ideal candidate for scalable data science tools. By which I mean not Excel. Using only open-source tools, a quality end-to-end software solution is a realistic objective.

The challenge is the input: ingesting curated data at scale. There is no point running software on rubbish scraped from unstructured PDFs. Once the data is curated and properly stored, pool generation and reporting become a lot easier, and as market disclosures improve, machine learning becomes a real option.

This series covers the how. Yes, the coding is AI-heavy, but the architecture is set as it is on purpose. Good luck to those doing this for real; it is not as easy as you might think. I would spend most of my time on the ingested and curated data set first, and on the challenge of dragging it out of dated banking systems. The objective should be no manual processing at all, and agentic approaches will likely help with legacy systems. HTML, Markdown and open-source data libraries should be your only choice. If you create a Word document or an Excel file (other than where the BoE submission requires it), give up and go back to the start.

---

## Securitisation: what is it?

A mortgage is just that, a mortgage from a bank or building society. You can't really sell it or transfer it; it is not a security.

**So here is the magic:**

1. Take a lot of mortgages, pool them and put them into a legal entity (the SPV). The pool's cash flows are now aggregated. If a loan defaults, the pool takes the hit.
2. Allocate the pool's cash in a fixed order of priority. This is tranching. It does **not** create cash; it only allocates it. All of the cash first pays the most senior notes (AAA). Only if they are paid in full does the next class get anything, and so on down.
3. If I am paid from all the mortgages rather than one, the chance of many loans defaulting at the same time is lower than that of one loan. This is diversification, or imperfect correlation. The lower the correlation, the better.
4. Less risk should mean less yield. If the mortgages pay a credit spread of, say, 200bp, you cannot sell AAA notes at 200bp as well; the maths does not work. Ponder this until it makes sense. Part 3 shows what happens when a rate move between warehouse and issue squeezes this margin.
5. There are no other sources of funds. What comes in gets paid out.

❗ **Important:** securitisation is a zero-sum game. Like the second law of thermodynamics, the process only allocates the cash already in the system (the SPV). Sources and uses must reconcile, in total and in every period, apart from small liquidity amounts that are paid out at the end. The model checks this every month and over the whole life of the deal, against every note.

---

## The process: generate, then test

A rating agency reviews a securitisation **after** it has been tranched. This model works the other way round. It **creates** the deal from the warehouse, with the rating tests built in, so the finished deal should pass review without change:

1. **Ingest and curate** loan and borrower data into the BoE template, with data-quality checks.
2. **Ingest market data**: Bank Rate, mortgage rates, note margins, swap rates, house prices and costs.
3. **Select and price the pool** from the warehouse.
4. **Create the securitisation**: notes, swap, reserve and day-1 costs, with sources equal to uses.
5. **Freeze the static set**: the cut-off pool and its loan scores, fixed while the stresses run.
6. **Stress and tranche**: run every rating-level stress through the monthly waterfall, size each class, and add a sensitivity cushion.
7. **Issue the outputs**: BoE tape, investor report, pitch deck and a draft prospectus skeleton.
8. **Report through the life of the deal**, to final redemption (still a placeholder).

Steps 3 to 6 loop until the deal is viable. If a market move makes it uneconomic before issue, the result is an *issuance failure*, flagged for manual assessment rather than forced through.

---

## The sample deal

The current sample deal from the model:

| Item | Value |
|---|---|
| Pool | 9,951 UK mortgages, £1,449m (average £145,600) |
| Credit profile | Prime proxy: 90% of balance still in an introductory fix, 2% with past adverse credit, 14% buy-to-let |
| WA original LTV / interest rate | 72.7% / 5.24% |
| Notes | Class A Notes, AAA(sf), £1,351m (Bank Rate + 70bp); Class Z Notes, unrated first loss, £128m, retained |
| Class A credit enhancement | 8.8% subordination + 1.5% reserve = 10.3%, 1.45x its AAA stressed loss |
| Excess spread after the swap | 89bp a year |

![RMBS Legal Structure](/images/comp-science/rmbs_legal_structure.png)

Day-1 [sources and uses](/html/sources_and_uses.html) reconcile to the penny: the cash raised from the notes buys the pool, funds the reserve and pays the costs. Part 2 walks through the parties and the waterfall.

---

### Securitisation 101 series

**Next:** [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)

**Full series**
1. Part 1: What It Is, and Why the Data Comes First (this post)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
