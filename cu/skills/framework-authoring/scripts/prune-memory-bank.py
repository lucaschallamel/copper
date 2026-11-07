#!/usr/bin/env python3
"""Roll closed history out of the live memory-bank files into their archives.

US-264. This is the MECHANICAL half of `/memory-update`: the command keeps the
judgement (what is worth writing), this script keeps the invariant (the live head
stays inside its Rule 03a budget, and nothing is ever lost doing so).

Why a script and not more prose (US-264 S2): `memory-update.md` has carried
archive instructions since v2.2.0 and they pointed at `progress.md`, which is
itself budgeted, so following them breached that budget while moving nothing to
either archive. Nobody noticed because prose has no gate. AC4's central safety
claims ("running it twice is a no-op", "never deletes content that is not
already in the archive") are unverifiable against prose , there is nothing to run
twice.

The ordering is the safety property: a block is APPENDED to the archive and
confirmed present there BEFORE it is removed from the live file. A crash between
the two leaves a duplicate, which the next run detects and resolves. The reverse
order would lose history outright.

Usage:
    prune-memory-bank.py <repo-root>              # perform the roll
    prune-memory-bank.py <repo-root> --check      # exit 1 if a roll is needed
    prune-memory-bank.py <repo-root> --dry-run    # report, change nothing

Exit codes: 0 nothing to do / roll completed; 1 roll needed (--check) or over
budget; 2 usage or structural error.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# The documentation root is DISCOVERED, not assumed (TD-178). Copied from
# `check-memory-bank-consistency.py`, the sibling this script was modelled on,
# which in turn took it from `check-adr-index.py`. Deliberately DUPLICATED rather
# than imported, for the reason that sibling records: core scripts have no import
# seam, and the one script that builds one is deployed to NEITHER host.
#
# A2 (S5): this script originally hardcoded `docs-copper` with a bare
# `memory-bank/` fallback, so an adopter whose documentation lives in `docs/` had
# their bank SILENTLY SKIPPED. I had copied the sibling's location and manifest
# treatment but not the thing that makes it portable.
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs", ".")
EXPECTED_SUBTREE = "memory-bank"

# The live files that carry rolling history, and where each one's history goes.
# Keyed to what US-261 and US-262 actually built, not to the shape the command
# prose used to describe.
ROLLING = {
    "activeContext.md": "archive/activeContext-archive.md",
    "progress.md": "archive/progress-archive.md",
    "systemPatterns.md": "archive/systemPatterns-archive.md",
}

# A closed-history block. Anchored on the shape the bank ACTUALLY uses across all
# 30 existing blocks (`## Session 2026-09-27: US-263 , ...`), not the
# `### Session N:` form the command prescribed and nothing ever wrote.
BLOCK_RE = {
    "activeContext.md": re.compile(r"^## Session \d{4}-\d{2}-\d{2}\b", re.M),
    "progress.md": re.compile(r"^## Recent Milestones \(\d{4}-\d{2}-\d{2}\)", re.M),
    # TD-194: a top-level pattern section whose heading ENDS in a parenthetical that
    # carries a story tag: `## A guard ... (TD-181)`, `## X (TD-172, ADR-029 v1.2.0)`.
    # A tag anywhere else in the heading does not make it a pattern (Rule 03a grammar).
    "systemPatterns.md": re.compile(
        r"^## [^\n]*\([^()\n]*\b(?:US|TD|BUG|SEC|SP|EP|CI)-\d+\b[^()\n]*\)[ \t]*$",
        re.M,
    ),
}

# TD-194 S4/C2: a nested `###` pattern travelling with its parent, indexed too.
NESTED_RE = re.compile(
    r"^### ([^\n]*\([^()\n]*\b(?:US|TD|BUG|SEC|SP|EP|CI)-\d+\b[^()\n]*\))[ \t]*$",
    re.M,
)

# TD-194: an ACCUMULATING file. Its tagged sections are not contiguous , Rule 03a
# must-include sections sit BETWEEN them , so a block must end at the next `## ` of
# ANY kind; ending at the next matching heading would swallow the durable sections.
ANY_H2_BOUNDARY = {"systemPatterns.md"}

# TD-194: where a rolled pattern leaves its one-line pointer in the live file. Found
# by its heading LINE (S4/F3), never by a substring a prose mention could match.
INDEX_HEADING = "## Pattern index (archived)"
INDEX_RE = re.compile(r"^## Pattern index \(archived\)[ \t]*$", re.M)
FENCE_RE = re.compile(r"^(```|~~~)")

# Sections that are DURABLE state, never history. Rolling one of these out would
# silently delete live context, so they can never be candidates (US-264 R3).
NEVER_ROLL = (
    "## Next Steps",
    "## Active Decisions",
    "## Blockers",
    "## Known follow-ups",
    "## In Progress",
    # TD-194: Rule 03a must-include sections of systemPatterns.md, and its index.
    "## System Architecture",
    "## Key Technical Decisions",
    "## Design Patterns in Use",
    "## Component Relationships",
    "## Critical Implementation Paths",
    "## Anti-Patterns to Avoid",
    "## Architectural ADRs",
    INDEX_HEADING,
)

# How many history blocks each live head keeps. Rule 03 says "the last 1-2
# sessions" for activeContext.md; progress.md holds a ROLLING MILESTONE HEAD, which
# is a different shape, so one number for both is wrong. Measured at S3: a
# KEEP of 1 on progress.md proposed rolling 24 milestones at once, which is a
# migration, not a session-end prune. The head is sized to the budget instead.
KEEP_BLOCKS = {
    "activeContext.md": 1,
    "progress.md": 8,
    # TD-194: patterns have no session to protect and no reliable order, so every
    # tagged section rolls and only its index line stays live.
    "systemPatterns.md": 0,
}

ARCHIVE_SEPARATOR = "\n---\n\n"


def resolve_docs_root(root: Path) -> Path | None:
    """Return the directory holding `memory-bank/`, or None if there is none.

    Three layers: COPPER_DOCS_ROOT wins; else the first candidate that CONTAINS
    the subtree (containment, not mere existence); else None, and the caller says
    so rather than reporting a pass. `.` is included as a candidate so a bank at
    the repository root still resolves, which is the shape this script's own
    fallback used to handle.
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


