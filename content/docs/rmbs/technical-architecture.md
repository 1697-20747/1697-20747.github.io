---
title: "RMBS Technical Architecture & Implementation"
description: "Complete technical documentation for RMBS system architecture, codebase, and integration"
weight: 10
---

# RMBS Technical Documentation: Architecture, Code Solutions & Integration

Complete technical guide to the RMBS modeling and reporting system architecture, codebase, and operational workflows.

---

## Executive Summary

This RMBS system consists of:
- **1 Python pool generator** (10,000 mortgages → £733.1m)
- **5 financial models** (CPR, CDR/LGD, loss cascading, sources & uses, tranching)
- **1 reporting engine** (investor reports in CSV + Parquet)
- **1 dashboard system** (3 interactive dark-mode HTML dashboards)
- **1 REST API server** (secure access with API keys)
- **6+ bash scripts** (orchestration and automation)
- **3,700+ lines of documentation**

All components work together in a modular pipeline: **Pool → Models → Reports → Dashboards/API → Distribution**

---

<details>
<summary><h2>Part 1: Project Architecture Overview</h2></summary>

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     RMBS SYSTEM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  INPUT                                                            │
│  ├─ Pool Parameters (10k loans, £733.1m)                        │
│  ├─ HPI Data (House Price Index adjustments)                    │
│  └─ Assumptions (CPR, CDR, LGD, fees, rates)                    │
│                ↓                                                  │
│  GENERATION LAYER                                                │
│  ├─ generate_rmbs_pool.py (creates 10k loans)                   │
│  └─ → rmbs_pool_10000_hpi_adjusted.parquet (733.1m)             │
│                ↓                                                  │
│  MODELING LAYER                                                  │
│  ├─ prepayment_model.py (CPR seasonality)                       │
│  ├─ default_model.py (CDR by credit score)                      │
│  ├─ fee_loader.py (82 bps admin fees)                           │
│  ├─ sources_and_uses.py (59.5 bps costs)                        │
│  └─ rmbs_tranching_model_complete.py (Monte Carlo)              │
│                ↓                                                  │
│  CALCULATION LAYER                                               │
│  ├─ calculate_amortisation_with_fees.py (schedules)             │
│  └─ loss_cascading.py (waterfall)                               │
│                ↓                                                  │
│  REPORTING LAYER                                                 │
│  ├─ rmbs_report_generator.py (CSV + Parquet)                    │
│  └─ generate_rmbs_report.sh (orchestrator)                      │
│                ↓                                                  │
│  OUTPUT LAYER                                                    │
│  ├─ Dashboard: rmbs_dashboard_generator.py (3 HTML)             │
│  ├─ API: rmbs_api_server.py (REST endpoints)                    │
│  ├─ Client: rmbs_api_client.py (Python library)                 │
│  └─ Bash: generate_dashboards.sh, run_all_standalone.sh         │
│                ↓                                                  │
│  DISTRIBUTION                                                    │
│  ├─ HTML Dashboards (browser viewing)                           │
│  ├─ API Endpoints (secure access)                               │
│  ├─ CSV Reports (spreadsheet import)                            │
│  ├─ Parquet Files (data science)                                │
│  └─ PNG Diagrams (visual reference)                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Pool Generator
    ↓
[rmbs_pool_10000_hpi_adjusted.parquet] ← 10k loans, £733.1m
    ↓
Loan Scheduler
    ↓
[loan_schedules_10000.parquet] ← 2.3m rows, monthly amortization
    ↓
Financial Models (CPR, CDR, LGD)
    ↓
Tranching Model (Monte Carlo)
    ↓
[tranche_results_*.parquet] ← Class A-Z cash flows
    ↓
Reporting Engine
    ├─ investor_report_YYYY-MM.csv
    └─ investor_report_YYYY-MM.parquet
    ↓
Dashboard Generator
    ├─ dashboard_pool_YYYYMM.html
    ├─ dashboard_tranches_YYYYMM.html
    └─ dashboard_summary_YYYYMM.html
    ↓
API Server
    └─ REST endpoints (secured with API keys)
