---
title: "Securitisation 101"
date: 2026-05-17T07:13:28Z
draft: false
categories: ["comp-science"]
tags: [securitisation, tranching, RMBS, mortgages, finance]
description: "A complete start-to-finish guide to securitisation with real-world examples and working code"
summary: "A practical guide to RMBS securitisation mechanics and structure."
ShowToc: false
disableAnchoredHeadings: true
cover:
  image: "images/comp-science/rmbs_legal_structure.png"
  alt: "RMBS Legal Structure and Mortgage Transfer Flow"
  caption: "Complete securitisation architecture showing mortgage transfer through SPV to investors"
---
<!--more-->

## Overview

This is about the dark art of securitisation (securitization?!), what it is, how it works, the concepts behind it and how it works IRL.

A few notes before we proceed:
- This is based on real processes, actual credit concepts, and done at scale.
- The data set is made up of course, but the loans are all realistic in nature.
- Data tape standards as per BoE have been adopted.
- The code does a few things:
    - Creates random portfolio of loans (10,000 mortgages, GBP 733.1m pool)
    - Creates loan level cash flows for P&I
    - Creates pool level aggregation of cash flows (all loans together into monthly schedules)
    - Incorporates recent real world transaction and prospectus (see references)
    - Full reporting is properly generated from data using stand alone scripts, output onto log files
    - This approach is based on stand alone bash scripts, so you can run from CLI and don't need any IDE
    - It is stable and lean, but to change best you know how to read code (code on github)
    - From this applies stress and credit methodologies to tranche the loans (this is the key functional task here)
    - The tranching model is stand alone, can be applied at scale to any pool of mortgages
    - Reporting dashboard and summary statistics for the mortgage pool and the tranches
    - Key assumptions are in stand alone files and read in as needed (change them and model still works)
    - These are big data sets, CSV is poor choice. For key tables Apache Parquet is used for good reason (computational efficiency on the Monte Carlo runs)

?? **Warning:** The tranching model is complex, but is highly realistic. It is based on open source data sets and features all of the key aspects required. The Monte Carlo process is set for n runs (10,000 is good enough). Test. The variance and correlation assumptions are based on real world data, historical interest rates, HPI data, etc. It adopts rating agency concepts based on public domain methodologies. It is about 90% complete-you can definitely use this for tranching purposes when assessing mortgage pools to give you realistic results. But it is not 100%. **Do not use in production environment.** The last 10% needs use of brain cells. If you don't know what you are doing, do not use this in production. The 100% version is not going on my git hub for lots of reasons. The last parts are not so easy. There is enough here you should be able to tweak this to your own choices, which is part of the last 10%-your assumptions and mine not the same.

---

## Securitisation - What Is It?

A mortgage is just that, a mortgage from a bank or building society. You can't really sell it or transfer it-it is not a security.

**So here's the magic:**

1. If we take a lot of mortgages, pool them (aggregate), put them into a legal entity, we have aggregated all the cash flows. If a loan defaults and does not pay, then the pool experiences the same impacts.

2. Now we can allocate the cash flows from the pool in an ordered manner of priority. This is called tranching. This does NOT create more cash flow-it only allocates. What this means, for example, is that all of the cash from the pool will first pay the first ranking tranche investors (AAA). If and only if they get paid in full, then left over cash can be allocated to the next tranche (AA), and so on.

3. If I get paid from all mortgages, not just one, presumably the probability of many loans defaulting at the same time is less than that of one loan. This is diversification, or imperfect correlations. The lower the correlation the better.

4. If I take less risk on cash flows from all mortgages, then in an efficient market this should result in lower yield, as the security is lower risk. You must ponder this until you understand the concept. If mortgages have credit spreads (risk premium over time value of money) of say 200bps, you cannot create a securitisation if the AAA spreads are 200bps. This would be mathematically impossible. This is a bit abstract, so we will cover it in sources and uses later by shocking yields and breaking the securitisation from day one.

5. There are no other sources of funds-what pays in gets paid out. There is no more funds coming in for any reason.

? **Important:** Securitisation is a zero sum game. It cannot create cash flow. Much like the 2nd law of thermodynamics (the total entropy of an isolated system can never decrease over time), the process only allocates existing cash flow from the system (the SPV). Total sources and uses must reconcile, in total and for every period, other than small liquidity amounts.

---

## The Formal Process

Here is a logical step by step process for creating an RMBS (or any ABS) from scratch:

### RMBS Creation Process

1. **Acquire Mortgage Pool**  
   Gather a portfolio of residential mortgages with standardized loan-level data including balances, rates, borrower characteristics, and payment history.

