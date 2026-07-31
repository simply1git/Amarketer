#!/usr/bin/env python3
"""Internal Link & Site Structure Checker.

Scans site/src/content/posts/ for markdown links, verifies internal target pages exist,
and reports linking density across posts.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO / "site" / "src" / "content" / "posts"

LINK_RE = re.compile(r"\[([^\]]+)\]\((/posts/[^\)]+)\)")

def main():
    if not POSTS_DIR.exists():
        print(f"Posts directory not found: {POSTS_DIR}", file=sys.stderr)
        sys.exit(1)

    posts = list(POSTS_DIR.glob("*.md"))
    valid_slugs = {f"/posts/{p.stem}" for p in posts}
    valid_slugs.add("/disclosure")

    errors = 0
    total_links = 0

    print(f"Checking {len(posts)} posts for internal links...")
    for post in posts:
        text = post.read_text(encoding="utf-8")
        links = LINK_RE.findall(text)
        total_links += len(links)
        if not links:
            print(f"WARN  {post.name}: 0 internal links found (recommended at least 1)")
        for anchor, href in links:
            clean_href = href.split("#")[0]
            if clean_href not in valid_slugs:
                print(f"ERROR {post.name}: broken internal link -> {href} (anchor: '{anchor}')")
                errors += 1

    print(f"\nScan complete: {len(posts)} posts, {total_links} internal links, {errors} error(s).")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