def _budgets(root: Path) -> dict[str, int]:
    """Read Rule 03a's budget table , the SINGLE source, never a copy.

    US-264 S2 R5: a second hardcoded table would be a third copy of one contract
    and would drift. The guard's `test_the_guard_table_matches_the_rule_it_enforces`
    parses the same table the same way, so all three agree by construction.

    R5 MATERIALISED AT S3 and this is only half the fix: reading the budget table
    alone made `--check` report `systemPatterns.md` over budget (46,851 > 12,000)
    while the guard reported PASS, because the file carries a RATCHETED EXEMPTION
    at cap 48,000. Two gates on one contract, disagreeing. The exemption is part of
    the same contract, so `_exemptions()` reads it from the same guard module rather
    than hardcoding a third copy.
    """
    # The kit source in this repository; the compiled copy in an adopter's project,
    # where kits/core/ does not exist (US-378 S5: the budgets were unreadable there).
    candidates = [
        root / "kits/core/rules/03a-memory-bank.rules.md",
        root / ".claude/rules/03a-memory-bank.rules.md",
        root / ".opencode/rules/03a-memory-bank.rules.md",
    ]
    rule = next((c for c in candidates if c.is_file()), None)
    if rule is None:
        return {}
    text = rule.read_text(encoding="utf-8")
    try:
        section = text[text.index("## Live-File Token Budget") :]
        section = section[: section.index("## Core Files")]
    except ValueError:
        return {}
    return {
        m.group(1): int(m.group(2).replace(",", ""))
        for m in re.finditer(
            r"\|\s*`([^`]+\.md)`\s*\|[^|]*\|[^|]*\|\s*\*{0,2}([\d,]+)", section
        )
    }


