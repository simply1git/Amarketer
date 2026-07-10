---
id: seo-content-site
type: channel
name: SEO niche content site playbook
description: Use when planning site structure, choosing what to write, drafting articles, or doing on-page SEO for the niche site.
summary: >
  Link-hub + SEO channel (secondary since the 2026-07 pivot; youtube-faceless
  is primary). Static site on free-tier hosting hosts the written breakdowns
  videos and pins link to, and carries the /go/ affiliate redirects. Content
  strategy: bottom-of-funnel buyer-intent keywords, E-E-A-T, ftc-disclosure.
source:
  origin: synthesized from standard solo-affiliate SEO practice; to be refined by learned/ entries with real metrics
  retrieved: 2026-07-09
status: verified
created: 2026-07-09
updated: 2026-07-09
confidence:
  level: medium
  basis: widely-replicated practice, not yet validated by our own campaign data
related: [ftc-disclosure, youtube-faceless, no-income-claims]
triggers:
  - "IF choosing what to write first THEN prioritize bottom-of-funnel buyer-intent keywords (best-X-for-Y, X-vs-Y, X-review) over informational topics"
  - "IF an article mentions a product we have an offer entry for THEN link with the tracked affiliate link and cite the offer entry id in the draft's frontmatter"
  - "IF publishing cadence is decided THEN prefer consistent small cadence (2-3 posts/week) over bursts"
  - "IF a post is older than 6 months AND ranks positions 5-15 THEN schedule a refresh update before writing new content"
ai_instructions: >
  Drafts go to ops/content/ with frontmatter status: draft. Every draft must
  pass the ftc-disclosure triggers before being proposed for approval.
---

# Site (Link Hub + SEO) — Playbook

> Role changed at the 2026-07 pivot: the site is the link hub behind YouTube/Pinterest (hosts written breakdowns + /go/ redirects); SEO traffic is a compounding byproduct, not the primary strategy. See ops/niche/2026-07-pivot-decision.md.

## Stack (open-source, $0)

- **Astro** (static site generator, MIT license) — fast, content-collections fit our frontmatter workflow, agent-editable Markdown.
- **Cloudflare Pages** free tier (unlimited bandwidth on free plan makes it preferable to Vercel's 100GB) with `*.pages.dev` subdomain at launch; custom domain optional later.
- **GitHub free** — repo, deploy-on-push, content approval via the `draft → approved → published` frontmatter state.

## Content strategy

1. **Bottom-of-funnel first.** Buyer-intent formats ("best X for Y", "X vs Y", "X review") convert; informational posts come later to build topical authority around the money pages.
2. **Topical clusters.** Pick one product sub-category, cover it completely (one pillar + 5–10 supporting posts) before starting another. Search engines reward depth over breadth for new sites.
3. **E-E-A-T signals.** Real comparisons with concrete data, honest cons, named author page, cited sources. Thin AI-generated content is actively penalized; every draft must add something not on page 1 already (data table, decision framework, genuine testing notes).
4. **Structure per post:** verdict/answer first, comparison table (disclosure above it), then detail. Readers and featured snippets both reward answer-first.

## On-page rules (apply to every draft)

- One target keyword per post; in title, H1, first 100 words, URL slug.
- Internal links: every post links to its pillar and 2+ siblings.
- Affiliate links: `rel="sponsored nofollow"`, tracked, disclosure per [[ftc-disclosure]].
- Images with descriptive alt text; compressed.

## Measurement (Phase 4 feeds learned/)

- Google Search Console (free) from day one — impressions/clicks per page.
- Plausible-style analytics via self-hosted or free tier alternative; defer if it costs money.
- Per-post frontmatter carries target keyword + linked offer ids so performance reports can be joined back to KB entries.
