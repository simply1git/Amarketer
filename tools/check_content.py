#!/usr/bin/env python3
"""Compliance linter: scan content for income claims and missing disclosures.

Enforces kb/policies/no-income-claims.md and kb/policies/ftc-disclosure.md
mechanically. Run in CI and before any content is approved.

Usage: python tools/check_content.py [paths...]   (default: ops/content site/src/content)
Exit 0 = clean; exit 1 = violations listed.
"""
import re
import sys
from pathlib import Path

DEFAULT_PATHS = ["ops/content", "site/src/content"]

# (severity, pattern, message)
RULES = [
    ("ERROR", re.compile(r"\b(make|earn|making|earning|made|earned)\s+(me\s+|you\s+)?\$\s?\d", re.I),
    "income claim: earning + dollar amount (no-income-claims)"),
    ("ERROR", re.compile(r"\$\s?[\d,]+\s*(/|\bper\s+|\ba\s+)(day|week|month|year)\b", re.I),
     "income claim: $X per period (no-income-claims)"),
    ("ERROR", re.compile(r"\b(quit\s+your\s+job|replace\s+your\s+(salary|income)|financial\s+freedom\s+guaranteed)\b", re.I),
     "income claim: lifestyle-outcome promise (no-income-claims)"),
    ("ERROR", re.compile(r"\bguaranteed\s+(income|earnings|profit|results)\b", re.I),
     "income claim: guarantee (no-income-claims)"),
    ("WARN", re.compile(r"\bpassive\s+income\b", re.I),
     "risky phrase: 'passive income' — reframe as automation/time saved"),
    ("WARN", re.compile(r"\b(get\s+rich|easy\s+money|money\s+while\s+you\s+sleep)\b", re.I),
     "risky phrase: hype language"),
]

AFFILIATE_HINT = re.compile(r"affiliate|/go/|\{HUB_URL\}|#ad", re.I)
DISCLOSURE_HINT = re.compile(r"affiliate links|#ad|earn (a )?commission", re.I)
# Internal planning docs are never published; income-claim rules still apply
# to them, but the disclosure-presence rule does not.
PLANNING_TYPES = re.compile(
    r"^type:\s*(content-plan|decision-record|performance-report|runbook|research-\w+)", re.M)


def lint_file(path: Path):
    problems = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        for severity, pattern, message in RULES:
            if pattern.search(line):
                problems.append((severity, lineno, message, line.strip()[:90]))
    # disclosure presence: any publishable file that references affiliate
    # mechanics must contain disclosure language somewhere
    if AFFILIATE_HINT.search(text) and not DISCLOSURE_HINT.search(text) and not PLANNING_TYPES.search(text):
        problems.append(("ERROR", 0, "affiliate content without disclosure language (ftc-disclosure)", ""))
    return problems


def main():
    targets = sys.argv[1:] or DEFAULT_PATHS
    files = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            files.append(p)

    errors = warnings = 0
    for f in files:
        for severity, lineno, message, snippet in lint_file(f):
            loc = f"{f}:{lineno}" if lineno else str(f)
            print(f"{severity} {loc} — {message}")
            if snippet:
                print(f"    | {snippet}")
            if severity == "ERROR":
                errors += 1
            else:
                warnings += 1

    print(f"\n{len(files)} files checked: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
