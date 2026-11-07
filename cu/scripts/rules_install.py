"""Install, uninstall or report a plugin's rules in a project (US-369, ADR-053 D2).

Shipped as `scripts/rules_install.py` in every plugin with rules, run by
`bin/<plugin>-rules`. Standard library only: the plugin cache has no `deploy` package
(AC9). Records use `deploy/kit/install_record.py`'s format, pinned by a test (AC2).
Rules land in `.claude/rules/<plugin>/`, staged outside `.claude/rules/` (which Claude
Code loads), swapped in by two renames that undo on failure, record last (AC3). Only
record-listed, unmodified files are replaced or removed; the rest is carried over.
The record and the project tree are untrusted input: a recorded path that is not one
of our rule files, or a symlink on the way to one, refuses (S4 C1, H1).
"""

# Runs on the adopter's Python 3.8+: no pyupgrade to datetime.UTC (3.11+); tested.
# ruff: noqa: UP017
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

HOST = "claude-plugin"
STATE_DIR = ".copper/kits"
RECORD_SUFFIX = f".{HOST}.install.json"
ACTIONS = ("install", "uninstall", "status")
FLAGS = {"--local": "install", "--backup": "install"}
SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SAFE_RULE = re.compile(r"^[\w.-]+\.md$")
DONE, REFUSED, FAILED = 0, 1, 2


class RulesError(Exception):
    """A refusal the user can act on; the message names what and why."""


def parse_args(argv: list[str]) -> tuple[str, set[str]]:
    """Split the quoted `"$ARGUMENTS"` word; allowlisted words only, no path (AC6)."""
    words = [w for arg in argv for w in arg.split()]
    action = words.pop(0) if words else "status"
    if action not in ACTIONS:
        raise RulesError(f"unknown action '{action}' (use {' | '.join(ACTIONS)})")
    flags = set(words)
    for flag in flags:
        if FLAGS.get(flag) != action:
            raise RulesError(f"'{flag}' is not an option of '{action}'")
    return action, flags


