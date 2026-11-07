#!/usr/bin/env python3
"""check-adr-index , ADR index-integrity guard (TD-159).

Diffs each ADR's frontmatter `status:` against its row in the `adr/README.md`
index table and fails (exit 1) on any drift. Follows the US-178
`check-white-label-core.py` / TD-158 `check-portability.py` "guard not a grep"
model: a structured checker with `file:line` reporting and a non-zero exit.

Checks (status-only by design , the index table records Status, not Version;
ADR frontmatter is the single source of truth and the index FOLLOWS it,
so duplicating version into the index would create a second drift surface):

  A. Status mismatch , an ADR file's frontmatter `status:` differs from its
     index-row Status cell.
  B. Missing row , an ADR-NNN file exists but has no row in the index table.
  C. Orphan row , an index row points at an ADR-NNN that has no file.
  D. Diagram drift (TD-161) , the newest ADR on disk must appear as an
     EXPLICIT `ADR-NNN` node/token in the "Recommended Sequencing" mermaid
     block. A subgraph-title range/enumeration spanning the newest number is
     NOT enough (that is the "widened the title, forgot the node" drift this
     guard exists to catch, S5 R1). Older ADRs may still be covered by ranges,
     so the clustered style stays legal , only the newest needs a real node.
     If the section or its mermaid block is absent the hard check SKIPS (the
     guard polices drift of an existing diagram, it does not mandate one); a
     NON-FATAL warning then flags the absence so a deleted diagram is visible
     in CI, not silent.

Plus one NON-FATAL warning (TD-161): the "Related Backlog Streams" section
lagging the newest `EP-NNN` in the backlog prints a WARNING to stderr but
never changes the exit code.

A gap in the numbering (e.g. ADR-022 reserved for an unwritten story) with
NO file AND NO row is NOT a violation , it is an intentional reservation.

Scope: the committed ADR estate at `docs-copper/architecture/adr/`. The guard
resolves the repo root by walking up, so it runs from the source tree or any
generated copy. Exit 0 = consistent.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# TD-178: the documentation root is discovered. This script ALREADY layered
# explicit-argument -> _default_root() -> find_repo_root() validation; it simply
# assumed the directory was named `docs-copper`. Now it tries `docs/` too.
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
_ADR_SUBPATH = "architecture/adr"


def _docs_root(start: Path) -> Path:
    """The documentation ROOT as a path (TD-178 S4 G4).

    An earlier version returned `Path(override).name` , the BARE BASENAME , so an
    override pointing OUTSIDE the project silently resolved to `start/<basename>`,
    which does not exist. Measured: `COPPER_DOCS_ROOT=/tmp/x/mydocs` made this guard
    print "cannot find mydocs/architecture/adr". The override is AC1's EXPLICIT
    layer , the thing a user reaches for when discovery fails , so breaking it broke
    the one contract that is supposed to always work.
    """
    override = os.environ.get(DOCS_ROOT_ENV)
    if override:
        candidate = Path(override)
        return candidate if candidate.is_absolute() else start / candidate
    for name in DOCS_ROOT_CANDIDATES:
        if (start / name / _ADR_SUBPATH).is_dir():
            return start / name
    return start / DOCS_ROOT_CANDIDATES[0]


ADR_DIR_REL = f"{DOCS_ROOT_CANDIDATES[0]}/{_ADR_SUBPATH}"
INDEX_REL = f"{ADR_DIR_REL}/README.md"
BACKLOG_DIR_REL = f"{DOCS_ROOT_CANDIDATES[0]}/roadmap/backlog"

# An ADR file: ADR-NNN-slug.md (NNN = 3+ digits). README.md is not an ADR.
_ADR_FILE_RE = re.compile(r"^ADR-(\d{3,})-.+\.md$")
# A frontmatter status line.
_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
# An index table row: | `ADR-NNN` | Title | Status |
_INDEX_ROW_RE = re.compile(
    r"^\|\s*`ADR-(\d{3,})`\s*\|[^|]*\|\s*([A-Za-z]+)\s*\|", re.MULTILINE
)

# --- TD-161: sequencing-diagram coverage + backlog-stream freshness ---------
_SEQ_HEADER_RE = re.compile(r"^##\s+Recommended Sequencing\s*$", re.MULTILINE)
_STREAMS_HEADER_RE = re.compile(r"^##\s+Related Backlog Streams\s*$", re.MULTILINE)
_MERMAID_BLOCK_RE = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
_ADR_TOKEN_RE = re.compile(r"ADR-(\d{3,})")
_SUBGRAPH_TITLE_RE = re.compile(r"^\s*subgraph\s+\S+\[(.+?)\]\s*$", re.MULTILINE)
# A prefix-qualified reference (EP-112, TD-101, ADR-030): stripped from a
# subgraph title BEFORE bare/range ADR extraction so an epic or story number
# can never be mistaken for an ADR (that would be a false-coverage hole in the
# very drift guard this check exists to be). Bare ADR items in titles are
# unqualified (`023, 039`), so stripping qualified tokens removes only noise.
_PREFIX_TOKEN_RE = re.compile(r"[A-Za-z]+-\d+")
# Bare/range ADR numbers: {3,6} covers ADR-100..999999 (well past parity with
# _ADR_FILE_RE) while capping width so a pathological title range cannot expand
# into an astronomically large set or trip Python's int-string-conversion limit.
_RANGE_RE = re.compile(r"\b(\d{3,6})-(\d{3,6})\b")
_BARE_NUM_RE = re.compile(r"\b(\d{3,6})\b")
# Streams entries are backtick-fenced list items (`- `EP-NNN`: ...`). Matching
# only the fenced form means a stray EP mention in PROSE cannot inflate the
# referenced max and silently suppress the freshness warning (S5 Info#5).
_EPIC_TOKEN_RE = re.compile(r"`EP-(\d+)`")
_EPIC_FILE_RE = re.compile(r"^EP-(\d+)")


def _frontmatter(text: str) -> str:
    """Return the YAML frontmatter block (between the first two '---'), or ''."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def adr_status(path: Path) -> str | None:
    m = _STATUS_RE.search(_frontmatter(path.read_text(encoding="utf-8")))
    return m.group(1) if m else None


