---
title: "RMBS Technical Architecture"
weight: 2
description: "How the UK RMBS generation model is built: order of operations, main modules and commands."
summary: "Architecture of the UK RMBS generation model."
aliases: ["/docs/rmbs/technical-architecture/"]
ShowToc: true
TocOpen: false
---

## Design

- **Generate, then test.** The model creates a UK-compliant securitisation from a warehouse of loans, with the rating tests built into the build loop, so the finished deal should pass review without change.
- **Data first.** Loans are held in the Bank of England loan-level template (field codes AR1…AR236) in Parquet, from generation through to the BoE tape.
- **Config, not code.** Every assumption lives in `assumptions.json`, `interest_rate_assumptions.json` and `pool_config.csv`, each listed in an assumptions register with the real input that replaces it.
- **Cash conservation.** Sources equal uses every month and over the life of the deal, against every note. It is tested on every run.
- **Jurisdiction as a setting.** The profile is UK (BoE template, UK prospectus note terms); others can be added.

## Order of operations

1. Ingest and curate loan and borrower data (BoE field dictionary, validator, data-quality checks)
2. Ingest market data (Bank Rate, mortgage rates, note margins, swap rates, house prices, costs)
3. Select and price the pool ← loop start
4. Create the securitisation (notes, swap, reserve, day-1 costs; post-swap issuance economics)
5. Freeze the static set
6. Stress and tranche (rating stresses → capital stack → sensitivity cushion) → viability ← loop end
7. Issue outputs (BoE tape, investor report, deck, draft prospectus)
8. Life-of-deal reporting (placeholder)

If the deal is not viable, the loop returns to step 3. If it is uneconomic at issue, the build stops with an **issuance failure** for manual assessment.

## Main modules

| Area | Module | Role |
|---|---|---|
| Data | `boe_dictionary.py`, `boe_lld_validator.py`, `data_quality.py` | BoE field dictionary, template validation, post-generation data-quality checks |
| Pool | `loan_generator.py`, `generate_pool.py`, `mortgage_rate_pricer.py` | Synthetic new-issue pool (calibrated to BoE MLAR) and risk-based pricing |
| Selection | `pre_filter.py`, `rl_pool_selector.py` | Eligibility filter and simulated-annealing pool selection |
| Cash flows | `rmbs_tranching_model_complete.py`, `interest_rate_swap.py` | Loan-level monthly projection, revenue and principal waterfalls, PDLs, reserve, triggers, swap, call |
| Credit | `uk_credit_model.py`, `rating_stress_core.py`, `credit_model_registry.py` | Generic calculated credit model (score → PD → rating default rate × LGD); blank agency slots for benchmarking |
| Structuring | `static_set.py`, `ce_sizing.py`, `capital_stack.py`, `sensitivity.py` | Frozen static set, rating stresses, capital-stack sizing, sensitivity cushion |
| Build | `securitisation_builder.py` | The loop: select → create → freeze → stress & tranche → viability |
| Outputs | `deal_outputs.py`, `rmbs_report_generator.py`, `boe_report_generator.py` | Tape, investor report, deck, sources and uses, stress waterfall, draft prospectus, per-month investor pack |

## Running it

```bash
./generate_pool.sh pool_config.csv
```

```bash
python3 securitisation_builder.py output/rmbs_pool_10000_hpi_adjusted.parquet --output-dir output/build
```

```bash
./generate_outputs.sh all
```

```bash
python3 credit_model_registry.py output/rmbs_pool_10000_hpi_adjusted.parquet
```

The last command benchmarks the registered credit models side by side.

## Capital stacks

The stack is a profile in `assumptions.json`:
- `prime_master_trust` (A + Z, the default);
- `sequential_mezz` (A, B, C, D + Z).

Class Z can be **retained** (at par, no yield test) or **sold** (margin solved for the required yield, with a discount only beyond a cap).

## Tests

The test suite covers:
- cash reconciliation every month and over the life of the deal;
- loss ordering;
- the credit model against hand-computed values;
- stack profiles;
- the builder loop;
- sensitivity and issuance economics;
- every output generator.
