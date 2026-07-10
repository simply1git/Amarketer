---
id: open-source-toolchain
type: reference
name: Open-source toolchain decisions
description: Consult when choosing tools for production automation or when an owner-suggested repo needs an adoption verdict.
summary: >
  Verdicts on evaluated open-source tools. Adopted: pocket-tts (offline TTS,
  tested), STORM's research method (not the software). Conditional:
  Agent-Reach (read-only research, ban risk on posting). Rejected for now:
  alook (multi-agent org layer), dograh (voice telephony).
source:
  origin: hands-on evaluation + repo review, 2026-07-10 (owner-suggested repos)
  retrieved: 2026-07-10
status: verified
created: 2026-07-10
updated: 2026-07-10
confidence:
  level: high
  basis: pocket-tts tested end-to-end in our pipeline; others assessed from repo docs
related: [youtube-faceless]
---

# Open-Source Toolchain Decisions

Design principle (owner, 2026-07-10): **single-user system** — no multi-tenant auth, no hosted dependencies where a local script works; everything readable and editable in the repo.

## Adopted

- **pocket-tts** (Kyutai, MIT) — offline CPU TTS, 100M params, ~6x realtime. Wired into `tools/make_voiceover.py --engine pocket`; supports `--clone <audio>` for a consistent owned channel voice. **Tested working.** edge-tts remains the default (higher polish) — pocket is the no-cloud fallback and the voice-cloning path.
- **STORM's method** (Stanford, MIT) — *not running the software* (needs paid LLM+search API keys; our agent already does grounded research). Adopted its two techniques into our drafting protocol: (1) perspective-guided questioning — before drafting, enumerate 3-4 reader perspectives (skeptic, beginner, budget-constrained, power user) and research the questions each would ask; (2) simulated expert QA — interrogate the draft against sources before publishing.

## Conditional

- **Agent-Reach** (MIT) — unified read access to Reddit/YouTube/X etc. for trend research without per-platform APIs. **Rule: read-only research use only; never automated posting; never main accounts** (its own docs warn of account bans on cookie-based automation — exactly the risk our human-gate model exists to avoid). Install only when trend-research volume justifies it.

## Rejected (for now)

- **alook** (Apache 2.0) — org-chart/email coordination layer for teams of agents. We are one agent + one owner; Claude Code already orchestrates; adds a hosted WebSocket dependency. Revisit only if the system ever runs multiple parallel agents.
- **dograh** (BSD-2) — self-hosted voice-call agents (Vapi alternative). No telephony use case in this system.
