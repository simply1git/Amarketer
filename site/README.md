# Classroom Stack — site

Astro static site. Free-tier stack: Cloudflare Pages + GitHub.

## Local dev

```
npm install
npm run dev      # http://localhost:4321
npm run build    # output in dist/
```

## Content workflow (enforced by build)

Posts live in `src/content/posts/*.md`. Frontmatter `status` must be `published` for a post to appear — `draft` and `approved` posts are excluded from the build, so only the owner flipping `status: published` makes anything public (see repo CLAUDE.md, Human gates).

Required frontmatter: `title`, `description`, `pubDate`, `targetKeyword`, `cluster`; `offers` lists the kb entry ids used; `amazon: true` adds the Amazon-mandated disclosure sentence. The disclosure block renders automatically before post content — never remove it.

## Deploy (owner, one-time setup)

1. Create a free GitHub repo, push this project.
2. Cloudflare Dashboard → Workers & Pages → Create → Pages → connect the repo.
3. Build settings: framework preset **Astro**, root directory `site`, build command `npm run build`, output `dist`.
4. Site goes live at `classroomstack.pages.dev` (or chosen subdomain — then update `site` in astro.config.mjs and robots.txt).

## Before launch checklist

- [ ] Wire the footer email form to a free-tier newsletter provider (form is marked `data-todo="newsletter-provider"`).
- [ ] Add Google Search Console verification + submit sitemap.
- [ ] Confirm `site` URL in astro.config.mjs matches the real deployment URL.
