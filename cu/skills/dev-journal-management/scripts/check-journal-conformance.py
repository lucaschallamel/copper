#!/usr/bin/env python3
"""Check dev-journal entries conform to the template structure (forward-only).

Part of the dev-journal-management skill's self-contained quality suite: it ships
with the skill and travels to every deployed harness, so a harness can verify its
OWN new journals conform to the template.

Forward-only by design: only entries dated on/after CUTOFF are checked. Historical
entries (pre-cutoff) are records of what was true when written and are NOT
retroactively conformed.

Usage:
    python3 check-journal-conformance.py [ROOT_DIR] [--cutoff YYYY-MM-DD]

Exit codes (THREE states, fail closed , TD-178):
    0 - all in-scope journals conform (and the scanned directory is named)
    1 - one or more non-conforming journals
    2 - usage error, OR the documentation root could not be resolved , NOTHING
        CHECKED. A guard that reports PASS without looking is worse than one that
        errors: it hands back a clean bill of health for a scan of nothing.
"""

from __future__ import annotations

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
EXPECTED_SUBTREE = "dev-journal"


def resolve_docs_root(root: Path) -> Path | None:
    """Return the directory holding EXPECTED_SUBTREE, or None if there is none.

    Three layers, in order:
      1. ``COPPER_DOCS_ROOT`` if set , explicit always wins.
      2. The first of ``docs-copper/`` or ``docs/`` that actually CONTAINS the
         expected subtree. Containment, not mere existence, so a project holding
         both directories resolves to the one with the content.
      3. ``None`` , the caller reports SKIP and exits 2. NEVER a silent pass.
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


# Entries from this date forward are held to the template structure. Set to the
# date the prescribed structure was adopted (TD-157). Pre-cutoff = historical.
CUTOFF = "2026-06-07"

REQUIRED_FRONTMATTER = {
    "entry_date",
    "author",
    "focus_area",
    "status",
    "tags",
    "version",
    "last_updated",
    "maintained_by",
}
# Top-level sections every new entry must carry (the prescribed structure).
REQUIRED_SECTIONS = {
    "Why (High-Level Context)",
    "How (The Journey)",
    "Final State & Next Steps",
}
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

# Line-anchored frontmatter delimiter: a leading `---`, the YAML block, then a
# closing `---` on its own line. NOT a content-blind `text.split("---")`, which
# truncates the frontmatter at a `---` INSIDE a value (e.g. a focus_area that
# describes a "---in-value" fix) and reports present keys as missing. Mirrors the
# shared reader in deploy/kit/validate.py + deploy/targets/base.py (US-266 S4).
# CRLF-tolerant (`\r?\n`); accepts a closing `---` at EOF with no trailing newline.
_FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)


def _split_frontmatter(text: str) -> tuple[str, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end() :]


def _headings(body: str) -> set[str]:
    out = set()
    for line in body.splitlines():
        m = re.match(r"^#{2,3}\s+(.*?)\s*$", line)
        if m:
            out.add(re.sub(r"\s*\(Optional\)\s*$", "", m.group(1)).strip())
    return out


def _entry_date(name: str, fm_text: str) -> str | None:
    m = _DATE_RE.search(name)
    if m:
        return m.group(0)
    m = re.search(r"entry_date:\s*'?(\d{4}-\d{2}-\d{2})", fm_text)
    return m.group(1) if m else None


def check(root: Path, cutoff: str, journal_dir: Path) -> list[str]:
    failures: list[str] = []
    for path in sorted(journal_dir.rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm_text, body = _split_frontmatter(text)
        date = _entry_date(path.name, fm_text)
        if date is None or date < cutoff:
            continue  # forward-only: skip undated + historical entries
        # frontmatter fields (cheap text check, avoids a yaml dependency)
        missing_fm = {
            f for f in REQUIRED_FRONTMATTER if not re.search(rf"(?m)^{f}:", fm_text)
        }
        if missing_fm:
            failures.append(f"{path.name}: missing frontmatter {sorted(missing_fm)}")
        # sections
        missing_sec = REQUIRED_SECTIONS - _headings(body)
        if missing_sec:
            failures.append(f"{path.name}: missing sections {sorted(missing_sec)}")
    return failures


def main(argv: list[str]) -> int:
    root = Path(".")
    cutoff = CUTOFF
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--cutoff" and i + 1 < len(args):
            cutoff = args[i + 1]
            i += 2
        else:
            root = Path(args[i])
            i += 1
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
    journal_dir = docs_root / EXPECTED_SUBTREE
    failures = check(root, cutoff, journal_dir)
    if failures:
        print(f"FAIL: dev-journal conformance ({len(failures)} issue(s), >= {cutoff}):")
        for f in failures:
            print(f"  - {f}")
        print("")
        print("Remediation: use the dev-journal-template.md structure.")
        return 1
    print(
        f"PASS: all dev-journal entries (>= {cutoff}) in {journal_dir} conform "
        "to the template."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
