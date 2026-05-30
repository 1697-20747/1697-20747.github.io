#!/usr/bin/env python3
"""Run once to complete the blog post."""
from pathlib import Path

p = Path("/Users/bruceschultz/Documents/blog/169720747/content/blog/comp-science/llm-credit-paper-generator.md")

suffix = """

Assistant (the target output the model learns to produce):

  ## Capital Adequacy (C)

  **Assessment: Strong**

  ### Key Metrics
  - CET1 ratio: 14.0% [Source: p.53] — 950bp above the 4.5% Pillar 1 minimum,
    7th decile globally (median: 13.8%, n=847 bank-years)
  - Leverage ratio: 5.4% [Source: p.53] — 175bp above the 3.25% UK minimum
  - MREL: 35.7% [Source: p.54] — above the indicative 2025 requirement

  ### Analysis
  Lloyds maintains a strong capital position with a CET1 ratio of 14.0% [Source: p.53],
  comfortably above both regulatory minimums and internal targets. The 50bp year-on-year
  improvement reflects strong organic capital generation...

  ### Peer Context
  At the 7th decile globally (median: 13.8%), Lloyds is positioned above the peer median.
  Among UK peers the ratio is broadly in line with Barclays (13.8%) and above NatWest (13.6%).

  ### Key Risks
  - Basel IV output floor (72.5% by 2030) — estimated 30-40bp CET1 headwind
  - Ongoing share buyback programme creates downward pressure
  - Pension deficit sensitivity under rising discount rates
```

The benchmark decile context is pre-computed from the population index and injected into the user prompt before the model sees it. The model learns to incorporate it into narrative prose. Every metric gets this treatment for every bank.

For full technical detail on the six training pipelines, quality tiers, the interface to Qwen training, and what the model actually learns — see the [technical documentation](/docs/camels-llm/).

---

## The Benchmarking Problem

A credit paper that says CET1 ratio is 14.0% is useless without context. Is that strong? Weak? This was a design requirement from day one — every number needs population context.

The benchmark index is built from all processed financial data. For each metric: mean, median, p10, p25, p75, p90, decile thresholds. Separate distributions for all years and recent years (last 3). Regional breakdowns for UK, EU, US, AU, CA where sample covers RWA in the same currency — GBP figures are not comparable to USD figures, so regional distributions are kept separate.

At inference time every extracted metric gets its decile appended before the LLM sees it. The benchmark table appears at the top of every generated credit paper:

| Metric | Value | Global Decile | Median | p10-p90 |
|--------|-------|---------------|--------|---------|
| CET1 Ratio | 14.0% [p.53] | **7th** | 13.8% | 10.5-14.2% |
| Leverage Ratio | 5.4% [p.53] | **5th** | 5.5% | 5.1-9.3% |
| LCR | 145% [p.183] | **4th** | 165% | 150-171% |

The benchmark improves as more data is added. With FDIC and EBA included it covers 800+ bank-years across five currency regions.

---

## The Compute Problem

16GB of unified memory on an M2 Pro. This is the constraint everything else bends around.

The base Qwen2.5-7B model at full precision loads at 15GB. There is essentially nothing left for training. Solution: the pre-quantised 4-bit version from the MLX community hub — 4GB loaded, 12GB remaining. Even then, sequence length has to be 512 tokens to avoid Metal GPU OOM errors.

Training speed: 0.5 iterations per second. 600 iterations: about 20 minutes. Validation loss: 3.14 to 0.876 across three Mac training rounds.

The MLX API changes between versions. mlx-lm 0.31.3 uses `python -m mlx_lm lora` (subcommand style). `--lora-layers` was renamed `--num-layers`. LoRA rank and alpha moved to a YAML config. The training script detects the version at runtime and adapts.

Post-training GGUF export for Ollama fails with a U32 data type error — known MLX/Ollama incompatibility. The workaround is an MLX direct server on port 8080. This works for inference but crashes the system under load. 16GB is not enough for production inference with a 7B model. Colab Pro will produce a proper GGUF via Unsloth, which does the conversion cleanly.

---

## How Post-Training of Qwen Actually Works

For anyone who has not done this before.

**The base model.** Qwen2.5-7B-Instruct is a 7-billion parameter language model trained by Alibaba on a large general corpus. It already knows how to follow instructions, write structured text, and reason. It knows the word CET1. What it does not know: what a good CAMELS analysis looks like, the correct regulatory thresholds, when to cite page numbers, when to refuse to fabricate. That is what post-training fixes.

**HuggingFace** is a model registry — a place to download model weights. Qwen2.5-7B-Instruct is published there by Alibaba under Apache 2.0. Free, open weights, no approval required. Download once, runs locally forever. You need a free account and an access token. That is it — it is a file download, not a service.

The `mlx-community` organisation on HuggingFace publishes pre-quantised versions optimised for Apple Silicon. `mlx-community/Qwen2.5-7B-Instruct-4bit` loads in 4GB instead of 15GB. This is what makes training feasible on 16GB Mac.

**QLoRA.** Instead of updating all 7.6 billion parameters — requiring 30-60GB — you freeze the base model and train small adapter matrices injected into specific layers. This project's adapters have 1.4 million trainable parameters out of 7.6 billion total. That is 0.019%. The trained adapter file is 7MB. The base model is 4GB. They combine at inference time.

**Sequence length is the critical hyperparameter.** At 512 tokens (Mac), most pairs are truncated — the model never sees the complete peer comparison or refusal sections. At 4,096 tokens (Colab A100), every pair is seen in full. This is the single biggest quality improvement available. More than model size. More than dataset size.

---

## Training Results

| Round | Platform | Tokens | Pairs | Val Loss |
|-------|----------|--------|-------|----------|
| 1 | Mac 16GB MLX | 512 | 1,737 | 3.14 to 1.30 |
| 2 | Mac 16GB MLX | 512 | 3,832 | 2.53 to 1.07 |
| 3 | Mac 16GB MLX | 512 | 3,832 | — to **0.876** |
| 4 | Colab Pro A100 | 4,096 | ~5,000 | ~0.5-0.6 (pending) |

Val loss of 0.876 represents a model that has genuinely internalised domain structure. The remaining weaknesses — fabricated peer comparisons, invented rating agency citations — come from truncated training at 512 tokens. Round 4 on Colab Pro at 4,096 tokens should fix both categorically.

---

## What's Left

The model works end to end. Annual report in, credit paper out, benchmark table included, all figures cited. Three rounds of Mac training complete.

What remains:

- **Colab Pro training** at 4,096 tokens — fixes fabricated peer/rating citations, deeper analyses
- **More real analyst credit papers** — behind paywalls mostly, but every one added is worth it
- **Asset class generalisation** — same pipeline, different training data. Project finance next.

Code is at [github.com/1697-20747/llm_credit_paper](https://github.com/1697-20747/llm_credit_paper). Apache 2.0.

Technical documentation: [/docs/camels-llm/](/docs/camels-llm/)

---

## Key Takeaways

- Fine-tuning a 7B model on domain data produces meaningfully better output than prompting a generic model, even with a strong system prompt
- The benchmarking requirement (population percentiles for every metric) is non-trivial to implement but essential for the output to be analytically useful
- 16GB unified memory is insufficient for production inference with a 7B model but sufficient for training with 4-bit quantisation and short sequences
- The data pipeline is the majority of the work. The model training is the easy part
- QLoRA means training 0.019% of parameters. The adapter is 7MB. This is the entire reason consumer hardware training is possible
- HuggingFace is a file download service, not a cloud provider. The model runs entirely locally
- Sequence length is the single most important training hyperparameter for output quality on this task
- Open source regulatory data (Basel papers, OCC handbooks, FDIC manuals) is underutilised as LLM training material
- Anti-hallucination is an architectural problem, not a prompting problem

---

## References

- [FDIC BankFind API](https://banks.data.fdic.gov/api/)
- [EBA EU-wide Transparency Exercise](https://www.eba.europa.eu/eu-wide-transparency-exercise-0)
- [BIS Basel Committee Publications](https://www.bis.org/bcbs/publications.htm)
- [OCC Comptroller's Handbook](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/index-comptrollers-handbook.html)
- [Qwen2.5 Model Family](https://huggingface.co/Qwen)
- [MLX Framework](https://github.com/ml-explore/mlx)
- [Unsloth — Fast LLM Fine-tuning](https://github.com/unslothai/unsloth)
- [Technical Documentation](/docs/camels-llm/)
- [Project Repository](https://github.com/1697-20747/llm_credit_paper)
"""

current = p.read_text(encoding="utf-8")
p.write_text(current + suffix, encoding="utf-8")
print(f"Done. File is now {len(p.read_text())} chars")