```

</details>

---

<details>
<summary><h2>Part 2: Core Generation Files</h2></summary>

<details>
<summary><h3>generate_rmbs_pool.py (500+ lines)</h3></summary>

**Purpose:** Creates the mortgage pool from scratch

**What it does:**
- Generates 10,000 synthetic mortgages with realistic parameters
- Assigns loan amounts (£10k-£500k range)
- Calculates LTV ratios (60%-100%+)
- Assigns credit scores (300-850 range)
- Sets interest rates based on credit quality
- Applies HPI (House Price Index) adjustments by region
- Adds UK regional data (London, SE, EA, Midlands, North)

**Input:** None (generates from seed=42)

**Output:**
```
rmbs_pool_10000_hpi_adjusted.parquet (733.1 million pounds)
├─ 10,000 rows (one per mortgage)
├─ Columns: loan_id, original_balance, current_balance, ltv, 
│           interest_rate, credit_score, region, hpi_adjustment, etc.
└─ Size: ~1.5 MB
```

**Key Parameters:**
- Pool size: £733.1m
- Loan count: 10,000
- Average loan: £73,309
- Average LTV: 78.5%
- Weighted avg rate: 4.65%
- Regions: London (64.5%), SE (15.5%), EA (8%), Midlands (6%), North (6%)

</details>

<details>
<summary><h3>calculate_amortisation_with_fees.py (400+ lines)</h3></summary>

**Purpose:** Generates monthly payment schedules for each loan

**What it does:**
- Reads the mortgage pool
- For each of 10,000 mortgages, creates a 30-year amortization schedule
- Calculates monthly payment based on interest rate
- Tracks principal reduction each month
- Tracks interest paid each month
- Handles scheduled payoff
- Creates 480 monthly records per loan (40 years of history)

**Input:** `rmbs_pool_10000_hpi_adjusted.parquet`

**Output:**
```
loan_schedules_10000.parquet (2,363,988 rows)
├─ One row per loan per month
├─ Columns: loan_id, month, payment, principal, interest, 
│           remaining_balance, etc.
└─ Size: ~150 MB
```

**Logic:**
```
For each loan over 360 months:
  Monthly Payment = Loan Balance × (Rate × (1+Rate)^n) / ((1+Rate)^n - 1)
  Interest = Remaining Balance × Monthly Rate
  Principal = Payment - Interest
  New Balance = Previous Balance - Principal
