---
title: "CAMELS LLM System"
description: "Technical documentation for the CAMELS Credit Analysis System — offline AI-powered bank credit paper generator"
weight: 1
---

Technical documentation for the CAMELS Credit Analysis System. An offline, fine-tuned LLM pipeline that generates structured bank credit analyses from annual reports and Pillar 3 disclosures. The model runs entirely locally via Ollama once trained — no cloud API, no data leaving the machine.

## Documentation

- **[How Training Pairs Work](training-pairs/)** — How raw financial data becomes LLM training examples, and how Qwen2.5-7B is fine-tuned on them
- **[Data Sources](data-sources/)** — All six data pipelines, bank coverage, and the industry data quality problem

## Getting Started

Start with the [main blog post](/blog/comp-science/llm-credit-paper-generator/) for context and motivation, then come here for the technical detail.

## Repository

[github.com/1697-20747/llm_credit_paper](https://github.com/1697-20747/llm_credit_paper) — Apache 2.0. If you know what you are doing, the README is sufficient.
