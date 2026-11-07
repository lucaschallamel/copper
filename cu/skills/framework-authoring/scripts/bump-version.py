#!/usr/bin/env python3
"""Bump the COPPER framework version consistently across all mechanical version files.

Single source of truth: pyproject.toml [project] version.

This script handles the DETERMINISTIC files only. It does NOT write CHANGELOG
prose, the AGENTS.md changelog narrative, or perform any git operations - those
are owned by the /cu-version-bump command (human/agent judgment + Git-safety gates).

Files rewritten:
  - pyproject.toml : [project] version = "X.Y.Z"
  - README.md      : version badge, dist zip examples, footer version+date
  - AGENTS.md      : frontmatter version (own track) + last_updated date
  - kits/core/VERSION : the core plugin's version, which every kit plugin pins (US-368)

Usage:
  bump-version.py <major|minor|patch|X.Y.Z> [--date YYYY-MM-DD] [--dry-run]

The AGENTS.md frontmatter version is on its own track (it references the framework
release in its changelog). This script bumps the AGENTS.md frontmatter MINOR by
default and updates last_updated; the changelog entry is added by the command.

Author: COPPER framework
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


def _find_repo_root() -> Path:
    """Walk up to the repo root (the dir holding .git) , see check-identity-drift.py.

    A fixed `parents[4]` is wrong for at least one of the three copies (kits/core
    source, .opencode/, .claude/), and this script WRITES version bumps, so
    resolving to the wrong tree would edit the wrong files.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists() or (parent / ".gitlab-ci.yml").exists():
            return parent
    print("ERROR: cannot find repository root (.git).", file=sys.stderr)
    raise SystemExit(2)


REPO_ROOT = _find_repo_root()
PYPROJECT = REPO_ROOT / "pyproject.toml"
README = REPO_ROOT / "README.md"
AGENTS = REPO_ROOT / "AGENTS.md"
CORE_VERSION = REPO_ROOT / "kits" / "core" / "VERSION"

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
DASH_RE = re.compile(r"[–—]")  # en dash / em dash (forbidden by house rule)


def read_pyproject_version() -> str:
    with PYPROJECT.open("rb") as fh:
        return tomllib.load(fh)["project"]["version"]


def compute_new_version(current: str, bump: str) -> str:
    if SEMVER_RE.match(bump):
        return bump  # explicit version
    m = SEMVER_RE.match(current)
    if not m:
        raise ValueError(f"current version {current!r} is not semver-like")
    major, minor, patch = (int(x) for x in m.groups())
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"bump must be major|minor|patch|X.Y.Z, got {bump!r}")


def bump_minor(version: str) -> str:
    m = SEMVER_RE.match(version)
    if not m:
        return version
    major, minor, _ = (int(x) for x in m.groups())
    return f"{major}.{minor + 1}.0"


def _replace(text: str, old: str, new: str, label: str, changes: list[str]) -> str:
    if old not in text:
        return text
    n = text.count(old)
    changes.append(f"{label}: {n}x {old!r} -> {new!r}")
    return text.replace(old, new)


def rewrite_pyproject(old_v: str, new_v: str, changes: list[str]) -> tuple[Path, str]:
    text = PYPROJECT.read_text(encoding="utf-8")
    text = _replace(
        text, f'version = "{old_v}"', f'version = "{new_v}"', "pyproject.toml", changes
    )
    return PYPROJECT, text


def rewrite_readme(
    old_v: str, new_v: str, date: str, changes: list[str]
) -> tuple[Path, str]:
    text = README.read_text(encoding="utf-8")
    text = _replace(
        text, f"version-{old_v}-blue", f"version-{new_v}-blue", "README badge", changes
    )
    text = _replace(
        text, f"copper-{old_v}.zip", f"copper-{new_v}.zip", "README zip refs", changes
    )
    # footer: "_Framework version : X.Y.Z (DD Mon YYYY)_"
    footer_re = re.compile(r"_Framework version : " + re.escape(old_v) + r" \([^)]*\)_")
    if footer_re.search(text):
        text = footer_re.sub(f"_Framework version : {new_v} ({date})_", text)
        changes.append(f"README footer: version {old_v} -> {new_v}, date -> {date}")
    return README, text


def rewrite_core_version(new_v: str, changes: list[str]) -> tuple[Path, str]:
    """The core plugin `cu` takes the release version (US-368 G1)."""
    changes.append(f"kits/core/VERSION -> {new_v}")
    return CORE_VERSION, f"{new_v}\n"


def rewrite_agents(date: str, changes: list[str]) -> tuple[Path, str]:
    text = AGENTS.read_text(encoding="utf-8")
    # AGENTS.md frontmatter version is on its own track: bump its MINOR.
    m = re.search(r"^version: '([0-9.]+)'", text, re.MULTILINE)
    if m:
        old_fm = m.group(1)
        new_fm = bump_minor(old_fm)
        text = text.replace(f"version: '{old_fm}'", f"version: '{new_fm}'", 1)
        changes.append(f"AGENTS.md frontmatter version: {old_fm} -> {new_fm}")
    text = re.sub(
        r"^last_updated: '[0-9-]+'",
        f"last_updated: '{date}'",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    changes.append(f"AGENTS.md last_updated -> {date}")
    return AGENTS, text


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Bump COPPER framework version (mechanical files)."
    )
    p.add_argument("bump", help="major | minor | patch | X.Y.Z")
    p.add_argument(
        "--date",
        default=None,
        help="Release date YYYY-MM-DD (required for reproducibility)",
    )
    p.add_argument(
        "--dry-run", action="store_true", help="Show changes without writing"
    )
    args = p.parse_args(argv)

    current = read_pyproject_version()
    try:
        new_v = compute_new_version(current, args.bump)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if new_v == current:
        print(
            f"error: new version {new_v} equals current; nothing to do", file=sys.stderr
        )
        return 2

    # The command passes the canonical date. Without one, a write is refused: it
    # used to write a TODO-SET-DATE placeholder into the release files (TD-201).
    if not args.date and not args.dry_run:
        print("error: pass --date YYYY-MM-DD (the release date)", file=sys.stderr)
        return 2
    date = args.date or "YYYY-MM-DD"

    changes: list[str] = []
    edits = [
        rewrite_pyproject(current, new_v, changes),
        rewrite_readme(current, new_v, date, changes),
        rewrite_agents(date, changes),
        rewrite_core_version(new_v, changes),
    ]

    # Guard: never introduce em/en dashes.
    for path, text in edits:
        if DASH_RE.search(text):
            # only fail if WE added one; check is best-effort - report which file.
            print(
                f"warning: {path.name} contains en/em dash (check it was pre-existing)",
                file=sys.stderr,
            )

    print(f"Version: {current} -> {new_v}  (date: {date})")
    for c in changes:
        print(f"  - {c}")

    if args.dry_run:
        print("\n[dry-run] no files written.")
        return 0

    for path, text in edits:
        path.write_text(text, encoding="utf-8")
    print("\nWritten. NEXT (owned by /cu-version-bump command, not this script):")
    print(f"  1. Add CHANGELOG.md [{new_v}] entry")
    print(f"  2. Add AGENTS.md changelog entry referencing 'Release v{new_v}'")
    print("  3. Run tests, then commit + tag + push (with confirmation gates).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
