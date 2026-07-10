#!/usr/bin/env python3
"""Report KB entries that need re-verification (stale or expired).

Rules (from CLAUDE.md):
- valid_until in the past  -> EXPIRED (must re-verify before any use)
- type offer/program with updated > 30 days ago -> STALE-OFFER (re-verify)
- any entry updated > 90 days ago -> AGING (prefer fresher data)

Usage: python tools/check_freshness.py [--kb-dir kb]
Exit 0 = nothing expired; exit 1 = expired entries exist. Output is
markdown suitable for a GitHub issue body.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SKIP_NAMES = {"INDEX.md", "README.md"}


def parse_date(value):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb-dir", default="kb")
    args = ap.parse_args()

    today = dt.date.today()
    expired, stale_offers, aging = [], [], []

    for path in sorted(Path(args.kb_dir).rglob("*.md")):
        if path.name in SKIP_NAMES:
            continue
        m = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        if fm.get("status") == "deprecated":
            continue
        entry_id = fm.get("id", path.stem)

        vu = parse_date(fm.get("valid_until"))
        if vu and vu < today:
            expired.append(f"`{entry_id}` — valid_until {vu} ({path})")
            continue
        updated = parse_date(fm.get("updated"))
        if updated:
            age = (today - updated).days
            if fm.get("type") in ("offer", "program") and age > 30:
                stale_offers.append(f"`{entry_id}` — updated {age} days ago ({path})")
            elif age > 90:
                aging.append(f"`{entry_id}` — updated {age} days ago ({path})")

    print(f"# KB freshness report — {today}\n")
    for title, items in (("EXPIRED (re-verify before ANY use)", expired),
                         ("Stale offer/program data (>30 days)", stale_offers),
                         ("Aging entries (>90 days)", aging)):
        print(f"## {title}\n")
        print("\n".join(f"- {i}" for i in items) if items else "- none")
        print()
    return 1 if expired else 0


if __name__ == "__main__":
    sys.exit(main())
