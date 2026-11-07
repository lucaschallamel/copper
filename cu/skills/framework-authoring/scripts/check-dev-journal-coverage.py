#!/usr/bin/env python3
"""Verify every Done story has a matching dev-journal entry.

Usage:
    python3 check-dev-journal-coverage.py [ROOT_DIR]

Exit codes:
    0 - All Done stories have journal coverage
    1 - Coverage gaps found
    2 - Usage error
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# The documentation root is DISCOVERED, not assumed (TD-178). Copied from the
# `check-adr-index.py` precedent (explicit argument -> walk-and-discover ->
# validate-the-subtree). Deliberately DUPLICATED rather than imported: core scripts
# have no import seam, and the one script that builds one (`telemetry_cli.py`, via
# `sys.path.insert`) is deployed to NEITHER host, so an import would rest on an
# untested foundation (TD-178 S2, C4).
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
EXPECTED_SUBTREE = "dev-journal"


def resolve_docs_root(root: Path) -> Path | None:
    """Return the directory holding EXPECTED_SUBTREE, or None if there is none.

    COPPER_DOCS_ROOT wins; else the first of docs-copper/ or docs/ that CONTAINS
    the expected subtree (containment, not mere existence); else None, and the
    caller reports SKIP and exits 2. NEVER a silent pass.
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


# Story IDs completed before dev-journal convention was established
PRE_CONVENTION_EXEMPTIONS = {
    "CI-101",
    "EP-101",
    "TD-101",
    "TD-102",
    "US-104",
    "US-108",
    "US-144",
}


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


def extract_story_ids_with_status_done(backlog_dir: Path) -> set[str]:
    """Parse backlog frontmatter; return IDs where status is Done."""
    done_ids: set[str] = set()
    for fp in sorted(backlog_dir.glob("*.md")):
        text = fp.read_text(encoding="utf-8")
        # Extract status from frontmatter
        status_match = re.search(r"^status:\s*(\S+)", text, re.MULTILINE)
        id_match = re.search(r"^story_id:\s*(\S+)", text, re.MULTILINE)
        if status_match and id_match:
            status = status_match.group(1).strip()
            story_id = id_match.group(1).strip()
            if status == "Done":
                done_ids.add(story_id.upper())
    return done_ids


def extract_journal_story_ids(journal_dir: Path) -> set[str]:
    """Extract story IDs referenced in dev-journal filenames."""
    found: set[str] = set()
    for fp in sorted(journal_dir.rglob("*.md")):
        if fp.name == "README.md":
            continue
        # Match any of the 8 story-type prefixes in the filename, e.g.
        # US-102, TD-154, EP-101, SP-101, BUG-002, SEC-001, CI-101, RA-001.
        matches = re.findall(r"(?i)(?:US|TD|EP|SP|BUG|SEC|CI|RA)-\d+[a-z]?", fp.stem)
        found.update(m.upper() for m in matches)
    return found


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else _find_repo_root()
    root = root.resolve()

    docs_root = resolve_docs_root(root)
    if docs_root is None:
        looked = ", ".join(
            str(root / c / EXPECTED_SUBTREE) for c in DOCS_ROOT_CANDIDATES
        )
        print(
            f"ERROR: no '{EXPECTED_SUBTREE}' directory found , NOTHING CHECKED "
            f"(fail closed). Looked for: {looked}. "
            f"Override with {DOCS_ROOT_ENV}=<dir>.",
            file=sys.stderr,
        )
        return 2
    backlog_dir = docs_root / "roadmap" / "backlog"
    journal_dir = docs_root / EXPECTED_SUBTREE

    if not backlog_dir.is_dir():
        print(f"ERROR: Backlog directory not found: {backlog_dir}", file=sys.stderr)
        return 2

    if not journal_dir.is_dir():
        print(f"ERROR: Dev-journal directory not found: {journal_dir}", file=sys.stderr)
        return 2

    done_ids = extract_story_ids_with_status_done(backlog_dir)
    journal_ids = extract_journal_story_ids(journal_dir)

    uncovered = sorted((done_ids - journal_ids) - PRE_CONVENTION_EXEMPTIONS)

    if uncovered:
        print(f"FAIL: {len(uncovered)} Done story/stories lack dev-journal coverage:")
        for story_id in uncovered:
            print(f"  - {story_id}")
        print()
        print(f"Done stories: {len(done_ids)}")
        print(f"Journal entries covering: {len(journal_ids)} distinct story IDs")
        print()
        print("Remediation: Create a dev-journal entry referencing the story ID")
        print(
            f"  in {journal_dir}/YYYY/MM/"
            f"YYYY-MM-DD-{uncovered[0].lower()}-description.md"
        )
        return 1

    print(f"PASS: All {len(done_ids)} Done stories have dev-journal coverage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
