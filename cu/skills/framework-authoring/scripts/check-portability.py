#!/usr/bin/env python3
"""Check shipped kits/core/ assets for portability violations (TD-158).

Enforces the "ship agnostic & stateless" invariant: shipped assets must carry
no machine-specific state, no Claude load-time side effects, and no reliance on
a host-specific interpreter name. Three checks (scope: kits/core/ source only):

  A. Hardcoded home paths   - /Users/<name>, /home/<name>, C:\\Users\\<name>
                              (generic placeholders like XXX / <user> are allowed)
  B. Claude load-time block - a !`...` command-expansion directive in any body
                              loaded as Claude context: commands/*.md, agents/*.md,
                              and skills/**/SKILL.md (executes at load time;
                              BUG-002 widened this from commands-only)
  C. Bare `python`          - `python `/`python -m ` that assumes a PATH
                              interpreter. Allowed: `python3`, `uv run python`,
                              `uv run pytest`, explicit paths (.venv/bin/python),
                              and substrings (python3, python_requires, prose).

Exits non-zero on any violation. Models check-white-label-core.py (US-178).

Usage:
    python3 check-portability.py [ROOT_DIR]

    ROOT_DIR defaults to the repository root (resolved upward from this file).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# This file holds the forbidden patterns as regex literals, so it must not scan
# itself (mirrors check-white-label-core.py's self-exemption).
SELF_EXEMPT = {"check-portability.py"}

# Files that DOCUMENT the portability policy legitimately quote the forbidden
# forms as examples; exempt them (mirrors check-em-dash exempting the
# language-formatting skill that documents the dash rule). Keyed by core-rel path.
DOC_EXEMPT = {"skills/framework-authoring/SKILL.md"}

SKIP_DIRS = {
    "node_modules",
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}

SCAN_SUFFIXES = {".md", ".py", ".sh"}

# --- Check A: hardcoded home paths -----------------------------------------
# Capture the first path segment after the home root; allow generic placeholders.
_PATH_RE = re.compile(r"(?:/Users/|/home/|C:\\Users\\)([A-Za-z0-9_.$<>~-]+)")
_PATH_ALLOW = {
    "xxx",
    "user",
    "username",
    "name",
    "home",
    "<user>",
    "<name>",
    "$home",
    "...",  # prose ellipsis placeholder, e.g. "(/Users/...)"
}

# --- Check B: Claude load-time command-expansion directive --------------------
# A `!`...`` directive executes at command-load time wherever it appears in the
# body (not just line-leading), so it is detected anywhere after removing
# double-backtick spans (which markdown uses to DISPLAY `!`...`` as literal text).
_DOUBLE_CODE_RE = re.compile(r"``.+?``")


def _has_loadtime_directive(line: str) -> bool:
    return "!`" in _DOUBLE_CODE_RE.sub("", line)


def _is_loadtime_body(rel: str) -> bool:
    """True for markdown bodies the host loads as Claude context, where a
    `!`...`` directive fires at load time: command bodies, agent bodies, and
    skill SKILL.md bodies. Resource files (skills/*/resources/*) are not loaded
    eagerly, so they are out of scope (BUG-002 AC5)."""
    if not rel.endswith(".md"):
        return False
    return (
        rel.startswith("commands/")
        or rel.startswith("agents/")
        or (rel.startswith("skills/") and rel.endswith("/SKILL.md"))
    )


# --- Check C: bare python invocation ---------------------------------------
# `python ` as a whole token, NOT preceded by a word char or '/' (so python3,
# python_requires and .venv/bin/python are excluded) and NOT 'uv run python',
# followed by an invocation-like token (-m, or a token containing '/' or '.py').
# Trade-off (accepted): requiring an invocation-like token means an extension-less
# `python myscript` is not flagged, but it avoids false-positives on prose
# ("a python utility"). The fixture test in tests/unit pins both directions.
_BARE_PY_RE = re.compile(r"(?<![\w/])(?<!run )python (?:-m\b|\S*(?:/|\.py))")


def _strip_fenced(lines: list[str]) -> list[str]:
    """Blank out fenced code blocks (``` ... ```), preserving line numbers."""
    out, in_fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def _frontmatter_end(lines: list[str]) -> int:
    """Index of the line after a leading YAML frontmatter block, else 0."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0


def check_asset(path: Path, rel: str) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    violations: list[str] = []

    # A + C scan every line (bare-python invocations live inside fenced blocks
    # and .py docstrings, so fenced code is NOT stripped for these).
    for i, line in enumerate(lines, start=1):
        for m in _PATH_RE.finditer(line):
            if m.group(1).lower() not in _PATH_ALLOW:
                violations.append(f"{rel}:{i} hardcoded home path: {line.strip()[:90]}")
        if _BARE_PY_RE.search(line):
            violations.append(
                f"{rel}:{i} bare `python` (use python3 / uv run): {line.strip()[:90]}"
            )

    # B applies to every body loaded into Claude context , command, agent, and
    # skill SKILL.md bodies all execute a load-time `!`...`` directive at load
    # time (BUG-002: an unguarded SKILL.md directive crashed the agile-coach
    # launch). Scanned outside frontmatter + fenced code; DOC_EXEMPT files that
    # legitimately quote the pattern are skipped by the caller.
    if _is_loadtime_body(rel):
        body = _strip_fenced(lines)
        start = _frontmatter_end(lines)
        for i in range(start, len(body)):
            if _has_loadtime_directive(body[i]):
                violations.append(
                    f"{rel}:{i + 1} load-time !`...` directive: {lines[i].strip()[:70]}"
                )
    return violations


def find_core_root(root: Path) -> Path | None:
    if (root / "kits" / "core").is_dir():
        return root / "kits" / "core"
    if root.name == "core" and root.parent.name == "kits":
        return root
    return None


def _default_root() -> Path:
    """Walk up from this script to the repo root , robust whether the script
    runs from the kits/core source OR a generated .opencode/.claude copy."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "kits" / "core").is_dir() or (parent / ".git").exists():
            return parent
    return here.parents[-1]


def main(argv: list[str]) -> int:
    start = Path(argv[1]).resolve() if len(argv) > 1 else _default_root()
    core = find_core_root(start)
    if core is None:
        print(f"portability: cannot find kits/core from {start}", file=sys.stderr)
        return 1

    violations: list[str] = []
    for path in sorted(core.rglob("*")):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        if any(p in SKIP_DIRS for p in path.parts) or path.name in SELF_EXEMPT:
            continue
        rel = str(path.relative_to(core))
        if rel in DOC_EXEMPT:
            continue
        violations.extend(check_asset(path, rel))

    if violations:
        print(f"portability: {len(violations)} violation(s) under {core}:")
        for v in violations:
            print(f"  - {v}")
        print(
            "\nRemediation: python3 (user-facing) or `uv run python`/`uv run pytest`"
            " (internal); no load-time !`...` blocks; no hardcoded home paths."
        )
        return 1

    print("portability: clean (kits/core scanned, agnostic & stateless).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
