---
id: youtube-faceless
type: channel
name: YouTube faceless channel playbook
description: Use when scripting, packaging, or scheduling YouTube videos — the primary distribution channel.
summary: >
  Primary channel. Faceless format: screen recordings of tools + TTS or owner
  voiceover + AI-drafted scripts in proven formats. Affiliate links live in the
  description via hub-page URLs. Packaging (title+thumbnail) decides reach.
source:
  origin: modeled on widely-replicated faceless AI-tools channel practice; to be validated by learned/ entries
  retrieved: 2026-07-09
status: verified
created: 2026-07-09
updated: 2026-07-09
confidence:
  level: medium
  basis: proven format category; unvalidated by own channel data yet
related: [seo-content-site, pinterest-distribution, ftc-disclosure, no-income-claims]
triggers:
  - "IF scripting a video THEN use a proven format: 'I tested N tools', 'best X for Y', 'X vs Y', or 'stop using X, use Y'"
  - "IF a video mentions a promoted tool THEN the description carries the hub-page link + #ad disclosure in the first visible lines, and the video includes a spoken/on-screen disclosure"
  - "IF a video's CTR < 4% after 48h THEN propose a title/thumbnail variant before making new content"
  - "IF a format's avg view duration > 50% THEN record a learned/ entry and repeat the format"
ai_instructions: >
  Agent produces the full package per video: script (TTS-ready narration +
  scene/screen directions), title options, thumbnail concept, description with
  link placeholders, tags. Owner records/uploads (publishing gate). Never
  script income claims (kb: no-income-claims).
---

# YouTube Faceless — Playbook

## Production pipeline (per video)
1. Agent hands-on tests the tools (free tiers) → testing notes with screenshots/screen recordings.
2. Agent writes the package: 6–10 min script, 3 title options, thumbnail concept, description, tags.
3. Owner (or free TTS pipeline) records voiceover over screen captures; free editor (CapCut/DaVinci free) assembles.
4. Owner uploads (gate); links point to SoloStack hub pages, `#ad` disclosure up top.

## Format library (proven categories — model, don't copy)
- **Tested-list**: "I tested 7 free AI tools — 3 are worth it" (curiosity + credibility)
- **Best-for**: "Best free funnel builder for beginners (2026)"
- **Versus**: "Systeme.io vs ClickFunnels: the $0 answer"
- **Contrarian**: "Stop paying for X — this free tool does it"

## Packaging rules
Title ≤ 60 chars, one curiosity gap, year for freshness. Thumbnail: ≤ 4 words, one visual focal point, high contrast. Hook (first 20s): state the payoff and the credibility ("I actually tested all of these") before anything else.

## Compliance
Spoken + description disclosure every monetized video; no income claims ever; check each program's ToS entry for YouTube-specific rules before first use.

## Measurement
Monthly YouTube Studio CSV export → import_report.py → learned entries keyed on format, CTR, avg view duration, hub-page clicks.
