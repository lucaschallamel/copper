#!/usr/bin/env python3
"""Compare on-disk counts (agents, skills, commands, rules) against documented claims.

Checks README.md badges and .opencode/instructions.md for count claims and
verifies they match actual filesystem counts.

Usage:
    python3 check-count-drift.py [ROOT_DIR]

Exit codes:
    0 - All counts match
    1 - Drift detected
    2 - Usage error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def _find_repo_root() -> Path:
    """Walk up from this file to the repo root (the dir holding .git).

    Robust to WHICH copy runs: the `kits/core` source and the deployed `.opencode/`
    and `.claude/` copies sit at different depths, so a fixed `parents[N]` is wrong
    for at least one of them. Fail loud if no marker is found rather than silently
    scanning the wrong tree , a gate that resolves to an empty tree and reports PASS
    is worse than one that errors (measured: this script printed "All counts match
    on-disk reality: {'agents': 0, ...}" and exited 0).

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


def count_on_disk(root: Path) -> dict[str, int]:
    """Count actual framework artefacts on disk."""
    opencode = root / ".opencode"
    return {
        "agents": len(list((opencode / "agents").glob("*.md")))
        if (opencode / "agents").is_dir()
        else 0,
        "skills": len([d for d in (opencode / "skills").iterdir() if d.is_dir()])
        if (opencode / "skills").is_dir()
        else 0,
        "commands": len(list((opencode / "commands").glob("*.md")))
        if (opencode / "commands").is_dir()
        else 0,
        "rules": len(_rule_files(opencode, ANCHOR_RULE)),
        "scoped_rules": len(_rule_files(opencode, SCOPED_RULE)),
    }


# ADR-054 D2: anchors are `NN-<topic>.rules.md` (always-on), scoped rule files are
# `NN<letter>-<topic>.rules.md` (`paths`-scoped). They are counted apart so the
# README badge keeps naming the 8 anchors (US-378 AC1). The canonical patterns are in
# deploy/rule_layout.py; this standalone gate keeps a copy, pinned equal by a test.
ANCHOR_RULE = re.compile(r"^\d{2}-[\w.-]+\.rules\.md$")
SCOPED_RULE = re.compile(r"^\d{2}[a-z]-[\w.-]+\.rules\.md$")


def _rule_files(opencode: Path, pattern: re.Pattern[str]) -> list[str]:
    rules = opencode / "rules"
    if not rules.is_dir():
        return []
    return sorted(p.name for p in rules.glob("*.rules.md") if pattern.match(p.name))


def unclassified_rules(root: Path) -> list[str]:
    """Rule files that are neither an anchor nor a scoped file: never silently
    uncounted."""
    rules = root / ".opencode" / "rules"
    if not rules.is_dir():
        return []
    return sorted(
        p.name
        for p in rules.glob("*.rules.md")
        if not ANCHOR_RULE.match(p.name) and not SCOPED_RULE.match(p.name)
    )


def extract_badge_counts(readme_path: Path) -> dict[str, int]:
    """Extract counts from shields.io badge URLs in README.md."""
    if not readme_path.exists():
        return {}
    text = readme_path.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for category in ("agents", "skills", "commands", "rules"):
        match = re.search(rf"badge/{category}-(\d+)", text)
        if match:
            counts[category] = int(match.group(1))
    return counts


def extract_instructions_counts(instructions_path: Path) -> dict[str, int]:
    """Extract counts from .opencode/instructions.md folder hierarchy comments."""
    if not instructions_path.exists():
        return {}
    text = instructions_path.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    # The hierarchy fence names `.opencode/` or the host-neutral `<harness-root>/`
    # (US-378: a plugin build refuses an OpenCode path in a rule body).
    hierarchy_block = re.search(
        r"(?:\.opencode/|<harness-root>/).*?^```", text, re.MULTILINE | re.DOTALL
    )
    if not hierarchy_block:
        return {}
    block = hierarchy_block.group(0)
    for category in ("agents", "skills", "commands", "rules"):
        match = re.search(rf"#\s*(\d+)\s+{category}", block)
        if match:
            counts[category] = int(match.group(1))
    scoped = re.search(r"(\d+)\s+scoped rules", block)
    if scoped:
        counts["scoped_rules"] = int(scoped.group(1))
    return counts


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else _find_repo_root()
    root = root.resolve()

    disk = count_on_disk(root)

    # THREE-STATE, fail closed (US-356 S7 P3-2). A gate that resolves to a tree with
    # no assets and reports "All counts match" is worse than one that errors: it hands
    # back a clean bill of health for a scan of nothing. The docstring on
    # _find_repo_root already warned about exactly this, but the guard lived only in
    # the ROOT-FINDER , a hand-passed argument bypassed it. Measured: passing
    # `kits/core` resolves `kits/core/.opencode`, finds zeros, and exits 0.
    #
    # Contract, mirroring check-personal-data.py: 0 clean | 1 drift | 2 DID NOT RUN.
    # Assert BREADTH (the measured set is non-trivial), never merely non-violation.
    opencode = root / ".opencode"
    if not opencode.is_dir():
        print(
            f"ERROR: no .opencode/ tree under {root} , NOTHING COUNTED (fail closed).\n"
            "  This gate counts the DEPLOYED harness tree, not a kit source tree.\n"
            "  Run it with no argument (it walks up to the repo root) or pass a root\n"
            "  that CONTAINS .opencode/.",
            file=sys.stderr,
        )
        return 2
    if not any(disk.values()):
        print(
            f"ERROR: .opencode/ under {root} holds no agents, skills, commands or "
            "rules , NOTHING COUNTED (fail closed).\n"
            "  Zero on-disk assets cannot be compared against a documented claim; a "
            "PASS here would be vacuous.",
            file=sys.stderr,
        )
        return 2
    badge = extract_badge_counts(root / "README.md")
    instructions = extract_instructions_counts(root / ".opencode" / "instructions.md")

    drift: list[str] = [
        f"  rules/: {name} is neither an anchor (NN-) nor a scoped file (NN<letter>-)"
        for name in unclassified_rules(root)
    ]

    if not drift and not badge and not instructions:
        # Nothing documented, so no count was compared (TD-201 L7). A rule file
        # that cannot be classified is still a finding, reported above.
        print(
            "ERROR: NO CLAIMS FOUND , no README.md badge and no count in "
            ".opencode/instructions.md, so NOTHING COMPARED (fail closed).",
            file=sys.stderr,
        )
        return 2

    for category in sorted(disk):
        actual = disk[category]
        badge_claim = badge.get(category)
        instr_claim = instructions.get(category)

        if badge_claim is not None and badge_claim != actual:
            drift.append(f"  README.md badge: {category}={badge_claim}, disk={actual}")
        if instr_claim is not None and instr_claim != actual:
            drift.append(f"  instructions.md: {category}={instr_claim}, disk={actual}")

    if drift:
        print("FAIL: Count drift detected:")
        for line in drift:
            print(line)
        print()
        print(f"On-disk counts: {disk}")
        print()
        print("Remediation: Update badge(s) in README.md and/or count claims")
        print("in .opencode/instructions.md to match the actual filesystem.")
        print()
        print("Files to check:")
        print("  - README.md (shields.io badges)")
        print("  - .opencode/instructions.md (framework hierarchy comments)")
        print("  - AGENTS.md (folder structure comment)")
        return 1

    print(f"PASS: All counts match on-disk reality: {disk}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
