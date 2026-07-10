#!/usr/bin/env python3
"""Generate video voiceover audio from a script file using edge-tts (free).

Extracts narration from a video package markdown file (quoted paragraphs after
[SECTION] headings, skipping [SCREEN] directions) or reads a plain text file,
then synthesizes an mp3 per section plus a combined track.

Usage:
  python tools/make_voiceover.py ops/content/youtube/video-01-package.md
  python tools/make_voiceover.py narration.txt --voice en-US-AndrewNeural

Voices: en-US-AndrewNeural (default, natural male), en-US-AvaNeural (female),
en-GB-RyanNeural. List all: edge-tts --list-voices

Requires: pip install edge-tts
"""
import argparse
import asyncio
import re
import sys
from pathlib import Path

import edge_tts

SECTION_RE = re.compile(r"^\*\*\[(?P<name>[^\]]+)\]\*\*", re.M)
QUOTE_RE = re.compile(r'^"(.*)"$', re.DOTALL)


def extract_narration(md_text: str):
    """Return [(section, narration)] from a video package markdown."""
    sections = []
    parts = SECTION_RE.split(md_text)
    # parts: [pre, name1, body1, name2, body2, ...]
    for name, body in zip(parts[1::2], parts[2::2]):
        lines = []
        for para in body.strip().split("\n"):
            para = para.strip()
            if not para or para.startswith("[SCREEN"):
                continue
            m = QUOTE_RE.match(para)
            if m:
                lines.append(m.group(1))
        if lines:
            clean = " ".join(lines)
            if "[VERIFY" in clean:
                print(f"  WARN {name}: contains unfilled [VERIFY] slots — synthesizing anyway", file=sys.stderr)
            sections.append((name.split("—")[0].strip().replace(":", ""), clean))
    return sections


async def synth(text: str, voice: str, out: Path):
    await edge_tts.Communicate(text, voice, rate="+4%").save(str(out))
    print(f"  wrote {out}")


async def run(args):
    src = Path(args.script)
    text = src.read_text(encoding="utf-8")
    out_dir = Path(args.out_dir or f"ops/content/youtube/audio/{src.stem}")
    out_dir.mkdir(parents=True, exist_ok=True)

    if src.suffix == ".md":
        sections = extract_narration(text)
        if not sections:
            print("No narration found (expected quoted lines under **[SECTION]** headings)", file=sys.stderr)
            return 1
    else:
        sections = [("full", text)]

    for i, (name, narration) in enumerate(sections, 1):
        safe = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        await synth(narration, args.voice, out_dir / f"{i:02d}-{safe}.mp3")

    combined = " ... ".join(n for _, n in sections)
    await synth(combined, args.voice, out_dir / "combined.mp3")
    print(f"Done: {len(sections)} sections -> {out_dir}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="video package .md or plain .txt")
    ap.add_argument("--voice", default="en-US-AndrewNeural")
    ap.add_argument("--out-dir")
    args = ap.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
