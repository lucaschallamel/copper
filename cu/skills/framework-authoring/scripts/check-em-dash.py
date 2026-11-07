#!/usr/bin/env python3
"""Check for em-dash (U+2014) and en-dash (U+2013) in markdown files.

Exits non-zero if any dashes are found outside fenced code blocks
in files not matched by the ignore list.

Usage:
    python3 check-em-dash.py [ROOT_DIR]

    ROOT_DIR defaults to the repository root (parent of .gitlab-ci.yml).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

EM_DASH = "\u2014"
EN_DASH = "\u2013"

# Directories and paths to skip entirely
SKIP_DIRS = {
    "node_modules",
    ".git",
    ".serena",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".claude",  # Git-ignored generated artifact (compiled via deploy.regenerate)
}


# Local-only "intake" dirs (git-ignored source material, never shipped) are skipped
# by suffix so the rule stays org-agnostic (no org name baked into core tooling).


def _find_repo_root() -> Path:
    """Walk up from this file to the repo root (the dir holding .git).

    Robust to WHICH copy runs: the `kits/core` source and the deployed `.opencode/`
    and `.claude/` copies sit at different depths, so a fixed `parents[N]` is wrong
    for at least one of them. Fail loud if no marker is found rather than silently
    scanning the wrong tree , a gate that resolves to an empty tree and reports PASS
    is worse than one that errors (measured: `check-count-drift.py` printed "All
    counts match on-disk reality: {'agents': 0, ...}" and exited 0).

    Shared implementation (US-352 S6 follow-up); the original is in
    `check-identity-drift.py`, which documented the hazard without it being applied
    to its siblings.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists() or (parent / ".gitlab-ci.yml").exists():
            return parent
    print(
        "ERROR: cannot find repository root (.git) from this script.", file=sys.stderr
    )
    raise SystemExit(2)


def _is_intake_dir(part: str) -> bool:
    return part == "_intake" or part.endswith("-intake")


# Glob patterns for files exempted from the check
# TD-178 AC8: these are TEMPLATES, resolved against the discovered documentation
# root at runtime. Hardcoding `docs-copper/` here made the guard fail INVERTED on a
# `docs/` project: nothing matched, so it FLAGGED the very historical records the
# exemptions exist to protect , and its remediation ("replace em-dash with hyphens")
# would have corrupted dated records. Rooting the SCAN alone does not fix that; the
# pattern list must be rooted too.
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
# Any of these marks a candidate as the documentation root.
DOCS_ROOT_MARKERS = ("dev-journal", "roadmap", "memory-bank")


def resolve_docs_root_name(root: Path) -> str:
    """Return the NAME of the documentation directory (e.g. 'docs-copper'/'docs').

    A name, not a path, because EXEMPT_TEMPLATES are matched against repo-relative
    strings. Falls back to the historical default so this repository is untouched.
    """
    override = os.environ.get(DOCS_ROOT_ENV)
    if override:
        # TD-178 S4 G5: this consumer computes REPO-RELATIVE strings from the scan
        # (`path.relative_to(root)`), so a documentation root OUTSIDE the project is
        # structurally unsupportable , not merely awkward. An earlier fix returned
        # the override as an absolute string, which made the walk leave `root` and
        # raise ValueError (measured), and returning a bare BASENAME silently
        # resolved to a directory that does not exist. Both are worse than refusing.
        # Fail closed with the reason, consistent with this guard's contract.
        candidate = Path(override)
        if not candidate.is_absolute():
            candidate = root / candidate
        try:
            return str(candidate.resolve().relative_to(root.resolve()))
        except ValueError:
            print(
                f"ERROR: {DOCS_ROOT_ENV}={override} is outside {root} , this guard "
                "computes repo-relative paths and cannot scan an external tree. "
                "Point it at a directory INSIDE the project.",
                file=sys.stderr,
            )
            raise SystemExit(2) from None
    for name in DOCS_ROOT_CANDIDATES:
        candidate = root / name
        if candidate.is_dir() and any(
            (candidate / m).is_dir() for m in DOCS_ROOT_MARKERS
        ):
            return name
    return DOCS_ROOT_CANDIDATES[0]


EXEMPT_TEMPLATES = [
    "{docs}/roadmap/analysis/*",  # Audit reports (historical)
    "{docs}/roadmap/pipeline-audit-trail/artifacts/*",  # Pipeline artifacts
    "{docs}/roadmap/backlog/*",  # Backlog stories (historical)
    "{docs}/dev-journal/*",  # Dev journals (historical records)
    ".opencode/skills/language-formatting/*",  # the skill that documents the dash rule
    "kits/core/skills/language-formatting/*",  # US-183: migrated core copy
    "_benchmark/*",  # TD-162: gitignored third-party clones, not COPPER source
    "build/plugins/*",  # US-368: gitignored plugin build output, generated from kits/
]


def exempt_patterns(docs: str) -> list[str]:
    """EXEMPT_TEMPLATES with the discovered documentation root substituted in."""
    return [p.format(docs=docs) for p in EXEMPT_TEMPLATES]


def is_exempt(relative_path: str, patterns: list[str]) -> bool:
    """Check if a file path matches any exemption pattern."""
    from fnmatch import fnmatch

    return any(fnmatch(relative_path, pattern) for pattern in patterns)


def strip_code_blocks(text: str) -> str:
    """Blank out fenced code blocks (``` ... ```), keeping their newlines so the
    line numbers reported after a fence stay true (TD-201)."""
    return re.sub(
        r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL
    )


def check_file(
    filepath: Path, root: Path, patterns: list[str]
) -> list[tuple[int, str, str]]:
    """Return list of (line_number, dash_type, line_content) for violations."""
    relative = str(filepath.relative_to(root))
    if is_exempt(relative, patterns):
        return []

    text = filepath.read_text(encoding="utf-8")
    # Strip fenced code blocks before checking
    clean = strip_code_blocks(text)

    violations: list[tuple[int, str, str]] = []
    for i, line in enumerate(clean.split("\n"), start=1):
        if EM_DASH in line:
            violations.append((i, "em-dash (U+2014)", line.strip()))
        if EN_DASH in line:
            violations.append((i, "en-dash (U+2013)", line.strip()))
    return violations


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else _find_repo_root()
    root = root.resolve()

    if not (root / ".gitlab-ci.yml").exists() and not (root / ".git").exists():
        print(f"ERROR: Cannot find repository root from {root}", file=sys.stderr)
        return 2

    docs = resolve_docs_root_name(root)
    patterns = exempt_patterns(docs)

    all_violations: list[tuple[str, int, str, str]] = []
    md_files = sorted(root.rglob("*.md"))

    for filepath in md_files:
        # Skip blacklisted directories
        parts = filepath.relative_to(root).parts
        if any(p in SKIP_DIRS or _is_intake_dir(p) for p in parts):
            continue

        violations = check_file(filepath, root, patterns)
        for line_no, dash_type, content in violations:
            rel = str(filepath.relative_to(root))
            all_violations.append((rel, line_no, dash_type, content))

    if all_violations:
        print(f"FAIL: Found {len(all_violations)} dash violation(s) in living docs:")
        print()
        for rel, line_no, dash_type, content in all_violations:
            print(f"  {rel}:{line_no}  [{dash_type}]")
            print(f"    {content[:120]}")
            print()
        print(
            "Remediation: Replace em-dash (\\u2014) and en-dash"
            " (\\u2013) with hyphens (-)."
        )
        print("Exempt paths:", ", ".join(patterns))
        return 1

    print("PASS: No em-dash or en-dash violations found in living docs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
