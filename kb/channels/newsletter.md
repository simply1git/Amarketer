---
id: newsletter
type: channel
name: Newsletter playbook
description: Use when writing the weekly issue, wiring the signup form, or planning email monetization.
summary: >
  Owned-audience channel from day one. Weekly short issue ("one useful
  classroom-AI find per week") built from the week's testing notes. Free-tier
  provider; email list is the hedge against search volatility.
source:
  origin: synthesized from standard creator-newsletter practice; provider choice pending
  retrieved: 2026-07-09
status: verified
created: 2026-07-09
updated: 2026-07-09
confidence:
  level: medium
  basis: widely-replicated practice; unvalidated by own data yet
related: [seo-content-site, ftc-disclosure, pinterest-distribution]
triggers:
  - "IF the site launches THEN wire the footer form to the chosen free-tier provider before the first post is published"
  - "IF an issue contains an affiliate link THEN disclosure appears in the body before the first such link (ftc-disclosure)"
  - "IF list passes 500 subscribers THEN evaluate a dedicated tools-deal issue format"
ai_instructions: >
  Draft issues as markdown in ops/content/newsletter/ with status: draft; the
  owner approves and sends (publishing gate applies to email too).
---

# Newsletter

## Provider (free-tier comparison — owner picks at launch)
- **Buttondown** free ≤ 100 subs (markdown-native, simplest for our pipeline)
- **MailerLite** free ≤ 1,000 subs, 12k emails/mo (best free ceiling; automation included)
- **Brevo** free 300 emails/day (no sub cap; daily send limit)
Recommendation: **MailerLite** — highest free ceiling, form embeds work with a static site.

## Format (weekly, short)
1. One tool find of the week — 3 sentences from our actual testing notes.
2. One practical tip using a tool we've covered (links to the post).
3. What we're testing next (builds anticipation, invites replies).
Disclosure line above the first affiliate link, every issue.

## Growth mechanics
- Footer form on every page (already scaffolded), inline form after the verdict section in posts.
- Pinterest pins for "checklist" content gated behind signup once list infrastructure works (v1.5, only if organic capture is slow).

## Measurement
Provider stats (open rate, click rate per issue) exported monthly → `ops/reports/` → learned entries on subject-line and item formats.
