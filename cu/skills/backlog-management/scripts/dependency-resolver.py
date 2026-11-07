#!/usr/bin/env python3
"""Backlog dependency resolver , build + resolve the GLOBAL cross-epic dependency tree.

Scans every story/epic markdown file's ``depends_on`` frontmatter, builds one directed
graph, and resolves it into an actionable view:

- integrity: dangling dependencies (dep -> a non-existent story) and cycles,
- a topological order over not-Done work,
- the UNBLOCK-THE-MOST ranking (not-Done stories by how many not-Done stories they
  transitively unblock) , i.e. what to do first to open the most downstream scope,
- ready-now (all deps Done) and near-ready (exactly one unmet dep) lists,
- a Mermaid overview of the not-Done frontier.

Local only , no network, no external rendering service. Deterministic.

Usage:
    uv run python .../dependency-resolver.py <backlog-dir> [--out FILE] [--check]

    --check : exit non-zero if any dangling dependency or cycle is found (CI gate mode),
              and (when --out given) if the generated file is stale vs. what would be
              produced (so CI catches an un-regenerated index).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

# Story ids: PREFIX-NUMBER with an optional lowercase letter suffix for split stories
# (e.g. SP-103b). The suffix is significant , SP-103 and SP-103b are DIFFERENT stories.
ID_RE = re.compile(r"^(EP|US|TD|SP|RA|BUG|CI|SEC)-\d+[a-z]?", re.IGNORECASE)
AC_RE = re.compile(r"^##+\s*Acceptance Criteria\s*$.*?^- \[", re.M | re.S)
# A park marker counts only OUTSIDE a quoted progress note. A note QUOTING a past
# park ("US-255 said DO NOT PULL") is history, not a live state , reading the
# quotation as the state is the same narrative-vs-contract confusion this backlog
# keeps hitting. `unblocks_if:` is frontmatter and is authoritative on its own.
UNBLOCKS_IF_RE = re.compile(r"^unblocks_if:", re.M)
PARK_WORD_RE = re.compile(r"^(?!>)(?=.*(?:PARKED|NO-GO|DO NOT PULL))", re.M)

DONE_STATES = {"done", "completed", "cancelled"}
ACTIONABLE = {"todo", "ready", "in progress", "in-progress", "scheduled", "pending"}


def _frontmatter(text: str) -> str:
    parts = re.split(r"(?m)^---[ \t]*$", text, maxsplit=2)
    return parts[1] if len(parts) >= 3 else ""


def _scalar(fm: str, key: str) -> str | None:
    m = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.+?)[ \t]*$", fm)
    if not m:
        return None
    return m.group(1).strip().strip("'\"")


def canon(sid: str) -> str:
    """Canonical id: PREFIX-NUMBER uppercased, an optional letter suffix lowercased.
    SP-103b and SP-103B and sp-103B all -> 'SP-103b'; distinct from 'SP-103'."""
    s = sid.strip().strip("'\"")
    m = re.match(r"^([A-Za-z]+)-(\d+)([A-Za-z]?)$", s)
    if not m:
        return s
    return f"{m.group(1).upper()}-{m.group(2)}{m.group(3).lower()}"


def _deps(fm: str) -> list[str]:
    m = re.search(r"(?m)^depends_on:[ \t]*\[(.*?)\]", fm)
    if not m or not m.group(1).strip():
        return []
    return [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]


def load(backlog: Path) -> dict[str, dict]:
    stories: dict[str, dict] = {}
    for f in sorted(backlog.glob("*.md")):
        m = ID_RE.match(f.name)
        if not m:
            continue
        text = f.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        # Prefer the frontmatter story_id (authoritative) over the filename-derived id.
        sid = canon(_scalar(fm, "story_id") or _scalar(fm, "epic_id") or m.group(0))
        stories[sid] = {
            "id": sid,
            "status": (_scalar(fm, "status") or "?").lower(),
            "depends_on": [canon(d) for d in _deps(fm)],
            "epic": (_scalar(fm, "epic") or _scalar(fm, "parent") or "").strip("'\""),
            "is_epic": sid.startswith("EP-"),
            "file": f.name,
            # Ready-bar inputs (see backlog-management/SKILL.md, the
            # "Draft -> Ready bar" section).
            # Condition 2: a card with no acceptance criteria cannot be FINISHED, only
            # abandoned. Condition 3: a parked card is deliberately stopped, and an
            # `unblocks_if:` field is the machine-readable form of that.
            "has_acs": bool(AC_RE.search(text)),
            "parked": bool(UNBLOCKS_IF_RE.search(text) or PARK_WORD_RE.search(text)),
        }
    return stories


def analyse(stories: dict[str, dict]) -> dict:
    ids = set(stories)
    # integrity
    dangling = {
        s: [d for d in v["depends_on"] if d not in ids]
        for s, v in stories.items()
        if any(d not in ids for d in v["depends_on"])
    }
    # graph over KNOWN edges only
    rev: dict[str, set[str]] = defaultdict(set)  # dep -> {stories depending on dep}
    adj: dict[str, set[str]] = defaultdict(set)  # story -> {its deps}
    for s, v in stories.items():
        for d in v["depends_on"]:
            if d in ids:
                rev[d].add(s)
                adj[s].add(d)

    # Topological order + TRUE cycle detection. Only KNOWN edges count toward indegree
    # (adj already excludes dangling deps), so a dangling reference never manifests as a
    # phantom cycle. A node left unemitted after Kahn is in a real cycle.
    indeg = {s: len(adj[s]) for s in ids}  # s depends on len(adj[s]) known stories
    emitted: list[str] = []
    q = sorted([s for s in ids if indeg[s] == 0])
    remaining = dict(indeg)
    while q:
        n = q.pop(0)
        emitted.append(n)
        for m in sorted(rev[n]):
            remaining[m] -= 1
            if remaining[m] == 0:
                q.append(m)
        q.sort()
    # A truly-cyclic node still has remaining indegree > 0; a node only blocked by a
    # DANGLING dep has all-known deps satisfiable, so it WILL be emitted (its known
    # indegree reaches 0). Thus unemitted == genuine cycle members.
    cyclic = sorted(s for s in ids if s not in emitted)

    # transitive downstream (not-Done) per not-Done story
    def downstream(x: str) -> set[str]:
        seen: set[str] = set()
        stack = [x]
        while stack:
            cur = stack.pop()
            for y in rev.get(cur, ()):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    def is_done(s: str) -> bool:
        return stories[s]["status"] in DONE_STATES

    def is_parked(s: str) -> bool:
        """Parked == deliberately stopped, not merely waiting.

        A `blocked` story is NOT Done, so it belongs in every other listing, but it
        must not be COUNTED as something a story unblocks: the resolver cannot tell a
        live dependent from a parked one, and an inflated count actively misdirects
        prioritisation. US-205 ranked #2 in the backlog on 5 transitive unblocks, 4 of
        which were mechanism-dead parked cards , a 1-story unblock wearing a 5-story
        badge.
        """
        return stories[s]["status"] == "blocked"

    unblock = []
    for s in ids:
        if stories[s]["is_epic"] or is_done(s):
            continue
        ds = sorted(
            y
            for y in downstream(s)
            if not stories[y]["is_epic"] and not is_done(y) and not is_parked(y)
        )
        if ds:
            unblock.append((len(ds), s, ds))
    unblock.sort(key=lambda t: (-t[0], t[1]))

    # ready / near-ready (not-Done, non-epic)
    ready, near = [], []
    for s, v in stories.items():
        if v["is_epic"] or is_done(s):
            continue
        unmet = [d for d in v["depends_on"] if d not in ids or not is_done(d)]
        if not unmet:
            ready.append(s)
        elif len(unmet) == 1:
            near.append((s, unmet[0]))
    ready.sort()
    near.sort()

    return {
        "stories": stories,
        "dangling": dangling,
        "cyclic": cyclic,
        "topo": emitted,
        "unblock": unblock,
        "ready": ready,
        "near": near,
    }


def _title_hint(sid: str, stories: dict) -> str:
    return sid


def render(res: dict) -> str:
    stories = res["stories"]

    def line(s: str) -> str:
        v = stories[s]
        return f"`{s}` ({v['status']})"

    out: list[str] = []
    out.append("# Backlog dependency resolution")
    out.append("")
    out.append(
        "> GENERATED , do not edit by hand. Regenerate with "
        "`uv run python "
        "kits/core/skills/backlog-management/scripts/dependency-resolver.py "
        "docs-copper/roadmap/backlog "
        "--out docs-copper/roadmap/backlog/DEPENDENCIES.md`. "
        "Source of truth: each story's `depends_on:` frontmatter. "
        "Local only, no external tools."
    )
    out.append("")

    n_story = sum(1 for v in stories.values() if not v["is_epic"])
    n_open = sum(
        1
        for v in stories.values()
        if not v["is_epic"] and v["status"] not in DONE_STATES
    )
    out.append(f"**{n_story} stories** ({n_open} not-Done). ")
    out.append("")

    # integrity
    out.append("## Integrity")
    out.append("")
    if res["dangling"]:
        out.append(
            "**Dangling dependencies** (a `depends_on` points at a story that does "
            "not exist , likely renamed/split/closed; fix the frontmatter):"
        )
        out.append("")
        for s, missing in sorted(res["dangling"].items()):
            out.append(f"- `{s}` -> {', '.join(f'`{m}`' for m in missing)} , MISSING")
        out.append("")
    else:
        out.append("- No dangling dependencies.")
        out.append("")
    if res["cyclic"]:
        out.append(
            "**Dependency CYCLE detected** involving: "
            + ", ".join(f"`{c}`" for c in res["cyclic"])
            + ". The topological order below is partial until the cycle is broken."
        )
        out.append("")
    else:
        out.append("- No dependency cycles.")
        out.append("")

    # unblock ranking
    out.append("## Unblock-the-most ranking")
    out.append("")
    out.append(
        "Not-Done stories ranked by how many **not-Done** stories they transitively "
        "unblock. Deliver the top items first to open the most downstream scope."
    )
    out.append("")
    out.append("| Rank | Story | Status | Unblocks (n) | Transitively unblocks |")
    out.append("| ---- | ----- | ------ | ------------ | --------------------- |")
    for i, (n, s, ds) in enumerate(res["unblock"][:20], 1):
        shown = ", ".join(f"`{d}`" for d in ds[:8]) + ("..." if len(ds) > 8 else "")
        out.append(f"| {i} | `{s}` | {stories[s]['status']} | {n} | {shown} |")
    out.append("")

    # ready / near
    out.append("## Ready now (all dependencies Done)")
    out.append("")
    if res["ready"]:
        for s in res["ready"]:
            v = stories[s]
            if v["status"] in ACTIONABLE:
                tag = " , ACTIONABLE"
            elif v["parked"]:
                tag = " , PARKED (condition 3: carries a park marker)"
            elif not v["has_acs"]:
                tag = " , needs acceptance criteria (condition 2)"
            else:
                # Dependencies are satisfied by construction here, so conditions 1-3
                # all hold: this card is promotable by a one-word status edit. The
                # resolver says what COULD be promoted, never what should be.
                tag = " , **MEETS THE READY BAR** (promotable)"
            out.append(f"- {line(s)}{tag}")
    else:
        out.append("- (none)")
    out.append("")
    out.append("## Near-ready (exactly one unmet dependency , the fastest unlocks)")
    out.append("")
    if res["near"]:
        for s, blocker in res["near"]:
            bst = stories.get(blocker, {}).get("status", "?")
            out.append(f"- {line(s)} , blocked only by `{blocker}` ({bst})")
    else:
        out.append("- (none)")
    out.append("")

    # mermaid: the not-Done frontier (not-Done stories + their direct deps)
    out.append("## Not-Done frontier (dependency overview)")
    out.append("")
    out.append(
        "**Dependency graph** , green=Done, amber=actionable, grey=Draft. "
        "Edge A -> B means B depends on A. Only edges touching not-Done work shown."
    )
    out.append("")
    frontier: set[str] = set()
    for s, v in stories.items():
        if v["is_epic"]:
            continue
        if v["status"] not in DONE_STATES:
            frontier.add(s)
            frontier.update(d for d in v["depends_on"] if d in stories)
    L = ["```mermaid", "flowchart LR"]
    for s in sorted(frontier):
        v = stories[s]
        cls = (
            "done"
            if v["status"] in DONE_STATES
            else ("active" if v["status"] in ACTIONABLE else "draft")
        )
        L.append(f'  {s.replace("-", "_")}["{s}"]:::{cls}')
    for s in sorted(frontier):
        for d in stories[s]["depends_on"]:
            if d in frontier:
                L.append(f"  {d.replace('-', '_')} --> {s.replace('-', '_')}")
    L.append("  classDef done fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20")
    L.append("  classDef active fill:#ffe0b2,stroke:#ef6c00,color:#e65100")
    L.append("  classDef draft fill:#eeeeee,stroke:#9e9e9e,color:#424242")
    L.append("```")
    out.append("\n".join(L))
    out.append("")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Resolve the global backlog dependency tree."
    )
    ap.add_argument(
        "backlog", type=Path, help="backlog directory of story/epic .md files"
    )
    ap.add_argument(
        "--out", type=Path, default=None, help="write the generated report here"
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero on dangling deps / cycles (and staleness if --out)",
    )
    args = ap.parse_args()

    stories = load(args.backlog)
    if not stories:
        print(f"no story files found in {args.backlog}", file=sys.stderr)
        return 2
    res = analyse(stories)
    report = render(res)

    # Write mode (not --check): regenerate the file.
    if args.out and not args.check:
        args.out.write_text(report, encoding="utf-8")
        print(f"wrote {args.out}")
    elif not args.out and not args.check:
        sys.stdout.write(report)

    if args.check:
        # A missing index is not a current one (TD-201 L6).
        missing = bool(args.out and not args.out.is_file())
        stale = bool(
            args.out
            and args.out.is_file()
            and args.out.read_text(encoding="utf-8") != report
        )
        dangling = bool(res["dangling"])
        cyclic = bool(res["cyclic"])
        if dangling:
            print(
                f"FAIL: {len(res['dangling'])} story(ies) with a dangling dependency: "
                f"{', '.join(sorted(res['dangling']))}.",
                file=sys.stderr,
            )
        if cyclic:
            print(f"FAIL: dependency cycle among {res['cyclic']}.", file=sys.stderr)
        if stale:
            print(
                f"FAIL: {args.out} is stale , regenerate the dependency index.",
                file=sys.stderr,
            )
        if missing:
            print(
                f"FAIL: {args.out} is missing , regenerate the dependency index.",
                file=sys.stderr,
            )
        if dangling or cyclic or stale or missing:
            return 1
        print("dependency integrity OK (no dangling deps, no cycles, index current).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
