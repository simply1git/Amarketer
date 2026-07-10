# Amarketer

A self-improving, AI-operated affiliate marketing system for a solo owner. Open-source and free-tier only.

**Start here:**
- [STATUS.md](STATUS.md) — **current state, owner checklist, and how to resume work in a new session**
- [ops/RUNBOOK.md](ops/RUNBOOK.md) — how to operate it (launch checklist + weekly/monthly cycles)
- [PLAN.md](PLAN.md) — architecture, decisions, phases, model strategy
- [CLAUDE.md](CLAUDE.md) — rules the AI agent operates under (factual discipline, human gates)

**Layout:**

| Path | What |
|---|---|
| `kb/` | Knowledge base — programs, offers, tactics, channels, policies, learned insights ([index](kb/INDEX.md)) |
| `site/` | The public site (Astro → Cloudflare Pages free tier) — see [site/README.md](site/README.md) |
| `ops/` | Operations — niche decisions, content pipeline, performance reports, runbook |
| `tools/` | `validate_kb.py` (schema), `check_content.py` (compliance lint), `check_freshness.py` (stale-data report), `import_report.py` (CSV → reports), `make_voiceover.py` (free TTS narration) |
| `site/scripts/` | `make-pin.mjs` — renders branded 1000×1500 Pinterest pin PNGs |
| `.github/workflows/` | CI (KB validation + compliance lint + site build on every push); monthly KB-freshness issue |
| `research/kb-design/` | The production-sourced research behind the KB architecture |

**How it works in one paragraph:** the AI agent researches programs and topics, hands-on tests tools, and drafts content grounded in a versioned knowledge base with provenance and freshness rules; the owner gates everything public (publish/signup/spend); real performance data flows back as measured insights that get consolidated into verified tactics — so every campaign makes the next one smarter.
