---
title: "Sample Reports"
description: "Example investor reports and performance metrics from TGT-RMBS-2025-001"
weight: 30
---

## Sample Monthly Investor Report

This is an example of the monthly investor report generated for May 2026:

### Pool Performance Summary

| Metric | Value |
|--------|-------|
| **Reporting Date** | 2026-05-31 |
| **Pool Balance** | £733,087,150 |
| **Number of Loans** | 10,000 |
| **Average Loan** | £73,309 |
| **Weighted Average Rate** | 4.65% |
| **Weighted Average LTV** | 78.5% |

---

### Monthly Cash Collections

| Item | Amount |
|------|--------|
| **Principal Collected** | £6,105,300 |
| **Interest Collected** | £2,431,940 |
| **Total Mortgage Payments** | £8,537,240 |
| **Admin Fees** | £500,835 |
| **Net Available to Investors** | £8,036,405 |

---

### Interest & Principal Distributions (Waterfall)

| Tranche | Interest Due | Interest Paid | Principal Paid |
|---------|---|---|---|
| **Class A (AAA)** | £1,099,600 | £1,099,600 | £3,000,000 |
| **Class B (AA)** | £733,100 | £733,100 | £1,500,000 |
| **Class C (A)** | £733,100 | £733,100 | £750,000 |
| **Class D (BBB)** | £733,100 | £733,100 | £500,000 |
| **Class Z (NR)** | £0 | £0 | £256,300 |
| **TOTAL** | **£3,299,000** | **£3,299,000** | **£6,006,300** |

---

### Delinquency & Default Metrics

| Metric | Value | % |
|--------|-------|---|
| **30-Day Arrears** | 45 loans | 0.45% |
| **60-Day Arrears** | 28 loans | 0.28% |
| **90-Day Arrears** | 18 loans | 0.18% |
| **In Foreclosure** | 8 loans | 0.08% |
| **Total Delinquent** | 99 loans | 0.99% |
| **Current/Paid to Date** | 9,901 loans | 99.01% |

---

### Prepayment & Loss Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **CPR (Prepayment)** | 5.8% | In line with assumptions |
| **CDR (Default)** | 0.24% | Within expected range |
| **Current Losses** | £156,400 | Expected loss level |
| **Cumulative Losses (YTD)** | £892,300 | Normal |
| **Loss Severity** | 16.5% | Stable |

---

### Reserve Account Status

| Reserve | Balance | Target | % of Target |
|---------|---------|--------|-------------|
| **Interest Reserve** | £2,431,940 | £2,400,000 | 101% ✅ |
| **Principal Reserve** | £1,200,000 | £1,000,000 | 120% ✅ |
| **Total Reserve** | **£3,631,940** | **£3,400,000** | **107% ✅** |

---

### Class-by-Class Summary

#### **Class A (AAA) - Senior Most**
- **Notional**: £219,932,450
- **Interest Rate**: SONIA + 50 bps = 5.00%
- **Monthly Interest**: £1,099,600
- **YTD Principal Reduction**: £18,000,000
- **Current Balance**: £201,932,450
- **Status**: ✅ Fully paid, well-protected

#### **Class B (AA)**
- **Notional**: £146,621,630
- **Interest Rate**: SONIA + 100 bps = 5.50%
- **Monthly Interest**: £733,100
- **YTD Principal Reduction**: £9,000,000
- **Current Balance**: £137,621,630
- **Status**: ✅ Paid in full, protected

#### **Class C (A)**
- **Notional**: £146,621,630
- **Interest Rate**: SONIA + 150 bps = 6.00%
- **Monthly Interest**: £733,100
- **YTD Principal Reduction**: £4,500,000
- **Current Balance**: £142,121,630
- **Status**: ✅ Paid in full, moderate protection

#### **Class D (BBB)**
- **Notional**: £146,621,630
- **Interest Rate**: SONIA + 250 bps = 7.00%
- **Monthly Interest**: £733,100
- **YTD Principal Reduction**: £3,000,000
- **Current Balance**: £143,621,630
- **Status**: ✅ Paid in full, absorbs some losses

#### **Class Z (Unrated - Equity)**
- **Notional**: £73,310,810
- **Interest Rate**: Residual (0% until seniors paid)
- **Monthly Interest**: £0
- **YTD Principal Reduction**: £1,536,300
- **Current Balance**: £71,774,510
- **Status**: ✅ Absorbs losses first

---

## Performance Comparison vs. Assumptions

| Metric | Assumption | Actual | Variance |
|--------|-----------|--------|----------|
| **CPR** | 6.0% | 5.8% | -3% (better) |
| **CDR** | 0.25% | 0.24% | -4% (better) |
| **Delinquency Rate** | 1.0% | 0.99% | In line |
| **Loss Severity** | 85% | 16.5% expected | In line |
| **Interest Collections** | 100% | 100% | On target |

---

## Key Observations

✅ **Collections on track** — Pool collecting as expected  
✅ **Delinquencies stable** — Low and manageable  
✅ **Reserves adequate** — Exceeding targets  
✅ **Senior classes protected** — AAA & AA fully paid  
✅ **Performance vs model** — Better than base assumptions  

---

## Available Report Formats

This data is available in two formats:

### **CSV Format**
- Human-readable spreadsheet format
- Compatible with Excel, Google Sheets
- File: `investor_report_202605.csv`

### **Parquet Format**
- Optimized for data analysis
- Used by data scientists & analysts
- File: `investor_report_202605.parquet`

---

## Historical Reports

Monthly reports are generated for all periods:
- May 2026 (current example)
- April 2026
- March 2026
- February 2026
- (Going back to origination)

---

## Next Steps

For:
- **Interactive dashboards** showing this data visually: See [Dashboard Guide](/docs/rmbs/dashboards-guide/)
- **Complete technical details**: See [Technical Architecture](/docs/rmbs/technical-architecture/)
- **Raw mortgage & pool data**: See [Sample Data](/docs/rmbs/sample-mortgage-data/)

