---
title: Applying the Findings to the Amarketer Affiliate Marketing KB
type: design-implications
status: proposal
ai_usage: >
  Bridge document — maps each research finding to a concrete Amarketer KB
  decision. Read before designing the KB framework. Nothing here is built yet.
related: [01-kb-design-patterns.md, 02-prompting-methods.md, 03-metadata-schema.md, 04-red-flags.md]
---

# How the Findings Shape the Amarketer KB Framework

## Proposed KB shape (synthesis)

Plain Markdown files with YAML frontmatter ([schema](03-metadata-schema.md)), in a semantic tree, retrieved agentically (grep/glob/read) with an always-loaded index — the Pattern 1 + Pattern 3 combination. Add embedding/BM25 indexing (Pattern 2) only for the fuzzy-content areas (tactic prose, content guidelines), and only once those exceed the 200K-token full-context threshold.

```
kb/
  INDEX.md                  # tier-1: name + when-to-use line per entry (budgeted)
  programs/                 # affiliate programs & networks — volatile, structured
    amazon-associates.md
    shareasale-overview.md
  offers/                   # live offers, rates, terms — valid_until MANDATORY
  tactics/                  # trigger-action encoded, metrics-ranked
    seasonal-gift-guides.md
  channels/                 # SEO, email, social, PPC playbooks
  policies/                 # FTC disclosure, network ToS, brand rules
  learned/                  # agent-written insights, status: unverified until promoted
```

## Finding → decision map

| Research finding | Amarketer decision |
|---|---|
| Progressive disclosure (Agent Skills) | `INDEX.md` with one *when-to-use* line per entry is always in the agent's context; bodies loaded on demand. Tactic entries are effectively "affiliate skills". |
| Agentic search beat vector RAG on structured corpora (Claude Code) | Program names, network names, offer IDs are exact identifiers → greppable plain files first; no vector DB in v1. |
| ≤200K tokens ⇒ full context (Anthropic) | Early-stage Amarketer KB will be small; don't build retrieval infrastructure prematurely (red flag 12). Revisit per-directory as it grows. |
| Contextual retrieval −49/67% failures | When tactic/content corpora outgrow full-context, ingest with the exact Anthropic situating prompt + hybrid BM25, rerank, top-20. |
| Staleness risk of pre-computed data | Commission rates and offer terms are the most volatile facts in this domain. `valid_until` is mandatory on `offers/`; expired entries force re-verification (live fetch) before the agent may quote them. |
| Provenance cuts fabrication ~42% | Every entry carries `source.origin` + `retrieved`; agent outputs that state rates/terms must cite entry `id`; a post-generation check verifies citations resolve. Critical: wrong commission claims are a money- and trust-losing hallucination class. |
| Trigger-action encoding | Tactics stored with `triggers: ["IF Q4 AND physical-product niche THEN publish gift guides 6 weeks pre-holiday"]` + `metrics` (EPC, conv-rate, sample size) so the agent selects tactics by measured outcome, not prose. |
| Self-improving loop (memory tool, 84% token savings / +39% perf) | Campaign outcomes flow back as `learned/` entries (`status: unverified`, with `metrics`); a scheduled consolidation pass dedupes, resolves contradictions against curated tactics, promotes to `verified`. This is Amarketer's compounding moat: the KB gets better with every campaign. |
| Contradiction handling (`supersedes`) | Rate changes are the norm — new offer entries supersede old ones rather than editing history away; agent sees the chain and can reason about trends. |
| GraphRAG for relational questions (LinkedIn −28.6% resolution time) | Defer. A graph layer ("which tactics performed for programs similar to X in niche Y") is a v2+ addition once `learned/` has volume; the frontmatter `related`/`type` fields already give a lightweight graph. |
| Uncertainty gating | Agent may never state a rate/term not present in a valid KB entry; missing ⇒ emit `NEED_MORE` and trigger live lookup. Compliance answers (FTC/ToS) must cite `policies/` or abstain. |
| Right-altitude system prompt | Amarketer agent prompt carries heuristics ("offer data > 30 days requires re-verification", "always check policies/ before generating promotional copy"), not hardcoded per-network branching. |

## Suggested build order (when we start building)

1. Define the entry schema + JSON Schema CI validation ([03](03-metadata-schema.md)).
2. Scaffold the directory tree + `INDEX.md` convention; seed a handful of entries per type.
3. Agent harness: grep/glob/read tools + system prompt with KB-usage rules ([02](02-prompting-methods.md)).
4. Citation + uncertainty gating in the output path (highest ROI against costly hallucinations).
5. `learned/` write-back loop with promotion gate.
6. Only then, measure: retrieval hit rate and token spend per task — and add Pattern 2/4 machinery where the numbers say it's needed.
