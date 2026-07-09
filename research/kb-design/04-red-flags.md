---
title: Red Flags — KB Design Mistakes That Degrade Agent Performance
type: research-findings
status: complete
ai_usage: Checklist for auditing any KB design. Each item cites the production evidence behind it.
related: [01-kb-design-patterns.md, 02-prompting-methods.md]
---

# Red Flags: KB Design Mistakes with Documented Consequences

1. **Dumping everything into context ("more context = better").** Context rot is measured: model performance degrades as the window fills; attention budgets are finite (n² token relationships, less long-range training data). Anthropic's stated objective is the *smallest* set of high-signal tokens. Fix: progressive disclosure + just-in-time loading (Pattern 1/3).

2. **Context-free chunking.** Splitting documents destroys the context that made chunks retrievable — the failure mode contextual retrieval was built to fix (5.7% baseline failure rate on Anthropic's evals). A chunk saying "the company grew 3%" is unretrievable without knowing which company, which quarter. Fix: Pattern 2.

3. **Embedding-only retrieval over identifier-heavy content.** Vector search fuzzes exact matches — error codes, program names, SKUs, commission tiers. This is the precision argument that made Claude Code drop vector RAG for grep. Fix: hybrid BM25 + embeddings, or plain-file agentic search.

4. **Pre-built indexes over volatile data (staleness).** Anthropic flags pre-computed retrieval's stale-data risk; for affiliate data (rates, terms change monthly) a stale index confidently serves wrong numbers. Fix: just-in-time reads for volatile fields + `valid_until` hard gates.

5. **No provenance metadata.** Without source/date in the prompt wrapper, the model can't weigh trust and the pipeline can't verify citations — the ~42% fabrication reduction from attribution is forfeited. Fix: schema in [03-metadata-schema.md](03-metadata-schema.md).

6. **Trusting model self-reported confidence scores.** "Rate your confidence 0–100" is not calibrated; production systems gate on reranker/verifier scores and abstention behavior instead ([02-prompting-methods.md](02-prompting-methods.md), uncertainty gating).

7. **Overlapping/ambiguous entries and tools.** Anthropic's tool-writing and context-engineering guidance: when it's ambiguous which of two similar entries/tools applies, agents pick wrongly or waffle. Same for near-duplicate KB entries answering the same question differently. Fix: one canonical entry per fact, `supersedes` chains, dedupe at ingestion.

8. **Unbounded always-loaded index.** Claude Code's memory index has a 200-line hard limit for a reason — the tier-1 index competes with task context every single turn. Fix: index budget + archival policy.

9. **Chunk overlap and oversized chunks as "safety margin".** Systematic chunking studies: overlap = higher indexing cost, no quality gain; quality cliff beyond ~2.5K-token chunks. Fix: boundary-aware chunking, no overlap, parent/child auto-merging when more context is needed.

10. **Self-improvement without a promotion gate.** Letting agent-written learnings land as trusted facts pollutes the KB with unvalidated, possibly hallucinated content that future retrievals then amplify (the classic self-improving-loop failure). Fix: `status: unverified` quarantine + scheduled consolidation/review (Pattern 5).

11. **Prose-only tactics knowledge.** Advice written as narrative ("consider seasonality when…") can't be ranked or matched to conditions. Skills-style trigger-action encoding (`IF holiday season AND physical product THEN apply gift-guide placement`) plus a `metrics` field makes tactics selectable by measured outcome.

12. **Building RAG infrastructure before checking corpus size.** Under 200K tokens, full-context + prompt caching beats a retrieval pipeline on both quality and engineering cost (Anthropic's explicit threshold). Many teams build vector infrastructure for corpora that fit in one prompt.
