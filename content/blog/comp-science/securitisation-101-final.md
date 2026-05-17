---
title: "Securitisation 101"
date: 2026-05-17T07:13:28Z
draft: false
categories: ["comp-science"]
tags: [securitisation, tranching, RMBS, mortgages, finance]
description: "A complete start-to-finish guide to securitisation with real-world examples and working code"
showToc: true
tocopen: false
cover:
  image: "images/comp-science/rmbs_legal_structure.png"
  alt: "RMBS Legal Structure and Mortgage Transfer Flow"
  caption: "Complete securitisation architecture showing mortgage transfer through SPV to investors"
---

## Overview

This is about the dark art of securitisation (securitization?!), what it is, how it works, the concepts behind it and how it works IRL.

A few notes before we proceed:
- This is based on real processes, actual credit concepts, and done at scale.
- The data set is made up of course, but the loans are all realistic in nature.
- Data tape standards as per BoE have been adopted.
- The code does a few things:
    - Creates random portfolio of loans (10,000 mortgages, £733.1m pool)
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

⚠️ **Warning:** The tranching model is complex, but is highly realistic. It is based on open source data sets and features all of the key aspects required. The Monte Carlo process is set for n runs (10,000 is good enough). Test. The variance and correlation assumptions are based on real world data, historical interest rates, HPI data, etc. It adopts rating agency concepts based on public domain methodologies. It is about 90% complete—you can definitely use this for tranching purposes when assessing mortgage pools to give you realistic results. But it is not 100%. **Do not use in production environment.** The last 10% needs use of brain cells. If you don't know what you are doing, do not use this in production. The 100% version is not going on my git hub for lots of reasons. The last parts are not so easy. There is enough here you should be able to tweak this to your own choices, which is part of the last 10%—your assumptions and mine not the same.

---

## Securitisation - What Is It?

A mortgage is just that, a mortgage from a bank or building society. You can't really sell it or transfer it—it is not a security.

**So here's the magic:**

1. If we take a lot of mortgages, pool them (aggregate), put them into a legal entity, we have aggregated all the cash flows. If a loan defaults and does not pay, then the pool experiences the same impacts.

2. Now we can allocate the cash flows from the pool in an ordered manner of priority. This is called tranching. This does NOT create more cash flow—it only allocates. What this means, for example, is that all of the cash from the pool will first pay the first ranking tranche investors (AAA). If and only if they get paid in full, then left over cash can be allocated to the next tranche (AA), and so on.

3. If I get paid from all mortgages, not just one, presumably the probability of many loans defaulting at the same time is less than that of one loan. This is diversification, or imperfect correlations. The lower the correlation the better.

4. If I take less risk on cash flows from all mortgages, then in an efficient market this should result in lower yield, as the security is lower risk. You must ponder this until you understand the concept. If mortgages have credit spreads (risk premium over time value of money) of say 200bps, you cannot create a securitisation if the AAA spreads are 200bps. This would be mathematically impossible. This is a bit abstract, so we will cover it in sources and uses later by shocking yields and breaking the securitisation from day one.

5. There are no other sources of funds—what pays in gets paid out. There is no more funds coming in for any reason.

❗ **Important:** Securitisation is a zero sum game. It cannot create cash flow. Much like the 2nd law of thermodynamics (the total entropy of an isolated system can never decrease over time), the process only allocates existing cash flow from the system (the SPV). Total sources and uses must reconcile, in total and for every period, other than small liquidity amounts.

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

1. **Aggregating mortgages** — A lender originates thousands of mortgages to borrowers
2. **Creating a SPV** — A special purpose vehicle (independent company) is created to own the pool
3. **Issuing tranches** — The SPV issues notes with different risk/return profiles to investors
4. **Distributing cash** — Monthly mortgage payments flow through the SPV to investors based on priority

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
Borrowers → Servicer → SPV → Agent Bank → Investors
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
- Typically ranging from £30,000 to £500,000 per loan

In our example, we have **10,000 mortgages totaling £733.1 million** with:
- Average loan size: £73,309
- Average LTV (Loan-to-Value): 78.5%
- Weighted average rate: 4.65%

These mortgages represent the actual collateral—the real assets backing the entire securitization.

##### **Center: The Securitization Engine (SPV/Issuer)**