def project_root(env: dict[str, str]) -> Path:
    """`CLAUDE_PROJECT_DIR`, else the working directory; never an argument (AC6).
    Never git's top level: the hook has `CLAUDE_PROJECT_DIR`, the Bash tool does not
    (measured, US-370 S4), and both start in the launch folder, so they agree."""
    root = Path(env.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
    if not root.is_dir():
        raise RulesError(f"project root {root} is not a directory")
    return root


def plugin_identity(plugin_root: Path) -> tuple[str, str]:
    manifest = plugin_root / ".claude-plugin" / "plugin.json"
    try:
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        name, version = meta.get("name", ""), meta.get("version", "")
    except (ValueError, AttributeError) as exc:
        raise RulesError(f"{manifest} is not a plugin manifest: {exc}") from exc
    if not isinstance(name, str) or not SAFE_NAME.match(name) or not version:
        raise RulesError(f"plugin.json names no usable plugin ('{name}', '{version}')")
    return name, str(version)


def source_rules(plugin_root: Path) -> dict[str, bytes]:
    """The plugin's rule files, by name; a symlink or odd name is refused [IV]."""
    rules = {}
    for path in sorted((plugin_root / "rules").iterdir()):
        if path.is_symlink() or not SAFE_RULE.match(path.name):
            raise RulesError(f"refusing plugin rule entry {path.name}")
        if path.is_file():
            rules[path.name] = path.read_bytes()
    if not rules:
        raise RulesError(f"the plugin ships no rules under {plugin_root / 'rules'}")
    return rules


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


class Project:
    """Where one plugin's rules, record and scratch folders live in a project."""

    def __init__(self, root: Path, plugin: str) -> None:
        self.root, self.plugin = root, plugin
        self.rel = f".claude/rules/{plugin}"
        self.dest = root / ".claude" / "rules" / plugin
        self.record = root / STATE_DIR / f"{plugin}{RECORD_SUFFIX}"
        self.lock = root / ".claude" / f".rules-lock-{plugin}"
        # Unique per run: an undeletable leftover must not block the next rename.
        tag = f"{plugin}-{os.getpid()}-{os.urandom(3).hex()}"
        self.staging = root / ".claude" / f".rules-staging-{tag}"
        self.old = root / ".claude" / f".rules-old-{tag}"

    def guard(self) -> None:
        """Refuse a symlink anywhere on the way to what we write (S4 H1)."""
        # shortcut: checked once, not before every write, so a writer racing this run
        # could still swap in a symlink; that writer already controls the project.
        # Upgrade to dir fds + O_NOFOLLOW if this ever runs with more privilege.
        claude, copper = self.root / ".claude", self.root / ".copper"
        on_the_way = (claude, claude / "rules", self.dest, copper, copper / "kits")
        for path in (*on_the_way, self.record):
            if path.is_symlink():
                raise RulesError(f"{path.relative_to(self.root)} is a symlink")

    def leftovers(self) -> list[Path]:
        kinds = ("staging", "old")
        return [
            p
            for k in kinds
            for p in self.root.glob(f".claude/.rules-{k}-{self.plugin}-*")
        ]

    def read(self) -> dict | None:
        """The record, validated, or None. Every recorded path must be one of our
        rule files (S4 C1): unreadable or anything else refuses, never skips."""
        if not self.record.is_file():
            return None
        prefix = self.rel + "/"
        try:
            data = json.loads(self.record.read_text(encoding="utf-8"))
            files = {f["path"]: f["checksum"] for f in data["files"]}
            data["version"] = str(data["version"])
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise RulesError(f"cannot read {self.record}: {exc}") from exc
        for path, checksum in files.items():
            ours = isinstance(path, str) and path.startswith(prefix)
            name = path[len(prefix) :] if ours else ""
            if not SAFE_RULE.match(name) or not isinstance(checksum, str):
                raise RulesError(f"{self.record} names a path that is not ours: {path}")
        data["owned"] = {p[len(prefix) :]: c for p, c in files.items()}
        return data

    def live(self, name: str) -> bytes | None:
        path = self.dest / name
        if path.is_symlink():
            raise RulesError(f"refusing to touch symlink {self.rel}/{name}")
        return path.read_bytes() if path.is_file() else None


def stale(lock: Path) -> bool:
    """A lock whose process is gone (a hard kill), on POSIX only: on Windows
    `os.kill(pid, 0)` would signal the process, not probe it (ponytail 2)."""
    if os.name != "posix" or not lock.is_file():
        return False
    try:
        os.kill(int(lock.read_text(encoding="utf-8").strip()), 0)
    except ProcessLookupError:
        return True
    except (ValueError, OSError):
        return False  # unreadable, or alive under another user: keep the lock
    return False


@contextmanager
def locked(project: Project):
    """One run at a time: recovery must never touch a live run's folders (S4 M3)."""
    project.lock.parent.mkdir(parents=True, exist_ok=True)
    if stale(project.lock):
        os.unlink(project.lock)
    try:
        fd = os.open(project.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RulesError(
            f"{project.lock.relative_to(project.root)} exists: another run is going, "
            "or a killed one left it; delete it if no install is running"
        ) from None
    with os.fdopen(fd, "w") as fh:
        fh.write(f"{os.getpid()}\n")
    try:
        yield
    finally:
        os.unlink(project.lock)


def was_local(record: dict | None) -> bool:
    return bool(record and (record.get("source") or {}).get("local") is True)


def modified(project: Project, rules: dict[str, bytes], owned: dict[str, str]):
    """Files edited since install, or unrecorded and different (clone rule): ours to
    neither overwrite nor drop."""
    out = []
    for name in sorted(set(rules) | set(owned)):
        data = project.live(name)
        if data is not None and data != rules.get(name):
            if name not in owned or digest(data) != owned[name]:
                out.append(name)
    return out


def remove(path: Path) -> None:
    """Best-effort delete of a scratch folder: a leftover is reported, never fatal
    (S4 H2: Windows refuses to delete a read-only or open file)."""
    try:
        shutil.rmtree(path)
    except OSError as exc:
        print(f"could not remove {path.name} ({exc}); the next install retries")


def recover(project: Project) -> None:
    """Undo a killed run: restore the old folder if the live one is gone (AC3)."""
    for path in project.leftovers():
        if path.name.startswith(".rules-old-") and not project.dest.exists():
            os.rename(path, project.dest)
        else:
            remove(path)


def stage(project, rules, owned, conflicts, stamp) -> None:
    """Build the new folder; live files are COPIED so a failed swap loses none (AC3)."""
    project.staging.mkdir(parents=True)
    for name, data in rules.items():
        (project.staging / name).write_bytes(data)
    if not project.dest.is_dir():
        return
    for path in sorted(project.dest.iterdir()):
        if path.name in conflicts and path.name in rules:
            target = f"{path.name}.bak-{stamp}"  # not *.md: never loaded
        elif path.name in rules or (path.name in owned and path.name not in conflicts):
            continue  # replaced, or ours, unmodified and no longer shipped
        else:
            target = path.name  # the user's own file, or an edit no longer shipped
        if path.is_dir() and not path.is_symlink():
            shutil.copytree(path, project.staging / target, symlinks=True)
        else:
            shutil.copy2(path, project.staging / target, follow_symlinks=False)


def swap(project: Project) -> None:
    """Two renames, undone on failure: Windows cannot rename over a folder."""
    had = project.dest.exists()
    project.dest.parent.mkdir(parents=True, exist_ok=True)
    if had:
        os.rename(project.dest, project.old)
    try:
        os.rename(project.staging, project.dest)
    except OSError:
        if had:
            os.rename(project.old, project.dest)
        raise
    if had:
        remove(project.old)


def keep_out_of_git(copper: Path) -> None:
    """`.copper/` holds install state only. Deploy never edits a project's
    `.gitignore`, so a folder this run created ignores itself (US-374 AC4).
    Exclusive create: a file or link already at the name is left alone (BUG-019)."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(copper / ".gitignore", flags, 0o666)
    except FileExistsError:
        return
    with os.fdopen(fd, "wb") as handle:
        handle.write(b"*\n")


def write_record(project: Project, version: str, rules, local: bool) -> None:
    """install_record.write_record's payload, renamed into place last (AC2, AC3)."""
    payload = {
        "kit": project.plugin,
        "version": version,
        "host": HOST,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "source": {"type": "claude-plugin", "local": local},
        "dependencyKits": [],
        "files": [
            {"path": f"{project.rel}/{n}", "writeMode": "create", "checksum": digest(d)}
            for n, d in sorted(rules.items())
        ],
        "host_config_deltas": [],
        "arbitration": "",
        "arbitratedFrom": "",
        "namespace": "",
        "removedOnUpgrade": [],
    }
    copper = project.root / ".copper"
    new_folder = not copper.exists()
    project.record.parent.mkdir(parents=True, exist_ok=True)
    if new_folder:
        keep_out_of_git(copper)
    # Created fresh, so a link planted at the name is refused, never written through
    # (BUG-019). Inline: this script ships in a plugin and imports nothing of ours.
    tag = f"{os.getpid()}.{os.urandom(4).hex()}"  # unguessable, so a link cannot wait
    tmp = project.record.with_name(f"{project.record.name}.{tag}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    fd = os.open(tmp, flags, 0o666)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(payload, indent=2) + "\n")
        os.replace(tmp, project.record)
    except BaseException:
        tmp.unlink()
        raise


def _git(root: Path, *args: str) -> str:
    try:
        done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    except OSError as exc:
        raise RulesError(f"--local needs git ({exc})") from exc
    if done.returncode:
        raise RulesError("--local needs a git work tree (git rev-parse failed)")
    return done.stdout.strip()


def _exclude(project: Project) -> tuple[Path, str, str]:
    """The exclude file, our line in it, and its current text."""
    top = Path(_git(project.root, "rev-parse", "--show-toplevel")).resolve()
    where = _git(project.root, "rev-parse", "--git-path", "info/exclude")
    exclude = (project.root / where).resolve()
    line = "/" + project.dest.relative_to(top).as_posix() + "/"
    return (
        exclude,
        line,
        exclude.read_text(encoding="utf-8") if exclude.is_file() else "",
    )


def git_exclude(project: Project, found: tuple[Path, str, str]) -> None:
    """Add the rules folder to the local git exclude once (AC4 `--local`); `found`
    is looked up before any write, so a missing git refuses first (ponytail 1)."""
    exclude, line, text = found
    if line not in text.splitlines():
        exclude.parent.mkdir(parents=True, exist_ok=True)
        sep = "" if not text or text.endswith("\n") else "\n"
        exclude.write_text(f"{text}{sep}{line}\n", encoding="utf-8")
    if _git(project.root, "ls-files", "--", project.rel):
        print(f"note: {project.rel}/ is already tracked by git; --local cannot hide it")


def drop_exclude(project: Project) -> None:
    """Remove our exclude line, so a committed install is not silently ignored (M1)."""
    try:
        exclude, line, text = _exclude(project)
    except RulesError as exc:
        print(f"note: could not drop the --local git exclude ({exc})")
        return
    kept = [entry for entry in text.splitlines() if entry != line]
    if len(kept) != len(text.splitlines()):
        exclude.write_text("".join(f"{entry}\n" for entry in kept), encoding="utf-8")


def install_rules(project: Project, plugin_root: Path, flags: set[str]) -> int:
    _, version = plugin_identity(plugin_root)
    rules = source_rules(plugin_root)
    found = _exclude(project) if "--local" in flags else None
    recover(project)
    record = project.read()
    owned = record["owned"] if record else {}
    conflicts = modified(project, rules, owned)
    if conflicts and "--backup" not in flags:
        listing = ", ".join(f"{project.rel}/{n}" for n in conflicts)
        raise RulesError(
            f"locally modified: {listing}. Nothing changed; --backup "
            "keeps them as *.bak-<time> and installs."
        )
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stage(project, rules, owned, set(conflicts), stamp)
    swap(project)
    if found:
        git_exclude(project, found)
    elif was_local(record):
        drop_exclude(project)
    write_record(project, version, rules, "--local" in flags)
    print(f"installed {len(rules)} rules ({project.plugin} {version}): {project.rel}/")
    for name in conflicts:
        print(f"kept your edit as {project.rel}/{name}.bak-{stamp}")
    return DONE


def uninstall_rules(project: Project) -> int:
    record = project.read() or {"owned": {}}
    for name, checksum in record["owned"].items():
        data = project.live(name)
        if data is not None and digest(data) == checksum:
            (project.dest / name).unlink()
        elif data is not None:
            print(f"kept (modified): {project.rel}/{name}")
    if project.dest.is_dir() and not any(project.dest.iterdir()):
        project.dest.rmdir()
    if was_local(record):
        drop_exclude(project)
    project.record.unlink()
    print(f"uninstalled {project.plugin} rules from {project.rel}/")
    return DONE


def show_status(project: Project, plugin_root: Path) -> int:
    _, version = plugin_identity(plugin_root)
    record = project.read()
    if record is None:
        present = project.dest.is_dir() and any(project.dest.glob("*.md"))
        state = "present, no record (from another checkout)" if present else "absent"
        print(f"{project.plugin} rules: {state}")
        return DONE
    print(f"{project.plugin} rules: installed {record['version']} (plugin {version})")
    # Ownership, not integrity: that is the plugin's signed copy (ADR-053 D8, US-370).
    print("  checked against this project's record, not the plugin's signed copy")
    if not record["owned"]:
        print("  the record lists no files")
    for name, checksum in sorted(record["owned"].items()):
        data = project.live(name)
        if data is None or digest(data) != checksum:
            verdict = "missing" if data is None else "modified"
            print(f"  {verdict}: {project.rel}/{name}")
    for path in project.leftovers():
        print(f"  interrupted run left {path.name} (the next install recovers it)")
    return DONE


def run(action: str, flags: set[str], project: Project, plugin_root: Path) -> int:
    project.guard()
    if action == "status":
        return show_status(project, plugin_root)
    if action == "uninstall" and not project.record.is_file():
        print(f"no install record for {project.plugin}: nothing removed")
        return DONE
    with locked(project):
        if action == "install":
            return install_rules(project, plugin_root, flags)
        return uninstall_rules(project)


def main(argv: list[str], env: dict[str, str], plugin_root: Path) -> int:
    try:
        action, flags = parse_args(argv)
        name, _ = plugin_identity(plugin_root)
        return run(action, flags, Project(project_root(env), name), plugin_root)
    except RulesError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return REFUSED
    except OSError as exc:
        print(f"failed: {exc}", file=sys.stderr)
        return FAILED


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], dict(os.environ), Path(__file__).resolve().parents[1]))
