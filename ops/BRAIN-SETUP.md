---
title: Independent Brain Setup (no Claude subscription needed)
type: runbook
date: 2026-07-10
---

# Autonomous Mode — Setup

The system has **two subscription-free brains** that execute tasks from `ops/tasks/` (created in the `/admin` panel → "Agent Tasks"). Either one alone is enough; together they're redundant.

| Brain | Runs | Needs | Best at |
|---|---|---|---|
| Local — [free-claude-code](https://github.com/Alishahryar1/free-claude-code) proxy + Claude Code harness on a free backend | your PC, every 20 min | one free API key | full tool use, best harness |
| Cloud — GitHub Actions + [gemini-cli](https://github.com/google-gemini/gemini-cli) | GitHub's servers, 2×/day + on-demand button | one free API key as repo secret | running while PC is off |

Both read the same CLAUDE.md rules, obey the same guardrails, and can only produce **drafts** — publishing still requires your dropdown flip in /admin.

## A. One free API key (pick one, both brains can share the Gemini one)

- **Google AI Studio key** (recommended): https://aistudio.google.com → Get API key → create. Free tier, no card.
- Alternative: https://openrouter.ai → free account → key → use `:free` models.

## B. Cloud brain (10 minutes — works even with your PC off)

1. GitHub repo → Settings → Secrets and variables → Actions → **New repository secret**: name `GEMINI_API_KEY`, value = your key.
2. That's it. The workflow `.github/workflows/agent-task.yml` now runs twice daily, and you can trigger it any time: repo → **Actions → "Agent task runner (cloud brain)" → Run workflow**.
3. Without the secret, the workflow exits harmlessly.

## C. Local brain (~20 minutes, one-time)

1. Install `uv` (open-source Python manager): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Install free-claude-code per its README quickstart (https://github.com/Alishahryar1/free-claude-code) — installer script sets up the proxy + `fcc-claude` command.
3. Open its Admin UI → add your API key → set the backend. **Tier routing** (so drafting gets the best free model): opus/sonnet tier → strongest free Gemini model; haiku tier → flash-lite. (Both tiers can point at the same model to keep it simple.)
4. Sanity check from the repo root: `fcc-claude -p "Read kb/INDEX.md and list the entry ids"` — a correct list means harness + backend + rules all work.
5. Register the scheduler (runs every 20 min, exits instantly when no tasks):

```powershell
schtasks /create /tn "AmarketerAgent" /sc minute /mo 20 /f /tr "powershell -NoProfile -ExecutionPolicy Bypass -File \"E:\New folder\tools\run_agent_task.ps1\""
```

Remove with `schtasks /delete /tn "AmarketerAgent" /f`.

## How to use it day-to-day

1. `/admin` → **Agent Tasks → New**: write instructions like briefing an assistant ("research affiliate programs for standing desks and add KB entries", "draft a roundup about desk lighting"). Save with status `todo`.
2. A runner claims it (you'll see status flip to `in-progress`, then `done`), results appear as **drafts** in Site Posts / the repo.
3. Check **Agent Activity Log** in /admin for what ran and when. `blocked` status = validation failed twice; the log file path is in the activity note.
4. Recurring tasks (`weekly`/`monthly`) re-queue themselves automatically after their interval.

## Honest quality note

Free models are weaker than Claude: expect drafts that need more editing, especially early. The guardrails, validators, and your approval gate catch rule violations — they don't make prose brilliant. The `learned/` loop improves the *instructions* over time, which lifts every brain. For revenue-critical copy, a Claude session remains the premium option — but nothing in the system requires it.