def _exemptions(root: Path) -> dict[str, int]:
    """Ratcheted exemption caps, read from the guard that enforces them.

    US-263 exempted `systemPatterns.md` at its measured value plus tolerance, so a
    budget check that ignores the exemption CONTRADICTS the 18-test guard. Importing
    the guard's table keeps one source of truth; if the guard is absent (an adopter
    without it), no exemption applies and the plain budget governs.
    """
    guard = root / "tests/regression/test_memory_bank_archive_losslessness.py"
    if not guard.is_file():
        return {}
    text = guard.read_text(encoding="utf-8")
    try:
        block = text[text.index("RATCHETED_EXEMPTIONS = {") :]
        block = block[: block.index("}")]
    except ValueError:
        return {}
    return {
        m.group(1): int(m.group(2).replace("_", ""))
        for m in re.finditer(r'"([^"]+\.md)":\s*\(\s*([\d_]+)', block)
    }


def _tokens(text: str) -> int | None:
    """Real token count, or None when no tokeniser is installed.

    US-264 R8: `tiktoken` is optional. A missing tokeniser must SKIP the budget
    check, never fail it, mirroring the guard's `importorskip`.
    """
    try:
        import tiktoken
    except ImportError:
        return None
    return len(tiktoken.get_encoding("cl100k_base").encode(text))


def _split_blocks(
    text: str, pattern: re.Pattern[str], any_h2: bool = False
) -> list[tuple[int, int]]:
    """Return (start, end) spans of history blocks, in document order.

    A block runs from its heading to the next top-level `## ` heading, so a block
    with no intermediate heading is still captured whole , the US-261 S2 lesson,
    where BUG-003's block ran 1090 lines and a boundary keyed on "the last
    heading" would have under-extracted by 41%.
    """
    if any_h2:
        # TD-194 S4/F1: only headings OUTSIDE code fences start or end a block.
        h2 = _h2_starts(text)
        ends = h2[1:] + [len(text)]
        return [(s, e) for s, e in zip(h2, ends) if pattern.match(text, s)]
    starts = [m.start() for m in pattern.finditer(text)]
    if not starts:
        return []
    next_heading = re.compile(r"^## ", re.M)
    spans = []
    for i, start in enumerate(starts):
        if i + 1 < len(starts):
            limit = starts[i + 1]
        else:
            # Last block: run to the next top-level heading (a durable section) or
            # to end of file. Verified: a trailing `## Next Steps` is NOT absorbed.
            nxt = next_heading.search(text, start + 1)
            limit = nxt.start() if nxt else len(text)
        spans.append((start, limit))
    return spans


def _h2_starts(text: str) -> list[int]:
    """Offsets of every `## ` heading line that is not inside a code fence."""
    out, pos, fenced = [], 0, False
    for line in text.splitlines(keepends=True):
        if FENCE_RE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            out.append(pos)
        pos += len(line)
    return out


def _is_durable(block: str) -> bool:
    """A durable heading, matched EXACTLY and case-insensitively (TD-194 S4/F5).

    A trailing parenthetical is ignored, so `## Known follow-ups (grooming)` and a
    tagged `## Design patterns in use (TD-004)` are durable, while a lookalike such as
    `## Key Technical Decisions history (TD-005)` is not.
    """
    head = block.strip().split("\n", 1)[0][3:]
    title = re.sub(r"\s*\([^()]*\)\s*$", "", head).strip().casefold()
    return title in {d[3:].casefold() for d in NEVER_ROLL}


def _candidate_spans(text: str, name: str) -> list[tuple[int, int]]:
    """Rollable block spans of a live file: its blocks minus the durable ones."""
    spans = _split_blocks(text, BLOCK_RE[name], name in ANY_H2_BOUNDARY)
    return [s for s in spans if not _is_durable(text[s[0] : s[1]])]


