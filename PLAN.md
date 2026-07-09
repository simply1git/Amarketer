---
title: Amarketer — System Plan v1
type: plan
status: approved (2026-07-09) — Phase 1 in progress
date: 2026-07-09
owner: solo operator (no existing product, no existing audience, no APIs)
ai_usage: Master plan. Read before any build work. Research backing every KB decision is in research/kb-design/.
---

# Amarketer — System Plan v1

> **PIVOT (2026-07-09):** direction updated by owner delegation — social-first distribution (YouTube faceless primary, Pinterest secondary, site = link hub), niche = **AI tools for one-person businesses** ("SoloStack"), proven-format modeling. Details: [ops/niche/2026-07-pivot-decision.md](ops/niche/2026-07-pivot-decision.md). Sections below describing "SEO site primary" and the education niche are superseded but kept for history.

## What we're building

A personal AI affiliate-marketing operator: a Claude-based agent system + a self-improving knowledge base that together take a solo beginner from zero (no niche, no site, no programs) to a running affiliate operation — and get smarter with every campaign.

**Operating model: hybrid autonomy.** The agent does research, drafting, analysis, and KB maintenance autonomously; the human approves and executes anything irreversible or account-bound (publishing, signing up to programs, spending money). Over time, approved-action categories can be promoted to autonomous.

## Scoping decisions (made 2026-07-09)

