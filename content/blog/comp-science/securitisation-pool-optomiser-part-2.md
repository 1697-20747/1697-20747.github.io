---
title: "Building a Securitisation Pool Optimiser -- Part 2: Code, Design and Deal Structure"
date: 2026-05-20T07:28:00Z
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "optimisation", "python", "machine-learning"]
description: "Code inventory, IRS swap, BoE compliance, Fitch alignment, and the full RMBS deal structure."
summary: "Full code inventory, IRS swap design, BoE compliance, Fitch Phase 1+2 fixes, deal structure, trigger framework and SA design decisions."
ShowToc: true
TocOpen: true
ShowBreadCrumbs: true
disableAnchoredHeadings: false
cover:
  image: ""
  alt: "RMBS deal structure"
---

## Code File Summary

| File | Role |
|------|------|
| `pool_selector_config.csv` | All target deal parameters. Edit one file to change the deal. |
| `pre_filter.py` | Hard-elimination filter; reduces 20,000 loans to ~17,800 eligible; runs feasibility check. |
| `adaptive_monte_carlo.py` | Scales MC (50-2,000 sims) to completion; 4 scenarios x 3 timing distributions. |
| `rl_pool_selector.py` | SA optimiser with RL reward function; greedy warm-start then SA loop. |
| `run_pool_selector.sh` | Standalone bash launcher; auto-installs packages. |
| `benchmark_optimizer.py` | Measures SA and MC speed on local hardware before committing to a full run. |
| `loan_generator.py v1.1.0` | Loan generator; BoE + Fitch compliant: AR65=1, AR118 codes, AR154 rental, AR166/169. |
| `mortgage_rate_pricer.py` | Risk-based pricer using ONS lenders formula (APCP-T(21)07). |
| `generate_pool.py` | Pool assembler: iterates loans, writes BoE LLD AR1-AR236 Parquet. |
| `generate_pool.sh` | Bash launcher; auto-installs packages; validates output. |
| `interest_rate_swap.py` | IRS model: SPV pays fixed (pool WAC), receives BBR + spread. |
| `default_model.py v1.1.0` | CDR model + Fitch FSA-based LGD by property type and sector. |
| `sltv_calculator.py` | Fitch SLTV: HPI indexing + regional Sustainable Price Discount. New in Phase 2. |
| `boe_report_generator.py` | BoE PRA ABS compliant: LLD data tape (AR1-AR236), 7 CSV outputs. |
| `boe_excel_report.py` | 6-tab Excel workbook generated only after pool passes validation. |
| `boe_lld_validator.py` | 50-point compliance check against BoE PRA ABS April 2024. |
| `run_boe_report.sh` | Runs validator then CSV reports then Excel workbook. |
| `interest_rate_assumptions.json` | Single source of truth for all rates, swap config, tranche structure, VRR. |
| `assumptions.json` | MC parameters: CDR, CPR, LGD, scenario definitions, trigger thresholds. |
| `rmbs_tranching_model_complete.py` | Full MC tranching model v2.2.0; swap-integrated waterfall. |
| `vrr_entity.py` | TGT-VRR-LTD: 5% of each note class per UK SecReg Article 6(3)(b). |
| `asset_triggers.py` | Asset trigger (reversible) and non-asset trigger (permanent pass-through). |
| `master_trust.py` | Master trust vehicle; revolving framework PENDING. |
| `run_tranching_model.sh` | Tranching model launcher; six stress scenarios. |

---

## Interest Rate Swap

The pool contains 14,552 fixed-rate loans (72.8%, GBP 1,912m). All notes
are floating rate (BBR-indexed). Without a swap the SPV has a fixed/float
mismatch: pool income is fixed, coupon obligations move with BBR.

**Solution: plain-vanilla IRS under ISDA Master Agreement 2002.**

```
SPV pays:     5.867% fixed  (= pool fixed WAC)  x notional / 12
SPV receives: (BBR + 211.7 bps)                 x notional / 12
```

At inception (BBR = 3.75%) net = GBP 0. Break-even. BBR +100bps adds
+GBP 1.594m/month to the waterfall.

The swap notional amortises monthly in line with the fixed-rate pool balance.
All income entering the waterfall is on a floating basis -- fixed coupons are
converted via the swap before reaching `interest_collected`.

Termination events (non-asset triggers): counterparty downgrade below BBB-,
MTM exposure above GBP 5m without collateral posting, counterparty insolvency.

---

## BoE LLD Compliance

Validated against BoE PRA ABS Data Reporting Instructions April 2024.
**Status: 50/50 checks pass -- COMPLIANT.**

Three fixes applied to `loan_generator.py`:

| Field | Problem | Fix |
|-------|---------|-----|
| AR65 | Was `2` (EUR code) | Fixed to `1` (GBP) |
| AR118 | Was text labels (SVR, TRACKER) | Fixed to BoE numeric codes: 9=BBR, 11=SVR |
| AR212 | Missing from schema | Added as empty string |

