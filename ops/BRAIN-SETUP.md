---
title: Independent Brain Setup (no Claude subscription needed)
type: runbook
date: 2026-07-10
---

# Autonomous Mode — Setup

The system has **two subscription-free brains** that execute tasks from `ops/tasks/` (created in the `/admin` panel → "Agent Tasks"). Either one alone is enough; together they're redundant.

| Brain | Runs | Needs | Best at |
|---|---|---|---|
| Local — [free-claude-code](https://github.com/Alishahryar1/free-claude-code) proxy + Claude Code harness on the OpenRouter backend | your PC, every 20 min | the OpenRouter key | full tool use, best harness |
| Cloud — GitHub Actions + [aider](https://aider.chat) on OpenRouter | GitHub's servers, 2×/day + on-demand button | the same key as repo secret | running while PC is off |

Both read the same CLAUDE.md rules, obey the same guardrails, and can only produce **drafts** — publishing still requires your dropdown flip in /admin.

## A. The one key (owner decision 2026-07-10: OpenRouter)

1. https://openrouter.ai → sign up free → **Keys → Create key**. Copy it once (shown once).
2. Free models carry the `:free` suffix — browse https://openrouter.ai/models?q=free. Good defaults change over time; pick a large recent one (e.g. a DeepSeek or Qwen `:free` model).
3. (Alternative kept documented: Google AI Studio key + gemini-cli — the workflow auto-falls back to it if only `GEMINI_API_KEY` is set.)

## B. Cloud brain (10 minutes — works even with your PC off)

1. GitHub repo → Settings → Secrets and variables → Actions → **New repository secret**: name `OPENROUTER_API_KEY`, value = your key.
2. Optional: repo **variable** `OPENROUTER_MODEL` to choose the model (default is set in the workflow; format `openrouter/<provider>/<model>:free`).
3. That's it. `.github/workflows/agent-task.yml` runs twice daily; trigger any time via repo → **Actions → "Agent task runner (cloud brain)" → Run workflow**.
4. Without any key secret, the workflow exits harmlessly.

## C. Local brain (~20 minutes, one-time)

1. Install `uv` (open-source Python manager): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Install free-claude-code per its README quickstart (https://github.com/Alishahryar1/free-claude-code) — installer script sets up the proxy + `fcc-claude` command.
3. Open its Admin UI → add your **OpenRouter** key → set backend to OpenRouter. **Tier routing** (so drafting gets the best free model): opus/sonnet tier → the biggest `:free` model you picked; haiku tier → a small fast `:free` model. (Both tiers can point at the same model to keep it simple.)
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
