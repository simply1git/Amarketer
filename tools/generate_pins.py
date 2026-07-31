#!/usr/bin/env python3
"""Automated Batch Pinterest Pin Generator CLI.

Wrapper around site/scripts/make-pin.mjs to generate branded 1000x1500 PNG pins.

Usage:
  python tools/generate_pins.py --title "Desk Lighting Under $60" --items "ScreenBar|LED Bar|Clamps" --out ops/content/pins/cluster-03/15-desk-lighting.png
  python tools/generate_pins.py --batch ops/content/pins/cluster-03/pins.json
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE_DIR = REPO / "site"
MAKE_PIN_MJS = SITE_DIR / "scripts" / "make-pin.mjs"

def run_make_pin(title: str, items: str, tag: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "node",
        str(MAKE_PIN_MJS),
        "--title", title,
        "--items", items,
        "--tag", tag,
        "--out", str(out_path)
    ]
    res = subprocess.run(cmd, cwd=str(SITE_DIR), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error generating pin ({out_path.name}): {res.stderr}", file=sys.stderr)
        return False
    print(f"Success: {res.stdout.strip()}")
    return True

def main():
    ap = argparse.ArgumentParser(description="Batch Pinterest Pin Generator")
    ap.add_argument("--title", help="Pin main title headline")
    ap.add_argument("--items", default="", help="Pipe-separated checklist items e.g. Item1|Item2")
    ap.add_argument("--tag", default="amarketer.25012004.xyz", help="Domain tag on pin footer")
    ap.add_argument("--out", help="Output PNG filepath")
    ap.add_argument("--batch", help="JSON file containing list of pin definitions")
    args = ap.parse_args()

    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            print(f"Batch file not found: {batch_file}", file=sys.stderr)
            sys.exit(1)
        pins = json.loads(batch_file.read_text(encoding="utf-8"))
        success_count = 0
        for p in pins:
            title = p.get("title")
            items = p.get("items", "")
            tag = p.get("tag", "amarketer.25012004.xyz")
            out_path = REPO / p.get("out")
            if run_make_pin(title, items, tag, out_path):
                success_count += 1
        print(f"\nBatch complete: {success_count}/{len(pins)} pins generated successfully.")
    elif args.title and args.out:
        out_path = REPO / args.out if not Path(args.out).is_absolute() else Path(args.out)
        if not run_make_pin(args.title, args.items, args.tag, out_path):
            sys.exit(1)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
