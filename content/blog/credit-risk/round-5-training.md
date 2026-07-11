---
title: "Round 5: Training a 7B Credit Analyst"
date: 2026-06-20T12:00:00Z
draft: false
categories: ["credit-risk"]
tags: ["machine-learning", "fine-tuning", "camels"]
description: "Training results from Round 5 QLoRA fine-tuning of Qwen2.5-7B for automated bank credit analysis. 6,359 training pairs, 3 epochs on an A100 80GB, and what the loss curve reveals about when to stop training."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## The Experiment

Round 5 of fine-tuning Qwen2.5-7B for CAMELS bank credit analysis completed on 20 June 2026. The goal: teach a 7-billion-parameter model to write structured credit assessments that cite their sources correctly, interpret financial ratios in the right direction, and refuse to fabricate figures when data is missing.

The model trained on 6,359 instruction-response pairs for 3 epochs on a rented NVIDIA A100 80GB GPU via Vast.ai. Total cost: approximately $8. Total runtime: 8.1 hours.

This post covers the training statistics, what the loss curve tells us about when training actually stops being useful, and what the numbers mean for the deployed model.

## What Went In

The training data was assembled over three weeks of iterative evaluation:

| Dataset | Pairs | What It Teaches |
|---------|-------|-----------------|
| Base CAMELS pairs (Rounds 1-4) | 6,066 | Core credit analysis structure — assessments, key metrics, analysis paragraphs, peer context, risk sections |
| Refusal pairs | 58 | When extraction returns nothing, write a clean refusal instead of inventing figures |
| Peer contamination pairs | 43 | Tag every peer value with `[Peer roster: Bank Year]`, never use one bank's figures for another |
| Agency citation pairs | 120 | Paraphrase rating agency commentary and cite as `[Moody's, 2025-11]`, never quote verbatim |
| Direction-of-goodness pairs | 72 | 10th decile CET1 = strong (not weak); NSFR at 100% = regulatory floor (not impressive) |
| **Total (deduplicated)** | **6,359** | |

The 293 new Round 5 pairs represent 4.6% of the training mix. They target specific failure modes identified through grading 60 evaluation rows across 10 banks and 6 CAMELS pillars. The question is whether 4.6% is enough signal to shift behaviour.

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Base model | Qwen2.5-7B |
| Method | QLoRA (4-bit NF4, double quantization) |
| LoRA rank / alpha | 64 / 128 |
| Trainable parameters | 161.5M / 4.5B (3.58%) |
| Effective batch size | 16 (batch=2 × grad_accum=8) |
| Max sequence length | 4,096 tokens |
| Learning rate | 2×10⁻⁴, cosine schedule |
| Hardware | NVIDIA A100 80GB PCIe |
| Runtime | 8.1 hours (29,261 seconds) |
| Steps | 1,194 (397 per epoch × 3 epochs) |
| Step speed | ~24.5 seconds/step |

## The Loss Curve

![Training loss curve showing train loss decreasing from 1.5 to 0.36 and eval loss plateauing at 0.627](/images/camels-round5/loss_curve.png)

The training loss dropped rapidly in the first epoch — from 1.51 to 0.59 — then continued a slower descent through epochs 2 and 3, ending at 0.36.

The eval loss tells a different story. It tracked the training loss closely through epoch 1 (0.94 → 0.74), continued falling through epoch 2 (0.74 → 0.63), then flatlined. From step 900 to step 1194, eval loss barely moved: 0.631 → 0.627.

| Step | Epoch | Train Loss | Eval Loss | Token Accuracy |
|------|-------|-----------|-----------|----------------|
| 10 | 0.03 | 1.514 | — | 67.1% |
| 100 | 0.25 | 0.834 | 0.943 | 82.3% |
| 200 | 0.50 | 0.812 | 0.848 | 81.4% |
| 400 | 1.00 | 0.592 | 0.741 | 86.6% |
| 600 | 1.50 | 0.534 | 0.673 | 86.6% |
| 800 | 2.00 | 0.441 | 0.633 | 89.1% |
| 1000 | 2.50 | 0.446 | 0.627 | 89.4% |
| 1194 | 3.00 | 0.357 | 0.627 | 90.9% |

## Where Training Stopped Being Useful

The most important chart is the gap between train and eval loss:

![Bar chart showing widening gap between train and eval loss, indicating memorisation in epoch 3](/images/camels-round5/gap_chart.png)

At step 100, the gap was 0.11 (train 0.83, eval 0.94). By step 800, it had widened to 0.19 (0.44 vs 0.63). By step 1194, it was 0.27 (0.36 vs 0.63).

This widening gap is the signature of memorisation. The model kept getting better at predicting the exact tokens in the training set, but that additional precision stopped transferring to held-out data after roughly step 900 — about two-thirds of the way through epoch 3.

In hindsight, **2 epochs would have been sufficient**. The third epoch consumed 2.7 hours of GPU time and moved eval loss by 0.006 — from 0.633 to 0.627. That is $2.70 worth of memorisation rather than learning.

## Token Accuracy

![Token accuracy rising from 67% to 91% with diminishing returns after epoch 2](/images/camels-round5/token_accuracy.png)

Token prediction accuracy — the fraction of next-token predictions the model gets right — rose from 67.1% at step 10 to 90.9% at step 1190. The curve shows the same pattern as the loss: rapid improvement in epoch 1, continued gains in epoch 2, and a plateau through epoch 3. The model was already predicting 89% of tokens correctly by step 800. The final 2% gain over 394 more steps was mostly memorisation of training-set-specific phrasing.

## The Pipeline Context

This training run exists within a broader eval progression. Before any fine-tuning, the pipeline was iteratively improved through prompt engineering, extraction fixes, and grounding mechanism additions:

![Eval progression from 68.3% baseline through pipeline fixes to 83.4%, with Round 5 result pending](/images/camels-round5/eval_progression.png)

| Run | Score | What Changed |
|-----|-------|-------------|
| Baseline (Jun 03) | 68.3% | Initial locked measurement |
| Pipeline fixes (Jun 11) | 79.3% | V4 extraction engine, dual peer groups, 29-bank roster |
| Pipeline fixes (Jun 12) | 79.7% | Sensitivity metrics, roster expansion |
| Pipeline fixes (Jun 13) | **83.4%** | Decile direction rules, direction-of-goodness tables, entity disambiguation |
| Pipeline fixes (Jun 14) | 80.8% | Rule 10 overcorrection — a lesson in regression testing |

The pipeline alone moved the score from 68.3% to 83.4% — a 15.1 percentage point improvement — without touching the model weights. The question Round 5 answers is whether fine-tuning can push past what structured prompting alone achieves.

The target is 87%. The eval is running now.

## Infrastructure Lessons

The training itself was straightforward once the environment was right. Getting the environment right was not straightforward. Three Vast.ai instances were rented and destroyed before training actually ran:

**Instance 1** failed because bitsandbytes has no pre-compiled binary for CUDA 13.x. Fix: `export BNB_CUDA_VERSION=130`.

**Instance 2** failed because the NGC PyTorch CUDA 13 container ships with system-installed versions of apex, torchvision, transformers, and peft that conflict with pip-installed versions. Every pip install uncovers the next broken import. The only fix is a clean virtual environment that ignores all system packages.

**Instance 2 also** failed because the trl library renamed three critical parameters between versions: `tokenizer` became `processing_class`, `max_seq_length` became `max_length`, and `TrainingArguments` became `SFTConfig`. Documentation lags behind the code.

**Instance 3** ran successfully after building a setup script (`setup_clean_env.sh`) that creates an isolated venv from scratch, installs pip via `get-pip.py`, and verifies every import before declaring the environment ready.

The actual training was the easy part. The infrastructure was the hard part.

## What Comes Next

The eval run is in progress — 60 rows, 10 banks, 6 CAMELS pillars, graded against the same five-dimension rubric used for all prior runs. If the Round 5 model scores ≥87%, training is validated. If it scores 84-86%, the training data worked but the 293 new pairs were too diluted in the 6,359-pair mix — Round 6 would upsample them 3-5× for stronger signal. If it doesn't improve over the 83.4% pipeline-only baseline, then structured prompting may simply be the ceiling for this architecture, and further work should focus on extraction coverage and peer roster depth rather than model weights.

The loss curve suggests the model learned *something*. Whether that something is useful for credit analysis — or just memorisation of training-set phrasing — is what the eval will reveal.