Run `./run_boe_report.sh` to produce: LLD data tape (AR1-AR236 per loan),
cover sheet, investor letter, pool summary, tranche report, swap summary,
regional breakdown, and 6-tab Excel workbook.

---

## Fitch UK RMBS Criteria Alignment

Reviewed against Fitch UK RMBS Rating Criteria May 2025.

### Phase 1 -- Data field fixes (loan_generator.py v1.1.0)

| Field | Fix | Why |
|-------|-----|-----|
| AR55 | Exact date DD-MM-YYYY (was quarter Q1-2025) | Fitch needs exact date for seasoning and SLTV |
| AR154 | Gross annual rental income for BTL (was wrong field) | BTL ICR in Fitch FF matrix |
| AR166 | Copy of AR146 (account status) | Fitch ResiGlobal reads AR166 not AR146 |
| AR169 | Copy of AR147 (arrears balance) | Fitch uses AR169 for arrears floor |

### Phase 2 -- Model improvements

**FSA-based LGD** (`default_model.py`): Loss Given Default now differentiated
by property type and sector per Fitch Foreclosure Sale Adjustment table:

| Sector | Property | FSA | LGD floor |
|--------|----------|-----|-----------|
| Owner-occupied | House | 20% | 20% |
| Owner-occupied | Flat | 25% | 25% |
| BTL | House | 30% | 30% |
| BTL | Flat | 35% | 35% |

HPI stress adds a further 2-5% to FSA in declining markets.

**AR122 restructuring** (`default_model.py`): 1.5x CDR multiplier for the
550 restructured loans (2.75% of pool, AR122=Y) per Fitch criteria.

**SLTV calculator** (`sltv_calculator.py`, new file): Computes Fitch
Sustainable LTV using regional HPI indexing and Sustainable Price Discount:

```
SLTV = total_balances / (original_valuation x HPI_ratio x (1 - SPD))
```

Regional SPDs: London 7.5%, South East 5.0%, Scotland 2.5%, Wales 2.5%.
Pool result: WA SLTV 32.3% vs WA origination LTV 39.4%.

**Default timing distributions** (`adaptive_monte_carlo.py`): Added
front-loaded, back-loaded, and even default shapes per Fitch criteria.
MC now runs 12 combinations (4 scenarios x 3 timing shapes). Back-loaded
is the binding case for this pool -- 20% IO loans mean defaults concentrate
at the interest-only reset date.

---

## Deal Structure

All amounts scale with the pool balance selected by the optimiser.

**Tranche structure** (all floating rate, BBR-indexed):

| Tranche | Rating | % | Coupon | Spread over BBR |
|---------|--------|---|--------|-----------------|
| Class A | AAA | 80% | 4.25% | +50 bps |
| Class B | AA | 8% | 4.75% | +100 bps |
| Class C | BBB | 5% | 5.75% | +200 bps |
| Class D | BB | 4% | 7.50% | +375 bps |
| Class Z | NR | 3% | Residual | n/a |

Waterfall: fees, then A/B/C/D coupon in seniority, then Z residual.
Loss cascade: Z absorbs first, then D, C, B, A.

**VRR Entity (TGT-VRR-LTD):** 5% of each tranche per UK SecReg Art 6(3)(b).

---

## Trigger Framework

**Asset trigger** (reversible, payments reduced to 75% of due):

| Metric | Watch | Trigger |
|--------|-------|---------|
| 90-day arrears | 5.0% | 7.5% of pool |
| Cumulative losses | 2.0% | 3.0% of original pool |
| Reserve fund | 1.2% | 1.0% of pool |

**Non-asset trigger** (permanent pass-through, mirrors Granite 2008):
seller share below 5%, originator rating below BBB-, servicer failure,
issuer insolvency.

---

## Key Design Decisions

**Why SA over PPO?** SA needs no training data. Penalty hierarchy is explicit,
temperature is visible, every iteration logged. PPO needs a corpus of warehouse
pools that does not yet exist.

**Why scale MC to completion?** The 60% gate lets the first half of SA
iterations run at near-zero MC cost. Above the gate, the optimiser becomes
progressively more conservative. Cuts MC compute by ~70%.

**Why S&U is the highest penalty?** S&U imbalance is binary -- the deal cannot
close. LTV and regional concentration have soft zones. Weight 1,000,000 ensures
the agent never accepts a structurally invalid portfolio.

**Why reserve is sized from actual pool balance?** When the pool is GBP 550m
vs a GBP 500m target, the reserve must be 1.5% of GBP 550m. Using target
balance caused 50% reserve breach rate in stress tests.

---

## References

- Fitch UK RMBS Rating Criteria, May 2025
- BoE PRA ABS Data Reporting Instructions, April 2024
- ONS APCP-T(21)07 Lenders formula for mortgage interest repayments
- NAO Introduction to Asset-Backed Securities, November 2016
- UK Securitisation Regulation Article 6(3)(b): Vertical slice retention
