---
title: Metadata Schema Recommendations for AI-Consumed KB Entries
type: research-findings
status: complete
ai_usage: >
  Canonical entry schema for the Amarketer KB. Fields marked REQUIRED gate
  ingestion; others are per-type. JSON Schema sketch at the bottom.
related: [01-kb-design-patterns.md, 02-prompting-methods.md]
---

# Metadata Schema for AI Reasoning

Synthesized from patterns that flow end-to-end in production systems: Agent Skills frontmatter (routing), LlamaIndex auto-retrieval filters (filtering), attribution pipelines (provenance), and memory-tool file conventions (lifecycle). Rule of thumb from LlamaIndex production guidance: **metadata must flow through the whole pipeline** — filter on it at retrieval, print it in the prompt, use it for access control. A field no stage reads is dead weight.

## Recommended fields

| Field | Type | Required | Purpose for AI reasoning |
|---|---|---|---|
| `id` | string (kebab-case slug) | ✅ | Stable citation target; greppable exact-match handle (Pattern 3) |
| `type` | enum (`program`, `tactic`, `channel`, `policy`, `learned-insight`, `reference`) | ✅ | Retrieval filtering; per-type prompt handling |
| `name` | string | ✅ | Tier-1 index line (progressive disclosure) |
| `description` | string, one line, phrased as *when to use* | ✅ | Does the routing — the agent triggers entries off this line (Agent Skills evidence) |
| `summary` | string ≤ 3 sentences | ✅ | Embedding-optimized concise variant; shown in candidate lists before full load |
| `source` | object `{origin: url\|doc\|human\|agent-session-id, retrieved: date}` | ✅ | Provenance → claim-level citation → ~42% fewer fabricated claims |
| `status` | enum (`draft`, `unverified`, `verified`, `deprecated`) | ✅ | Trust gating; self-written entries enter as `unverified` (Pattern 5) |
| `created` / `updated` | ISO dates | ✅ | Freshness heuristics ("prefer < 90 days") |
| `valid_until` | ISO date or null | per-type | Hard staleness gate — critical for commission rates/offer terms; expired ⇒ re-verify before use |
| `confidence` | enum (`high`, `medium`, `low`) + `basis` string | recommended | Evidence-based trust signal (set by pipeline/reviewer, **never** by model self-report) |
| `supersedes` / `superseded_by` | id refs | when relevant | Contradiction handling: retrieval drops superseded entries; prompt notes conflicts |
| `contradicts` | id refs + note | when relevant | Explicit conflict surfacing beats silently returning both versions |
| `related` | id refs | recommended | Agentic link-following (just-in-time expansion) |
| `triggers` | array of `IF <condition> THEN <action>` strings | for tactics | Machine-actionable tactic encoding (skills-style condition→procedure) |
| `metrics` | object (e.g., `{epc: 1.4, conv_rate: 0.031, sample_n: 220}` ) | for learned insights | Lets the agent rank tactics by measured outcome, not prose enthusiasm |
| `ai_instructions` | string | optional | Entry-specific usage rules ("execute the script, don't paraphrase it"; "quote rates verbatim") |
| `access` | enum/tags | if multi-tenant | Retrieval-time access control |

## Contradiction-handling protocol

1. Ingestion detects same-topic conflict (matching `id` family or high similarity + differing facts).
2. Newer verified entry gets `supersedes: old-id`; old entry gets `superseded_by` + `status: deprecated`.
3. If both remain plausible (e.g., conflicting sources), keep both with mutual `contradicts` and surface the conflict in the prompt wrapper so the model reasons about it explicitly instead of picking silently.

## JSON Schema sketch

```json
{
  "$id": "amarketer-kb-entry.schema.json",
  "type": "object",
  "required": ["id", "type", "name", "description", "summary", "source", "status", "created", "updated"],
  "properties": {
    "id": {"type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"},
    "type": {"enum": ["program", "tactic", "channel", "policy", "learned-insight", "reference"]},
    "name": {"type": "string", "maxLength": 80},
    "description": {"type": "string", "maxLength": 200},
    "summary": {"type": "string", "maxLength": 500},
    "source": {"type": "object", "required": ["origin"], "properties": {"origin": {"type": "string"}, "retrieved": {"type": "string", "format": "date"}}},
    "status": {"enum": ["draft", "unverified", "verified", "deprecated"]},
    "created": {"type": "string", "format": "date"},
    "updated": {"type": "string", "format": "date"},
    "valid_until": {"type": ["string", "null"], "format": "date"},
    "confidence": {"type": "object", "properties": {"level": {"enum": ["high", "medium", "low"]}, "basis": {"type": "string"}}},
    "supersedes": {"type": "array", "items": {"type": "string"}},
    "superseded_by": {"type": "string"},
    "contradicts": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "note": {"type": "string"}}}},
    "related": {"type": "array", "items": {"type": "string"}},
    "triggers": {"type": "array", "items": {"type": "string"}},
    "metrics": {"type": "object"},
    "ai_instructions": {"type": "string"},
    "access": {"type": "array", "items": {"type": "string"}}
  }
}
```

Store as YAML frontmatter on Markdown files (agent-greppable, human-editable, Pattern 3) with the JSON Schema used for CI validation at ingestion.