def _bind_docs_root(name: str) -> None:
    """Rebind the path constants UNCONDITIONALLY (TD-178 S4 F2).

    An earlier version rebound only on success, so a failed resolve left the
    constants at whatever a PRIOR call had set , and they are read at 17 sites,
    including the "cannot find {ADR_DIR_REL}" failure message itself, which would
    then name a directory from an unrelated project. Harmless for the one-shot CLI,
    wrong for any in-process caller (a test importing this module twice sees the
    contamination). Rebinding every time makes the state a pure function of the
    argument.
    """
    global ADR_DIR_REL, INDEX_REL, BACKLOG_DIR_REL
    ADR_DIR_REL = f"{name}/{_ADR_SUBPATH}"
    INDEX_REL = f"{ADR_DIR_REL}/README.md"
    BACKLOG_DIR_REL = f"{name}/roadmap/backlog"


def find_repo_root(start: Path) -> Path | None:
    """TD-178: try each candidate documentation root, not just `docs-copper/`."""
    docs = _docs_root(start)
    try:
        name = str(docs.relative_to(start))
    except ValueError:
        name = str(docs)  # an override outside the project: keep it absolute
    _bind_docs_root(name)
    return start if (docs / _ADR_SUBPATH).is_dir() else None


def _default_root() -> Path:
    """Walk up from this script to the repo root , robust whether the script
    runs from the kits/core source OR a generated .opencode/.claude copy."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (
            any((parent / n / _ADR_SUBPATH).is_dir() for n in DOCS_ROOT_CANDIDATES)
            or (parent / ".git").exists()
        ):
            return parent
    return here.parents[-1]


def collect_adr_files(adr_dir: Path) -> dict[str, tuple[str, str | None]]:
    """Map ADR number -> (filename, frontmatter status) for every ADR-NNN file."""
    files: dict[str, tuple[str, str | None]] = {}
    for p in sorted(adr_dir.glob("ADR-*.md")):
        m = _ADR_FILE_RE.match(p.name)
        if m:
            files[m.group(1)] = (p.name, adr_status(p))
    return files


def collect_index_rows(index_path: Path) -> dict[str, str]:
    """Map ADR number -> Status cell for every index table row."""
    text = index_path.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in _INDEX_ROW_RE.finditer(text)}


def check_index(root: Path) -> list[str]:
    files = collect_adr_files(root / ADR_DIR_REL)
    rows = collect_index_rows(root / INDEX_REL)
    violations: list[str] = []

    # A + B: every ADR file must have a matching index row with the same status
    for num, (fname, fstatus) in files.items():
        if num not in rows:
            violations.append(
                f"{fname}: ADR-{num} missing from index table (B: missing row)"
            )
        elif fstatus is None:
            violations.append(f"{ADR_DIR_REL}/{fname}: no frontmatter status: field")
        elif rows[num] != fstatus:
            violations.append(
                f"{INDEX_REL}: ADR-{num} index '{rows[num]}' != frontmatter "
                f"'{fstatus}' (A: status mismatch)"
            )

    # C: every index row must point at an existing ADR file
    for num in rows:
        if num not in files:
            violations.append(
                f"{INDEX_REL}: ADR-{num} index row has no ADR file (C: orphan row)"
            )

    return violations


def _section(text: str, header_re: re.Pattern[str]) -> str | None:
    """Return the README section from `header_re` to the next `## ` header."""
    m = header_re.search(text)
    if not m:
        return None
    nxt = text.find("\n## ", m.end())
    return text[m.end() : nxt if nxt != -1 else len(text)]


def _mermaid_coverage(block: str) -> set[int]:
    """ADR numbers loosely covered by the diagram: explicit ADR-NNN tokens
    anywhere, plus NNN-MMM ranges (expanded) and bare NNN items in subgraph
    titles. Prefix-qualified tokens (EP-/TD-/ADR-) are stripped from each title
    first so an epic/story number in a title (e.g. `EP-112 memory 044`) never
    leaks into ADR coverage , ADR-NNN tokens are collected from the block.
    Used to diagnose OLDER-ADR coverage; the newest ADR is held to the stricter
    explicit-node rule in `check_diagram_coverage`."""
    covered = {int(n) for n in _ADR_TOKEN_RE.findall(block)}
    for title in _SUBGRAPH_TITLE_RE.findall(block):
        bare_title = _PREFIX_TOKEN_RE.sub("", title)
        for lo, hi in _RANGE_RE.findall(bare_title):
            covered.update(range(int(lo), int(hi) + 1))
        covered.update(int(n) for n in _BARE_NUM_RE.findall(bare_title))
    return covered


def _diagram_block(root: Path) -> str | None:
    """The 'Recommended Sequencing' mermaid block body, or None if the section
    or its mermaid fence is absent."""
    section = _section((root / INDEX_REL).read_text(encoding="utf-8"), _SEQ_HEADER_RE)
    if section is None:
        return None
    m = _MERMAID_BLOCK_RE.search(section)
    return m.group(1) if m else None


def check_diagram_coverage(root: Path) -> list[str]:
    """D (TD-161): the newest ADR on disk must appear as an EXPLICIT `ADR-NNN`
    node/token in the sequencing diagram. A subgraph-title range/enumeration
    that merely spans the newest number does NOT count , that is exactly the
    'widened the title, forgot the node' drift this guard exists to catch
    (S5 R1). Older ADRs may still be covered by ranges (clustered style stays
    legal, AC2). Absent section/block = skip (drift guard, not a diagram
    mandate; a non-fatal `check_diagram_present` warning flags the absence)."""
    files = collect_adr_files(root / ADR_DIR_REL)
    if not files:
        return []
    block = _diagram_block(root)
    if block is None:
        return []
    newest = max(int(n) for n in files)
    node_adrs = {int(n) for n in _ADR_TOKEN_RE.findall(block)}
    if newest in node_adrs:
        return []
    if newest in _mermaid_coverage(block):
        return [
            f"{INDEX_REL}: the newest ADR (ADR-{newest:03d}) appears only via a "
            f"subgraph-title range/enumeration, not an explicit ADR-{newest:03d} "
            f"node in the 'Recommended Sequencing' diagram (D: diagram drift) "
            f", add it as a node so the newest ADR is actually placed"
        ]
    return [
        f"{INDEX_REL}: 'Recommended Sequencing' diagram does not cover the "
        f"newest ADR (ADR-{newest:03d}) (D: diagram drift) , add ADR-{newest:03d} "
        f"as a node in the mermaid block"
    ]


def check_diagram_present(root: Path) -> list[str]:
    """TD-161 NON-FATAL (S5 R3): warn when ADRs exist but the sequencing-diagram
    section/mermaid block is absent , otherwise deleting the diagram makes the
    hard coverage check silently skip. Warning, not a failure: the guard does
    not MANDATE a diagram, but its disappearance should be visible in CI."""
    if not collect_adr_files(root / ADR_DIR_REL):
        return []
    if _diagram_block(root) is not None:
        return []
    return [
        f"WARNING: {INDEX_REL}: no 'Recommended Sequencing' mermaid block found "
        f"but ADRs exist , diagram drift detection is skipped (non-fatal; "
        f"restore the diagram to re-enable it)"
    ]


def check_streams_freshness(root: Path) -> list[str]:
    """TD-161 NON-FATAL: warn when 'Related Backlog Streams' lags the newest
    EP-NNN in the backlog. Only backtick-fenced `EP-NNN` list tokens count as
    references, so a stray EP mention in prose cannot suppress the warning
    (S5 Info#5). Absent dir/section/references = silent skip."""
    backlog = root / BACKLOG_DIR_REL
    if not backlog.is_dir():
        return []
    epics = [
        int(m.group(1))
        for p in backlog.glob("EP-*.md")
        if (m := _EPIC_FILE_RE.match(p.name))
    ]
    if not epics:
        return []
    section = _section(
        (root / INDEX_REL).read_text(encoding="utf-8"), _STREAMS_HEADER_RE
    )
    if section is None:
        return []
    referenced = [int(n) for n in _EPIC_TOKEN_RE.findall(section)]
    if not referenced or max(epics) <= max(referenced):
        return []
    return [
        f"WARNING: {INDEX_REL}: 'Related Backlog Streams' stops at "
        f"EP-{max(referenced)} but the backlog reaches EP-{max(epics)} , "
        f"consider refreshing the list (non-fatal)"
    ]


def main(argv: list[str]) -> int:
    start = Path(argv[1]).resolve() if len(argv) > 1 else _default_root()
    root = find_repo_root(start)
    if root is None:
        print(f"adr-index: cannot find {ADR_DIR_REL} from {start}", file=sys.stderr)
        return 1

    violations = check_index(root) + check_diagram_coverage(root)
    for w in check_diagram_present(root) + check_streams_freshness(root):
        print(w, file=sys.stderr)
    if violations:
        print(f"adr-index: {len(violations)} violation(s):")
        for v in violations:
            print(f"  - {v}")
        print(
            "\nRemediation: ADR frontmatter `status:` is the source of truth; "
            "update the adr/README.md index row(s) to match, fix the orphan "
            "row, or bring the 'Recommended Sequencing' diagram up to date."
        )
        return 1

    print(
        "PASS: ADR index consistent (status == index rows; no missing/orphan; "
        "sequencing diagram covers the newest ADR)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
