---
title: "Building a Securitisation Pool Optimiser -- Part 1: Architecture and Pipeline"
date: 2026-05-20T07:27:29Z
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "optimisation", "python", "machine-learning"]
description: "How we built an ML-driven pool selection engine that maximises Class A note issuance from a 20,000-loan warehouse using simulated annealing and adaptive Monte Carlo."
summary: "Four-stage pipeline combining deterministic pre-filtering, greedy initialisation, simulated annealing, and adaptive Monte Carlo to solve a 2^20 combinatorial optimisation problem in minutes."
ShowToc: true
TocOpen: true
ShowBreadCrumbs: true
disableAnchoredHeadings: false
cover:
  image: ""
  alt: "RMBS pool optimiser architecture"
---

## The Problem

Structuring a residential mortgage-backed security (RMBS) is a combinatorial
optimisation problem. You have a warehouse of 20,000 loans. You need to select
a subset that, when securitised, maximises the face value of the senior
(Class A, AAA-rated) notes issued -- subject to hard constraints: sources must
equal uses exactly, the reserve fund must meet rating agency minimums, regional
concentration cannot exceed limits, and the pool must survive Monte Carlo stress
tests across multiple scenarios.

The search space is 2^20 -- over one million possible subsets. Brute force is
impossible. This post describes the four-stage pipeline we built to solve it.

---

## Pipeline Architecture

```
warehouse_pool_1.parquet  (20,000 loans, locked universe)
         |
         v
1. pool_selector_config.csv
   Target GBP, yield indications, LTV cap, region limits
         |
         v
2. pre_filter.py  (deterministic, runs once)
   Hard-eliminate: defaults, LTV > cap, score < floor
   Output: ~17,800 eligible loans, composite-scored
         |
         v  Feasibility: WAC > coupon floor? Pool > 120% of target?
         |  INFEASIBLE if not -- exits before running SA
         v
3. rl_pool_selector.py  (simulated annealing)
   Phase 1: Greedy warm-start (composite score)
   Phase 2: SA loop -- ADD / REMOVE / SWAP
   Reward = Class A GBP - weighted constraint penalties
         |
         v  Gate: portfolio >= 60% of target balance?
         v
4. adaptive_monte_carlo.py
   Below 60% : fast heuristic checks (microseconds)
   60-95%    : 600-1,400 simulations
   100%      : 2,000 simulations x 4 scenarios
         |
         v
output/optimised_pool.parquet
output/optimised_pool_report.txt
output/optimisation_history.csv
```

---

## Stage 1 -- Pre-filter

`pre_filter.py` makes one deterministic pass over all 20,000 loans.
Hard elimination criteria -- any one disqualifies a loan:

- Account status = default (`AR146 == 3`) or redeemed (`AR146 == 4`)
- Original LTV above pool cap (`AR135 > max_pool_wltv_pct / 100`)
- Credit score below floor (`AR46 < min_credit_score`)
- Zero or negative current balance (`AR67 <= 0`)

Applied to our warehouse this yields 17,783 eligible loans (88.9%), GBP 2,356m,
WAC 5.96%.

A feasibility check runs before any SA iteration. It computes the minimum pool
WAC needed to cover coupon expense plus operating costs, and exits with
`INFEASIBLE` if not met. If the Class B yield indication is too aggressive,
this fires immediately -- no iteration wasted.

Each eligible loan then receives a composite desirability score:

```python
score = 0.40 * normalised_WAC
      + 0.35 * (1 - normalised_LTV)   # low LTV preferred
      + 0.25 * normalised_credit_score
      - 0.10 * is_interest_only
      - 0.05 * is_buy_to_let
```

---

## Stage 2 -- Greedy Warm-Start

Cold-starting SA from a random portfolio wastes iterations on obviously bad
solutions. `greedy_initialise()` iterates composite-scored eligible loans and
greedily adds each one until the target balance is reached. Concentration caps
are only enforced after 20 loans -- single-loan dominance is unavoidable early.

