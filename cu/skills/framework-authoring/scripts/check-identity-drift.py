#!/usr/bin/env python3
"""Guard against RAHAN identity drift in COPPER metadata.

COPPER is the harness/framework name. RAHAN is ONLY the distribution name
(the two-axis identity: COPPER core vs RAHAN distribution). RAHAN must never
appear as an authoring, decider, maintainer, or IRI identity , that is drift.

This lint flags RAHAN ONLY in identity-metadata contexts where it is wrong,
NOT in legitimate distribution-name prose. It exists because the drift recurred
(story author fields, then codebook IRIs) and a human grep is not a durable guard.

Exits non-zero if any identity-drift line is found.

Usage:
    python3 check-identity-drift.py [ROOT_DIR]
    ROOT_DIR defaults to the repository root.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKIP_DIRS = {
    "node_modules",
    ".git",
    ".serena",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".obsidian",
}

# Identity-metadata field patterns where RAHAN is a DEFECT (case-insensitive).
# The value begins with RAHAN (optionally quoted); a trailing descriptor like
# "RAHAN (IT PM agent)" still counts as drift.
IDENTITY_PATTERNS = [
    re.compile(r"^\s*author:\s*['\"]?rahan\b", re.IGNORECASE),
    re.compile(r"^\s*maintained_by:\s*['\"]?rahan\b", re.IGNORECASE),
    re.compile(r"^\s*epic_owner:\s*['\"]?rahan\b", re.IGNORECASE),
    re.compile(r"deciders:\s*\[[^\]]*['\"]rahan['\"]", re.IGNORECASE),
    re.compile(r"reviewers:\s*\[[^\]]*\brahan\b", re.IGNORECASE),
]

# IRI authority: rahan.dev (or any rahan-based namespace host). Handled separately
# so a URL quoted in backticks inside PROSE (e.g. a note documenting that the drift
# was corrected) is NOT flagged , only a live, unbacktick'd declaration is drift.
IRI_PATTERN = re.compile(r"https?://[a-z0-9.-]*rahan[a-z0-9.-]*/", re.IGNORECASE)

# Legitimate distribution-name contexts , RAHAN here is CORRECT, never flagged.
# A line matching any of these is exempt even if it also hits a pattern above.
ALLOW_CONTEXTS = [
    re.compile(r"rahan distribution", re.IGNORECASE),
    re.compile(r"rahan vault", re.IGNORECASE),
    re.compile(r"rahan-industrialisation", re.IGNORECASE),
    re.compile(r"rahan lives as a kit", re.IGNORECASE),
    re.compile(r"the rahan distribution", re.IGNORECASE),
    # Documented deliberate exception (ADR-046): the schema $id domain
    # rahan.regdata.ch is kept as-is until a COPPER domain exists. Recorded, not drift.
    re.compile(r"rahan\.regdata\.ch", re.IGNORECASE),
]


def _is_drift(line: str) -> bool:
    if not re.search(r"rahan", line, re.IGNORECASE):
        return False
    if any(ctx.search(line) for ctx in ALLOW_CONTEXTS):
        return False
    if any(pat.search(line) for pat in IDENTITY_PATTERNS):
        return True
    # An IRI is drift only when it is a LIVE declaration, not a backtick-quoted
    # mention in prose (e.g. a note recording that the drift was corrected).
    m = IRI_PATTERN.search(line)
    if m and not _in_backticks(line, m.start()):
        return True
    return False


def _in_backticks(line: str, pos: int) -> bool:
    """True if the char at pos sits inside an inline `code span`."""
    return line.count("`", 0, pos) % 2 == 1


def scan(root: Path) -> list[tuple[Path, int, str]]:
    hits: list[tuple[Path, int, str]] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix not in {
            ".md",
            ".ttl",
            ".py",
            ".yaml",
            ".yml",
        }:
            continue
        # Never scan this guard or its test (both legitimately contain the
        # drift-shaped patterns/fixtures they exist to describe).
        if path.name in {"check-identity-drift.py", "test_check_identity_drift.py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if _is_drift(line):
                hits.append((path, n, line.strip()))
    return hits


def _find_repo_root() -> Path:
    """Walk up from this file to the repo root (the dir holding .git).

    Robust to WHICH copy runs: the kits/core source and the deployed .opencode/
    and .claude/ copies sit at different depths, so a fixed parents[N] is wrong
    for at least one of them. Fail loud if no marker is found rather than
    silently scanning the wrong tree.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists() or (parent / ".gitlab-ci.yml").exists():
            return parent
    print(
        "ERROR: cannot find repository root (.git) from this script.", file=sys.stderr
    )
    raise SystemExit(2)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else _find_repo_root()
    hits = scan(root)
    if hits:
        print(
            "RAHAN identity drift found (RAHAN is the distribution name, never an",
            file=sys.stderr,
        )
        print(
            "authoring/decider/maintainer/IRI identity , use COPPER/QUAD):",
            file=sys.stderr,
        )
        for path, n, line in hits:
            rel = path.relative_to(root) if path.is_relative_to(root) else path
            print(f"  {rel}:{n}: {line}", file=sys.stderr)
        return 1
    print("PASS: no RAHAN identity drift.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
