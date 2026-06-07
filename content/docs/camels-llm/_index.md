---
title: "CAMELS LLM System"
description: "Technical documentation for the CAMELS Credit Analysis System — offline AI-powered bank credit paper generator built on structured prompting and grounded data injection."
weight: 1
---

Technical documentation for the CAMELS Credit Analysis System. An offline pipeline
that generates structured bank credit analyses from annual reports and Pillar 3
disclosures, using base Qwen2.5-7B via Ollama with three grounding mechanisms:
extracted metrics, decile benchmarks, and peer values from a real bank roster.

The model runs entirely locally — no cloud API at inference, no data leaving
your machine. The only API used is Anthropic's Claude Haiku, called once during
training-data generation; it does not run at inference time.

## Documentation

- **[How It Works](how-it-works/)** — The structured prompting architecture and three grounding mechanisms
- **[Data Sources](data-sources/)** — The six data pipelines, bank coverage, and the industry data quality problem
- **[Fine-Tuning Retrospective](fine-tuning-retrospective/)** — Four rounds of QLoRA experiments and why they didn't ship

## Getting Started

Start with the [main blog post](/blog/comp-science/llm-credit-paper-generator/)
for context and motivation, then come here for the technical detail.

## Repository

[github.com/1697-20747/llm_credit_paper](https://github.com/1697-20747/llm_credit_paper)
— Apache 2.0. If you know what you are doing, the README is sufficient.