def _keep_for(text: str, name: str, block_count: int, budget: int | None) -> int:
    """How many blocks to keep , the COUNT, tightened until the file fits its BUDGET.

    `KEEP_BLOCKS` is a count and Rule 03 constrains a SIZE, and the two can
    disagree. Measured: a `progress.md` of 32,147 tokens with EXACTLY 8 blocks was
    COUNT-COMPLIANT and 12,147 over its 20,000 budget, so `_plan` returned nothing
    while `_over_budget` complained , and `--check` exited 1 telling the operator to
    "roll history to the archives", which did NOTHING. **The remedy the gate named
    could not work.** A deadlock is worse than either defect alone.

    So the count is a FLOOR-SEEKING START, not a fixed rule: keep dropping one more
    block while the retained head would still exceed the budget, down to a minimum
    of 1. The newest block is never rolled , a live head with no current session is
    not a saving, it is a loss.
    """
    keep = KEEP_BLOCKS[name]
    if keep == 0:
        return 0  # TD-194: keep nothing, so there is no floor to protect
    if budget is None:
        return keep  # no budget readable (A1): count rule only, and --check says so
    spans = _candidate_spans(text, name)
    while keep > 1:
        retained = text[: spans[keep][0]] if keep < len(spans) else text
        n = _tokens(retained)
        if n is None or n <= budget:
            break
        keep -= 1
    return keep


def _plan(root: Path) -> list[dict]:
    """What would move, without moving it."""
    docs = resolve_docs_root(root)
    if docs is None:
        return []
    mb = docs / EXPECTED_SUBTREE
    actions = []
    for live_name, arch_rel in ROLLING.items():
        live = mb / live_name
        arch = mb / arch_rel
        if not live.is_file() or not arch.is_file():
            continue  # adopter shape differs (R4): skip, never fail
        text = live.read_text(encoding="utf-8")
        spans = _candidate_spans(text, live_name)
        keep = _keep_for(text, live_name, len(spans), _budgets(root).get(live_name))
        if len(spans) <= keep:
            continue
        # Keep the newest `keep` blocks (they appear first, newest-first convention).
        for start, end in spans[keep:]:
            actions.append(
                {
                    "live": live,
                    "archive": arch,
                    "block": text[start:end],
                    "name": live_name,
                }
            )
    return actions


def _roll(action: dict) -> None:
    """Append to the archive, CONFIRM, then remove from the live file.

    The order is the safety property (AC1 lossless, AC4 "never deletes content
    that is not already in the archive"). A crash between append and remove
    leaves a duplicate, which the next run resolves; the reverse order loses the
    block outright.
    """
    block = action["block"]
    arch_text = action["archive"].read_text(encoding="utf-8")

    if block.strip() not in arch_text:
        # F2 (S4): the separator marks the end of the archive's own header, and
        # newest-first means we insert straight after it. An archive without one is
        # an adopter-shaped file, not a corrupt one, so APPEND AT END rather than
        # crashing with a bare `ValueError: substring not found`. Every other
        # function here skips or degrades on an unrecognised shape (`_plan` skips a
        # missing archive, `_budgets` returns {}, `_tokens` returns None); this was
        # the one path that did not.
        sep = arch_text.find(ARCHIVE_SEPARATOR)
        if sep == -1:
            arch_text = arch_text.rstrip("\n") + "\n\n" + block.strip() + "\n"
        else:
            idx = sep + len(ARCHIVE_SEPARATOR)
            arch_text = arch_text[:idx] + block.strip() + "\n\n" + arch_text[idx:]
        _write_atomic(action["archive"], arch_text)

    # CONFIRM before removing. Re-read from disk rather than trusting the write.
    if block.strip() not in action["archive"].read_text(encoding="utf-8"):
        raise RuntimeError(
            f"refusing to prune {action['name']}: the block was not confirmed "
            f"present in {action['archive'].name} after the append. Nothing removed."
        )

    _remove_from_live(action)


def _remove_from_live(action: dict) -> None:
    """Remove a confirmed-archived block from the live file, indexing it if needed.

    Removal and its index line(s) land in ONE write, so neither can exist without
    the other, and the write itself is atomic (TD-194 S4/F7).
    """
    block = action["block"]
    live_text = action["live"].read_text(encoding="utf-8").replace(block, "", 1)
    if action["name"] in ANY_H2_BOUNDARY:
        titles = [_head(action, width=None)[3:]] + NESTED_RE.findall(block)
        live_text = _add_index_lines(live_text, titles)
    _write_atomic(action["live"], live_text)


def _write_atomic(path: Path, text: str) -> None:
    """Write via a sibling temp file and `os.replace`, so a crash never truncates.

    The temp file is created fresh: a link planted at its name is refused, never
    written through (BUG-019). Inline because this script stands alone.
    """
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{os.urandom(4).hex()}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    fd = os.open(tmp, flags, 0o666)  # O_BINARY: one newline translation on Windows
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink()
        raise


