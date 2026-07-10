#!/usr/bin/env python3
"""Autonomous task runner core — executes one task from ops/tasks/ headlessly.

Flow: git pull -> requeue due recurring tasks -> claim oldest todo (race-safe
via push) -> run the agent harness on the task -> enforce guardrails ->
validate (KB schema + compliance lint) -> one self-fix retry on failure ->
commit results as drafts, mark done/blocked -> append ops/agent-activity.md.

Entry points:
  local  (Windows Task Scheduler): tools/run_agent_task.ps1 -> this, --runner local
  cloud  (GitHub Actions):         .github/workflows/agent-task.yml -> this, --runner cloud

Agent command is a template; {prompt} is replaced by the full prompt argv:
  local default: fcc-claude -p {prompt} --dangerously-skip-permissions
  cloud default: gemini --yolo -p {prompt}
Override with --agent-cmd for testing (e.g. a stub script).
"""
import argparse
import datetime as dt
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
TASKS_DIR = REPO / "ops" / "tasks"
LOGS_DIR = TASKS_DIR / "logs"
ACTIVITY = REPO / "ops" / "agent-activity.md"
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RECURRING_DAYS = {"weekly": 7, "monthly": 30}

GUARDRAILS = """You are the Amarketer autonomous agent running headless in this repository.
First read CLAUDE.md and kb/INDEX.md and obey all operating rules there.
HARD LIMITS (non-negotiable):
- Any content you create or edit must have frontmatter `status: draft`. NEVER set status to approved or published anywhere.
- NEVER edit site/public/_redirects. NEVER delete or deprecate KB entries.
- NEVER state a commission rate, cookie window, or offer term that is not in a KB entry with status verified and unexpired valid_until.
- No signups, no spending, no publishing, no external posting. Prepare; the owner executes.
- Do NOT run git commit or git push; the runner handles all git operations.
When finished, ensure `python tools/validate_kb.py` and `python tools/check_content.py` would pass.

YOUR TASK:
"""


def sh(*args, check=True, capture=False, cwd=REPO, timeout=None):
    return subprocess.run(list(args), check=check, cwd=str(cwd), timeout=timeout,
                          capture_output=capture, text=True, encoding="utf-8", errors="replace")


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def parse_task(path: Path):
    # utf-8-sig: tolerate BOM from Windows editors
    text = path.read_text(encoding="utf-8-sig")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, None
    fm = yaml.safe_load(m.group(1))
    return (fm, text[m.end():]) if isinstance(fm, dict) else (None, None)


def write_task(path: Path, fm: dict, body: str):
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{front}\n---\n{body}", encoding="utf-8")


def log_activity(runner, task_name, outcome, detail=""):
    stamp = now_utc().strftime("%Y-%m-%d %H:%M UTC")
    line = f"- {stamp} · {runner} · {task_name} · **{outcome}**{' · ' + detail if detail else ''}\n"
    ACTIVITY.parent.mkdir(parents=True, exist_ok=True)
    with open(ACTIVITY, "a", encoding="utf-8") as f:
        f.write(line)


def requeue_recurring():
    for path in sorted(TASKS_DIR.glob("*.md")):
        fm, body = parse_task(path)
        if not fm or fm.get("recurring") in (None, "none"):
            continue
        days = RECURRING_DAYS.get(fm.get("recurring"))
        if not days or fm.get("status") != "done":
            continue
        last = fm.get("last_run")
        try:
            last_dt = dt.datetime.fromisoformat(str(last)).replace(tzinfo=dt.timezone.utc)
        except (TypeError, ValueError):
            last_dt = None
        if last_dt is None or (now_utc() - last_dt).days >= days:
            fm["status"] = "todo"
            fm.pop("claimed_by", None)
            write_task(path, fm, body)


def pick_task(runner):
    candidates = []
    for path in sorted(TASKS_DIR.glob("*.md")):
        fm, body = parse_task(path)
        if not fm or fm.get("status") != "todo":
            continue
        if fm.get("runner", "any") not in ("any", runner):
            continue
        prio = {"high": 0, "normal": 1, "low": 2}.get(fm.get("priority", "normal"), 1)
        candidates.append((prio, str(fm.get("created", "9999")), path, fm, body))
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[0], c[1], c[2].name))
    return candidates[0][2:]


def claim(path: Path, fm: dict, body: str, runner: str) -> bool:
    fm["status"] = "in-progress"
    fm["claimed_by"] = runner
    write_task(path, fm, body)
    sh("git", "add", str(path))
    sh("git", "commit", "-m", f"agent: claim task {path.stem} ({runner})", capture=True)
    pushed = sh("git", "push", check=False, capture=True)
    if pushed.returncode != 0:
        # lost the race — undo local claim and resync
        sh("git", "reset", "--hard", "HEAD~1", capture=True)
        sh("git", "pull", "--rebase", check=False, capture=True)
        return False
    return True


def split_cmd(template: str):
    # posix=False on Windows so backslash paths survive; then strip quoting
    if os.name == "nt":
        parts = shlex.split(template, posix=False)
        return [p[1:-1] if len(p) > 1 and p[0] == p[-1] and p[0] in "\"'" else p
                for p in parts]
    return shlex.split(template)


