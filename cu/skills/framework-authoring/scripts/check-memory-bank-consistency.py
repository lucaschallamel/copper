#!/usr/bin/env python3
"""Check the memory-bank's current-state counts + dates for drift.

Part of framework-authoring's self-contained quality suite (ships with the harness).
Guards only the CURRENT-state figures, not historical narrative:
  - the explicit "**Framework counts**:" line must match the actual repo
  - every memory-bank file must carry a well-formed "**Last Updated**: YYYY-MM-DD"

Historical snapshots in Prior Work / Recent Changes / Session N blocks are records
of what was true then and are NOT checked. Rule 03's Phase 3 consistency check,
automated.

Usage:
    python3 check-memory-bank-consistency.py [ROOT_DIR]

Exit codes:
    0 - consistent
    1 - count drift or missing/malformed date
    2 - usage error
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path

# The documentation root is DISCOVERED, not assumed (TD-178). Copied from the
# `check-adr-index.py` precedent, which already layered explicit-argument ->
# walk-and-discover -> validate-the-subtree. Deliberately DUPLICATED rather than
# imported: core scripts have no import seam, and the one script that builds one
# (`telemetry_cli.py`, via `sys.path.insert`) is deployed to NEITHER host, so an
# import would rest on an untested foundation (TD-178 S2, C4).
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
# The subtree this guard needs. A candidate must CONTAIN it, not merely exist.
EXPECTED_SUBTREE = "memory-bank"


def resolve_docs_root(root: Path) -> Path | None:
    """Return the directory holding EXPECTED_SUBTREE, or None if there is none.

    Three layers: COPPER_DOCS_ROOT wins; else the first of docs-copper/ or docs/
    that CONTAINS the expected subtree (containment, not mere existence); else
    None, and the caller reports SKIP and exits 2. NEVER a silent pass.
    """
    override = os.environ.get(DOCS_ROOT_ENV)
    if override:
        candidate = Path(override)
        if not candidate.is_absolute():
            candidate = root / candidate
        return candidate if (candidate / EXPECTED_SUBTREE).is_dir() else None
    for name in DOCS_ROOT_CANDIDATES:
        candidate = root / name
        if (candidate / EXPECTED_SUBTREE).is_dir():
            return candidate
    return None


COUNT_FILES = ["activeContext.md", "systemPatterns.md"]
DATE_FILES = [
    "activeContext.md",
    "progress.md",
    "systemPatterns.md",
    "techContext.md",
    "productContext.md",
    "projectbrief.md",
]
# The counts text runs to the next blank line: Prettier wraps the paragraph, so the
# numbers are often on the lines after the label (TD-201 A12).
COUNT_LINE_RE = re.compile(
    r"(?ims)^[-*\s]*\*\*Framework counts\*\*[ \t]*:?(.*?)(?:\n[ \t]*\n|\Z)"
)
CATEGORIES = ("agents", "skills", "commands")
DATE_RE = re.compile(r"\*\*Last Updated\*\*\s*:?\s*(\d{4}-\d{2}-\d{2})")


def _count_on_disk(root: Path) -> dict[str, int]:
    """Reuse count_on_disk from the sibling count-drift script (single source)."""
    script = Path(__file__).resolve().parent / "check-count-drift.py"
    spec = importlib.util.spec_from_file_location("_count_drift", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.count_on_disk(root)


def check(root: Path, mb: Path) -> list[str]:
    disk = _count_on_disk(root)
    failures: list[str] = []
    found = False
    for name in COUNT_FILES:
        path = mb / name
        if not path.is_file():
            continue
        m = COUNT_LINE_RE.search(path.read_text(encoding="utf-8"))
        if not m:
            continue
        found = True
        line = m.group(1)
        missing = []
        for category in CATEGORIES:
            cm = re.search(rf"(\d+)\s+{category}\b", line)
            if not cm:
                missing.append(category)
            elif int(cm.group(1)) != disk[category]:
                failures.append(
                    f"{name}: 'Framework counts' says {cm.group(1)} {category}, "
                    f"repo has {disk[category]}"
                )
        if missing:
            # An unnamed category is an unchecked one (TD-201 S7).
            failures.append(
                f"{name}: 'Framework counts' names no count of {', '.join(missing)}"
            )
    if not found:
        where = " or ".join(COUNT_FILES)
        if (root / "kits" / "core").is_dir():
            # The framework repository documents its counts: no line compares
            # nothing (TD-201 A12).
            failures.append(
                f"no '**Framework counts**' line in {where}: nothing to compare"
            )
        else:
            # An adopter's bank need not carry one; say what was not checked.
            print(
                f"NOTE: counts not checked , no '**Framework counts**' line in {where}."
            )
    for name in DATE_FILES:
        path = mb / name
        if not path.is_file():
            failures.append(f"{name}: missing")
            continue
        if not DATE_RE.search(path.read_text(encoding="utf-8")[:600]):
            failures.append(f"{name}: no well-formed '**Last Updated**' date header")
    return failures


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    docs_root = resolve_docs_root(root)
    if docs_root is None:
        looked = ", ".join(
            str(root / c / EXPECTED_SUBTREE) for c in DOCS_ROOT_CANDIDATES
        )
        print(
            f"SKIP: no '{EXPECTED_SUBTREE}' directory found , NOTHING CHECKED "
            "(fail closed).",
            file=sys.stderr,
        )
        print(f"  Looked for: {looked}", file=sys.stderr)
        print(
            f"  Point it elsewhere with {DOCS_ROOT_ENV}=<dir> or pass a ROOT_DIR "
            "argument.",
            file=sys.stderr,
        )
        return 2
    mb = docs_root / EXPECTED_SUBTREE
    failures = check(root, mb)
    if failures:
        print(f"FAIL: memory-bank consistency ({len(failures)} issue(s)):")
        for f in failures:
            print(f"  - {f}")
        print("")
        print("Remediation: fix the Framework counts line + Last Updated dates.")
        return 1
    print(f"PASS: memory-bank current-state counts + dates are consistent in {mb}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
