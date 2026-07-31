---
title: Web Admin Setup (one-time, ~10 minutes)
type: runbook
date: 2026-07-10
---

# Web Admin Panel — One-Time Setup

The admin panel lives at **https://amarketer.25012004.xyz/admin**. It edits the GitHub repo directly, so it needs to authenticate you with GitHub once. That requires two free pieces: a GitHub OAuth App and a tiny Cloudflare Worker that handles the login handshake.

## Step 1 — Deploy the auth worker (Cloudflare, free)

1. Open https://github.com/sveltia/sveltia-cms-auth
2. Click the **"Deploy to Cloudflare Workers"** button in its README and follow the flow (sign in with your Cloudflare account; it creates a worker for free).
3. Note the worker URL it gives you, e.g. `https://sveltia-cms-auth.YOURNAME.workers.dev`.

## Step 2 — Create the GitHub OAuth App

1. GitHub → Settings → Developer settings → **OAuth Apps → New OAuth App**
2. Fill in:
   - Application name: `Amarketer Admin`
   - Homepage URL: `https://amarketer.25012004.xyz`
   - Authorization callback URL: `https://YOUR-WORKER-URL.workers.dev/callback`
3. Register, then copy the **Client ID** and generate + copy a **Client Secret**.

## Step 3 — Give the worker the credentials

1. Cloudflare Dashboard → Workers & Pages → your `sveltia-cms-auth` worker → **Settings → Variables**
2. Add two secrets: `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` (values from Step 2).
3. Optional but recommended: add `ALLOWED_DOMAINS` = `amarketer.25012004.xyz` so only our site can use the worker.

## Step 4 — Tell the agent (or edit yourself)

Paste the worker URL to the agent, or edit `site/public/admin/config.yml` yourself: replace the `base_url` placeholder with your worker URL. Commit/push → done.

## Using the panel

- **Approve a post:** open it → change *Status* to `published` → Save. That's a commit; the site deploys itself (~2 min). CI still lints every save for compliance.
- **Add a post:** *Site Posts → New*. It lands as `draft` — the same gate applies.
- **Everything is still files:** anything you do in the panel is a git commit you can see, revert, or edit in the repo. No hidden state.

## Security notes

- Only your GitHub account can log in usefully (the CMS writes with *your* GitHub permissions; others get rejected by GitHub).
- The worker stores no data; secrets stay in Cloudflare.
- The `/admin` page is `noindex` and harmless to expose — the login is the gate.
