---
title: "Sample Mortgage & Pool Data"
description: "Example mortgage loan and pool-level data from the TGT-RMBS-2025-001 securitization"
weight: 20
---

## Sample Mortgage Loan

Here's an example of a single mortgage in the 10,000 loan pool:

| Field | Value |
|-------|-------|
| **Loan ID** | LOAN-0001 |
| **Original Balance** | £125,000 |
| **Current Balance** | £118,500 |
| **Interest Rate** | 4.65% |
| **Maturity (years)** | 25 |
| **Monthly Payment** | £631.42 |
| **Loan-to-Value (LTV)** | 78.5% |
| **Credit Score** | 745 |
| **Region** | London |
| **Property Type** | Terraced House |
| **Origination Date** | 2023-06-15 |
| **First Payment Date** | 2023-07-01 |

---

## Pool Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Loans** | 10,000 |
| **Pool Balance** | £733,087,150 |
| **Average Loan** | £73,309 |
| **Median Loan** | £42,883 |
| **Min Loan** | £10,000 |
| **Max Loan** | £500,000 |
| **Average LTV** | 78.5% |
| **Weighted Average Rate** | 4.65% |
| **Average Credit Score** | 715 |
| **Average Age (months)** | 24 |

---

## Geographic Distribution

| Region | Count | % | Balance |
|--------|-------|---|---------|
| **London** | 6,450 | 64.5% | £473.2m |
| **South East** | 1,550 | 15.5% | £113.7m |
| **East Anglia** | 800 | 8.0% | £58.6m |
| **Midlands** | 600 | 6.0% | £43.9m |
| **North** | 600 | 6.0% | £43.6m |
| **TOTAL** | **10,000** | **100%** | **£733.1m** |

---

## LTV Distribution

| LTV Range | Count | % | Description |
|-----------|-------|---|-------------|
| **60-70%** | 2,100 | 21% | Prime mortgages |
| **70-80%** | 3,800 | 38% | Standard mortgages |
| **80-90%** | 2,900 | 29% | Higher LTV |
| **90-100%** | 900 | 9% | High LTV |
| **100%+** | 300 | 3% | Equity release |

---

## Credit Score Distribution

| Score Range | Count | % | Risk Level |
|-------------|-------|---|------------|
| **750+** | 3,200 | 32% | Excellent |
| **700-749** | 4,100 | 41% | Good |
| **650-699** | 2,100 | 21% | Fair |
| **<650** | 600 | 6% | Poor |

---

## Monthly Cash Flow Example

For a typical month (e.g., May 2026) with normal performance:

| Component | Amount | Notes |
|-----------|--------|-------|
| **Mortgage Payments** | £8,537,240 | Principal + Interest collected |
| **Scheduled Principal** | £6,105,300 | Amortization |
| **Scheduled Interest** | £2,431,940 | At weighted rate |
| **Admin Fees** | £500,835 | 82 bps annually = ~£500k/month |
| **Available to Investors** | £8,036,405 | After fees |

---

## Key Assumptions (Base Case)

| Assumption | Value | Description |
|-----------|-------|-------------|
| **CPR (Prepayment)** | 6.0% | Conditional Prepayment Rate |
| **CDR (Default)** | 0.25% | Conditional Default Rate |
| **LGD (Loss Given Default)** | 85% | Loss recovery rate |
| **SONIA Rate** | 4.50% | BoE Base Rate |
| **Lender SVR** | 8.00% | Standard Variable Rate |

---

## Tranche Structure (£733.1m Pool)

| Class | Notional | % | Rating | Spread | WAL* |
|-------|----------|---|--------|--------|-----|
| **Class A** | £219,932,450 | 30% | AAA | 50 bps | 3.2 yrs |
| **Class B** | £146,621,630 | 20% | AA | 100 bps | 4.1 yrs |
| **Class C** | £146,621,630 | 20% | A | 150 bps | 5.3 yrs |
| **Class D** | £146,621,630 | 20% | BBB | 250 bps | 6.8 yrs |
| **Class Z** | £73,310,810 | 10% | NR | Residual | 12.5 yrs |
| **TOTAL** | **£733,108,150** | **100%** | | | |

*WAL = Weighted Average Life

---

## Pricing & Issuance

| Item | Amount |
|------|--------|
| **Mortgage Pool Purchase Price** | £733,100,000 |
| **Note Issuance Amount** | £733,100,000 |
| **Issuance Costs** | £4,400,000 (59.5 bps) |
| **Note Pricing** | 100.59% |
| **Markup** | £4,360,000 |
| **Sources & Uses Balance** | £737,465,000 (balanced) |

---

## Expected Monthly Distributions

Based on base case assumptions:

| Class | Interest/Month | Principal/Month | Total/Month |
|-------|---|---|---|
| **Class A** | £1,099,600 | £3,000,000 | £4,099,600 |
| **Class B** | £733,100 | £1,500,000 | £2,233,100 |
| **Class C** | £733,100 | £750,000 | £1,483,100 |
| **Class D** | £733,100 | £500,000 | £1,233,100 |
| **Class Z** | £0 | £256,300 | £256,300 |
| **TOTAL** | **£3,299,000** | **£6,006,300** | **£9,305,300** |

(Note: Subject to cash flow availability and waterfall priority)

---

## Pool Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **Current Delinquency** | 0.8% | Normal |
| **Cumulative Defaults** | 1.2% | Expected |
| **Prepayment Rate (CPR)** | 5.8% | In line with assumption |
| **Loss Severity** | 16.5% | Within expected range |
| **Reserve Coverage** | 1.02x | Adequate |

---

## Data Sources & Assumptions

- Pool generated with seed=42 (reproducible)
- Based on BoE data tape standards
- HPI adjustments by UK region
- Credit score distribution from historical data
- Rate assumptions from SONIA + spread
- Loss assumptions from rating agency methodologies

---

## Next Steps

For complete details including:
- Loan-level schedules (2.3 million monthly records)
- Monthly pool aggregates (480 months of projections)
- Tranche-specific cash flows
- Stress scenario results
- Interactive dashboards

See the [Technical Documentation](/docs/rmbs/technical-architecture/) or [Dashboard Guide](/docs/rmbs/dashboards-guide/)