```

</details>

</details>

---

<details>
<summary><h2>Part 3: Financial Models</h2></summary>

<details>
<summary><h3>prepayment_model.py (300+ lines)</h3></summary>

**Purpose:** Models CPR (Conditional Prepayment Rate) with seasonality

**What it does:**
- Implements SeasonedCPRModel class
- Base CPR: 6% (seasonally adjusted pool)
- Seasoning curve: 3% → 12% (peak at month 30) → 3%
- Refi incentive: 0.3x to 3.0x multiplier based on rates
- Seasonal factors: Jul-Aug 1.20x, Dec 0.80x
- Applies to each loan monthly

**Usage:**
```python
from prepayment_model import SeasonedCPRModel
model = SeasonedCPRModel(base_cpr=0.06)
cpr = model.calculate_cpr(
    month=12,
    refi_incentive=1.5,
    season_month=5
)
# Returns: 0.08 (8% monthly CPR)
```

**Outputs:**
- Monthly CPR per loan
- Pool-level weighted CPR
- Sensitivity to rate changes

</details>

<details>
<summary><h3>default_model.py (350+ lines)</h3></summary>

**Purpose:** Models CDR (Conditional Default Rate) and LGD (Loss Given Default)

**What it does:**
- CDR calculation by credit score:
  - Score 750+: 0.05% base CDR
  - Score 700-749: 0.25% base CDR
  - Score 650-699: 0.50% base CDR
  - Score <650: 2.0% base CDR
- LTV stress multiplier: 1.0x to 2.0x
- HPI stress multiplier: 1.0x to 1.5x cap
- Unemployment stress: 1.0x to 1.5x cap
- LGD: 85% discount (stable market), 75% (falling market)

**Formula:**
```
Monthly CDR = Base CDR × LTV Stress × HPI Stress × Unemployment / 12
LGD = 85% (rising HPI) or 75% (falling HPI)
Recoverable Amount = Loan Balance × (1 - LGD)
Loss Amount = Loan Balance × LGD
```

**Outputs:**
- Monthly CDR per loan
- Pool-level weighted CDR
- Expected losses per scenario

</details>

<details>
<summary><h3>fee_loader.py (250+ lines)</h3></summary>

**Purpose:** Loads and validates admin fee structure (82 bps annual)

**What it does:**
- Reads fee structure from admin_fees_schedule.json
- Validates fee rates
- Calculates monthly fee allocation
- Handles dual JSON formats (legacy + new)
- Returns fee components:
  - Trustee fees: 20 bps
  - Servicer fees: 15 bps
  - Agent bank: 12 bps
  - Rating agencies: 6 bps
  - Other: ~29 bps
  - **Total: 82 bps annual**

**Monthly Calculation:**
```
Annual Admin Fee = £733.1m × 0.0082 = £6.0m
Monthly Admin Fee = £6.0m / 12 = £500k
```

**Outputs:**
- Fee schedule JSON
- Monthly fee allocation
- Fee impact on net cashflows

</details>

<details>
<summary><h3>sources_and_uses_balanced.py (400+ lines)</h3></summary>

**Purpose:** Creates balanced sources and uses statement (59.5 bps issuance costs)

**What it does:**
- **SOURCES:**
  - Mortgage pool: £733.1m
  - Note premium/discount: adjusts pricing
  - **Total: £733.1m to £737.5m**

- **USES:**
  - Class A notes: £219.9m
  - Class B notes: £146.6m
  - Class C notes: £146.6m
  - Class D notes: £146.6m
  - Class Z notes: £73.3m
  - Issuance costs: £4.4m (59.5 bps)
  - **Total: £737.5m**

- Pricing: Notes = 100.59% (1% premium)
- Markup: £4.36m
- Issuance costs: £4.4m
- Balance: £0 (self-funding)

**Outputs:**
```
sources_and_uses_ledger_balanced.json
├─ Mortgage purchase price: £733.1m
├─ Note issuance amounts (A-Z)
├─ Cost allocation
└─ Pricing matrices
```

</details>

<details>
<summary><h3>rmbs_tranching_model_complete.py (800+ lines)</h3></summary>

**Purpose:** Complete Monte Carlo tranching engine with all models integrated

**What it does:**
- Integrates CPR model (prepayment)
- Integrates CDR/LGD model (defaults & losses)
- Implements loss cascading waterfall
- Runs monthly projections (480 months)
- Calculates tranche cash flows
- Implements priority of payments
- Handles multiple scenarios (base, severe crash, high rates, etc.)
- Generates Parquet output files

**Monthly Loop (480 months):**
```
For each month:
  1. Apply CPR to get prepayments
  2. Apply CDR to get defaults
  3. Apply LGD to calculate losses
  4. Cascade losses through tranches (Z→D→C→B→A)
  5. Calculate available cash flow
  6. Implement waterfall distribution:
     - Operating fees
     - Class A interest
     - Class B interest
     - Class C interest
     - Class D interest
     - Principal paydown (A→B→C→D→Z)
  7. Update tranche balances
  8. Record outputs