def _add_index_lines(text: str, titles: list[str]) -> str:
    """Record rolled patterns in the live index, most recently rolled first, once.

    TD-194 S4: the index is found by its heading LINE (F3); duplicates are checked
    INSIDE the index section only (F4); lines go before the first existing bullet,
    or at the section's end when it has none, so no intro paragraph is required
    (F2).
    """
    if not INDEX_RE.search(text):
        text = text.rstrip("\n") + (
            f"\n\n{INDEX_HEADING}\n\nArchived in `archive/systemPatterns-archive.md`"
            " (read on demand). Most recently rolled first.\n"
        )
    start = INDEX_RE.search(text).end()
    end = next((h for h in _h2_starts(text) if h > start), len(text))
    section = text[start:end]
    have = {ln.strip() for ln in section.splitlines()}
    new = [f"- {t}" for t in dict.fromkeys(titles) if f"- {t}" not in have]
    if not new:
        return text
    first = re.search(r"^- ", section, re.M)
    at = start + first.start() if first else end
    lead = "" if first or text[:at].endswith("\n\n") else "\n"
    return text[:at] + lead + "\n".join(new) + "\n" + text[at:]


def _over_budget(root: Path) -> tuple[list[str], str | None]:
    """Return (complaints, reason-the-check-could-not-run).

    A1 (S5): this returned a bare list, so an EMPTY list meant both "every file is
    within budget" and "there was no budget to check against". Those are opposite
    facts and `--check` printed PASS for both. Measured on an adopter-shaped tree,
    a live file of 160,012 tokens against the shipped 6,000 budget produced
    "PASS: within budget" and exit 0, because `_budgets()` found no Rule 03 to read
    and the loop had nothing to iterate.

    An adopter is the normal case for that: `kits/core/` is compiled away into the
    host trees and the guard that holds the exemptions is repo-only, so NEITHER
    source resolves. A check that cannot fail must say so, not claim a pass , the
    posture the sibling resolver's docstring already states as "NEVER a silent pass".
    """
    docs = resolve_docs_root(root)
    if docs is None:
        return [], f"no {EXPECTED_SUBTREE}/ found under {root}"
    mb = docs / EXPECTED_SUBTREE
    budgets = _budgets(root)
    if not budgets:
        return [], (
            "no budget table found (Rule 03 is not readable from here), so file "
            "sizes were NOT checked"
        )
    exempt = _exemptions(root)
    over = []
    for name, budget in budgets.items():
        f = mb / name
        if not f.is_file():
            continue
        n = _tokens(f.read_text(encoding="utf-8"))
        if n is None:
            # R8: tiktoken is optional, so its absence must never FAIL. But it must
            # not silently PASS either (A1), so the caller is told why.
            return [], "no tokeniser installed (tiktoken), so sizes were NOT checked"
        cap = exempt.get(name, budget)
        if n > cap:
            how = (
                f"over its {cap} ratcheted-exemption cap"
                if name in exempt
                else f"over its {budget} Rule 03a budget"
            )
            over.append(f"{name} is {n} tokens, {how}")
    return over, None


def _head(action: dict, width: int | None = 72) -> str:
    """First line of a block, trimmed for one line of output (untrimmed: None)."""
    return action["block"].strip().split("\n", 1)[0][:width]


def _stuck_after_roll(root: Path, actions: list[dict]) -> list[str]:
    """Rolled files still over budget once every planned roll is done (S4/F6).

    Rolling cannot shrink a file's durable sections, so for such a file "run prune"
    would name a remedy that does not work , the US-264 S7 defect class.
    """
    budgets, exempt, stuck = _budgets(root), _exemptions(root), []
    for name in {a["name"] for a in actions} | set(ROLLING):
        live = next((a["live"] for a in actions if a["name"] == name), None)
        docs = resolve_docs_root(root)
        if live is None and docs is not None:
            live = docs / EXPECTED_SUBTREE / name
        if live is None or not live.is_file() or name not in budgets:
            continue
        text = live.read_text(encoding="utf-8")
        for a in actions:
            if a["name"] == name:
                text = text.replace(a["block"], "", 1)
        n = _tokens(text)
        if n is not None and n > exempt.get(name, budgets[name]):
            stuck.append(name)
    return sorted(stuck)


