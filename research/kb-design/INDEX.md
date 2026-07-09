---
title: AI-Optimized Knowledge Base Design for LLM Agents — Findings Index
project: Amarketer (affiliate marketing agent system)
type: research-index
audience: AI agents and engineers building the Amarketer KB framework
date: 2026-07-09
status: complete
ai_usage: >
  Read this file first. It summarizes every finding in one line each.
  Load the linked file only when its topic is relevant to your current task
  (progressive disclosure — see 01-kb-design-patterns.md, Pattern 1).
---

# AI-Optimized KB Design for LLM Agents — Findings Report

Deep-dive into production methodologies (Anthropic, Microsoft/LinkedIn, LlamaIndex, Letta, Amazon) for structuring knowledge that LLM agents consume. Every finding is sourced from a deployed system with verifiable implementation detail. Theoretical work was excluded.

## Report files

| File | Contents | Load when |
|---|---|---|
| [01-kb-design-patterns.md](01-kb-design-patterns.md) | Top 5 proven KB design patterns with implementation steps and production numbers | Designing KB structure, storage, or retrieval |
| [02-prompting-methods.md](02-prompting-methods.md) | Comparison table of prompting techniques for KB integration (effectiveness, token cost, use cases) | Writing prompts that consume KB content |
| [03-metadata-schema.md](03-metadata-schema.md) | Recommended metadata schema: fields, types, purpose for AI reasoning | Defining KB entry format |
| [04-red-flags.md](04-red-flags.md) | KB design mistakes that degrade agent performance, from documented post-mortems | Reviewing/auditing a KB design |
| [05-amarketer-applications.md](05-amarketer-applications.md) | How each finding maps to the Amarketer affiliate marketing KB framework | Planning the Amarketer KB build |
| [SOURCES.md](SOURCES.md) | All primary sources with what each one verifies | Checking provenance of any claim |

## One-paragraph TL;DR

The highest-leverage findings: (1) **Progressive disclosure** — expose name+description of every KB entry always, full content on demand; this is how Anthropic's Agent Skills make bundled context "effectively unbounded". (2) **Contextual retrieval** — prepend an LLM-generated 50–100 token situating context to every chunk before embedding; cuts retrieval failure 49% (67% with reranking) at ~$1.02/M document tokens. (3) **Agentic search beats one-shot RAG for structured/navigable corpora** — Claude Code dropped its vector-RAG pipeline for grep/glob because iterative search "outperformed everything, by a lot"; store KB as plain, greppably-named files. (4) **Provenance + freshness metadata is the main anti-hallucination lever** — claim-level citation requirements cut fabricated claims ~42% in attribution studies. (5) **Self-improving loops work via files, not fine-tuning** — Anthropic's memory tool + context editing gave 84% token savings and 39% performance gain on a 100-turn task; agents write learned tactics back as new KB entries.

## Key numbers to remember

- Contextual embeddings + contextual BM25: **−49%** retrieval failures; + reranking: **−67%** (Anthropic)
- KB ≤ **200K tokens** → skip RAG entirely, use full context + prompt caching (Anthropic)
- GraphRAG at LinkedIn customer support: **−28.6%** median ticket resolution time; Microsoft: **26–97% fewer tokens** vs baseline
- Memory tool + context editing: **84% token savings, +39% performance** on 100-turn agentic task (Anthropic internal benchmark)
- Amazon Finance Automation RAG: accuracy **49% → 86%** primarily via chunking + prompt iteration
- Chunking research: overlap gives **no measurable benefit**; quality "context cliff" beyond ~2.5K-token chunks
