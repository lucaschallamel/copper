"""SessionStart guard: the safety minimum and the installed-rules check (US-370).

Shipped as `scripts/rules_guard.py` beside `rules_install.py` in every plugin with
rules, run by `bin/<plugin>-rules hook` from the plugin's `hooks/hooks.json`. It
compares `.claude/rules/<plugin>/` with the plugin's own `rules/` (ADR-053 D8): the
project record only tells stale from modified and never makes a difference OK (AC2).
It never fails a session start: every error still prints the minimum, exit 0 (AC4).
Names from the project are counted, never echoed into context (AC7, RQ16). Like
Claude Code, it looks in the launch folder and every parent: the nearest install is
compared, and any further copy is reported, since Claude loads every one.
"""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

MINIMUM = "scripts/safety-minimum.md"
CHECK = "scripts/deploy_check.py"
MINIMUM_INTRO = "Always-on safety minimum, whether or not any rules are installed:"
ORDER = ("missing", "modified", "stale", "unreadable")
# The record is project content: its version is echoed only when it is plain numbers.
PLAIN_VERSION = re.compile(r"^\d+(\.\d+){0,3}$")


def _minimum(plugin_root: Path) -> str:
    try:
        return (plugin_root / MINIMUM).read_text(encoding="utf-8").strip()
    except (OSError, ValueError):
        return ""


def _state(ri, path: Path, want: bytes, recorded, record_version, version):
    """None when equal to the plugin's bytes, else the state's name."""
    if path.is_symlink():
        return "modified"
    try:
        info = path.stat()
        # shortcut: stat then read, so a live local process could swap in a FIFO
        # between them and stall the hook; that process already owns the project.
        if not stat.S_ISREG(info.st_mode):  # a FIFO would block the read (S4 #2)
            return "unreadable"
        if info.st_size > 4 * len(want) + 65536:  # never read a huge file whole
            return "modified"
        data = path.read_bytes()
    except OSError:
        return "unreadable"
    if data == want:
        return None
    if recorded == ri.digest(data) and record_version not in (None, version):
        return "stale"
    return "modified"


def _rule_files(dest: Path) -> tuple[set, int]:
    """Top-level *.md names, and the count of *.md in subfolders, which Claude Code
    loads too (measured, S4); symlinked folders are not followed."""
    top = {p.name for p in dest.iterdir() if p.name.endswith(".md")}
    nested = sum(
        1
        for here, _, files in os.walk(dest)
        if Path(here) != dest
        for f in files
        if f.endswith(".md")
    )
    return top, nested


def _installs(ri, root: Path, name: str, home: str | None) -> list:
    """Every install Claude would load, nearest first, with its rule files (None
    when unreadable): the launch folder and each parent (measured, S4), then the
    home, whose ~/.claude/rules/ every project loads (2.1.318 loader, US-372 S6)."""
    folders = [root, *root.parents]
    if home and Path(home).resolve() not in folders:
        folders.append(Path(home).resolve())
    found = []
    for folder in folders:
        project = ri.Project(folder, name)
        try:
            if not project.dest.is_dir():
                continue
            files = _rule_files(project.dest)
        except OSError:
            files = None
        if files is None or files[0] or files[1]:
            found.append((project, files))
    return found


def _compare(ri, project, files, shipped: dict, version: str):
    """The states with the plugin file names they concern, the extra count, the
    record's version and whether the record is unreadable."""
    if files is None:
        return {"unreadable": [f"{project.rel}/"]}, 0, None, False
    present, nested = files
    try:
        record, bad_record = project.read(), False
    except ri.RulesError:
        record, bad_record = None, True  # every difference is then "modified"
    owned = record["owned"] if record else {}
    rec_version = record["version"] if record else None
    states = {"missing": sorted(set(shipped) - set(present))}
    for name in sorted(set(shipped) & set(present)):
        path = project.dest / name
        state = _state(ri, path, shipped[name], owned.get(name), rec_version, version)
        if state:
            states.setdefault(state, []).append(name)
    extra = len(set(present) - set(shipped)) + nested
    return states, extra, rec_version, bad_record


def _status(plugin_root: Path, env: dict) -> tuple[str, str]:
    """One context line and the user notice ('' when OK)."""
    ri = _installer()
    unverifiable = "rules unverifiable, not checked"
    try:
        name, version = ri.plugin_identity(plugin_root)
        shipped = ri.source_rules(plugin_root)
    except ri.RulesError as exc:  # names plugin files only, never project text
        return f"{unverifiable}: {exc}", f"{unverifiable}: {exc}"
    except OSError as exc:
        why = f"{unverifiable}: plugin files unreadable ({type(exc).__name__})"
        return why, why
    try:
        root = ri.project_root(env)
        installs = _installs(ri, root, name, env.get("HOME"))
        if installs:
            installs[0][0].guard()  # a symlink on the way: report, never follow
    except ri.RulesError as exc:  # fixed paths and the root only
        return f"{name} rules not checked: {exc}", f"{name} rules not checked: {exc}"
    fix = f"run /{name}:rules install"
    if not installs:
        rel = f".claude/rules/{name}"
        line = f"{name} rules: not installed in {root} ({rel}/ has no rule files)"
        return f"{line}. To install, {fix}.", f"{name} rules not installed here: {fix}"
    project, files = installs[0]
    states, extra, rec_version, bad_record = _compare(
        ri, project, files, shipped, version
    )
    others = [str(p.dest) for p, _ in installs[1:]]
    if not (extra or bad_record or others or any(states.values())):
        files = "file" if len(shipped) == 1 else "files"
        return (
            f"{name} rules: installed and identical to the plugin's rules ({name} "
            f"{version}, {len(shipped)} {files}) in {project.dest}. This checks what "
            "is installed, not what Claude loaded.",
            "",
        )
    found = (states, extra, rec_version, bad_record, others)
    return _problems(ri, name, version, project, found)