def _print_remedy_notes(over: list[str], stuck: list[str]) -> None:
    """Name only remedies that work (US-264 S7; TD-194 S4/F6)."""
    unrollable = [o for o in over if not any(o.startswith(n) for n in ROLLING)]
    if unrollable:
        print(
            "NOTE: the file(s) above are not archive-backed, so this script cannot "
            "shrink them. Split the content by hand, or amend Rule 03 deliberately."
        )
    for name in stuck:
        print(
            f"NOTE: rolling cannot bring {name} under its budget: its durable "
            "sections alone exceed it. Condense them by hand, archiving the "
            "originals verbatim first."
        )


def _run_check(
    actions: list[dict],
    over: list[str],
    unchecked: str | None,
    stuck: list[str] | None = None,
) -> int:
    """Gate mode , exit 1 if a roll is needed or a file is over budget.

    Modelled on `dependency-resolver.py --check`, which is what makes AC4's
    idempotency observable: after a roll, this must exit 0.
    """
    if not (actions or over):
        if unchecked:
            # A1: distinguish "verified within budget" from "could not verify".
            # Reporting PASS for the second is worse than silence, because the
            # operator reads it as verification.
            print(f"PARTIAL: live files are pruned, but {unchecked}.")
            return 0
        print("PASS: memory-bank live files are pruned and within budget.")
        return 0
    counts: dict[str, int] = {}
    for a in actions:
        counts[a["name"]] = counts.get(a["name"], 0) + 1
    for name, n in sorted(counts.items()):
        print(f"ROLL NEEDED: {name} has {n} block(s) to archive")
    for o in over:
        print(f"OVER BUDGET: {o}")
    if actions:
        print("Run prune-memory-bank.py <root> to roll history to the archives.")
    # S7 sweep: three of the six budgeted files are NOT in ROLLING, so telling the
    # operator to "roll history" when only those are over budget names a remedy
    # this script cannot provide; TD-194 S4/F6 found the same for a rolled file
    # whose DURABLE sections alone exceed the budget.
    _print_remedy_notes(over, stuck or [])
    return 1


def _run_dry(actions: list[dict]) -> int:
    if not actions:
        print("nothing to roll.")
    for a in actions:
        print(f"would roll from {a['name']}: {_head(a)}")
    return 0


def _run_roll(actions: list[dict]) -> int:
    """Perform the roll, reporting progress even when one action fails.

    F3 (S4): a bare `for a in actions: _roll(a)` left a PARTIAL roll unreported , a
    failure on block 5 of 17 archived four and showed a traceback. Each completed
    roll is individually safe (append, confirm, remove) and the whole operation is
    idempotent, so re-running finishes the rest; the defect was that the operator
    could not tell how far it got. Now the count is reported and the exit code says
    it did not finish.
    """
    if not actions:
        print("nothing to roll; memory-bank already pruned.")
        return 0
    done = 0
    for a in actions:
        try:
            _roll(a)
        except (OSError, RuntimeError, ValueError) as exc:
            print(
                f"STOPPED after {done} of {len(actions)} block(s): {exc}",
                file=sys.stderr,
            )
            print(
                "Every completed roll is already archived and the run is "
                "idempotent, so re-run to finish the remainder.",
                file=sys.stderr,
            )
            return 1
        done += 1
        print(f"rolled from {a['name']}: {_head(a)}")
    print(f"done: {done} block(s) archived.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("root", type=Path, help="repository root")
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if a roll is needed or a live file is over budget",
    )
    ap.add_argument("--dry-run", action="store_true", help="report only")
    args = ap.parse_args(argv[1:])

    root = args.root.resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    actions = _plan(root)
    if args.check:
        over, unchecked = _over_budget(root)
        stuck = _stuck_after_roll(root, actions) if over else []
        return _run_check(actions, over, unchecked, stuck)
    if args.dry_run:
        return _run_dry(actions)
    return _run_roll(actions)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
