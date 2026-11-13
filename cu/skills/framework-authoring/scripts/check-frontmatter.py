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

# The contracts above are the SOURCE contract (kits/core). The deployed `.opencode/`
# tree is OpenCode 2's (TD-207, ADR-056): V2 keys only, because OpenCode 2 sends any key
# it does not know in an agent's model request body. Must match
# deploy/targets/opencode_v2.py.
DEPLOYED_COMMAND_REQUIRED = {"description"}
DEPLOYED_COMMAND_ALLOWED = DEPLOYED_COMMAND_REQUIRED | {
    "agent",
    "model",
    "subagent",
    "template",
}
DEPLOYED_AGENT_REQUIRED = {"description", "mode", "permissions"}
DEPLOYED_AGENT_ALLOWED = DEPLOYED_AGENT_REQUIRED | {
    "color",
    "hidden",
    "model",
    "steps",
    "disabled",
    "variant",
    "system",
    "request",
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


def _check_dir(
    base: Path, kind: str, required: set[str], allowed: set[str], errors: list[str]
) -> int:
    """Validate each `*.md` in `base/<kind>s` (or singular); return the count."""
    found = next((d for d in (base / f"{kind}s", base / kind) if d.is_dir()), None)
    if found is None:
        errors.append(f"{base.name}: {kind}s directory not found")
        return 0
    files = sorted(found.glob("*.md"))
    for f in files:
        errors.extend(validate_file(f, required, allowed, f"{found.name}/{f.name}"))
    return len(files)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]) if args else _find_repo_root()
    root = root.resolve()

    errors: list[str] = []
    counts: list[str] = []
    # Canonical layout is PLURAL (commands/, agents/) per framework-authoring/SKILL.md;
    # the singular form is accepted for portability across hosts that emit it.
    source = root / "kits" / "core"
    if (
        source.is_dir()
    ):  # this framework's own repository; an adopter's tree has no source
        cmds = _check_dir(source, "command", COMMAND_REQUIRED, COMMAND_ALLOWED, errors)
        agents = _check_dir(source, "agent", AGENT_REQUIRED, AGENT_ALLOWED, errors)
        counts.append(f"source: {cmds} commands, {agents} agents")
    opencode = root / ".opencode"
    cmds = _check_dir(
        opencode, "command", DEPLOYED_COMMAND_REQUIRED, DEPLOYED_COMMAND_ALLOWED, errors
    )
    agents = _check_dir(
        opencode, "agent", DEPLOYED_AGENT_REQUIRED, DEPLOYED_AGENT_ALLOWED, errors
    )
    counts.append(f"deployed (OpenCode 2): {cmds} commands, {agents} agents")

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

    print(f"PASS: frontmatter contracts hold ({'; '.join(counts)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