The **Special Purpose Vehicle (SPV)**, also called the Issuer or Securitization Trust, is the legal linchpin of the entire structure:

- **Independence**: The SPV is a bankruptcy-remote entity, meaning if the originator fails, the mortgages in the SPV are legally protected from the originator's creditors
- **Ownership**: The SPV legally owns the mortgage pool after purchasing it from the originator
- **Capital Raising**: The SPV issues notes (securities) to raise the capital needed to pay the originator
- **Payment Reception**: The SPV receives monthly mortgage payments forwarded by the servicer
- **Distribution**: The SPV distributes these payments to investors according to the waterfall priority

In our example, the **TGT-RMBS Plc** (a UK SPV) issues 5 classes of notes to raise £733.1 million to purchase the mortgage pool.

##### **Right Side: Investor Tranches**

The SPV divides the mortgage pool's cash flows into 5 tranches with different risk/return profiles:

**Class A: £219.9 million (30% of pool)**
- Rating: AAA (highest credit quality)
- Spread: 50 basis points over SONIA
- Priority: First to receive payments
- Risk: Lowest (protected by 70% of subordinate classes)

**Class B: £146.6 million (20% of pool)**
- Rating: AA
- Spread: 100 basis points
- Priority: Second to receive payments
- Risk: Low (protected by 50% subordinate)

**Class C: £146.6 million (20% of pool)**
- Rating: A
- Spread: 150 basis points
- Priority: Third to receive payments
- Risk: Moderate (protected by 30% subordinate)

**Class D: £146.6 million (20% of pool)**
- Rating: BBB (lowest investment grade)
- Spread: 250 basis points
- Priority: Fourth to receive payments
- Risk: High (only protected by equity)

**Class Z: £73.3 million (10% of pool)**
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
- This represents the legal flow of funds from borrowers → SPV
- SPV receives approximately £6.1 million in monthly principal and £2.4 million in monthly interest

**Stage 3: Distribution to Investors** (Arrows to tranches)
- SPV distributes funds to investors through the Agent Bank
- Distribution follows strict priority: Class A → B → C → D → Z
- Each class receives its promised coupon rate if funds are available
- Senior classes are paid in full before junior classes receive anything

---

### Part 3: Entity Roles & Responsibilities (The Complete Picture)

Now let's examine each entity's specific role, responsibilities, and relationships:

#### The Nine Key Entities and Their Functions:

![RMBS Entity Roles](/images/comp-science/rmbs_entity_roles.png)

#### Detailed Entity Roles:

##### **1. Originator**

The originator is the entity that creates the mortgages and initiates the securitization.

**Key Responsibilities:**
- Originates mortgages through traditional underwriting processes
- Funds loans to qualified borrowers
- Ensures mortgages meet regulatory and investor requirements
- Sells mortgages to the SPV and receives proceeds
- May provide representations and warranties about loan quality

**Why They Do This:**
- Immediate capital recovery to continue lending
- Risk transfer (mortgages no longer on their balance sheet)
- Fee income from loan origination and servicing
- Access to capital markets through securitization

**In Our Example:**
- Together Financial Services originates 10,000 mortgages
- Total loan volume: £733.1 million
- Sells entire pool to TGT-RMBS Plc and receives proceeds to fund new originations

##### **2. Issuer / Special Purpose Vehicle (SPV)**

The SPV is the legal and financial center of the securitization structure.

**Key Responsibilities:**
- Owns the mortgage pool (typically a bankruptcy-remote entity)
- Issues notes (bonds) to raise capital for purchasing mortgages
- Receives mortgage payments and manages cash flows
- Distributes funds to investors according to the payment waterfall
- Maintains accounts and records for the transaction
- Complies with all indenture agreements and regulatory requirements

**Why This Structure:**
- Bankruptcy remoteness protects mortgages from originator insolvency
- Separate legal entity isolates assets from other business risks
- Can issue multiple classes of securities with different risk profiles
- Investors' recourse is limited to the mortgage pool's cash flows

**In Our Example:**
- TGT-RMBS Plc is the SPV
- Purchases £733.1 million mortgage pool from Together Financial Services
- Issues £733.1 million of notes (Classes A-Z)
- Receives £8.5 million in monthly cash flows (£6.1m principal + £2.4m interest)
- Distributes according to the waterfall

##### **3. Loan Servicer**

