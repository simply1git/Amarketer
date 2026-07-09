---
title: Prompting Methods for KB Integration — Comparison
type: research-findings
status: complete
ai_usage: >
  Comparison table first, then implementation notes per method with the exact
  patterns used in production systems. Combine methods; they are not exclusive.
related: [01-kb-design-patterns.md, 03-metadata-schema.md]
---

# Prompting Methods for Maximizing AI Utility from a KB

## Comparison table

| Method | What it does | Effectiveness (evidence) | Token cost | Best for |
|---|---|---|---|---|
| **Structured context sections** (XML/MD-delimited KB blocks with metadata headers) | Model can distinguish sources, dates, trust levels | Baseline requirement in Anthropic's context-engineering guidance; enables everything below | Near-zero overhead | Every KB-consuming prompt |
| **Citation-enforced generation** ("every claim must cite [source_id]") | Makes hallucination structurally harder; enables verification layer | ~42% fewer fabricated claims vs no-attribution RAG (attribution-technique studies); standard in medical RAG deployments | +5–15% output tokens | User-facing factual answers, compliance-sensitive output |
| **Uncertainty gating** ("answer only from provided context; if insufficient, say so / trigger another retrieval") | Converts silent hallucination into a recoverable signal | Core of production retrieve→generate→inspect→score→repair pipelines | Minimal; may add a retrieval round-trip | Agentic loops where a fallback action exists |
| **Chain-of-thought scaffolding around retrieval** (plan → search → read → refine → answer) | Iterative query refinement instead of one-shot retrieval | The mechanism behind Claude Code's agentic search beating vector RAG "by a lot" | High (multiple turns) — offset by retrieving only what's needed | Complex/multi-hop questions over navigable KBs |
| **Few-shot canonical examples of KB queries** | Teaches query formulation and result interpretation | Anthropic: curated "diverse, canonical examples" beat exhaustive edge-case rule lists | Moderate, fixed (cacheable) | Teaching agents to use custom KB query tools |
| **Contextual chunk annotation** (ingestion-time prompt, see Pattern 2) | Chunks carry their own document context into the index | −49% retrieval failures (−67% with rerank) — Anthropic | One-time ~$1.02/M doc tokens | Any embedded/BM25-indexed KB |
| **Right-altitude system prompts** | Heuristics, not hardcoded if-else logic; not vague platitudes either | Anthropic's "Goldilocks zone" guidance from Claude/Claude Code development | Zero marginal | System prompt of any KB-backed agent |

## Implementation notes

### Structured context sections
Wrap each retrieved entry with its metadata so the model can reason about trust and recency:

```xml
<kb_entry id="amazon-associates-rates" updated="2026-06-12" status="verified" confidence="high" source="curated">
...content...
</kb_entry>
```

Formatting *is* provenance: source ID, date, and relevance score in the wrapper measurably change how the model attributes and weighs claims.

### Citation-enforced generation
Contract must be precise — specify the citation token format (`[id]`), the condition ("every factual sentence"), and pair it with a post-generation inspection step that checks each citation resolves to a retrieved passage; repair or strip unsupported claims before delivery.

### Uncertainty gating
LLMs don't emit calibrated numeric confidence reliably; production systems gate on *behavior*, not self-reported scores:
- "If the answer is not in the provided entries, do not answer from your own knowledge. Instead, output `NEED_MORE: <refined query>`." The harness then runs another retrieval round (bounded retries).
- Retrieval-side gating uses real scores: if the top reranker score < threshold, escalate (broaden query, ask the user, or answer with an explicit low-confidence disclaimer).
- "When confidence < X trigger Y" thus lives partly in the *pipeline* (reranker/verifier scores), partly in the prompt (permission to abstain). Prompt-only numeric self-scores are a red flag — see [04-red-flags.md](04-red-flags.md).

### CoT scaffolding for KB integration
The production shape (Claude Code, Cursor, Devin):
1. Restate the information need.
2. Enumerate candidate KB locations from the always-loaded index.
3. Search (grep/filtered vector query); **read results before answering**.
4. If results don't answer the need, refine and repeat (bounded).
5. Answer citing entry IDs.
Prompt it as process instructions + one worked example, not rigid pseudocode.

### Few-shot examples for KB querying
Include 2–4 worked examples covering *distinct* query types (exact-lookup, fuzzy-concept, relational, negative/"not in KB"). The negative example matters most — it demonstrates abstention.

### Right-altitude system prompts
Organize with distinct sections (`<background>`, `<kb_usage_rules>`, `<output_format>`). State heuristics ("prefer entries updated in the last 90 days; commission data older than 30 days must be re-verified") rather than exhaustive branching rules.