def run_agent(cmd_template: str, prompt: str, timeout: int):
    argv = [prompt if a == "{prompt}" else a for a in split_cmd(cmd_template)]
    return sh(*argv, check=False, capture=True, timeout=timeout)


def enforce_guardrails():
    """Revert forbidden changes the agent may have made."""
    notes = []
    changed = sh("git", "diff", "--name-only", capture=True).stdout.split()
    if "site/public/_redirects" in changed:
        sh("git", "checkout", "--", "site/public/_redirects")
        notes.append("reverted _redirects edit")
    for rel in changed:
        if rel.startswith("site/src/content/posts/") and rel.endswith(".md"):
            p = REPO / rel
            text = p.read_text(encoding="utf-8")
            if re.search(r"^status:\s*(published|approved)\s*$", text, re.M):
                prev = sh("git", "show", f"HEAD:{rel}", check=False, capture=True)
                prev_published = prev.returncode == 0 and re.search(
                    r"^status:\s*published\s*$", prev.stdout, re.M)
                if not prev_published:
                    p.write_text(re.sub(r"^status:\s*(published|approved)\s*$",
                                        "status: draft", text, flags=re.M), encoding="utf-8")
                    notes.append(f"demoted {rel} to draft")
    # new (untracked) posts must also be drafts
    untracked = sh("git", "ls-files", "--others", "--exclude-standard", capture=True).stdout.split()
    for rel in untracked:
        if rel.startswith("site/src/content/posts/") and rel.endswith(".md"):
            p = REPO / rel
            text = p.read_text(encoding="utf-8")
            if re.search(r"^status:\s*(published|approved)\s*$", text, re.M):
                p.write_text(re.sub(r"^status:\s*(published|approved)\s*$",
                                    "status: draft", text, flags=re.M), encoding="utf-8")
                notes.append(f"demoted new {rel} to draft")
    return notes


def validate():
    out = []
    ok = True
    for tool in ("validate_kb.py", "check_content.py"):
        r = sh(sys.executable, str(REPO / "tools" / tool), check=False, capture=True)
        out.append(f"$ {tool}\n{r.stdout}{r.stderr}")
        ok = ok and r.returncode == 0
    return ok, "\n".join(out)


def finalize(path, fm, body, status, runner, detail=""):
    fm["status"] = status
    if fm.get("recurring") not in (None, "none"):
        fm["last_run"] = now_utc().strftime("%Y-%m-%dT%H:%M")
    write_task(path, fm, body)
    log_activity(runner, path.stem, status, detail)
    sh("git", "add", "-A")
    sh("git", "commit", "-m", f"agent task {status}: {fm.get('title', path.stem)} [{runner}]", capture=True)
    push = sh("git", "push", check=False, capture=True)
    if push.returncode != 0:
        sh("git", "pull", "--rebase", check=False, capture=True)
        sh("git", "push", check=False, capture=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runner", choices=["local", "cloud"], default="local")
    ap.add_argument("--agent-cmd", default=None,
                    help='command template with {prompt}; defaults per runner')
    ap.add_argument("--timeout", type=int, default=3600)
    args = ap.parse_args()

    cmd_template = args.agent_cmd or (
        "fcc-claude -p {prompt} --dangerously-skip-permissions" if args.runner == "local"
        else "gemini --yolo -p {prompt}")

    sh("git", "pull", "--rebase", check=False, capture=True)
    requeue_recurring()
    picked = pick_task(args.runner)
    if not picked:
        print("no todo tasks — exiting")
        return 0
    path, fm, body = picked
    print(f"claiming: {path.name}")
    if not claim(path, fm, body, args.runner):
        print("lost claim race — exiting")
        return 0

    prompt = GUARDRAILS + f"# {fm.get('title', path.stem)}\n\n{body.strip()}"
    result = run_agent(cmd_template, prompt, args.timeout)
    guard_notes = enforce_guardrails()
    ok, report = validate()

    if not ok:
        print("validation failed — self-fix retry")
        fix_prompt = (GUARDRAILS + "Your previous changes failed validation. "
                      "Fix ONLY these errors, changing as little as possible:\n\n" + report)
        run_agent(cmd_template, fix_prompt, args.timeout)
        guard_notes += enforce_guardrails()
        ok, report = validate()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"{path.stem}-{now_utc().strftime('%Y%m%d-%H%M')}.log"
    log_file.write_text(
        f"agent stdout/stderr:\n{result.stdout}\n{result.stderr}\n\nvalidation:\n{report}\n"
        f"\nguardrail actions: {guard_notes or 'none'}\n", encoding="utf-8")

    detail = "; ".join(guard_notes) if guard_notes else ""
    if ok:
        finalize(path, fm, body, "done", args.runner, detail)
        print("task done")
        return 0
    finalize(path, fm, body, "blocked", args.runner,
             f"validation failed — see ops/tasks/logs/{log_file.name}. {detail}")
    print("task blocked — validation failed after retry")
    return 1


if __name__ == "__main__":
    sys.exit(main())