The loan servicer is the operational backbone of the transaction, managing day-to-day mortgage servicing.

**Key Responsibilities:**
- Services mortgages on behalf of the SPV
- Collects monthly payments from borrowers
- Maintains borrower accounts and handles escrow accounts
- Handles payment posting, accounting, and reconciliation
- Reports monthly performance metrics, delinquencies, and defaults
- Manages loss mitigation and forbearance programs
- Initiates and manages foreclosures if needed
- Forwards all collections to the SPV
- Complies with servicing standards and regulations

**Operational Workflow:**
1. Borrower makes payment to servicer bank account
2. Servicer receives and processes payment
3. Servicer posts payment to borrower's account
4. Servicer prepares monthly remittance report
5. Servicer forwards all collections to SPV within specified timeframe

**In Our Example:**
- SVC-TGT-001 (Services Together Mortgages) services the 10,000 loans
- Collects approximately £8.5 million monthly from borrowers
- Reports metrics like 90-day delinquency rate, CPR, CDR to trustee and rating agencies
- Forwards collections to SPV within 2 business days

##### **4. Master Loan Servicer**

The master servicer provides oversight and quality assurance for the loan servicer.

**Key Responsibilities:**
- Provides operational oversight of the loan servicer
- Monitors servicer performance against required standards
- Ensures servicer compliance with transaction documents and regulations
- Reviews servicer reports and audits for accuracy
- Can substitute the servicer if performance deteriorates materially
- Escalates servicer failures to the trustee if necessary
- Takes corrective action if servicer breaches obligations

**When Master Servicer Intervenes:**
- Servicer fails to remit collections on time
- Servicer fails to provide required reports
- Delinquency management is inadequate
- Foreclosure timelines are missed
- Servicer becomes insolvent or loses license

**In Our Example:**
- Independent Master Loan Servicer monitors SVC-TGT-001's performance
- Reviews monthly remittance and servicing reports
- Monitors timely payment of interest and principal to investors
- Can replace SVC-TGT-001 if they fail to perform

##### **5. Trustee (Mortgage Trustee)**

The trustee holds the mortgages and represents investor interests in the underlying collateral.

**Key Responsibilities:**
- Holds legal title to the mortgages in trust for the benefit of noteholders
- Represents investor interests in the transaction
- Monitors SPV and servicer compliance with transaction terms
- Takes enforcement action if either the SPV or servicer breaches obligations
- Enforces security interests in the mortgages
- Manages the mortgage pool and collateral
- Maintains mortgage documents and records
- Files and maintains UCC filings and security interests

**Enforcement Powers:**
- Can replace servicer if not performing
- Can accelerate mortgages if SPV fails to pay investors
- Can initiate foreclosures on mortgages
- Can sue servicer or SPV for breach of contract

**In Our Example:**
- Trustee holds 10,000 mortgage notes and mortgage/deeds of trust
- Ensures servicer properly collects and remits payments
- Monitors SPV's compliance with waterfall distribution requirements
- Takes action if servicer fails to foreclose on defaulted mortgages

##### **6. Note Trustee (Indenture Trustee)**

The note trustee represents the interests of the noteholders and enforces the terms of the bonds.

**Key Responsibilities:**
- Represents the interests of all noteholders (investors)
- Enforces the terms of the notes and transaction documents
- Collects payments from the issuer/SPV
- Prepares and delivers notices to noteholders
- Communicates material events and breaches to investors
- Takes enforcement action on behalf of noteholders
- Initiates actions against SPV if it defaults on its obligations
- Manages any reorganization or workout if needed

**Investor Protection Role:**
- Ensures SPV pays interest and principal on time
- Verifies cash flows are distributed according to waterfall
- Reports any material changes in pool performance
- Escalates breaches or concerns immediately to noteholders

**In Our Example:**
- Note Trustee ensures TGT-RMBS Plc distributes funds to noteholders each month
- Collects principal and interest from SPV and distributes to investors
- Sends monthly statements to Class A-Z noteholders
- Takes action if SPV fails to pay investors

##### **7. Agent Bank (Paying Agent)**

The agent bank manages the logistics of payments and investor accounts.