```

**Input Scenarios:**
- `base`: Normal economic conditions
- `severe_crash`: 30% HPI drop, 2% unemployment rise
- `high_rates`: SONIA at 6%, prepayments drop
- `rising_defaults`: +200 bps CDR stress

**Outputs:**
```
tranche_results_scenario.parquet
├─ Month-by-month flows
├─ Class A-Z principal balances
├─ Class A-Z interest received
├─ Total losses realized
├─ Cumulative defaults
└─ Performance metrics
```

</details>

</details>

---

<details>
<summary><h2>Part 4: Reporting & Visualization</h2></summary>

<details>
<summary><h3>rmbs_report_generator.py (600+ lines)</h3></summary>

**Purpose:** Generates investor reports in CSV and Parquet formats

**What it does:**
- Takes pool data, loan schedules, and model outputs
- Calculates investor report metrics for specified month
- Generates comprehensive investor report with:
  - Pool statistics (balance, count, avg LTV, WAR)
  - Tranche notionals and ratings
  - Monthly cashflows (interest, principal)
  - Admin fees and cost allocation
  - Delinquency and default metrics
  - Prepayment rates (CPR)
  - Performance summary

**Report Columns:**
```
Reporting_Date, Pool_Balance, Num_Loans, Avg_Loan,
Class_A_Notional, Class_A_Rate, Class_A_Interest,
Class_B_Notional, Class_B_Rate, Class_B_Interest,
... (all tranches)
Admin_Fees_Monthly, Interest_Total, Principal_Total,
Arrears_Count, Arrears_Balance, Delinquency_Rate,
CPR, CDR, Weighted_Avg_Rate, ...
```

**Output Formats:**
- CSV: Human-readable, Excel compatible
- Parquet: Compressed, optimized for data analysis

</details>

<details>
<summary><h3>rmbs_dashboard_generator.py (1,100+ lines)</h3></summary>

**Purpose:** Generates 3 interactive dark-mode HTML dashboards

**What it does:**
- Reads pool data and generates 3 separate HTML files:

**1. Pool Dashboard** (8.3 KB)
- Key metrics (balance, count, avg size, LTV, rate)
- Key assumptions box (CPR, CDR, LGD, fees)
- LTV distribution histogram
- Geographic distribution pie chart
- Dark mode styling
- Chart.js visualizations

**2. Tranches Dashboard** (9.5 KB)
- Waterfall diagram (Class A-Z boxes)
- Tranche economics table
- Monthly interest/principal
- Class A coupon display
- Tranche allocation pie chart
- Spread comparison bar chart

**3. Executive Summary** (9.9 KB)
- Top KPI cards (4 metrics)
- Capital structure breakdown
- Monthly cashflows bar chart
- Key metrics & assumptions (4 info boxes)
- Risk metrics (equity buffer, protection levels)

**Features:**
- Dark mode (#0f0f0f background)
- Interactive charts (hover tooltips)
- Responsive design (mobile to desktop)
- Chart.js from CDN
- Color-coded by entity type
- Standalone HTML (no dependencies)

**Output:**
```
logs/YYYY-MM_HHMMSS/
├─ dashboard_pool_YYYYMM.html (8.3 KB)
├─ dashboard_tranches_YYYYMM.html (9.5 KB)
└─ dashboard_summary_YYYYMM.html (9.9 KB)
```

</details>

</details>

---

<details>
<summary><h2>Part 5: API System</h2></summary>

<details>
<summary><h3>rmbs_api_server.py (1,500+ lines)</h3></summary>

**Purpose:** REST API server for secure access to reports and dashboards

**What it does:**
- Flask-based REST API
- API key authentication
- Fine-grained permissions (read_reports, read_dashboards)
- Rate limiting (prevent abuse)
- Audit logging (track access)
- Key management (create, revoke keys)
- 13 endpoints total

**Public Endpoints:**
```
GET /api/v1/health                  → Health check
GET /api/v1/docs                    → API documentation
```

**Authentication:**
```
GET /api/v1/auth/key-info           → Get current key info
```

**Reports:**
```
GET /api/v1/reports/list            → List all reports
GET /api/v1/reports/summary         → Get summary stats
GET /api/v1/reports/download/{date}/{file} → Download report
```

**Dashboards:**
```
GET /api/v1/dashboards/list         → List dashboards
GET /api/v1/dashboards/download/{date}/{file} → Download
GET /api/v1/view/dashboard/{date}/{file} → View HTML
```

**Admin (Master key required):**
```
POST /api/v1/admin/keys/create      → Create API key
GET /api/v1/admin/keys/list         → List all keys
POST /api/v1/admin/keys/revoke      → Revoke key
```

**Features:**
- Secure API keys (SHA256 hashed)
- Expiration dates (configurable)
- Usage tracking (count, last used)
- Rate limiting (5 tiers)
- HTTPS support
- Production-ready (Gunicorn)

</details>

<details>
<summary><h3>rmbs_api_client.py (200+ lines)</h3></summary>

**Purpose:** Python client library for API access

**What it does:**
- Provides easy-to-use Python interface to API
- Methods for all endpoints:
  - `health_check()`
  - `get_key_info()`
  - `list_reports()`
  - `download_report(year, month, format)`
  - `list_dashboards()`
  - `download_dashboard(year, month, type)`
  - `view_dashboard(year, month, type)`
  - `get_reports_summary()`

**Usage:**
```python
from rmbs_api_client import RMBSAPIClient

client = RMBSAPIClient(
    base_url='https://api.rmbs.example.com',
    api_key='your_key'
)

# List reports
reports = client.list_reports()
print(f"Available: {reports['count']} reports")

# Download report
client.download_report(2026, 5, 'csv', 'report.csv')

