#!/usr/bin/env python3
"""Normalize performance-data CSV exports into ops/reports/ as dated Markdown.

Supported sources (auto-detected by columns, or force with --source):
  gsc        Google Search Console performance export (Queries or Pages tab)
  pinterest  Pinterest analytics export
  generic    any CSV — stored as-is with a summary block

Usage:
  python tools/import_report.py path/to/export.csv [--source gsc] [--note "june data"]

Output: ops/reports/YYYY-MM-DD-<source>.md with a summary table (top rows by
the primary metric) + the full CSV copied alongside. The agent reads these
files during analysis; learned/ entries must cite the report filename.
"""
import argparse
import csv
import datetime as dt
import shutil
import sys
from pathlib import Path

REPORTS_DIR = Path("ops/reports")

SOURCE_SIGNATURES = {
    "gsc": {"clicks", "impressions"},
    "pinterest": {"impressions", "saves"},
}


def detect_source(headers):
    lower = {h.strip().lower() for h in headers}
    for source, sig in SOURCE_SIGNATURES.items():
        if sig <= lower:
            return source
    return "generic"


def primary_metric(headers):
    lower = [h.strip().lower() for h in headers]
    for candidate in ("clicks", "outbound clicks", "saves", "impressions", "revenue", "earnings"):
        if candidate in lower:
            return headers[lower.index(candidate)]
    return None


def to_number(value):
    try:
        return float(str(value).replace(",", "").replace("%", ""))
    except ValueError:
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--source", choices=["gsc", "pinterest", "generic"])
    ap.add_argument("--note", default="")
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    if not args.csv_path.exists():
        print(f"File not found: {args.csv_path}", file=sys.stderr)
        return 1

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        print("CSV has no data rows", file=sys.stderr)
        return 1

    headers, data = rows[0], rows[1:]
    source = args.source or detect_source(headers)
    metric = primary_metric(headers)
    if metric:
        idx = headers.index(metric)
        data.sort(key=lambda r: to_number(r[idx]) if len(r) > idx else 0.0, reverse=True)

    today = dt.date.today().isoformat()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    base = f"{today}-{source}"
    csv_dest = REPORTS_DIR / f"{base}.csv"
    md_dest = REPORTS_DIR / f"{base}.md"
    n = 2
    while md_dest.exists():
        csv_dest = REPORTS_DIR / f"{base}-{n}.csv"
        md_dest = REPORTS_DIR / f"{base}-{n}.md"
        n += 1
    shutil.copy(args.csv_path, csv_dest)

    top = data[: args.top]
    lines = [
        "---",
        f"title: {source.upper()} report import {today}",
        "type: performance-report",
        f"source_file: {csv_dest.name}",
        f"imported: {today}",
        f"rows: {len(data)}",
        f"note: {args.note}",
        "---",
        "",
        f"# {source.upper()} performance report — imported {today}",
        "",
        f"Full data: [{csv_dest.name}]({csv_dest.name}) ({len(data)} rows). "
        f"Top {len(top)} rows by **{metric or 'file order'}**:",
        "",
        "| " + " | ".join(headers) + " |",
        "|" + "---|" * len(headers),
    ]
    for r in top:
        cells = (r + [""] * len(headers))[: len(headers)]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    lines += [
        "",
        "## Agent analysis checklist",
        "- Compare against the previous import of the same source (trend, not snapshot).",
        "- Attribute wins/losses to specific posts/pins; check their `offers` frontmatter.",
        f"- Write findings to kb/learned/ citing `{md_dest.name}` with sample sizes.",
        "",
    ]
    md_dest.write_text("\n".join(lines), encoding="utf-8")
    print(f"Imported {len(data)} rows -> {md_dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
