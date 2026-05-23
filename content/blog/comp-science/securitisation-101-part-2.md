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

Now let us examine each entity's specific role, responsibilities, and relationships:

#### The Nine Key Entities and Their Functions:

![RMBS Entity Roles](/images/comp-science/rmbs_entity_roles.png)

#### Detailed Entity Roles:

##### 1. Originator

The originator creates the mortgages and initiates the securitization.

**Key Responsibilities:**
- Originates mortgages through traditional underwriting processes
- Funds loans to qualified borrowers
- Sells mortgages to the SPV and receives proceeds
- May provide representations and warranties about loan quality

**Why They Do This:**
- Immediate capital recovery to continue lending
- Risk transfer -- mortgages no longer on their balance sheet
- Fee income from loan origination and servicing

**In Our Example:**
Together Financial Services originates 10,000 mortgages totalling GBP 733.1 million,
sells the pool to TGT-RMBS Plc and receives proceeds to fund new originations.

##### 2. Issuer / Special Purpose Vehicle (SPV)

The SPV is the legal and financial centre of the securitization structure.

**Key Responsibilities:**
- Owns the mortgage pool (bankruptcy-remote entity)
- Issues notes to raise capital for purchasing mortgages
- Receives mortgage payments and distributes funds per the waterfall
- Complies with all indenture agreements and regulatory requirements

**In Our Example:**
TGT-RMBS Plc purchases GBP 733.1 million of mortgages and issues GBP 744.3 million
of notes (Classes A through Z) to fund the purchase and reserve.

##### 3. Loan Servicer

The servicer is the operational backbone, managing day-to-day mortgage servicing.

**Key Responsibilities:**
- Collects monthly payments from borrowers
- Reports monthly performance metrics, delinquencies, and defaults
- Manages loss mitigation and forbearance programs
- Forwards all collections to the SPV

**In Our Example:**
SVC-TGT-001 services the 10,000 loans, collects approximately GBP 63.9 million
monthly, and forwards collections to the SPV within 2 business days.

##### 4. Master Loan Servicer

Provides oversight and quality assurance for the loan servicer.

**Key Responsibilities:**
- Monitors servicer performance against required standards
- Reviews servicer reports and audits for accuracy
- Can substitute the servicer if performance deteriorates materially

**In Our Example:**
Independent Master Loan Servicer monitors SVC-TGT-001 and can replace them if
they fail to perform.

##### 5. Trustee (Mortgage Trustee)

Holds the mortgages and represents investor interests in the underlying collateral.

**Key Responsibilities:**
- Holds legal title to the mortgages in trust for noteholders
- Monitors SPV and servicer compliance with transaction terms
- Takes enforcement action if either party breaches obligations
- Maintains mortgage documents and records

**In Our Example:**
Trustee holds 10,000 mortgage notes and ensures servicer properly collects and
remits payments.

##### 6. Note Trustee (Indenture Trustee)

Represents the interests of the noteholders and enforces the terms of the bonds.

**Key Responsibilities:**
- Enforces the terms of the notes and transaction documents
- Collects payments from the issuer/SPV and distributes to investors
- Takes enforcement action on behalf of noteholders if SPV defaults

**In Our Example:**
Note Trustee ensures TGT-RMBS Plc distributes funds to noteholders each month
and acts if the SPV fails to pay investors.

##### 7. Agent Bank (Paying Agent)

Manages the logistics of payments and investor accounts.

**Key Responsibilities:**
- Distributes monthly interest and principal payments to investors
- Prepares detailed account statements for each investor
- Handles tax reporting information

**In Our Example:**
Agent Bank receives approximately GBP 63.9 million monthly from the SPV,
calculates interest due to each class, and distributes accordingly.

##### 8. Cash Manager

Implements the priority of payments and manages reserves.

**Key Responsibilities:**
- Manages reserve accounts and maintains liquid funds
- Implements the priority of payments (the waterfall) each month
- Calculates interest and principal due to each tranche

**Monthly Waterfall Process:**
1. Receives collections from servicer via SPV
2. Allocates funds in priority order: Class A interest, Class B, C, D, then principal
3. Manages reserve accounts to ensure next month's interest is covered

**In Our Example:**
Manages reserve account of GBP 11.0 million (Moody's 1.5% minimum) and implements
the monthly waterfall with approximately GBP 63.9 million in collections.

##### 9. Rating Agencies

Assess credit quality and monitor performance.

**Key Responsibilities:**
- Rate each note tranche based on credit analysis before issuance
- Monitor pool performance quarterly
- Issue surveillance updates and rating changes if performance deteriorates

**In Our Example:**
Rate the five classes (AAA for Class A through NR for Class Z), monitor monthly
metrics, and flag if delinquencies exceed rating thresholds.

#### Relationships Between Entities:

**Originator -- Issuer/SPV:**
Clean transfer of risk from originator to investors via the SPV.

**Servicer -- Master Servicer:**
Master Servicer oversees Servicer; can replace them if performance fails.

**Trustee -- Note Trustee:**
Dual structure protects investors: Mortgage Trustee holds collateral,
Note Trustee enforces bond terms.

**Agent Bank -- Cash Manager:**
Cash Manager determines distribution amounts; Agent Bank executes them.

**All Entities to Rating Agencies:**
All entities provide performance data; rating changes signal market confidence.

#### The Waterfall Priority (Cash Distribution Order):

Monthly cash flows of approximately GBP 63.9 million are distributed as follows:

**Step 1: Operating Expenses (~GBP 52k/month)**
- Trustee fees: GBP 16,667/month
- Servicer fees: GBP 25,000/month
- Paying agent, legal, rating agency fees: GBP 10,000/month

**Step 2: Interest Payments (~GBP 3.3m/month)**
- Class A: ~GBP 2.1m (GBP 595.4m x 4.25% / 12)
- Class B, C, D: ~GBP 735k each
- Class Z: residual only

**Step 3: Principal (remainder)**
- Class A paid down first, then B, C, D, Z in order
- In a stressed month: less principal available; Class Z receives almost nothing
- In a severe loss event: losses cascade from Class Z upward

---

### Summary: The Complete Picture

An RMBS transaction creates a structure designed to benefit originators by
recovering capital immediately, protect investors through tranching and
oversight, and transform illiquid mortgages into tradeable securities.

The legal structure accomplishes this through bankruptcy remoteness of the SPV,
clear legal title held by the trustee, strict priority of payments protecting
senior classes, and multiple layers of oversight from trustees, master servicers,
and rating agencies.

---

## Key Takeaways

- Securitisation allocates existing cash flow from the mortgage pool to investors based on risk/return profiles
- The SPV is the legal linchpin isolating mortgages from the originator's creditors
- Tranching creates multiple security classes where senior classes (AAA) are highly protected
- Nine key entities each play critical roles in the securitization
- The waterfall distributes monthly cash flows in strict priority: fees, interest senior to junior, then principal
- Sources and uses must always reconcile -- what pays in must get paid out

---

## Next Steps

See [RMBS Technical Architecture & Implementation](/docs/rmbs-technical-architecture/)
for complete documentation including architecture overview, Python files, API endpoints and deployment.

---

## References

- Bank of England, Credit Risk Directorate. Data tape standards for mortgage data submission
- Rating agency methodologies (public domain)
- Historical mortgage performance data
