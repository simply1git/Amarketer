#!/usr/bin/env python3
"""Validate YAML frontmatter of every kb/ entry against kb-entry.schema.json.

Usage: python tools/validate_kb.py [--kb-dir kb]
Exit 0 = all valid; exit 1 = failures (printed per file).

Requires: pyyaml, jsonschema  (pip install pyyaml jsonschema)
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).parent / "kb-entry.schema.json"
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SKIP_NAMES = {"INDEX.md", "README.md"}


def extract_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def validate_file(path: Path, validator: Draft202012Validator):
    errors = []
    fm = extract_frontmatter(path.read_text(encoding="utf-8"))
    if fm is None:
        return ["missing YAML frontmatter block"]
    if not isinstance(fm, dict):
        return ["frontmatter is not a mapping"]
    # jsonschema expects JSON-compatible types; YAML parses dates natively
    fm_json = json.loads(json.dumps(fm, default=str))
    for err in validator.iter_errors(fm_json):
        loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"{loc}: {err.message}")
    # extra rule: id must match filename stem
    if isinstance(fm.get("id"), str) and fm["id"] != path.stem:
        errors.append(f"id '{fm['id']}' does not match filename '{path.stem}'")
    # extra rule: expired offers must not be status: verified
    vu = fm_json.get("valid_until")
    if fm_json.get("status") == "verified" and isinstance(vu, str):
        try:
            if dt.date.fromisoformat(vu) < dt.date.today():
                errors.append(f"valid_until {vu} is in the past but status is 'verified' — re-verify or deprecate")
        except ValueError:
            pass  # format error already reported by schema
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb-dir", default="kb")
    args = ap.parse_args()

    kb_dir = Path(args.kb_dir)
    if not kb_dir.is_dir():
        print(f"KB directory not found: {kb_dir}", file=sys.stderr)
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    entries = [p for p in sorted(kb_dir.rglob("*.md")) if p.name not in SKIP_NAMES]
    failed = 0
    for path in entries:
        errors = validate_file(path, validator)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for e in errors:
                print(f"  - {e}")
    print(f"\n{len(entries) - failed}/{len(entries)} entries valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
