#!/usr/bin/env python3
"""Tier-2 core (`/kits/core/`) must be self-contained: no CORE asset may reference a
non-core (vendor/kit) asset (US-188 AC5).

The white-label invariant (US-178, `check-white-label-core.py`) scans core CONTENT for
org-identity STRINGS. It does NOT resolve REFERENCES , so a core command that names a
shed vendor-kit agent (e.g. `agent: ra-<persona>`) slips through, leaving a core-only
base with a dangling delegation. This check closes that gap.

Check (scoped to `agent:` frontmatter references, the US-188 surface):
  For every core command and agent, the `agent:` frontmatter value (if present) MUST
  resolve to an agent PROVIDED BY core. Core agents compile prefix-free (their
  `namespace: core` strips the per-target prefix), so the resolvable core agent names
  are exactly the bare stems of `/kits/core/agents/*.md`. A reference that is prefixed
  (`ra-`/`ta-`) or otherwise absent from that set is a dangling cross-kit reference and
  fails , the core command must be made agent-agnostic, reclassified into the owning
  kit, or declare a kit dependency.

Exit 0 = all core references resolve within core; exit 1 = dangling reference(s).
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise RuntimeError("pyyaml required for check-core-references")


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def _core_agent_names(core: Path) -> set[str]:
    """Bare names of agents PROVIDED by core (these compile prefix-free)."""
    names: set[str] = set()
    for agent in sorted((core / "agents").glob("*.md")):
        meta = _frontmatter(agent)
        names.add(meta.get("name") or agent.stem)
    return names


def check_references(core: Path) -> list[str]:
    provided = _core_agent_names(core)
    violations: list[str] = []
    for sub in ("commands", "agents"):
        for asset in sorted((core / sub).glob("*.md")):
            meta = _frontmatter(asset)
            ref = meta.get("agent")
            if not ref:
                continue
            if ref not in provided:
                violations.append(
                    f"{asset}: core asset references non-core agent '{ref}' "
                    f"(core provides only: {sorted(provided) or '<none>'})"
                )
    return violations


def main(argv: list[str]) -> int:
    core = Path(argv[1]).resolve() if len(argv) > 1 else Path("kits/core").resolve()
    if not core.is_dir():
        # Nothing checked is not a pass (TD-201 A20).
        print(
            f"core-references: no core dir at {core} , NOTHING CHECKED (FAIL CLOSED). "
            "Pass the kits/core path.",
            file=sys.stderr,
        )
        return 2
    violations = check_references(core)
    if violations:
        print(f"core-references: {len(violations)} dangling reference(s) under {core}:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"core-references: all core `agent:` references resolve within core , {core}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
