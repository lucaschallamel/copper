#!/usr/bin/env python3
"""Validate YAML frontmatter for commands and agents against the canonical contract.

Enforces required keys, allows optional keys, rejects unknown keys.

Usage:
    python3 check-frontmatter.py [ROOT_DIR]

Exit codes:
    0 - All files conform
    1 - Validation failures detected
    2 - Usage error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

COMMAND_REQUIRED = {"description", "version", "last_updated", "maintained_by"}
COMMAND_OPTIONAL = {"agent", "changelog", "namespace"}
COMMAND_ALLOWED = COMMAND_REQUIRED | COMMAND_OPTIONAL

AGENT_REQUIRED = {
    "description",
    "mode",
    "temperature",
    "color",
    "tools",
    "permission",
    "version",
    "last_updated",
    "maintained_by",
}
AGENT_OPTIONAL = {"changelog", "namespace"}
AGENT_ALLOWED = AGENT_REQUIRED | AGENT_OPTIONAL


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


FRONTMATTER_RE = re.compile(r"---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from a Markdown file. Returns None if not found."""
    # The block ends at a line that is exactly `---`, not at the first `---`
    # anywhere (a value such as 'a---b' ended it early, TD-201).
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    block = m.group(1).strip()
    try:
        return yaml.safe_load(block)
    except yaml.YAMLError:
        return None


def validate_file(
    path: Path,
    required: set[str],
    allowed: set[str],
    label: str,
) -> list[str]:
    """Validate a single file's frontmatter. Returns list of error strings."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if fm is None:
        errors.append(f"{label}: no valid YAML frontmatter found")
        return errors

    if not isinstance(fm, dict):
        errors.append(f"{label}: frontmatter is not a YAML mapping")
        return errors

    keys = set(fm.keys())

    missing = required - keys
    if missing:
        errors.append(f"{label}: missing required keys: {sorted(missing)}")

    unknown = keys - allowed
    if unknown:
        errors.append(f"{label}: unknown keys not in contract: {sorted(unknown)}")

    for key in required & keys:
        val = fm.get(key)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            errors.append(f"{label}: required key '{key}' has empty value")

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else _find_repo_root()
    root = root.resolve()

    opencode = root / ".opencode"
    errors: list[str] = []

    # Canonical layout is PLURAL (.opencode/commands, .opencode/agents) per
    # framework-authoring/SKILL.md; accept the singular form too for portability
    # across hosts that emit it.
    cmd_dir = next(
        (d for d in (opencode / "commands", opencode / "command") if d.is_dir()), None
    )
    if cmd_dir is not None:
        for f in sorted(cmd_dir.glob("*.md")):
            errors.extend(
                validate_file(
                    f, COMMAND_REQUIRED, COMMAND_ALLOWED, f"{cmd_dir.name}/{f.name}"
                )
            )
    else:
        errors.append("commands directory not found")

    agent_dir = next(
        (d for d in (opencode / "agents", opencode / "agent") if d.is_dir()), None
    )
    if agent_dir is not None:
        for f in sorted(agent_dir.glob("*.md")):
            errors.extend(
                validate_file(
                    f, AGENT_REQUIRED, AGENT_ALLOWED, f"{agent_dir.name}/{f.name}"
                )
            )
    else:
        errors.append("agents directory not found")

    if errors:
        print("FAIL: Frontmatter contract violations detected:")
        for e in errors:
            print(f"  {e}")
        print()
        print(f"Total violations: {len(errors)}")
        print()
        print("See .opencode/skills/framework-authoring/SKILL.md")
        print("for the canonical frontmatter contract.")
        return 1

    cmd_count = len(list(cmd_dir.glob("*.md"))) if cmd_dir.is_dir() else 0
    agent_count = len(list(agent_dir.glob("*.md"))) if agent_dir.is_dir() else 0
    print(
        f"PASS: All {cmd_count} commands and {agent_count} agents "
        f"conform to the frontmatter contract."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
