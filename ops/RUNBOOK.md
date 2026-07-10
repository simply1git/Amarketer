---
title: Amarketer Operating Runbook
type: runbook
audience: owner (you) + AI agent
date: 2026-07-09
---

# How to Run Amarketer

This is the day-to-day manual. Architecture is in [PLAN.md](../PLAN.md); agent rules in [CLAUDE.md](../CLAUDE.md).

## One-time launch checklist (owner — ~30 minutes total)

1. **GitHub**: create a free account/repo, push this folder. *(5 min)*
2. **Cloudflare Pages**: connect the repo — exact clicks in [site/README.md](../site/README.md). Site goes live at `solostack.pages.dev` (or similar). *(10 min)*
3. **Newsletter**: create a free MailerLite account, paste the form embed where the footer form placeholder is (agent will do the paste — just provide the embed code). *(5 min)*
4. **Google Search Console**: add the site, submit the sitemap. *(5 min)*
5. **Pinterest**: free business account, claim the website. *(5 min)*
6. **YouTube**: create a channel (brand account, no face needed). *(5 min)*
7. **Affiliate programs**: sign up for Systeme.io and Grammarly programs first (both accept new affiliates). Paste the real terms + your tracking links to the agent afterward so the KB entries flip to `verified`. GetResponse/Notion/Canva applications come after the site has content.
8. **Test accounts**: create free accounts on the 5 tools in [video 01](content/youtube/video-01-package.md) so the agent can run the hands-on test protocol and fill the script's [VERIFY] slots (account creation is your gate; testing is agent work).

## Weekly operating cycle (steady state)

| Day | Who | What |
|---|---|---|
| 1 | Agent | Runs test protocol on next tool(s); fills the video package (script, description, titles) + hub-page draft (`status: draft`) |
| 2 | You (10 min) | Read the package; request edits or set `status: approved` |
| 2 | Agent | Generates voiceover mp3s (`make_voiceover.py`) + pins (`make-pin.mjs`); moves approved hub page into `site/src/content/posts/` |
| 3 | You (20–30 min) | Assemble video in a free editor (screen captures + generated voiceover), upload to YouTube; set hub page `status: published`, push; post pins; send newsletter |
| ongoing | Agent | Monitors, researches next programs/topics, maintains KB |

## Monthly cycle

1. You: export CSVs (Search Console, Pinterest, affiliate dashboards) into a folder, tell the agent.
2. Agent: `python tools/import_report.py <file>` per export → analysis → `kb/learned/` entries with metrics.
3. Agent: consolidation pass (dedupe learned entries, promote to verified, retire losers).
4. You: 15-minute review of the agent's monthly summary + any proposed autonomy promotions.

## Guardrails (what the agent will never do without you)

Publish, sign up, spend, or delete verified knowledge. If the agent asks you to do one of these, everything is already prepared — your action is the last step.

## Autonomous mode (no chat, no subscription)

Assign work from `/admin` → **Agent Tasks** (status `todo`); a free-LLM brain executes it and returns **drafts** — the local runner (every 20 min while the PC is on) or the cloud runner (GitHub Actions, 2×/day + "Run workflow" button, works with the PC off). Watch progress in **Agent Activity Log**. Setup (one free API key): [BRAIN-SETUP.md](BRAIN-SETUP.md). Recurring tasks (weekly content batch, monthly learning loop) re-queue themselves. Publishing still requires your dropdown flip — no brain can bypass it.

## Automation you get for free

- **Every push**: GitHub Actions validates the KB, lints all content for income claims/missing disclosures, and builds the site. A red X on a commit means something must be fixed before publishing.
- **Monthly**: a KB-freshness issue is opened automatically listing expired/stale program data needing re-verification.
- **Affiliate links**: all content uses `/go/<program>` URLs. Real tracking links get pasted once into `site/public/_redirects` — every video description, pin, and post updates instantly.
- **Voiceovers**: `python tools/make_voiceover.py <video-package.md>` produces mp3 narration per section (free Microsoft TTS) — no recording needed.
- **Pins**: `node site/scripts/make-pin.mjs --title "..." --items "A|B|C"` renders finished 1000×1500 pin images.

## When something breaks

- KB validation fails: `python tools/validate_kb.py` prints which file/field.
- Site build fails: `cd site && npm run build` — errors name the file; drafts with bad frontmatter are the usual cause.
- Wrong fact in a published post: tell the agent — it corrects the post *and* the KB entry that sourced it, and records the failure in `learned/`.