Tested result: 6,268 loans, GBP 500.2m, Class A GBP 406.25m (81.2% of pool).
This is the baseline the SA agent improves from.

---

## Stage 3 -- Simulated Annealing Agent

At each iteration the agent chooses one of three actions, weighted by how close
the portfolio is to target balance:

| Action | When preferred | Effect |
|--------|---------------|--------|
| ADD | Balance below 90% | Add a random eligible loan |
| SWAP | Balance 90-110% | Replace one loan with another |
| REMOVE | Balance above 110% | Remove a loan |

**Reward function:**

```
reward = class_a_notional_gbp
       - 1,000,000 * |sources - uses| / 1e6
       - 100,000   * reserve_shortfall / 1e6
       - 10,000    * max(0, pool_wltv - ltv_cap)
       - 5,000     * max(0, top_region_pct - region_cap)
       - 2,000     * max(0, io_pct - io_cap)
       - 500,000   * n_mc_hard_kills
```

Penalty weights create a strict hierarchy. Fixing a sources-and-uses imbalance
(weight 1,000,000) is always worth more than improving Class A. A structurally
invalid portfolio is never accepted regardless of its Class A size.

**Acceptance criterion (Metropolis):**

```
if delta > 0:
    accept always
else:
    P(accept) = exp(delta / T)    # probability decays with temperature
```

Temperature starts at 1.0, cools by 0.995 per iteration, floors at 0.001
around iteration 1,100. Early iterations accept worse solutions freely to
escape local optima; later iterations become increasingly selective.

---

## Stage 4 -- Adaptive Monte Carlo

Scale simulation count to portfolio completion:

```
pct = current_balance / target_balance
if pct < 0.60: run fast heuristic only
else:          n_sims = int((pct - 0.60) / 0.40 * 2000)
               # 60% -> 50 sims, 80% -> 1,000, 100% -> 2,000
```

Above the gate, simulations run across four scenarios:

| Scenario | BBR shift | HPI | Unemployment |
|----------|-----------|-----|--------------|
| Base | 0 | +2%/yr | 4% |
| Rate +100bps | +1% | 0% | +2% |
| HPI -15% | 0 | -15%/yr | +3% |
| Stress | +2% | -20%/yr | +4% |

Each path simulates 360 monthly periods. Losses cascade bottom-up:
Class Z absorbs first, then D, C, B, A. Three hard kill conditions
cause MC FAIL and a 500,000 reward penalty:

- Class A P99 loss greater than GBP 0
- Class B P99 loss greater than 5% of Class B notional
- Reserve breach in more than 10% of simulations

This cuts total MC compute by roughly 70% versus running full simulations
at every iteration.

---

## Running the Optimiser

Generate the warehouse pool first if not already present:

```bash
cd /path/to/securitisation_RMBS
chmod +x *.sh
./generate_pool.sh warehouse_pool_1_config.csv
```

Benchmark run time on your machine:

```bash
python3 benchmark_optimizer.py
```

Run with default config (GBP 500m target):

```bash
./run_pool_selector.sh
```

Run with a custom target:

```bash
./run_pool_selector.sh my_deal_config.csv
```

Quick test with 500 iterations:

```bash
# Reduce iterations for test
sed -i '' 's/sa_max_iterations,5000/sa_max_iterations,500/' pool_selector_config.csv
./run_pool_selector.sh
# Restore full run
sed -i '' 's/sa_max_iterations,500/sa_max_iterations,5000/' pool_selector_config.csv
```

Review results:

```bash
cat output/optimised_pool_report.txt
```

---

## Status Signals

| Signal | Meaning |
|--------|---------|
| `OPTIMAL` | All constraints met, best Class A found |
| `BINDING_CONSTRAINT` | Solution found but constrained -- see report detail |
| `INFEASIBLE` | No solution exists -- reduce target or check yields |

---

*Part 2 covers the full code file inventory, IRS swap mechanics, BoE LLD compliance
(50/50 pass), Fitch UK RMBS Phase 1 and Phase 2 alignment fixes, and the RMBS deal structure.*