| Question | Decision | Rationale |
|---|---|---|
| Autonomy | Hybrid: agent proposes + drafts; human gates publish/signup/spend | Matches user preference; safest while the KB is young |
| v1 channel | **SEO content site (niche blog)** as primary; **one** social distribution channel (chosen after niche is picked, e.g. Pinterest for visual niches, YouTube-shorts/Reddit for others) | Content+SEO is the standard solo-affiliate route: durable, compoundable, fully drivable by an AI writing agent, no ad budget needed. One channel at a time — multi-channel from day one is the classic beginner failure |
| Audience | Single-tenant (just the user) | No multi-tenant access control needed in v1 |
| Data sources | No APIs in v1. Agent web research + manual joins to affiliate networks + periodic CSV/dashboard-export import for performance data | Affiliate links work without APIs; reporting APIs (Impact, Awin, etc.) are a v2 upgrade once volume justifies it |
| Product | None — pure affiliate (promoting others' products) | Niche/program selection becomes Phase 0 of operations, run by the agent |

## Architecture (v1 — deliberately minimal)

Per the research (see [research/kb-design/INDEX.md](research/kb-design/INDEX.md)): plain-file KB, agentic retrieval, no vector DB, no web app in v1. Claude Code *is* the runtime — the "system" is a repository the agent operates inside.

```
amarketer/
  PLAN.md                    # this file
  CLAUDE.md                  # agent operating rules (KB usage, gates, heuristics)
  kb/                        # the knowledge base (schema: research/kb-design/03)
    INDEX.md                 # tier-1 progressive-disclosure index (budgeted)
    programs/                # networks & programs: terms, cookie windows, payout thresholds
    offers/                  # specific promotable offers — valid_until MANDATORY
    tactics/                 # trigger-action playbooks with metrics
    channels/                # SEO + chosen social channel playbooks
    policies/                # FTC disclosure rules, network ToS summaries
    learned/                 # agent-written insights, status: unverified until promoted
  ops/
    niche/                   # Phase-0 niche research outputs & decision record
    content/                 # article drafts → approved → published (state in frontmatter)
    reports/                 # imported performance CSVs + agent analyses
  tools/
    validate_kb.py           # JSON-Schema validation of entry frontmatter (CI gate)
    import_report.py         # normalize network CSV exports into ops/reports/
```

Human gates are enforced by convention + frontmatter state (`status: draft → approved → published`), with the agent forbidden (in CLAUDE.md) from advancing past `approved` itself.

## Build phases

### Phase 1 — Foundation (build)
1. KB entry schema + `tools/validate_kb.py` (from [research/kb-design/03-metadata-schema.md](research/kb-design/03-metadata-schema.md)).
2. Directory scaffold + `INDEX.md` convention.
3. `CLAUDE.md` operating rules: progressive-disclosure reading, citation of entry ids for any rate/term claim, uncertainty gating (never state an offer term not in a valid entry — trigger re-verification instead), `valid_until` enforcement, human-gate rules.
4. Seed `policies/` (FTC disclosure requirements — needed before any content) and `channels/seo-content-site.md` playbook.

### Phase 2 — Niche & program selection (operate: agent research + human decision)
5. Agent runs structured niche research (demand, competition, commission economics, user's interests — user input needed here) → shortlist with scored criteria in `ops/niche/`.
6. User picks the niche; agent researches matching programs/networks that accept new affiliates without traffic minimums → seeds `programs/` and `offers/` entries with provenance.
7. User joins 2–3 programs (human gate); real terms go into the KB, superseding researched estimates.

### Phase 3 — Channel launch (build + operate)
8. Stand up the niche site (static generator, e.g. Astro/Hugo — cheap, fast, agent-editable).
9. Content pipeline: agent drafts from KB tactics + keyword research → `ops/content/` → human approves → publish. Disclosure blocks injected from `policies/` automatically.
10. Pick and launch the one social distribution channel for the chosen niche.

### Phase 4 — Learning loop (the moat)
11. Monthly (then weekly) performance import → agent analysis → `learned/` entries with metrics.
12. Scheduled consolidation pass: dedupe, resolve contradictions, promote `unverified → verified` tactics; retire what doesn't perform.
13. Review autonomy gates: promote consistently-approved action types to autonomous.

## Model strategy (AI cost)

The system is deliberately **model-agnostic**: it is plain files (Markdown KB, Python tools, static site) operated by *any* capable coding agent — nothing is locked to Claude. Options by cost:

| Option | Cost | Trade-off |
|---|---|---|
| Claude Code (current) | existing plan | Best factual discipline + writing quality; already in use |
| Gemini CLI | free tier (generous daily quota) | Strong free option; same file-based workflow works |
| Open-source local: Qwen/Llama via Ollama + Cline/Aider/OpenHands | $0, runs on own hardware | Fully free forever; weaker long-form writing and instruction-following — riskier for compliance rules and content quality |

Practical recommendation: draft revenue-critical content with the strongest model available; use free models for mechanical tasks (report imports, KB validation runs, research summarization). Revisit when volume makes cost material — content quality is the revenue driver, so this is the wrong place to economize first.

## Channel roadmap (beyond v1)

v1 stays site + Pinterest + newsletter (focus wins for a solo operation). The architecture treats channels as plug-ins: adding one = a new `kb/channels/` playbook + a distribution step in the content pipeline. Expansion order, gated on the previous channel showing traction:
1. **YouTube** (screen-recorded tool walkthroughs — our hands-on testing already produces the material; highest affiliate conversion of any channel)
2. **Reddit / Quora** (answer-marketing in teacher/edtech communities; strict self-promotion norms — needs its own compliance playbook)
3. **Medium / LinkedIn syndication** (republishing with canonical links; near-zero marginal cost)
4. **X / Threads / Facebook groups** (community presence; higher upkeep, lowest per-post return)

## Explicitly deferred to v2+
Vector/BM25 retrieval (KB will be far under the 200K-token full-context threshold), reporting APIs, knowledge-graph layer, paid channels, multi-channel expansion, any web UI.

## Resolved items (2026-07-09)
- **Niche selection**: delegated to agent market research (Phase 2) — purely data-driven shortlist + recommendation; user holds veto.
- **Budget**: ~$0. Free-tier hosting (Cloudflare Pages / Vercel); free subdomain acceptable at launch, custom domain (~$10/yr) optional later when revenue justifies it.
- **Stack constraint**: open-source and free-tier only — static site generator (Astro/Hugo), Git + GitHub free tier, Python tooling. No paid SaaS in v1.
