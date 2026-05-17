---
title: "Securitisation 101: Party Roles and Waterfall"
date: 2026-05-17T07:13:29Z
draft: false
categories: ["comp-science"]
tags: [securitisation, tranching, RMBS, mortgages, finance]
description: "Entity roles, responsibilities and payment waterfall mechanics in RMBS securitisation."
summary: "Entity roles, responsibilities and payment waterfall mechanics in RMBS securitisation."
ShowToc: false
disableAnchoredHeadings: true
---
<!--more-->

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
- Total loan volume: GBP 733.1 million
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
- Purchases GBP 733.1 million mortgage pool from Together Financial Services
- Issues GBP 744.3 million of notes (Classes A-D plus Equity) to fund loan purchase and reserves
- Receives approximately GBP 63.9 million in monthly cash flows (GBP 61.1m principal + GBP 2.84m interest)
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
- Collects approximately GBP 63.9 million monthly from borrowers
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
- Sends monthly statements to Class A-D + Equity noteholders
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
- Agent Bank receives approximately GBP 63.9 million monthly from SPV
- Calculates interest due to each class based on their notional and coupon rate
- Distributes to Class A noteholders first (approximately GBP 2.1 million monthly interest)
- Then Class B, C, D (if funds available), then Equity
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
2. Calculates monthly interest obligation (Class A coupon rate x notional, etc.)
3. Allocates funds in priority order:
   - Interest to Class A
   - Interest to Class B
   - Interest to Class C
   - Interest to Class D
   - Remaining funds to principal (Class A first, then B, C, D, finally Z)
4. Manages reserve accounts to ensure next month's interest is covered

**In Our Example:**
- Manages reserve account of GBP 11.0 million (Moody's 1.5% minimum, calculated)
- Implements monthly waterfall with approximately GBP 63.9 million in collections
- Allocates approximately GBP 2.7 million to interest payments (across all tranches)
- Allocates approximately GBP 61.1 million to principal payments
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

**Originator ? Issuer/SPV:**
- Originator sells mortgages and receives proceeds
- SPV owns mortgages and issues securities to pay originator
- Clean transfer of risk from originator to investors

**Servicer ? Master Servicer:**
- Master Servicer oversees Servicer performance
- If Servicer fails, Master Servicer can replace them
- Ensures continuous, professional servicing

**Trustee ? Note Trustee:**
- Dual trustee structure protects investors from multiple angles
- Mortgage Trustee holds collateral, Note Trustee enforces bond terms
- Separate oversight creates checks and balances

**Agent Bank ? Cash Manager:**
- Cash Manager determines distribution amounts
- Agent Bank executes the distributions
- Coordinate on payment mechanics and investor communications

**All Entities -> Rating Agencies:**
- All entities provide performance data
- Rating agencies monitor pool health
- Rating changes signal market confidence in the structure

#### The Waterfall Priority (Cash Distribution Order):

This is how monthly cash flows of GBP 63.9 million are distributed:

**Step 1: Operating Expenses**
- Trustee fees (GBP 16,667/month, GBP 200k annual)
- Servicer fees (GBP 25,000/month, GBP 300k annual)
- Paying agent fees (GBP 1,250/month, GBP 15k annual)
- Legal & accounting fees (GBP 4,583/month, GBP 55k annual)
- Rating agency fees (GBP 4,167/month, GBP 50k annual)
- **Total: ~GBP 51,667/month (GBP 620k annual)**

**Step 2: Interest Payments** (in order of priority)
- Class A interest: ~GBP 2.1 million/month (GBP 595.4m x 4.25% ? 12)
- Class B interest: ~GBP 735,000 (AA, 100 bps spread)
- Class C interest: ~GBP 735,000 (A, 150 bps spread)
- Class D interest: ~GBP 735,000 (BBB, 250 bps spread)
- Equity interest: GBP 0 (deferred interest)
- **Total: ~GBP 3.3 million**

**Step 3: Principal** (if funds remain after interest)
- Class A principal: up to balance (gets paid down first)
- Class B principal: up to balance (only if A paid)
- Class C principal: up to balance (only if B paid)
- Class D principal: up to balance (only if C paid)
- Equity principal: remaining funds (if anything left)
- **Total: Remaining GBP 4.5-5 million goes to principal**

**Key Point:** In a normal month with adequate collections:
- All senior classes (A, B, C, D) receive full interest
- Principal is paid down starting with Class A
- Equity receives little to no distributions until others are paid

In a stressed month with high delinquencies:
- Operating expenses and senior interest still paid
- Less principal available
- Equity receives almost nothing
- Losses begin to impact Class D

In a severe loss event:
- Losses accumulate at Class Z level
- When Equity is exhausted, losses begin hitting Class D
- Then Class C, B, and finally Class A
- This is why Class A is AAA rated-very protected

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

- Securitisation is not about creating cash flow-it's about allocating existing cash flow from the mortgage pool to different investors based on risk/return profiles
- The SPV (Special Purpose Vehicle) is the legal linchpin that isolates mortgages from the originator's creditors
- Tranching creates multiple security classes with different priorities, where senior classes (AAA) are highly protected and subordinate classes absorb losses first
- Nine key entities (originator, servicer, master servicer, trustee, note trustee, agent bank, cash manager, rating agencies) each play critical roles in the securitization
- The waterfall mechanism is the engine that distributes monthly cash flows in strict priority order: operating fees -> Class A interest -> Class B interest -> ... -> Principal paydown (A to Equity)
- Diversification across thousands of mortgages reduces correlation risk, allowing for lower yields on senior classes despite the same underlying mortgage risks
- Securitisation is a zero-sum game subject to the second law of thermodynamics: total sources and uses must reconcile; what pays in must get paid out

---

## Next Steps

For comprehensive technical documentation including:
- Complete architecture overview
- All 11 Python files explained in detail
- Bash script orchestration
- API endpoints and integration
- Deployment guide
- Working code examples

See: [RMBS Technical Architecture & Implementation](/docs/rmbs-technical-architecture/)

---

## References

- Bank of England, Credit Risk Directorate. "Data tape standards for mortgage data submission"
- Real-world transaction prospectuses and recent securitization structures
- Rating agency methodologies (public domain)
- Historical mortgage performance data
- HPI (House Price Index) datasets