def _problems(ri, name: str, version: str, project, found) -> tuple[str, str]:
    """Word a difference: the context line and the notice, with advice per cause."""
    states, extra, rec_version, bad_record, others = found
    fix = f"run /{name}:rules install"
    shown = (
        rec_version
        if PLAIN_VERSION.fullmatch(rec_version or "")
        else "an earlier version"
    )
    label = {"stale": f"stale (installed from {shown})"}
    parts = [
        f"{label.get(s, s)}: {', '.join(states[s])}" for s in ORDER if states.get(s)
    ]
    summary = [s for s in ORDER if states.get(s)]
    advice = []
    if any(states.values()):
        backup = " (add --backup to keep your edits)" if states.get("modified") else ""
        advice.append(fix + backup)
    if bad_record:
        record = f"{ri.STATE_DIR}/{name}{ri.RECORD_SUFFIX}"
        parts.append("the install record is unreadable")
        summary.append("unreadable record")
        advice.append(f"delete {record}, then {fix}")
    if extra:  # install keeps the user's own files, so it cannot clear these
        files = "file" if extra == 1 else "files"
        parts.append(f"{extra} extra rule {files} not shipped by the plugin")
        summary.append(f"{extra} extra {files}")
        advice.append(f"move files that are not the plugin's out of {project.rel}/")
    if others:
        parts.append(f"also installed in {', '.join(others)} (Claude loads every copy)")
        summary.append(f"installed in {len(others) + 1} places")
        advice.append(
            f"keep one copy: /{name}:rules uninstall in the others, then delete any "
            "edited file it keeps"
        )
    return (
        f"{name} rules in {project.dest} ({name} {version}): {'; '.join(parts)}. "
        f"To fix: {'; '.join(advice)}.",
        f"{name} rules: {', '.join(summary)}: {'; '.join(advice)}",
    )


def _installer():
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import rules_install

    return rules_install


def _leftover(plugin_root: Path, env: dict) -> tuple[str, str] | None:
    """Core only: a deploy beside the plugins (US-372 AC3, `deploy_check.py`)."""
    ri = _installer()
    if not (plugin_root / CHECK).is_file():
        return None  # shipped with core's plugin only
    import deploy_check

    return deploy_check.leftover(ri.project_root(env), env)


def _pre_push(plugin_root: Path, env: dict) -> str | None:
    """Core only (TD-206 AC10); no project path or name reaches the context (RQ16)."""
    tools = plugin_root / "tools"
    if not (tools / "guard_install.py").is_file():
        return None  # shipped with core's plugin only
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))
    import guard_install

    root = str(_installer().project_root(env))

    def git(*args: str) -> str | None:
        done = subprocess.run(
            ["git", "-C", root, *args], capture_output=True, text=True, timeout=5
        )
        return done.stdout.strip() if done.returncode == 0 else None

    hook = git("rev-parse", "--git-path", "hooks/pre-push")
    if hook is None:
        return None  # not a git repository
    path, want, head = Path(root, hook), guard_install.HOOK.encode(), b""
    if path.is_file():  # a regular file only, never a FIFO; read no more than the hook
        with path.open("rb") as f:
            head = f.read(len(want) + 1)
    if head == want:
        return "pre-push guard: installed in this repository (/cu:guard status)."
    if guard_install.MARKER.encode() in head:
        return "pre-push guard: installed, changed since install (/cu:guard status)."
    if guard_install.delegated(path):
        return "pre-push guard: installed through your own hook (/cu:guard status)."
    if git("config", "--get", "core.hooksPath") or path.exists():
        return "pre-push guard: not installed; a hook exists (/cu:guard status)."
    return "pre-push guard: not installed here; /cu:guard install adds it."


def check_output(plugin_root: Path, env: dict) -> dict:
    """The hook JSON: the minimum first (cu only), then the status line (AC1, AC5)."""
    try:
        line, notice = _status(plugin_root, env)
    except Exception as exc:  # never block a session (AC4); class name only (RQ16)
        line = f"rules not checked: guard error {type(exc).__name__}"
        notice = line
    try:
        extra = _leftover(plugin_root, env)
    except Exception:  # the deploy check never costs the rules check (AC4)
        extra = None
    if extra:
        line, notice = (
            f"{line}\n\n{extra[0]}",
            "; ".join(filter(None, [notice, extra[1]])),
        )
    try:
        guard = _pre_push(plugin_root, env)
    except Exception:  # the pre-push status never costs the rules check (AC4)
        guard = None
    if guard:
        line = f"{line}\n\n{guard}"  # context only: no notice every session
    minimum = _minimum(plugin_root)
    lines = [MINIMUM_INTRO, minimum, line] if minimum else [line]
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n\n".join(lines),
        }
    }
    if notice:
        out["systemMessage"] = notice
    return out


def main() -> int:
    plugin_root = Path(__file__).resolve().parents[1]
    try:
        text = json.dumps(check_output(plugin_root, dict(os.environ)))
    except Exception:  # last resort: plain stdout still reaches Claude (S3 Phase 1)
        text = _minimum(plugin_root) + "\n\nrules not checked: guard error"
    sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