2. **Perform Due Diligence**  
   Review the mortgage pool for credit quality, underwriting standards, geographic concentration, delinquency status, and data integrity.

3. **Model Loan Cash Flows**  
   Generate projected monthly mortgage cash flows including scheduled principal, interest, prepayments, defaults, and recoveries.

4. **Analyze Credit Risk**  
   Estimate expected losses and stress performance using historical data, macroeconomic scenarios, and statistical or machine learning models.

5. **Create Special Purpose Vehicle (SPV)**  
   Transfer the mortgage pool into a bankruptcy-remote legal entity that will issue the RMBS securities.

6. **Structure the RMBS Tranches**  
   Divide the securitization into tranches (AAA, AA, A, BBB, residual) with different levels of seniority and credit protection.

7. **Build the Waterfall Mechanism**  
   Define how monthly mortgage cash flows and losses are allocated among tranches according to priority rules.

8. **Apply Credit Enhancement**  
   Add protections such as subordination, excess spread, reserve accounts, or overcollateralization to improve tranche credit quality.

9. **Run Stress Scenarios**  
   Simulate severe economic conditions such as house price declines, unemployment shocks, and elevated defaults to test tranche resilience.

10. **Size the Tranches**  
    Adjust tranche balances iteratively until each tranche satisfies target expected loss and rating criteria under stress conditions.

11. **Obtain Credit Ratings**  
    Submit the transaction to rating agencies for independent analysis and assignment of tranche credit ratings.

12. **Issue RMBS Securities**  
    Sell the structured securities to investors, with proceeds used to fund the mortgage acquisition.

13. **Service the Mortgage Pool**  
    Collect borrower payments, manage delinquencies and foreclosures, and distribute monthly cash flows through the waterfall.

14. **Monitor Ongoing Performance**  
    Continuously track collateral performance, tranche losses, prepayments, and trigger events throughout the life of the securitization.

---

## Deep Dive: RMBS Securitization in Detail

Now let's explore securitisation in comprehensive detail with real examples and working code.

### Introduction: What is RMBS?

A Residential Mortgage-Backed Security (RMBS) is a financial instrument created by aggregating thousands of individual mortgage loans into a single pool, then dividing that pool into different risk tiers (tranches) and selling them to investors.

The beauty of RMBS is that it transforms illiquid individual mortgages into liquid, tradeable securities while allowing originators to immediately recover their capital and continue lending.

But how does this complex transformation actually work? Let's start with a simplified overview and then dive into the complete legal structure.

---

### Part 1: How RMBS Structures Work (The Big Picture)

Before we explore the detailed legal structure and entity roles, let's understand the basic mechanics:

#### What Happens in RMBS:

1. **Aggregating mortgages** - A lender originates thousands of mortgages to borrowers
2. **Creating a SPV** - A special purpose vehicle (independent company) is created to own the pool
3. **Issuing tranches** - The SPV issues notes with different risk/return profiles to investors
4. **Distributing cash** - Monthly mortgage payments flow through the SPV to investors based on priority

#### The Key Players (Overview):

| Role | Function |
|------|----------|
| **Originator** | Creates mortgages, sells to SPV |
| **Servicer** | Collects borrower payments, reports performance |
| **Master Servicer** | Oversees servicer, ensures compliance |
| **Trustee** | Holds mortgages, protects investor interests |
| **Agent Bank** | Distributes payments to investors |
| **Cash Manager** | Manages reserves and waterfall |
| **Rating Agencies** | Rates tranches, monitors credit quality |

#### Mortgage Transfer Flow (Simplified):

```
Borrowers -> Servicer -> SPV -> Agent Bank -> Investors
           (monthly          (implements      (get paid
            payments)        waterfall)       per tranche)
```

This is the basic flow. But the actual legal structure is far more complex, with multiple entities playing specific roles to protect investors and ensure proper management of the pool.

---

### Part 2: Complete Legal Structure & Mortgage Transfer Flow

Now that you understand the basics, let's examine the complete legal structure in detail:

#### The Full Securitization Architecture:

![RMBS Legal Structure](/images/comp-science/rmbs_legal_structure.png)

#### Understanding the Diagram:

The legal structure diagram shows how mortgages physically and legally transfer through the securitization system.

##### **Left Side: Origination and the Mortgage Pool**

**Mortgage Originators** create individual mortgages through standard underwriting processes. These mortgages are:
- Made to qualified borrowers
- Secured by residential real estate
- Documented with promissory notes and mortgages/deeds of trust
- Typically ranging from GBP 30,000 to GBP 500,000 per loan

