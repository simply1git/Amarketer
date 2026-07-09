---
title: Primary Sources
type: bibliography
status: complete
ai_usage: Verify any claim in this report against the source listed for it.
---

# Sources

## Anthropic engineering (primary, implementation-verified)

- [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — exact chunk-situating prompt, failure-rate numbers (−35/−49/−67%), $1.02/M token cost, 200K-token full-context threshold, top-20 chunk guidance, embedding/reranker recommendations.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — context rot, smallest-high-signal-token-set principle, just-in-time vs pre-computed retrieval, compaction, structured note-taking, sub-agent summaries, right-altitude prompts, canonical few-shot examples.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — SKILL.md format, three-tier progressive disclosure, file-splitting guidance, PDF-skill example, iterate-with-Claude loop, anti-patterns.
- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — token-efficient tool results, naming clarity, evaluation-driven iteration.
- [Memory tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) + [Claude Cookbook: context engineering](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) — file-based cross-session memory; 84% token savings / +39% performance on 100-turn benchmark (with context editing).
- [Contextual retrieval cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) — runnable implementation.

## Agentic search vs RAG (Claude Code)

- [Why Claude Code abandoned RAG for agentic search](https://zenn.dev/karamage/articles/2514cf04e0d1ac?locale=en); [Claude Code doesn't index your codebase](https://vadim.blog/claude-code-no-indexing/); [Anthropic replaced their RAG pipeline with agentic search](https://robertheubanks.substack.com/p/anthropic-replaced-their-rag-pipeline) — Boris Cherny "outperformed everything, by a lot"; precision/freshness/simplicity rationale; Cursor/Devin convergence on plan→grep→read→refine.

## Hierarchical retrieval & metadata (LlamaIndex)

- [Structured hierarchical retrieval example](https://developers.llamaindex.ai/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval/) — per-doc summary + metadata-dict filters, auto-retrieval.
- [LlamaIndex production guide](https://zenvanriel.com/ai-engineer-blog/llamaindex-production-guide/) — metadata flows through the whole pipeline; summary-index-first drilling.
- [NVIDIA hierarchical node parser example](https://nvidia.github.io/GenerativeAIExamples/0.5.0/notebooks/04_llamaindex_hier_node_parser.html) — AutoMergingRetriever parent/child behavior.

## GraphRAG production numbers

- [LinkedIn customer-support GraphRAG paper](https://arxiv.org/html/2404.17723v1) — −28.6% median resolution time over ~6-month deployment, +77.6% MRR.
- [Neo4j GraphRAG manifesto](https://neo4j.com/blog/genai/graphrag-manifesto/) / [Vellum GraphRAG](https://www.vellum.ai/blog/graphrag-improving-rag-with-knowledge-graphs) — Microsoft's 26–97% token reduction figure.

## Hallucination reduction / attribution

- [Attribution techniques survey](https://arxiv.org/html/2601.19927v1) — ~42% fewer fabricated claims with attribution vs baseline RAG.
- [Production RAG hallucination reduction (Boldare)](https://www.boldare.com/blog/how-to-build-a-production-rag-system/) — retrieve→generate→inspect→score→repair pipeline.
- [RAG prompt engineering: context placement & citations](https://mbrenndoerfer.com/writing/rag-prompt-engineering-context-citations) — formatting-as-provenance, citation contracts.
- [Citation-enforced prompting in medical RAG](https://www.mdpi.com/2076-3417/16/6/3013) — deployed citation enforcement.

## Memory / self-improvement

- [Letta: agent memory](https://www.letta.com/blog/agent-memory/) and [Letta v1 agent loop](https://www.letta.com/blog/letta-v1-agent) — tiered memory (core blocks + archival), agent-managed memory via tool calls, forgetting policy.
- [Claude Code experimental memory system](https://giuseppegurgone.com/claude-memory) — MEMORY.md injection, 200-line hard limit.

## Chunking & cost

- [Systematic analysis of chunking strategies](https://arxiv.org/html/2601.14123v1) — overlap: no benefit; ~2.5K-token context cliff; sentence chunking cost-effectiveness.
- [ZenML: LLMOps in production, 457 case studies](https://www.zenml.io/blog/llmops-in-production-457-case-studies-of-what-actually-works) — incl. Amazon Finance Automation 49%→86% accuracy via chunking/prompt iteration.