# Download dashboard
client.download_dashboard(2026, 5, 'pool', 'dashboard.html')
```

</details>

</details>

---

<details>
<summary><h2>Part 6: Bash Scripts - Orchestration</h2></summary>

<details>
<summary><h3>generate_dashboards.sh</h3></summary>

**Purpose:** Generate all 3 dashboards in one command

**What it does:**
1. Accepts parameters: month, year, optional pool file, optional PNG flag
2. Finds the pool file (with fallback)
3. Calls rmbs_dashboard_generator.py
4. Creates timestamped output folder (logs/YYYY-MM_HHMMSS/)
5. Generates 3 HTML files (pool, tranches, summary)
6. Also generates investor report (CSV + Parquet)
7. Creates manifest.txt with metadata
8. Optionally exports to PNG (requires Chrome)

**Command:**
```bash
bash generate_dashboards.sh 5 2021
```

**Output:**
```
logs/2021-05_20260517_080204/
├─ dashboard_pool_202105.html
├─ dashboard_tranches_202105.html
├─ dashboard_summary_202105.html
├─ investor_report_2021-05.csv
├─ investor_report_2021-05.parquet
└─ manifest.txt
```

</details>

<details>
<summary><h3>generate_rmbs_report.sh</h3></summary>

**Purpose:** Generate investor report for specific month

**Command:**
```bash
bash generate_rmbs_report.sh 5 2021
```

**Output:**
```
logs/2021-05_HHMMSS/
├─ investor_report_2021-05.csv
├─ investor_report_2021-05.parquet
└─ manifest.txt
```

</details>

<details>
<summary><h3>generate_multi_reports.sh</h3></summary>

**Purpose:** Generate reports for multiple months in batch

**Command:**
```bash
bash generate_multi_reports.sh 1 12 2021
```

**Generates:** 12 months (Jan-Dec 2021) in sequence

</details>

<details>
<summary><h3>run_all_standalone.sh</h3></summary>

**Purpose:** Master runner for all standalone tests

**What it does:**
1. Tests pool generation
2. Runs prepayment model tests
3. Runs default model tests
4. Runs loss cascading tests
5. Runs sources & uses validation
6. Runs fee loader validation

**Runtime:** ~2-3 minutes

</details>

<details>
<summary><h3>Model-Specific Test Scripts</h3></summary>

**run_prepayment_model_standalone.sh**
- Tests CPR prepayment model
- Validates seasonal factors
- Tests refi incentive

**run_default_model_standalone.sh**
- Tests CDR by credit score
- Tests LTV stress multipliers
- Tests LGD calculations

**run_loss_cascading_standalone.sh**
- Tests waterfall priority
- Tests loss allocation
- Runs stressed scenarios

**run_sources_and_uses_standalone.sh**
- Validates balance (sources = uses)
- Checks pricing (100.59%)
- Verifies cost allocation

**run_fee_loader_standalone.sh**
- Validates 82 bps fee structure
- Calculates monthly fees
- Tests fee allocation

</details>

</details>

---

<details>
<summary><h2>Part 7: Summary & Integration</h2></summary>

### Quick File Count

**Python Files:** 11 files, 7,400+ lines
- 1 generator
- 2 scheduling/amortization
- 5 financial models
- 2 reporting & visualization
- 1 API server + client

**Bash Scripts:** 9 orchestration scripts

**Configuration:** 4 JSON files (fees, assumptions, costs)

**Documentation:** 3,700+ lines

### Typical Workflows

**Monthly Reporting:**
```bash
bash generate_dashboards.sh 5 2021
# Creates: dashboards + reports in timestamped folder
```

**Batch Annual:**
```bash
bash generate_multi_reports.sh 1 12 2021
# Generates all 12 months automatically
```

**Testing Everything:**
```bash
bash run_all_standalone.sh
# Validates all models and components
```

### System Status

✅ 11 Python files (production-ready)
✅ 9 Bash orchestration scripts
✅ 3 Interactive dark-mode dashboards
✅ REST API with key management
✅ Python client library
✅ 3,700+ lines of documentation
✅ Modular, tested architecture

**Complete RMBS modeling and reporting platform** ready for deployment.

</details>

---

## File Location

`/mnt/user-data/outputs/RMBS_TECHNICAL_DOCUMENTATION_COLLAPSIBLE.md`

This version uses HTML `<details>` and `<summary>` tags which allow:
- ✅ Click to expand/collapse sections
- ✅ Works in GitHub, modern markdown viewers
- ✅ Nested collapsible sections
- ✅ Preserves all content
- ✅ Clean visual hierarchy

