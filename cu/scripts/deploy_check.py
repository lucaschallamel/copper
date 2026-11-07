"""Core's check for a leftover deploy install beside the plugins (US-372 AC3).

Shipped as `scripts/deploy_check.py` with core's plugin only, imported by
`rules_guard.py`. A deploy left in the launch folder, a parent or `~/.claude` loads
the framework a second time beside the plugins, and Claude Code says nothing (S1
M3). The files read are untrusted project content: regular files only, at most
READ_LIMIT bytes, and the answer names categories of place, never a path or a name
from them (US-370 AC7, RQ16). Standard library only, like the guard.
"""

from __future__ import annotations

import json
import stat
from pathlib import Path

# Pinned by a test to `deploy.directive_merge` and `deploy.manifest`.
DEPLOY_MARKERS = (
    "<!-- COPPER:BEGIN (generated, do not edit) -->",
    "<!-- RAHAN:BEGIN (generated, do not edit) -->",
)
DEPLOY_MANIFESTS = (".copper-checksums.json", ".rahan-checksums.json")
DEPLOY_RECORDS = (".copper/kits", ".rahan/kits")
READ_LIMIT = 8 * 1024 * 1024


def _head(path: Path) -> bytes | None:
    """Up to READ_LIMIT bytes of a regular file, else None: never a FIFO (US-370 S4)."""
    try:
        # shortcut: stat then open, the same local race `_state` accepts.
        if not stat.S_ISREG(path.stat().st_mode):
            return None
        with path.open("rb") as f:
            return f.read(READ_LIMIT)
    except OSError:
        return None


def _tracks_claude(data: bytes) -> bool:
    """A manifest naming a Claude Code file; an unreadable one counts too."""
    try:
        files = json.loads(data).get("files")
    except (ValueError, AttributeError):
        return True
    if not isinstance(files, dict):
        return True
    return any(k.startswith(".claude/") or k == "CLAUDE.md" for k in files)


def _deployed(folder: Path) -> bool:
    """A deploy's manifest, `CLAUDE.md` block or Claude Code kit record in `folder`."""
    for name in DEPLOY_MANIFESTS:
        data = _head(folder / name)
        if data is not None and _tracks_claude(data):
            return True
    data = _head(folder / "CLAUDE.md") or b""
    if any(marker.encode() in data for marker in DEPLOY_MARKERS):
        return True
    for state in DEPLOY_RECORDS:
        try:
            if any((folder / state).glob("*.claude-code.install.json")):
                return True
        except OSError:
            continue
    return False


def _deploy_places(root: Path, env: dict) -> list[str]:
    """Where Claude Code would load a deploy from, as categories, never paths."""
    places = ["this project"] if _deployed(root) else []
    if any(_deployed(parent) for parent in root.parents):
        places.append("a parent folder")
    if _deployed(Path(env.get("HOME") or Path.home()) / ".claude"):
        places.append("~/.claude")
    return places


def leftover(root: Path, env: dict) -> tuple[str, str] | None:
    """The guard's context line and notice, or None when no deploy is loaded."""
    places = _deploy_places(root, env)
    if not places:
        return None
    where = ", ".join(places)
    also = " (add --global for ~/.claude)" if "~/.claude" in places else ""
    return (
        f"A COPPER deploy install is also loaded from {where}: Claude Code reads the "
        "framework twice, from it and from the plugins. To fix: run `deploy "
        f"--migrate-to-plugin` from your COPPER checkout{also}. It keeps any file you "
        "edited and lists it: review those files, then delete them.",
        f"COPPER deploy install also loaded from {where}: run deploy "
        f"--migrate-to-plugin{also}, then delete the files it keeps",
    )