**Key Responsibilities:**
- Manages investor accounts and maintains the register of noteholders
- Distributes monthly interest and principal payments to investors
- Prepares detailed account statements for each investor
- Handles investor inquiries and provides documentation
- Manages the mechanics of payment processing
- Reconciles payments received vs. payments distributed
- Provides tax reporting information

**Account Services:**
- Direct bank transfer of payments to investor accounts
- Monthly account statements showing activity
- Coupon payment records and documentation
- Tax reporting (UK tax authorities for any withholding)

**In Our Example:**
- Agent Bank receives £8.5 million monthly from SPV
- Calculates interest due to each class based on their notional and coupon rate
- Distributes to Class A noteholders first (approximately £1.1 million monthly)
- Then Class B, C, D (if funds available), then Class Z
- Sends investors monthly statements

##### **8. Cash Manager**

The cash manager implements the priority of payments and manages reserves.

**Key Responsibilities:**
- Manages reserve accounts and maintains liquid funds
- Implements the priority of payments (the waterfall) each month
- Calculates interest due to each tranche
- Determines principal due to each class
- Ensures adequate reserves for upcoming interest and principal
- Tracks and reports reserve balances to noteholders and rating agencies
- Manages timing of payments to optimize returns
- Handles interest rate calculations on SONIA-based coupons

**Monthly Waterfall Process:**
1. Receives collections from servicer via SPV
2. Calculates monthly interest obligation (Class A coupon rate × notional, etc.)
3. Allocates funds in priority order:
   - Interest to Class A
   - Interest to Class B
   - Interest to Class C
   - Interest to Class D
   - Remaining funds to principal (Class A first, then B, C, D, finally Z)
4. Manages reserve accounts to ensure next month's interest is covered

