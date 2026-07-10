# Amarketer — Project Status & Continuation Guide

> **Purpose of this file:** resume the project cold — in a new chat session, on a new machine, or months later. Read this, then [PLAN.md](PLAN.md) (architecture & decisions) and [CLAUDE.md](CLAUDE.md) (agent operating rules). Keep this file updated whenever a milestone lands.

*Last updated: 2026-07-10*

## What this project is

A **self-improving, AI-operated affiliate marketing system** for a solo owner. $0 budget, open-source/free-tier only, single-user, subscription-independent. Live site: **https://amarketer.25012004.xyz** (Cloudflare Pages, project `amarketer`, alias `amarketer.pages.dev`; root domain `25012004.xyz` reserved for other projects). Repo: https://github.com/simply1git/Amarketer.

## Strategy (decided, don't re-litigate)

- **Two revenue tracks.** Track A (fast): Pinterest product-roundup pins → hub pages on the site → Amazon Associates links (desk/home-office gear). Track B (compounding): faceless YouTube videos promoting recurring-commission SaaS (Systeme.io ~60% lifetime, GetResponse — rates unverified until signup). Full rationale: [ops/niche/2026-07-pivot-decision.md](ops/niche/2026-07-pivot-decision.md) + [ops/niche/2026-07-shortlist.md](ops/niche/2026-07-shortlist.md) (superseded history).
- **Brand:** SoloStack — "tested, not hyped" tool/gear reviews for one-person businesses.
- **Hard rules:** FTC disclosure before first affiliate link; NO income claims ever; never quote rates not verified in the KB; Amazon signup only AFTER pins demonstrably click (3-sales/180-day account rule).

## How the system works

- **KB** (`kb/`) — programs, tactics, policies, learned insights; schema-validated (`tools/validate_kb.py`); entry point [kb/INDEX.md](kb/INDEX.md).
- **Site** (`site/`) — Astro; posts publish ONLY with frontmatter `status: published` (the owner gate, enforced by the build).
- **Web admin** — `https://amarketer.25012004.xyz/admin` (Sveltia CMS): approve/edit/create posts, assign Agent Tasks, read the activity log. Auth setup: [ops/ADMIN-SETUP.md](ops/ADMIN-SETUP.md).
- **Autonomous brains** (no Claude subscription): local free-claude-code runner (Task Scheduler, 20-min) + cloud aider-on-OpenRouter GitHub Action. Task inbox `ops/tasks/` ← /admin. Setup: [ops/BRAIN-SETUP.md](ops/BRAIN-SETUP.md). **Owner chose OpenRouter as the key provider.**
- **Quality gates on every push:** CI validates KB, lints compliance (income claims/disclosures), builds site ([.github/workflows/ci.yml](.github/workflows/ci.yml)); monthly KB freshness issue.
- **Production tools:** pin generator (`site/scripts/make-pin.mjs`), voiceover (`tools/make_voiceover.py`, engines: edge-tts online / pocket-tts offline+cloning), report importer (`tools/import_report.py`).
- **Day-to-day operation:** [ops/RUNBOOK.md](ops/RUNBOOK.md).

## Milestones completed (all verified working)

| Date | Milestone |
|---|---|
| 2026-07-09 | KB-design research (research/kb-design/), system foundation, niche decisions, site scaffold + publish gate, pushed to GitHub |
| 2026-07-09 | Pivot to social-first SoloStack; video-01 package; automation layer (linters, CI, redirects, TTS, pins) |
| 2026-07-10 | Track A: 4 roundup hub pages (draft) + 14 pins + posting table; consistency audit; domain → amarketer.25012004.xyz; Pinterest verification tag live |
| 2026-07-10 | Web admin panel (/admin, Sveltia); autonomous mode: task inbox + dual free brains, runner tested end-to-end (guardrails, self-fix, blocked path) in isolated clone |

## OWNER CHECKLIST — everything pending is yours (agent is not blocked on itself)

**Activation (one-time):**
- [ ] OpenRouter key → GitHub repo secret `OPENROUTER_API_KEY` → test via Actions → "Run workflow" ([BRAIN-SETUP](ops/BRAIN-SETUP.md) §B)
- [ ] Local brain: install uv + free-claude-code, OpenRouter backend, register Task Scheduler ([BRAIN-SETUP](ops/BRAIN-SETUP.md) §C)
- [ ] Admin login: deploy sveltia-cms-auth worker + GitHub OAuth app, then put the worker URL into `site/public/admin/config.yml` `base_url` ([ADMIN-SETUP](ops/ADMIN-SETUP.md))
- [ ] Pinterest: finish claim of `amarketer.25012004.xyz` (tag is live — just click Verify), create boards `Desk Setup Ideas`, `Home Office On A Budget`, `WFH Tips`

**Content go-live:**
- [ ] Approve the 4 draft hub pages (in /admin once auth works, or tell the agent)
- [ ] Queue pins 1–3/day from [ops/content/pins/cluster-03/pin-descriptions.md](ops/content/pins/cluster-03/pin-descriptions.md) (images in the same folder)
- [ ] After pins click (>50 outbound/week, ~2–3 weeks): sign up Amazon Associates → give the agent the tracking IDs for the linking pass
- [ ] Track B when ready: YouTube channel + Systeme.io/Grammarly affiliate signups + free tool test accounts (video-01 package waits at [ops/content/youtube/video-01-package.md](ops/content/youtube/video-01-package.md))
- [ ] Newsletter: MailerLite free account → embed form (placeholder in site footer)

## How to resume in a new agent session

Say: *"Read STATUS.md, PLAN.md and CLAUDE.md, then continue Amarketer."* The agent should: check this checklist against reality (git log, ops/agent-activity.md, task statuses in ops/tasks/), ask nothing that's already decided here, and pick up the next unchecked item or the owner's new instruction.

## Known risks / honest notes

- Free OpenRouter models: rougher drafts than Claude; validators + owner gate catch violations, not mediocrity. Expect editing.
- Earnings timeline: pins can produce first commissions in 30–90 days per practitioner reports; nothing pays in week one. Consistency is the main variable.
- `notion-affiliate` direct program may be closed to new applicants (verify before applying); all program rates are `unverified` until confirmed at signup.
