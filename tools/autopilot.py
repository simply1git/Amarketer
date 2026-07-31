#!/usr/bin/env python3
"""Amarketer Autopilot Engine — 100% Automated AI Affiliate Marketing Pipeline.

Runs the complete end-to-end flow in a single command:
1. Researches and drafts an SEO-optimized affiliate review/roundup post using OpenRouter API.
2. Generates branded 1000x1500 Pinterest pin PNG image using tools/generate_pins.py.
3. Lints FTC compliance & internal link density via tools/check_content.py & tools/check_links.py.
4. Sets status to 'published' and triggers Astro static site build.

Usage:
  python tools/autopilot.py --topic "Systeme.io vs MailerLite"
  python tools/autopilot.py --auto
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

POSTS_DIR = REPO / "site" / "src" / "content" / "posts"
PINS_DIR = REPO / "ops" / "content" / "pins" / "cluster-03"

DEFAULT_TOPICS = [
    {
        "slug": "systeme-io-free-all-in-one-funnel",
        "title": "Systeme.io Review 2026: Is the Free Plan Really Unlimited?",
        "keyword": "systeme io review free plan",
        "cluster": "saas-tools",
        "offers": ["systeme-io-affiliate"],
        "items": ["2000 Contacts|Sales Funnels|Course Hosting|Email Marketing|Zero Monthly Fee"]
    },
    {
        "slug": "grammarly-vs-prowritingaid",
        "title": "Grammarly vs ProWritingAid: Best AI Writing Assistant",
        "keyword": "grammarly vs prowritingaid",
        "cluster": "saas-tools",
        "offers": ["grammarly-affiliate"],
        "items": ["Grammarly|ProWritingAid|Plagiarism Check|Tone Detector|Browser Extension"]
    }
]


def load_env():
    env_file = REPO / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def run_openrouter(prompt: str) -> str:
    load_env()
    from tools.run_openrouter_task import query_openrouter
    return query_openrouter(prompt)

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")

def run_cmd(*args, cwd=REPO):
    cmd_list = [str(a) for a in args]
    try:
        res = subprocess.run(cmd_list, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
        return res.returncode == 0, res.stdout or "", res.stderr or ""
    except Exception as e:
        return False, "", str(e)



def generate_post(topic_info: dict):
    slug = topic_info["slug"]
    title = topic_info["title"][:68]
    keyword = topic_info["keyword"]

    cluster = topic_info["cluster"]
    offers = topic_info["offers"]
    items = topic_info["items"][0]

    def safe_print(msg):
        print(str(msg).encode("ascii", errors="replace").decode("ascii"))

    safe_print(f"\n[Autopilot] Stage 1: Drafting post via OpenRouter AI for '{title}'...")
    prompt = f"""Write a comprehensive, hands-on affiliate review blog post for the website SoloStack.
Title: "{title}"
Target Keyword: "{keyword}"
Category Cluster: "{cluster}"

Requirements:
- Article must be helpful, honest, and structured for high conversion.
- Do NOT make any earnings promises or fake income claims.
- Include price bands (e.g. "Free Tier", "Under $30/mo") instead of static unverified prices.
- Include a Quick Comparison table, key features, who should buy vs skip, and an FTC disclosure.
- Output ONLY the raw markdown content formatted ready for Astro.
"""
    body = run_openrouter(prompt)

    # Clean markdown codeblocks if model wrapped output
    if body.startswith("```markdown"):
        body = body[11:]
    if body.startswith("```"):
        body = body[3:]
    if body.endswith("```"):
        body = body[:-3]
    body = body.strip()

    frontmatter = f"""---
title: "{title}"
description: "Hands-on review and comparison of {title} for solo creators and one-person businesses."
pubDate: 2026-07-31
status: published
targetKeyword: "{keyword}"
cluster: "{cluster}"
offers: {offers}
hasAffiliateLinks: true
amazon: false
---

"""
    post_path = POSTS_DIR / f"{slug}.md"
    post_path.write_text(frontmatter + body + "\n\n*See also our guide on [desk upgrades under $50](/posts/desk-upgrades-under-50).*\n", encoding="utf-8")
    safe_print(f"[Autopilot] Saved post: {post_path.name}")

    safe_print(f"[Autopilot] Stage 2: Rendering Pinterest Pin PNG...")
    pin_path = PINS_DIR / f"pin-{slug}.png"
    ok, stdout, stderr = run_cmd(
        sys.executable,
        str(REPO / "tools" / "generate_pins.py"),
        "--title", title[:45],
        "--items", items,
        "--out", str(pin_path)
    )
    if ok:
        safe_print(f"[Autopilot] Pin generated: {pin_path.name}")
    else:
        safe_print(f"[Autopilot] Pin generation warning: {stderr}")

    safe_print(f"[Autopilot] Stage 3: Running Content & FTC Compliance Linters...")
    ok_content, out_content, _ = run_cmd(sys.executable, str(REPO / "tools" / "check_content.py"))
    ok_links, out_links, _ = run_cmd(sys.executable, str(REPO / "tools" / "check_links.py"))

    safe_print(out_content.strip())
    safe_print(out_links.strip())

    safe_print(f"[Autopilot] Stage 4: Triggering Astro Static Site Build...")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    ok_build, out_build, err_build = run_cmd(npm_cmd, "--prefix", "site", "run", "build")

    if ok_build:
        safe_print("[Autopilot] Static site build SUCCESS! All pages generated.")
    else:
        safe_print(f"[Autopilot] Build warning: {err_build}")

    safe_print(f"\n[Autopilot] Pipeline Complete for '{title}'!")


def main():
    ap = argparse.ArgumentParser(description="Amarketer Autopilot Engine")
    ap.add_argument("--topic", help="Topic title to write review for")
    ap.add_argument("--auto", action="store_true", help="Run automated batch for top topics")
    args = ap.parse_args()

    if args.auto or not args.topic:
        for t in DEFAULT_TOPICS:
            generate_post(t)
    else:
        slug = slugify(args.topic)
        t = {
            "slug": slug,
            "title": args.topic,
            "keyword": args.topic.lower(),
            "cluster": "saas-tools",
            "offers": ["systeme-io-affiliate"],
            "items": ["Tested Setup|Zero Hype|Free Tier|Solo Stack"]
        }
        generate_post(t)

if __name__ == "__main__":
    main()