In our example, we have **10,000 mortgages totaling GBP 733.1 million** with:
- Average loan size: GBP 73,309
- Average LTV (Loan-to-Value): 78.5%
- Weighted average rate: 4.65%

These mortgages represent the actual collateral-the real assets backing the entire securitization.

##### **Center: The Securitization Engine (SPV/Issuer)**

The **Special Purpose Vehicle (SPV)**, also called the Issuer or Securitization Trust, is the legal linchpin of the entire structure:

- **Independence**: The SPV is a bankruptcy-remote entity, meaning if the originator fails, the mortgages in the SPV are legally protected from the originator's creditors
- **Ownership**: The SPV legally owns the mortgage pool after purchasing it from the originator
- **Capital Raising**: The SPV issues notes (securities) to raise the capital needed to pay the originator
- **Payment Reception**: The SPV receives monthly mortgage payments forwarded by the servicer
- **Distribution**: The SPV distributes these payments to investors according to the waterfall priority

In our example, the **TGT-RMBS Plc** (a UK SPV) issues 5 classes of notes to raise GBP 733.1 million to purchase the mortgage pool.

##### **Right Side: Investor Tranches**

The SPV divides the mortgage pool's cash flows into 5 tranches with different risk/return profiles:

**Class A: GBP 595.4 million (80.0% of total raised)**
- Rating: AAA (highest credit quality)
- Spread: 50 basis points over SONIA
- Priority: First to receive payments
- Risk: Lowest (protected by 70% of subordinate classes)

**Class B: GBP 59.5 million (8.0% of total raised)**
- Rating: AA
- Spread: 100 basis points
- Priority: Second to receive payments
- Risk: Low (protected by 50% subordinate)

**Class C: GBP 37.2 million (5.0% of total raised)**
- Rating: A
- Spread: 150 basis points
- Priority: Third to receive payments
- Risk: Moderate (protected by 30% subordinate)

**Class D: GBP 29.8 million (4.0% of total raised)**
- Rating: BBB (lowest investment grade)
- Spread: 250 basis points
- Priority: Fourth to receive payments
- Risk: High (only protected by equity)

**Equity: GBP 22.3 million (3.0% of total raised)**
- Rating: Unrated (residual/equity class)
- Spread: None (receives what remains after senior payments)
- Priority: Last to receive payments
- Risk: Highest (absorbs all losses first)

The tranching structure means senior classes (AAA) are highly protected from losses, while junior classes absorb credit losses first.

##### **Bottom: Supporting Infrastructure**

Four critical supporting entities ensure proper management:

**Loan Servicer** (colored in cyan)
- Collects monthly mortgage payments directly from borrowers
- Maintains borrower accounts and escrow accounts
- Handles payment processing and accounting
- Reports monthly performance metrics, delinquencies, and defaults
- Forwards all collections to the SPV

**Trustee** (colored in red)
- Holds legal title to the mortgages in trust for the noteholders
- Represents investor interests in the transaction
- Monitors SPV and servicer compliance with transaction documents
- Takes enforcement action if the SPV or servicer breaches their obligations
- Enforces security interests in the collateral if needed

**Agent Bank** (colored in gold)
- Maintains investor accounts and the register of noteholders
- Distributes monthly interest and principal payments to investors
- Prepares investor account statements
- Handles investor inquiries and provides documentation
- Manages cash collection and distribution logistics

**Cash Manager** (colored in light blue)
- Manages reserve accounts and liquid funds
- Implements the priority of payments (the waterfall) each month
- Ensures adequate reserves for upcoming interest and principal payments
- Tracks and reports reserve balances to investors and rating agencies

##### **The Cash Flow Process:**

The diagram shows three critical stages of the cash flow:

**Stage 1: Collection** (Green arrow from Originators)
- Borrowers make monthly mortgage payments to the Servicer
- Payments include principal, interest, and escrow amounts
- Servicer collects, processes, and accounts for all payments

**Stage 2: Transfer to SPV** (Dashed arrow from Servicer)
- Servicer forwards all mortgage collections to the SPV
- This represents the legal flow of funds from borrowers -> SPV
- SPV receives approximately GBP 61.1 million in monthly principal and GBP 2.84 million in monthly interest

**Stage 3: Distribution to Investors** (Arrows to tranches)
- SPV distributes funds to investors through the Agent Bank
- Distribution follows strict priority: Class A -> B -> C -> D -> Z
- Each class receives its promised coupon rate if funds are available
- Senior classes are paid in full before junior classes receive anything

---