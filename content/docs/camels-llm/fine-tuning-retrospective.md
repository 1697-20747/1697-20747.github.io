---
title: "Fine-Tuning Retrospective"
weight: 4
description: "An honest account of four rounds of QLoRA fine-tuning that did not improve output quality over base Qwen2.5-7B with structured prompting."
summary: "Four QLoRA rounds, what went wrong with each, and why structured prompting won."
---

## TL;DR

Four QLoRA training rounds were attempted. The first three (Mac MLX) produced
working adapters but were limited to 512-token sequences and didn't materially
improve output. Round 4 (Colab Pro A100, 4,096 tokens, 6,623 pairs) trained
successfully to validation loss 0.75 but the resulting deployed model was
**worse than the base model with structured prompting**. The system now ships
with base Qwen2.5-7B + system prompt + three-mechanism grounding, not with
any fine-tuned adapter.

The training data itself was high quality. The failure was in the
training-to-deployment pipeline, not the data.

---

## Training Rounds

| Round | Platform | Tokens | Pairs | Loss | Outcome |
|-------|----------|--------|-------|------|---------|
| 1 | Mac MLX (M2 Pro 16GB) | 512 | 1,737 | 3.14 → 1.30 | Working but limited |
| 2 | Mac MLX | 512 | 3,832 | 2.53 → 1.07 | Working but limited |
| 3 | Mac MLX | 512 | 3,832 | → 0.876 | Working, deployed briefly |
| 4 | Colab Pro A100 | 4,096 | 6,623 | → **0.75** | Failed deployment |

Round 4 had the best loss and the most training data and the biggest context
window. It should have been the best model. It wasn't.

---

## What Went Wrong in Round 4

### Issue 1 — Unsloth's `save_pretrained` produced a hybrid file

Cell 7 of the Colab notebook called:

```python
model.save_pretrained(adapter_path)
```

On a `FastLanguageModel.get_peft_model` object this saves files that look like
a standard PEFT LoRA adapter but the safetensors file is **154MB**. That's:

- Too small to be a full 7B model (~15GB at fp16)
- Too big to be a real LoRA delta (~7MB for rank 16)

It's some intermediate state — the in-memory representation of Unsloth's
optimised training graph, not a portable LoRA delta. No downstream tool
(`peft.PeftModel.from_pretrained`, `llama.cpp convert_hf_to_gguf.py`,
`mlx_lm.fuse`) knew what to do with this file.

### Issue 2 — Colab disk fills during GGUF conversion

Converting to GGUF requires re-downloading the full 30GB base model in 6
safetensor shards, merging with the adapter (another 30GB), then quantising.
Colab Pro's 112GB disk fills completely partway through. Two attempts both
crashed with `OSError: [Errno 28] No space left on device`. The workaround had
to be Mac local conversion.

### Issue 3 — Mac merge of the hybrid file produced a corrupted model

Without bitsandbytes (Linux/CUDA only) the Mac merge used standard
`Qwen/Qwen2.5-7B-Instruct` as the base. Applying the 154MB hybrid file as if
it were a LoRA delta produced a 14GB merged model that:

- Loaded successfully via `transformers`
- Converted cleanly to f16 GGUF via `llama.cpp`
- Quantised cleanly to Q4_K_M via `llama-quantize`
- Deployed cleanly via Ollama

But when tested:
- **Lost the base Qwen instruction-following** — fragmented, repetitive
  outputs echoing the prompt template
- **Did not gain trained behaviour** — citations missing, no benchmark
  decile language, no peer comparison structure
- **Behaved worse than base Qwen with system prompt only**

The merge had silently produced garbage. The LoRA delta math
(W_merged = W_base + B @ A * alpha/r) requires B @ A to be a meaningful
low-rank update to the base weights. The hybrid file's tensors were not that.

### Issue 4 — Colab idle timeout during 2-hour training

Colab disconnects sessions based on browser activity, not GPU utilisation. A
training run consuming 100% of an A100 for 2 hours will disconnect if the
browser tab is idle. Workaround was a JavaScript keep-alive pasted in the
developer console.

### Issue 5 — Google Drive credential propagation failures

`drive.mount('/content/drive')` frequently failed with
`MessageError: Error: credential propagation was unsuccessful`. The notebook
ended up not using Drive at all.

---

## What Was Tried to Fix It

