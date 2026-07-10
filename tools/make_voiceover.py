#!/usr/bin/env python3
"""Generate video voiceover audio from a script file using edge-tts (free).

Extracts narration from a video package markdown file (quoted paragraphs after
[SECTION] headings, skipping [SCREEN] directions) or reads a plain text file,
then synthesizes an mp3 per section plus a combined track.

Usage:
  python tools/make_voiceover.py ops/content/youtube/video-01-package.md
  python tools/make_voiceover.py narration.txt --voice en-US-AndrewNeural
  python tools/make_voiceover.py narration.txt --engine pocket   # fully offline
  python tools/make_voiceover.py narration.txt --engine pocket --clone my-voice.wav

Engines:
  edge   (default) Microsoft neural voices via edge-tts — best quality, needs
         internet. Voices: en-US-AndrewNeural (default), en-US-AvaNeural,
         en-GB-RyanNeural. List: edge-tts --list-voices
  pocket Kyutai pocket-tts — 100M-param model, runs offline on CPU (MIT).
         Supports voice cloning via --clone <audio-file> for a consistent
         channel voice we own. Outputs .wav.

Requires: pip install edge-tts pocket-tts
"""
import argparse
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

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


async def synth(text: str, args, out: Path):
    if args.engine == "pocket":
        exe = shutil.which("pocket-tts")
        if not exe:
            print("pocket-tts not found: pip install pocket-tts", file=sys.stderr)
            raise SystemExit(1)
        out = out.with_suffix(".wav")
        cmd = [exe, "generate", "-q", "--text", text, "--output-path", str(out)]
        if args.clone:
            cmd += ["--voice", args.clone]
        subprocess.run(cmd, check=True)
    else:
        import edge_tts
        await edge_tts.Communicate(text, args.voice, rate="+4%").save(str(out))
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
        await synth(narration, args, out_dir / f"{i:02d}-{safe}.mp3")

    combined = " ... ".join(n for _, n in sections)
    await synth(combined, args, out_dir / "combined.mp3")
    print(f"Done: {len(sections)} sections -> {out_dir}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="video package .md or plain .txt")
    ap.add_argument("--engine", choices=["edge", "pocket"], default="edge")
    ap.add_argument("--voice", default="en-US-AndrewNeural", help="edge engine voice name")
    ap.add_argument("--clone", help="pocket engine: audio file of the voice to clone")
    ap.add_argument("--out-dir")
    args = ap.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
