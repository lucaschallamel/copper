#!/usr/bin/env python3
"""Install, remove or report the git pre-push guard in this repository (TD-206 AC9).

The pre-push hook is the primary control against a direct push to main (ADR-053
D14): git hands it the resolved remote refs on stdin, so it sees every route,
whatever command or tool started the push. The PreToolUse guards on Claude Code and
OpenCode are tripwires that refuse earlier and explain.

    guard_install.py install | uninstall | status

`install` writes `pre-push` where git looks for it (`git rev-parse --git-path
hooks/pre-push`, shared by linked worktrees) and never overwrites: an existing hook,
or `core.hooksPath` set by a hook manager (husky, lefthook), makes it refuse and
print the hook to add there. `uninstall` removes only a file whose content is
exactly what `install` writes. Standard library only. Exit codes: 0 done, 1 refused
(left as it was), 2 usage or not a git repository.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

MARKER = "# cu pre-push guard (TD-206)"
HOOK = f"""#!/bin/sh
{MARKER}: refuse a push that would update main, master or the remote's
# default branch. Added by the cu guard command (/cu:guard on Claude Code, /cu-guard on
# OpenCode): `install`, removed by `uninstall`.
# git feeds one line per ref: <local ref> <local sha> <remote ref> <remote sha>
set -f  # no glob in a branch name
# Every remote's default branch counts, whichever remote or URL is named: two remotes
# can share a URL, and only one may have its HEAD recorded.
defaults=
for r in $(git remote); do
  d=$(git symbolic-ref "refs/remotes/$r/HEAD" 2>/dev/null) || continue
  d=$(printf '%s' "${{d#refs/remotes/"$r"/}}" | tr '[:upper:]' '[:lower:]')
  defaults="$defaults $d"
done
status=0
while read -r _local_ref _local_sha remote_ref _remote_sha; do
  name=${{remote_ref#refs/heads/}}
  [ "$name" = "$remote_ref" ] && continue
  lower=$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')
  hit=
  for d in $defaults; do [ "$lower" = "$d" ] && hit=1; done
  if [ "$lower" = main ] || [ "$lower" = master ] || [ -n "$hit" ]; then
    echo "pre-push: refusing to push to $name directly (cu pre-push guard)." >&2
    echo "pre-push: push a feature branch and open a pull request." >&2
    status=1
  fi
done
exit $status
"""
USAGE = "usage: guard_install.py install | uninstall | status"
READ_LIMIT = 1 << 16  # a hook is a few lines; never read a planted large file whole
DELEGATE = "cu-pre-push-guard"  # the file _refuse recommends beside the user's hook


def _git(args: list[str]) -> str | None:
    done = subprocess.run(
        ["git", *args], capture_output=True, text=True, timeout=10, check=False
    )
    return done.stdout.strip() if done.returncode == 0 else None


def _hook_path() -> Path | None:
    path = _git(["rev-parse", "--git-path", "hooks/pre-push"])
    # abspath, never resolve(): a symlinked hook must not lead uninstall to its target
    return Path(os.path.abspath(path)) if path else None


def _managed() -> str | None:
    """Why the hook belongs to someone else, or None when it is free for us."""
    if _git(["config", "--get", "core.hooksPath"]):
        return "core.hooksPath is set (a hook manager such as husky or lefthook)"
    return None


def _read(path: Path) -> str | None:
    """A regular file's text, bounded: never a FIFO or a device (S5 audit)."""
    try:
        if not path.is_file():
            return None
        with path.open("rb") as f:
            return f.read(READ_LIMIT).decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def delegated(path: Path) -> bool:
    """The user's own hook calls our script, saved beside it as _refuse recommends."""
    text = _read(path)
    return bool(text) and DELEGATE in text and _read(path.parent / DELEGATE) == HOOK


def _refuse(reason: str) -> int:
    print(f"cu guard: not installed: {reason}. Nothing was changed.")
    print("To add it yourself: save the script below as its own file (for example")
    print(
        ".husky/cu-pre-push-guard) and make this the FIRST line of your pre-push hook:"
    )
    print('    sh .husky/cu-pre-push-guard "$@" || exit 1')
    print("It reads the refs git passes on stdin, so nothing before it may read them.")
    print("Do not paste it inline: its `exit` would end your hook.")
    print(HOOK)
    return 1


def install(path: Path) -> int:
    managed = _managed()
    if managed:
        return _refuse(managed)
    if path.exists() or path.is_symlink():
        if _read(path) == HOOK:
            print("cu guard: already installed in this repository.")
            return 0
        return _refuse(f"a pre-push hook already exists at {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "x", encoding="utf-8", newline="\n") as f:  # LF; never overwrite
        f.write(HOOK)
    os.chmod(path, 0o755)
    print(f"cu guard: installed at {path}: pushes to main, master and the remote's")
    print("default branch are refused for every route, not only the agent's commands.")
    return 0


def uninstall(path: Path) -> int:
    if not (path.exists() or path.is_symlink()):
        print("cu guard: not installed; nothing to remove.")
        return 0
    text = _read(path)
    if text == HOOK and not path.is_symlink():
        path.unlink()
        print(f"cu guard: removed {path}.")
        return 0
    changed = bool(text) and MARKER in text
    why = "it was changed after install" if changed else "it is not ours"
    if path.is_symlink():
        why = "it is a symbolic link, which install never writes; remove it yourself"
    print(f"cu guard: {path} left in place: {why}.")
    return 1


def status(path: Path) -> int:
    managed = _managed()
    text = _read(path)
    if text == HOOK:
        print(f"cu guard: installed at {path}.")
    elif delegated(path):
        print(f"cu guard: installed through your own hook, which calls {DELEGATE}.")
    elif text and MARKER in text:
        print(f"cu guard: installed at {path}, changed since install.")
    elif managed:
        print(f"cu guard: not installed: {managed}; add the hook there (see install).")
    elif text is not None or path.exists():
        print(f"cu guard: not installed: another pre-push hook is at {path}.")
    else:
        print("cu guard: not installed. Run /cu:guard install to add it.")
    return 0


def main(argv: list[str]) -> int:
    action = argv[1].strip() if len(argv) == 2 else ""
    actions = {"install": install, "uninstall": uninstall, "status": status}
    if action not in actions:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        path = _hook_path()
        if path is None:
            print("cu guard: not a git repository.", file=sys.stderr)
            return 2
        return actions[action](path)
    except (OSError, subprocess.TimeoutExpired) as exc:  # no git, or git hung
        print(f"cu guard: git could not run ({type(exc).__name__}).", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
