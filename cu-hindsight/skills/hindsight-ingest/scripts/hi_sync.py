"""Sending, syncing and forgetting (US-380 AC7c, AC8, AC9, AC11-AC14).

Deletes touch only documents this tool sent: ids recorded in this machine's state,
which were all written with `metadata.source` set to `hi_plan.SOURCE` (Q27;
`obsidian-vault` before 2026-10-13). Every other document in the bank is left alone.
State is saved after each batch, so an interrupted run resumes where it stopped.
"""

from __future__ import annotations

import socket
import time
from dataclasses import dataclass, field
from pathlib import Path

import hi_client
import hi_plan
import hi_walk
from hi_state import State, digest, log


@dataclass
class Sent:
    sent: int = 0
    failed: int = 0
    error: str = ""
    operations: list[str] = field(default_factory=list)


@dataclass
class SyncPlan:
    plan: hi_plan.Plan
    deletes: list[str] = field(default_factory=list)
    purges: list[tuple[str, str]] = field(default_factory=list)
    renames: list[str] = field(default_factory=list)
    held: str = ""
    held_notes: list[str] = field(default_factory=list)
    links: list[Path] = field(default_factory=list)


def send(
    client, cfg, state: State, plan: hi_plan.Plan, chunk: str, sleep=time.sleep
) -> Sent:
    """Send in throttled batches; stop at the first error (fail closed, resumable)."""
    result = Sent()
    for start in range(0, len(plan.send), cfg.batch_size):
        batch = plan.send[start : start + cfg.batch_size]
        try:
            op = hi_client.retain(
                client, cfg.bank, [hi_plan.item(n, cfg, chunk) for n in batch]
            )
        except hi_client.ClientError as exc:
            result.failed, result.error = len(plan.send) - result.sent, str(exc)
            log(state.folder, f"FAIL {chunk} batch@{start} {exc}")
            break
        for n in batch:
            state.record(n.note, n.mtime, n.sha256, n.rules)
        state.save()
        result.sent += len(batch)
        result.operations.append(op)
        log(
            state.folder,
            f"OK   {chunk} batch@{start} {len(batch)} notes operation={op}",
        )
        if start + cfg.batch_size < len(plan.send):
            sleep(cfg.pause_s)
    return result


def host_matches(
    sync_host: str | None, hostname: str | None = None
) -> tuple[bool, str]:
    here = (hostname or socket.gethostname()).split(".")[0].lower()
    if sync_host is None:
        return True, here
    return sync_host.split(".")[0].lower() == here, here


def plan_sync(vault: Path, cfg, state: State, flagged=None, version=None) -> SyncPlan:
    """Plan a sync. A folder that cannot be read raises WalkError, so nothing is
    deleted on a partial view of the vault (fail closed)."""
    files, links, present = hi_walk.scan_all(vault, cfg)
    kwargs = {k: v for k, v in (("flagged", flagged), ("version", version)) if v}
    result = SyncPlan(hi_plan.plan_files(vault, cfg, state, files, **kwargs))
    result.links = links
    for note in sorted(state.notes):
        reason = hi_walk.id_blocked(note, cfg)
        if reason:
            result.purges.append((note, reason))
        elif note not in present:
            renamed = hi_walk.nfc(note) != note and hi_walk.nfc(note) in present
            (result.renames if renamed else result.deletes).append(note)
    # A non-NFC id whose NFC form is present is a rename, not a loss: never held.
    known = len(state.notes) - len(result.purges) - len(result.renames)
    # A sent note that is secret now (an edit, a gitleaks upgrade, new rules) leaves the
    # server too, not only the queue (BUG-018 AC2); it is re-sent once it is clean. Not
    # held by the ratio guard (that would keep a secret on the server), and not taken
    # out of `known`: the note is present, so it still counts against missing ones.
    result.purges += [(n, "secret") for n, _ in result.plan.secret if n in state.notes]
    if result.deletes and len(result.deletes) > cfg.max_delete_ratio * max(known, 1):
        result.held = (
            f"{len(result.deletes)} of {known} sent notes look missing, above "
            f"max_delete_ratio {cfg.max_delete_ratio:.0%}: deleting nothing"
        )
        result.held_notes, result.deletes = result.deletes, []
    return result


def delete(client, cfg, state: State, notes: list[str]) -> tuple[int, str]:
    """Delete documents this tool sent; stop at the first error.

    Returns (count, error)."""
    done = 0
    for note in notes:
        if note not in state.notes:
            continue  # never ours (Q27)
        try:
            hi_client.delete_document(client, cfg.bank, note)
        except hi_client.ClientError as exc:
            log(state.folder, f"FAIL delete {note} {exc}")
            return done, str(exc)
        state.forget(note)
        state.save()
        log(state.folder, f"DEL  {note}")
        done += 1
    return done, ""


def forget_targets(state: State, targets: list[str]) -> list[str]:
    """The sent ids under each target (a note id or a folder prefix), NFC-normalised."""
    wanted = [hi_walk.nfc(t.strip("/")) for t in targets]
    return sorted(
        n for n in state.notes if any(n == w or n.startswith(w + "/") for w in wanted)
    )


def import_pilot(
    vault: Path, cfg, state: State, pilot: dict[str, float]
) -> tuple[int, int]:
    """Seed state from a pilot state file without sending (AC8). Every pilot id was
    sent, so every one becomes ours: unchanged notes are imported as sent; the rest
    are recorded with no text hash, so the next sync re-sends a changed note, deletes
    a vanished one (behind the ratio guard), purges an out-of-scope one, and renames a
    non-NFC id. Every imported note is re-scanned by the next sync. Returns (imported,
    left to sync)."""
    imported = 0
    for raw_path, mtime in pilot.items():
        text = _unchanged_text(vault, cfg, raw_path, mtime)
        if text is None:
            state.record(raw_path, mtime, "")
            continue
        # No rules fingerprint: the pilot never ran gitleaks, so the next sync re-scans
        # each note once and re-sends only what changed (BUG-018 AC5).
        state.record(raw_path, mtime, digest(text), "")
        imported += 1
    state.save()
    return imported, len(pilot) - imported


def _unchanged_text(vault: Path, cfg, raw_path: str, mtime: float) -> str | None:
    """The outgoing text of a pilot note still in scope and untouched, else None."""
    path = vault / raw_path
    if raw_path != hi_walk.nfc(raw_path) or hi_walk.id_blocked(raw_path, cfg):
        return None
    if path.is_symlink() or not path.is_file() or path.stat().st_mtime != mtime:
        return None
    return hi_plan.outgoing(path, cfg)[0]