1. **Different merge bases.** Tried merging onto
   `unsloth/qwen2.5-7b-instruct-unsloth-bnb-4bit` (the original training base)
   — failed on Mac because of bitsandbytes dependency. Tried
   `Qwen/Qwen2.5-7B-Instruct` — merge ran but output was corrupted.

2. **Different conversion paths.** `mlx_lm.fuse` — failed with
   `AttributeError: 'types.SimpleNamespace' object has no attribute 'num_layers'`.
   `llama.cpp convert_hf_to_gguf.py` against the adapter folder directly —
   produced a 0-tensor GGUF (metadata only).

3. **Fresh Colab session for GGUF.** Two attempts. Both disk-filled at ~90GB
   used out of 112GB.

4. **Cell 7 rewrite.** Tried `model.save_pretrained_merged(adapter_path,
   tokenizer, save_method='lora')` instead of `save_pretrained`. Not tested
   in another full training round before pivot.

---

## What Would Need to Change for Round 5 to Succeed

If retrying:

1. **Replace Cell 7 with explicit LoRA-only save:**
   ```python
   model.save_pretrained_merged(adapter_path, tokenizer, save_method='lora')
   ```

2. **Don't use Colab.** Use Vast.ai or RunPod — A100 80GB at $1.50–2.50/hour
   with no idle timeouts and SSH access. ~$3–5 total per run.

3. **Validate the saved adapter before declaring success.** Load via
   `peft.PeftModel.from_pretrained`, merge into base model, run on 10 fixed
   test prompts. Compare side-by-side to base Qwen. Don't trust loss alone.

4. **Reduce learning rate to 5e-6** (was 2e-5) for slower learning.

5. **Increase LoRA rank to r=32** (was 16) for more capacity.

6. **Add 50–100 explicit refusal pairs** — examples where the source extract
   lacks a figure and the correct answer is "Data not available". This is the
   behaviour Round 4 most clearly failed to learn.

---

## Why the Pivot to Structured Prompting Worked

After Round 4 deployment failed, the system was reverted to use base Qwen +
system prompt via Ollama, with three grounding mechanisms added to the
inference pipeline:

1. **Metric extraction with page tagging** — `CET1 RATIO: 14.0 [Source:
   2025-lbg-annual-report.pdf, p.53]` injected into prompt
2. **Decile context** — `← 7th decile globally (median: 13.6%, p10: 12.34%,
   p90: 14.85%; n=36)` appended
3. **Peer values** — real same-region peers from roster injected as a block
   with explicit instruction to use only those values

See [How It Works](../how-it-works/) for full detail.

This combined approach produces output that is verifiably grounded:
- Every subject-bank figure cites a specific page
- Every peer figure cites a roster entry
- "No rating agency commentary available in source documents" where appropriate
- "Data not available" where the source lacks a figure

No fabrication.

---

## Lessons

### 1. Loss is not quality

Round 4 had the best loss and was the worst model. Always test deployed
outputs end-to-end, not just metrics. A diff-against-base-model on 10 fixed
prompts would have caught the regression in minutes.

### 2. Saving is harder than training

The Unsloth + Colab + Mac llama.cpp + Ollama deployment chain has more
failure points than the training step itself. Each tool boundary loses
information about the model state.

### 3. Structured prompting + grounding can match or beat naive fine-tuning

For domain tasks with clear formats and external data sources, prompt
engineering with explicit data injection often outperforms a fine-tuned
adapter — especially without rigorous evaluation infrastructure.

### 4. Build the evaluation harness first

Round 4 trained to loss 0.75 but nobody could tell the output was broken
until a full `test_analysis.py` run was generated and compared section-by-
section to the baseline.

### 5. Colab is unsuitable for serious training work

Idle timeouts, disk limits, credential failures, session crashes. For any
training run longer than 30 minutes use Vast.ai or RunPod instead.

### 6. Mac is fine for everything except the training step itself

GGUF conversion, merging, quantisation, inference, evaluation — all run
cleanly on Apple Silicon with `llama.cpp` + Ollama. The hostile environment
is the training platform, not the deployment platform.

### 7. The data pipeline survives the pivot

Every script written for fine-tuning still runs. The benchmark index, peer
roster, source extractor, and section classifier are all used at inference
time — just via prompt injection instead of weight updates.

---

[Back to CAMELS LLM docs](..) | [How It Works](../how-it-works/) | [Main blog post](/blog/comp-science/llm-credit-paper-generator/)