**In Our Example:**
- Manages reserve account with approximately £2.4 million (one month's interest)
- Implements monthly waterfall with £8.5 million in collections
- Allocates approximately £3.7 million to interest payments
- Allocates approximately £4.8 million to principal payments
- Reports reserve coverage ratios to rating agencies

##### **9. Rating Agencies**

Rating agencies assess credit quality and monitor performance.

**Key Responsibilities:**
- Rate each note tranche based on credit analysis before issuance
- Monitor pool performance quarterly and annually
- Issue credit reports and surveillance updates
- Track default rates, loss severity, and prepayment speeds
- Compare actual performance to original assumptions
- Update ratings if performance deteriorates significantly
- Communicate rating changes to investors
- Provide technical assistance to investors and management

**Surveillance Process:**
- Quarterly pool performance reports
- Analysis of delinquencies and defaults
- CPR (Conditional Prepayment Rate) tracking
- CDR (Conditional Default Rate) tracking
- Comparison to original rating assumptions
- Rating reviews and potential downgrades/upgrades

**In Our Example:**
- Rate the five classes (AAA for Class A, AA for Class B, etc.)
- Monitor monthly performance metrics
- Flag if delinquencies exceed thresholds
- Alert if default losses threaten lower-rated classes
- Issue surveillance reports quarterly

#### Relationships Between Entities:

The diagram shows critical relationships:

**Originator ↔ Issuer/SPV:**
- Originator sells mortgages and receives proceeds
- SPV owns mortgages and issues securities to pay originator
- Clean transfer of risk from originator to investors

**Servicer ↔ Master Servicer:**
- Master Servicer oversees Servicer performance
- If Servicer fails, Master Servicer can replace them
- Ensures continuous, professional servicing

**Trustee ↔ Note Trustee:**
- Dual trustee structure protects investors from multiple angles
- Mortgage Trustee holds collateral, Note Trustee enforces bond terms
- Separate oversight creates checks and balances

**Agent Bank ↔ Cash Manager:**
- Cash Manager determines distribution amounts
- Agent Bank executes the distributions
- Coordinate on payment mechanics and investor communications

**All Entities → Rating Agencies:**
- All entities provide performance data
- Rating agencies monitor pool health
- Rating changes signal market confidence in the structure

#### The Waterfall Priority (Cash Distribution Order):

This is how monthly cash flows of £8.5 million are distributed:

**Step 1: Operating Expenses**
- Trustee fees (approximately £50,000)
- Servicer fees (approximately £45,000)
- Agent bank fees (approximately £35,000)
- Cash manager fees (approximately £30,000)
- Rating agency fees (approximately £15,000)
- **Total: ~£175,000**

**Step 2: Interest Payments** (in order of priority)
- Class A interest: ~£1.1 million (AAA, 50 bps spread)
- Class B interest: ~£735,000 (AA, 100 bps spread)
- Class C interest: ~£735,000 (A, 150 bps spread)
- Class D interest: ~£735,000 (BBB, 250 bps spread)
- Class Z interest: £0 (deferred interest)
- **Total: ~£3.3 million**

**Step 3: Principal** (if funds remain after interest)
- Class A principal: up to balance (gets paid down first)
- Class B principal: up to balance (only if A paid)
- Class C principal: up to balance (only if B paid)
- Class D principal: up to balance (only if C paid)
- Class Z principal: remaining funds (if anything left)
- **Total: Remaining £4.5-5 million goes to principal**

**Key Point:** In a normal month with adequate collections:
- All senior classes (A, B, C, D) receive full interest
- Principal is paid down starting with Class A
- Class Z receives little to no distributions until others are paid

In a stressed month with high delinquencies:
- Operating expenses and senior interest still paid
- Less principal available
- Class Z receives almost nothing
- Losses begin to impact Class D

In a severe loss event:
- Losses accumulate at Class Z level
- When Class Z is exhausted, losses begin hitting Class D
- Then Class C, B, and finally Class A
- This is why Class A is AAA rated—very protected

---

### Summary: The Complete Picture

An RMBS transaction creates a sophisticated financial structure designed to:

1. **Benefit originators** by immediately recovering capital and transferring risk
2. **Protect investors** through tranching, priorities, and oversight
3. **Manage mortgages professionally** through specialized servicers
4. **Monitor performance** through multiple independent oversight entities
5. **Provide liquidity** by transforming illiquid mortgages into tradeable securities

The legal structure accomplishes this through:
- **Bankruptcy remoteness** of the SPV
- **Clear legal title** held by the trustee
- **Strict priority of payments** protecting senior classes
- **Professional management** by specialized servicers
- **Multiple layers of oversight** from trustees, master servicers, and rating agencies

Understanding these entities and their roles is essential for evaluating RMBS investments, as each entity's performance directly impacts investor returns.

---

## Key Takeaways

- Securitisation is not about creating cash flow—it's about allocating existing cash flow from the mortgage pool to different investors based on risk/return profiles
- The SPV (Special Purpose Vehicle) is the legal linchpin that isolates mortgages from the originator's creditors
- Tranching creates multiple security classes with different priorities, where senior classes (AAA) are highly protected and subordinate classes absorb losses first
- Nine key entities (originator, servicer, master servicer, trustee, note trustee, agent bank, cash manager, rating agencies) each play critical roles in the securitization
- The waterfall mechanism is the engine that distributes monthly cash flows in strict priority order: operating fees → Class A interest → Class B interest → ... → Principal paydown (A to Z)
- Diversification across thousands of mortgages reduces correlation risk, allowing for lower yields on senior classes despite the same underlying mortgage risks
- Securitisation is a zero-sum game subject to the second law of thermodynamics: total sources and uses must reconcile; what pays in must get paid out

---

## See Real Examples

- [Sample Mortgage & Pool Data](/docs/rmbs/sample-mortgage-data/)
- [Sample Monthly Reports](/docs/rmbs/sample-reports/)

## Geographic Distribution

{{< mortgage-map >}}

---

## Next Steps

For comprehensive technical documentation including:
- Complete architecture overview
- All 11 Python files explained in detail
- Bash script orchestration
- API endpoints and integration
- Deployment guide
- Working code examples
   - beyond this the approach here leads to automation
   - auto mortgage updating to warehouse pool
   - auto portfolio optimization for RMBS pools from warehouse pool
   - auto RMBS pool optimization based on live spreads and costs feeds
   - auto generated regulatory compliant data tape feeds

See: [RMBS Technical Architecture](/docs/rmbs/technical-architecture/)

## Related Documentation

- [API Reference](/docs/rmbs/api-reference/)
- [Dashboard User Guide](/docs/rmbs/dashboard-guide/)

---

## References

- Bank of England, Credit Risk Directorate. "Data tape standards for mortgage data submission"
- Real-world transaction prospectuses and recent securitization structures
- Rating agency methodologies (public domain)
- Historical mortgage performance data
- HPI (House Price Index) datasets
