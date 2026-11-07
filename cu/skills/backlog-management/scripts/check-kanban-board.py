#!/usr/bin/env python3
"""Kanban-board consistency gate , the board must agree with the cards.

`Lucas_Kanban.md` / `Kanban-Board.md` is a hand-maintained DENORMALISED VIEW of
data every card already carries in its ``status:`` frontmatter. Nothing gated it,
so it had no failure mode anyone noticed: on 2026-09-20 a single session left 17
newly-created cards off the board entirely and 5 freshly-Cancelled cards sitting
in TODO. Same class as the epic ``child_stories`` drift (BUG-004): a copy that is
not derived and not checked is a copy that rots.

This checks the two directions that actually mislead a reader:

1. every not-Done, non-epic card appears SOMEWHERE on the board , a card that
   exists but is invisible cannot be picked up;
2. no Done/Cancelled card sits in an ACTIVE column (TODO / DOING) , a finished
   or abandoned card presented as available is worse than an absent one.

Deliberately NOT checked: exact column placement and glyph for live cards. The
owner moves cards by hand as work proceeds, and a gate that fights that would be
turned off , which is how the last unenforced convention died.

Usage:
    python3 check-kanban-board.py [ROOT_DIR]

Exit codes:
    0 - board consistent
    1 - drift found
    2 - board or backlog not found
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
BOARD_REL = Path("roadmap/dashboards/Kanban-Board.md")
BACKLOG_REL = Path("roadmap/backlog")

DONE_STATES = {"done", "cancelled"}
ACTIVE_COLUMNS = {"TODO", "DOING"}

ID_IN_LINK = re.compile(r"\[\[([A-Z]+-\d+)")
COLUMN = re.compile(r"^##\s+(.+?)\s*$", re.M)


def resolve_docs_root(root: Path) -> Path | None:
    override = os.environ.get(DOCS_ROOT_ENV)
    if override:
        cand = Path(override)
        if not cand.is_absolute():
            cand = root / cand
        return cand if (cand / BACKLOG_REL).is_dir() else None
    for name in DOCS_ROOT_CANDIDATES:
        cand = root / name
        if (cand / BACKLOG_REL).is_dir():
            return cand
    return None


def load_cards(backlog: Path) -> dict[str, str]:
    """story_id -> lowercased status, for non-epic cards."""
    cards: dict[str, str] = {}
    for f in sorted(backlog.glob("*.md")):
        if f.name.startswith("EP-"):
            continue
        text = f.read_text(encoding="utf-8")
        sid = re.search(r"^story_id:\s*(\S+)", text, re.M)
        st = re.search(r"^status:\s*(.+)$", text, re.M)
        if sid and st:
            cards[sid.group(1)] = st.group(1).strip().lower()
    return cards


def board_columns(board_text: str) -> dict[str, set[str]]:
    """Column name -> the story ids listed under it."""
    out: dict[str, set[str]] = {}
    marks = list(COLUMN.finditer(board_text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(board_text)
        out[m.group(1).strip().upper()] = set(
            ID_IN_LINK.findall(board_text[m.end() : end])
        )
    return out


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    docs = resolve_docs_root(root)
    if docs is None or not (docs / BOARD_REL).is_file():
        print("SKIP: no board or backlog found", file=sys.stderr)
        return 2

    cards = load_cards(docs / BACKLOG_REL)
    cols = board_columns((docs / BOARD_REL).read_text(encoding="utf-8"))
    on_board = set().union(*cols.values()) if cols else set()
    active = set().union(*(cols.get(c, set()) for c in ACTIVE_COLUMNS))

    missing = sorted(
        sid
        for sid, st in cards.items()
        if st not in DONE_STATES and sid not in on_board
    )
    stale = sorted(sid for sid in active if cards.get(sid, "") in DONE_STATES)

    if not missing and not stale:
        print(f"PASS: board agrees with {len(cards)} cards")
        return 0

    if missing:
        print(
            f"FAIL: {len(missing)} live card(s) absent from the board , "
            "a card that exists but is invisible cannot be picked up:",
            file=sys.stderr,
        )
        print("  " + ", ".join(missing), file=sys.stderr)
    if stale:
        print(
            f"FAIL: {len(stale)} Done/Cancelled card(s) in an ACTIVE column , "
            "presented as available:",
            file=sys.stderr,
        )
        print("  " + ", ".join(stale), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
