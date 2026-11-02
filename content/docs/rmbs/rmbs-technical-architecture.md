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
- **Data isolated for audit.** Every critical number (market data, calibrations, published methodology parameters, regulatory rules, the model's own estimates) sits in its own data set under `data/inputs/` with its source, as-of date, status and owner. The config refers to it by id; `DATA_REGISTER.md` lists every set with its fingerprint, and each build records the ones it used.
- **As of the issue date.** Data sets carry effective dates. A build is priced as of its issue date (the pool cut-off plus the usual time to close) and takes every data set in the version in force then.
- **Pool and enhancement together.** Credit enhancement cannot be sized apart from the pool: a dynamic build selects and re-selects the pool until the deal is viable; a fixed build sizes the enhancement once, on the loans given.
- **Selective, recorded testing.** A master test list (`tranching_tests.json`) sets which stresses, sizing methods, gates and reports run, per jurisdiction and named run, with a mandatory floor no run can drop. Each build records its test plan; a regression harness compares builds with a stored baseline.
- **Cash conservation.** Sources equal uses every month and over the life of the deal, against every note. It is tested on every run.
- **Currency integrity.** Every loan must be in the deal currency, checked when the cash-flow engine loads the pool and again on the tape. Other currencies are allowed by design; for now the model works only in GBP.
- **Outputs tested after they are written.** The BoE tape is read back and tested against every rule in the tape rules data set before it is released.
- **Jurisdiction as a setting.** The profile is UK (BoE template, UK prospectus note terms); others can be added.

## Order of operations

1. Ingest and curate loan and borrower data (BoE field dictionary, validator, data-quality checks)
2. Ingest market data (Bank Rate, the OIS curve, note margins and deal terms from public issues, house prices, costs), each dated
3. Select and price the pool ← loop start (dynamic mode; a fixed pool skips selection)
4. Create the securitisation (notes, a swap sized to the expected fixed-rate balance, an amortising reserve, day-1 costs; post-swap issuance economics; currency check)
5. Freeze the static set
6. Stress and tranche (rating stresses → capital stack → sensitivity cushion → challengers) → market-terms check → viability ← loop end
7. Issue outputs (BoE tape, tested after writing; investor report, deck, draft prospectus)
8. Life-of-deal reporting: one pack per payment date from the servicer's performance file, with a tested tape refresh

If the deal is not viable, the loop returns to step 3. If it is uneconomic at issue, the build stops with an **issuance failure** for manual assessment.

## Main modules

| Area | Module | Role |
|---|---|---|
| Data | `boe_dictionary.py`, `boe_lld_validator.py`, `data_quality.py`, `boe_tape_tests.py`, `currency.py` | BoE field dictionary, template validation (rules from a dated data set), pool data-quality checks, post-generation tape tests (files read back, every rule checked), currency integrity |
| Market data | `build_rate_data.py`, `config_loader.py` | Bank Rate history and versions, the OIS curve, the SONIA–Bank Rate basis, Class A margins from public issues, the rate-model fit; every data set resolved as of the issue date |
| Pool | `loan_generator.py`, `generate_pool.py`, `mortgage_rate_pricer.py` | Synthetic new-issue pool (calibrated to BoE MLAR) and risk-based pricing |
| Selection | `pool_selection.py`, `pre_filter.py`, `rl_pool_selector.py`, `pool_register.py` | Step 3 in the build loop: eligibility filter, simulated-annealing selection on the model's own stack, pool exclusivity and whole security groups (same property or borrower) |
| Cash flows | `rmbs_tranching_model_complete.py`, `interest_rate_swap.py`, `prepayment_model.py` | Loan-level monthly projection, revenue and principal waterfalls, PDLs, reserve, triggers, swap, call variants; loan-level prepayment (early repayment charges, end-of-fix spike, refinancing incentive, burnout); options for a liquidity reserve, excess-spread notes, pro-rata principal, notes below par, compounded SONIA and a revolving period |
| Credit | `uk_credit_model.py`, `rating_stress_core.py`, `credit_model_registry.py` | Generic calculated credit model (score → PD → rating default rate × LGD) with loan-level adjustments (arrears, flats, high value, region); blank agency slots for benchmarking |
| Structuring | `static_set.py`, `ce_sizing.py`, `capital_stack.py`, `sensitivity.py`, `credit_coverage.py` | Frozen static set, rating stresses, capital-stack sizing by bisection, sensitivity cushion on the estimated parameters (re-solved), joint check and reverse stress, implied tranche PD / EL / LGD |
| Challengers | `breakeven.py`, `monte_carlo_validation.py`, `path_stability.py` | Break-even per class, EL-based tranching, Monte Carlo validation with importance sampling, swap termination and rate-move stresses, path stability |
| Build | `securitisation_builder.py`, `tranching_run.py`, `market_terms.py`, `run_registry.py`, `data_register.py` | The loop: select → create → freeze → stress & tranche → viability, dynamic or on a fixed pool, scoped by the master test list; terms checked against public deals issued by the date; every run registered (code version, config and data hashes, seed, pool fingerprint, test run, issue date, timings) |
| Outputs | `deal_outputs.py`, `rmbs_report_generator.py`, `boe_report_generator.py`, `monthly_reporting.py` | Tape, investor report, deck, sources and uses, stress waterfall, draft prospectus, monthly reporting per payment date (reconciled pack, HTML, tape refresh with cover sheet, data quality and diffs) |
| Console | `webapp.py`, `manual_review.py` | Local web console: dashboard, status flow, exceptions, control with a job queue, manual review, versioned assumptions editor |

## Running it

```bash
./generate_pool.sh pool_config.csv
```

```bash
python3 securitisation_builder.py output/synthetic_warehouse.parquet --output-dir output/build
```

Options: `--fixed-pool` sizes the enhancement on the loans given, once; `--as-of YYYY-MM-DD` sets the issue date (default: the cut-off plus the usual time to close); `--as-of current` runs on today's market, labelled a stale-pool stress.

```bash
./generate_outputs.sh all
```

```bash
python3 webapp.py --port 8765
```

The console runs all of the above from the browser, on the local machine only.

## Capital stacks

The stack is a profile in `assumptions.json`, following issued UK notes (each class one rating category below the class above, Class Z unrated, ratings shown as AAA(sf)):
- `prime_master_trust`: A (AAA) + Z, the default;
- `sequential_mezz`: A (AAA), B (AA), C (A), D (BBB) + Z;
- `uk_sequential_full`: A (AAA) to F (B) + Z.

Class Z can be **retained** (at par, the index flat, as in public prime deals; the originator's return is the residual) or **sold** (margin solved for the required yield, with a discount only beyond a cap). It funds the reserve, and released reserve repays it first.

## Tests

The test suite covers:
- cash reconciliation every month and over the life of the deal;
- loss ordering;
- the credit model against hand-computed values;
- stack profiles;
- the builder loop, pool selection and the pool exclusivity and security-group rules;
- the optimiser's bisection, sensitivity, the joint check and issuance economics;
- implied tranche risk against the public PD- and EL-based tranching results;
- the UK note conventions for every stack profile;
- loan-level prepayment, the structure options and the actual-period monthly waterfall;
- the data register, the master test list, the regression harness and the web console;
- every output generator;
- the BoE tape read back after writing, each kind of file defect caught by its rule, and every rule having a check;
- currency integrity, fixed and dynamic pool modes, the issue date and as-of runs, the market-terms check, the amortising reserve and the swap schedule.

CI runs the full suite on every push.
