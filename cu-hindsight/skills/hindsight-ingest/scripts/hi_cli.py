"""Command handlers for hindsight_ingest.py.

Every refusal is one line on stderr and exit status 1.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import hi_client
import hi_config
import hi_detectors
import hi_gate
import hi_plan
import hi_schedule
import hi_state
import hi_sync
import hi_walk

EXPECTED = (
    hi_config.ConfigError,
    hi_walk.ChunkRefused,
    hi_walk.WalkError,
    hi_gate.GateError,
    hi_client.ClientError,
    ValueError,
    OSError,
)
LOCKED = frozenset({"send", "sync", "forget", "import-state"})


@dataclass
class Ctx:
    vault: Path
    cfg: hi_config.Config
    state: hi_state.State
    environ: dict
    script: Path
    args: object
    ask: object = input
    resolver: object = None


def run(args, environ, script: Path, ask=input, resolver=None) -> int:
    try:
        vault = args.vault.resolve()
        cfg = hi_config.load(vault, hi_detectors.KNOWN)
        folder = hi_state.state_dir(cfg.bank, environ)
        if args.command not in LOCKED:
            return _dispatch(args, environ, script, ask, resolver, vault, cfg, folder)
        with hi_state.locked(folder):
            return _dispatch(args, environ, script, ask, resolver, vault, cfg, folder)
    except EXPECTED as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _dispatch(args, environ, script, ask, resolver, vault, cfg, folder) -> int:
    state = hi_state.State.load(folder, str(vault))
    ctx = Ctx(vault, cfg, state, environ, script, args, ask, resolver)
    return COMMANDS[args.command](ctx) or 0


def client(ctx: Ctx, need_bank: bool = True) -> hi_client.Client:
    kwargs = {"resolver": ctx.resolver} if ctx.resolver else {}
    c = hi_client.from_env(
        ctx.environ, ctx.cfg.allow_insecure_transport, ctx.cfg.timeout_s, **kwargs
    )
    if c.ep.scheme == "http":
        print(f"transport: plain http to a {c.ep.host_class} host (allowed)")
    if need_bank and ctx.cfg.bank not in hi_client.bank_ids(c):
        raise hi_client.ClientError(
            f"bank '{ctx.cfg.bank}' does not exist on the server; run init-bank"
        )
    return c


def report(chunk: str, header: str, plan: hi_plan.Plan, links=()) -> None:
    print(
        f"[{chunk}] {header}, redacted {len(plan.redacted)}, "
        f"secret-skipped {len(plan.secret)}, "
        f"other-skipped {len(plan.other)}"
    )
    for tag, rows in (
        ("REDACT ", plan.redacted),
        ("SECRET?", plan.secret),
        ("SKIP   ", plan.other),
    ):
        for note, reason in rows:
            print(f"  {tag} {note}  ({reason})")
    for link in links:
        print(f"  SKIP    {link.name}  (symlink, never followed)")


def cmd_chunks(ctx: Ctx) -> int:
    for name in hi_walk.chunk_names(ctx.vault, ctx.cfg):
        if name in hi_walk.RESERVED and name != hi_walk.ROOT_CHUNK:
            print(f"{name:<45}   (folder name is reserved: sent by sync only)")
            continue
        count = len(hi_walk.scan(ctx.vault, ctx.cfg, name)[0])
        print(f"{name:<45} {count:>5}")
    return 0


def cmd_check(ctx: Ctx) -> int:
    leaks = hi_gate.gitleaks_version()
    version, missing = hi_client.check(client(ctx, need_bank=False))
    print(f"server api {version}; gitleaks {leaks}")
    hi_state.log(ctx.state.folder, f"CHECK server api {version} gitleaks {leaks}")
    for path in missing:
        print(f"  MISSING {path}")
    return 1 if missing else 0


def cmd_dry_run(ctx: Ctx) -> int:
    files, links = hi_walk.scan(ctx.vault, ctx.cfg, ctx.args.chunk)
    plan = hi_plan.plan_files(ctx.vault, ctx.cfg, ctx.state, files)
    header = f"would send {len(plan.send)}, unchanged {plan.unchanged}"
    report(ctx.args.chunk, header, plan, links)
    return 0


def cmd_preview(ctx: Ctx) -> int:
    note = hi_walk.nfc(ctx.args.note.strip("/"))
    if hi_walk.id_blocked(note, ctx.cfg):
        raise hi_walk.ChunkRefused(
            f"refused: '{ctx.args.note}' is forbidden or excluded"
        )
    path = ctx.vault / note
    hops = [path, *path.parents[: len(path.relative_to(ctx.vault).parts) - 1]]
    if any(p.is_symlink() for p in hops) or not path.is_file():
        raise hi_walk.ChunkRefused(f"no such note (or a symlink): {ctx.args.note}")
    text = path.read_text(encoding="utf-8")
    redacted, _ = hi_detectors.redact(text, ctx.cfg.detectors)
    pairs = zip(text.splitlines(), redacted.splitlines(), strict=False)
    for n, (before, after) in enumerate(pairs, 1):
        if before != after:
            print(f"  L{n}: {after[:160]}")
    return 0


def cmd_send(ctx: Ctx) -> int:
    files, links = hi_walk.scan(ctx.vault, ctx.cfg, ctx.args.chunk)
    plan = hi_plan.plan_files(ctx.vault, ctx.cfg, ctx.state, files)
    result = hi_sync.send(client(ctx), ctx.cfg, ctx.state, plan, ctx.args.chunk)
    header = f"sent {result.sent}, failed {result.failed}, unchanged {plan.unchanged}"
    report(ctx.args.chunk, header, plan, links)
    stale = sum(note in ctx.state.notes for note, _ in plan.secret)
    if stale:  # send never deletes (BUG-018 S7)
        print(
            f"  {stale} SECRET? note(s) were sent before and are still on the server: "
            "run `sync` to purge them, then rotate the secret."
        )
    if result.error:
        print(f"stopped: {result.error}. Re-run the same command to resume.")
    return 1 if result.error else 0


def cmd_status(ctx: Ctx) -> int:
    folders: dict[str, int] = {}
    for note in ctx.state.notes:
        top = note.split("/")[0] if "/" in note else hi_walk.ROOT_CHUNK
        folders[top] = folders.get(top, 0) + 1
    print(
        f"bank {ctx.cfg.bank}: {len(ctx.state.notes)} notes sent from this machine; "
        f"state {ctx.state.folder}"
    )
    for top, count in sorted(folders.items()):
        print(f"  {top:<45} {count:>5}")
    return 0


def cmd_sync(ctx: Ctx) -> int:
    ok, here = hi_sync.host_matches(ctx.cfg.sync_host)
    if not ok:
        raise ValueError(
            f"refused: sync runs only on '{ctx.cfg.sync_host}', this host is '{here}'"
        )
    sp = hi_sync.plan_sync(ctx.vault, ctx.cfg, ctx.state)
    print(
        f"sync: send {len(sp.plan.send)}, delete {len(sp.deletes)}, "
        f"rename {len(sp.renames)}, purge {len(sp.purges)}"
        f", unchanged {sp.plan.unchanged}"
    )
    for note in sp.renames:
        print(f"  RENAME  {note}  (re-sent under its NFC id)")
    for note in sp.deletes:
        print(f"  DELETE  {note}")
    for note, reason in sp.purges:
        print(f"  PURGE   {note}  ({reason})")
    for note in sp.held_notes:
        print(f"  HELD    {note}  (not deleted)")
    if sp.held:
        print(f"  HELD    {sp.held}")
    if ctx.args.dry_run:
        report("sync", "dry run, nothing sent", sp.plan, sp.links)
        return 0
    return _apply_sync(ctx, sp)


def _apply_sync(ctx: Ctx, sp: hi_sync.SyncPlan) -> int:
    c = client(ctx)
    for note, reason in sp.purges:  # why it went, never what it held (BUG-018)
        hi_state.log(ctx.state.folder, f"PURGE {note} ({reason})")
    secret = any(reason == "secret" for _, reason in sp.purges)
    if secret:
        print(
            "  A secret was sent before: purging cleans the live bank only. The "
            "server's LLM provider and any backups may still hold it, so rotate it."
        )
    removed, error = hi_sync.delete(
        c, ctx.cfg, ctx.state, [n for n, _ in sp.purges] + sp.renames + sp.deletes
    )
    if not error:
        result = hi_sync.send(c, ctx.cfg, ctx.state, sp.plan, "sync")
        error = result.error
        hi_state.log(
            ctx.state.folder,
            f"SYNC sent {result.sent} removed {removed} held={bool(sp.held)}",
        )
    report("sync", f"removed {removed}", sp.plan, sp.links)
    if error:
        print(f"stopped: {error}. Re-run to resume.")
    # a secret purge needs a person to rotate: a nightly unit shows as failed
    return 1 if error or sp.held or secret else 0


def cmd_init_bank(ctx: Ctx) -> int:
    c = client(ctx, need_bank=False)
    if ctx.cfg.bank in hi_client.bank_ids(c):
        print(f"bank '{ctx.cfg.bank}' already exists")
        return 0
    if (
        ctx.ask(f"Create bank '{ctx.cfg.bank}'? Type its name to confirm: ").strip()
        != ctx.cfg.bank
    ):
        print("not created")
        return 1
    hi_client.create_bank(c, ctx.cfg.bank)
    print(f"bank '{ctx.cfg.bank}' created")
    return 0


def cmd_forget(ctx: Ctx) -> int:
    if ctx.args.all == bool(ctx.args.targets):
        raise ValueError("give note or folder targets, or --all (not both)")
    notes = (
        sorted(ctx.state.notes)
        if ctx.args.all
        else hi_sync.forget_targets(ctx.state, ctx.args.targets)
    )
    print(f"forget: {len(notes)} document(s) this tool sent to '{ctx.cfg.bank}'")
    if (
        ctx.args.all
        and ctx.ask("Type the bank name to delete them all: ").strip() != ctx.cfg.bank
    ):
        print("nothing deleted")
        return 1
    removed, error = hi_sync.delete(client(ctx), ctx.cfg, ctx.state, notes)
    print(f"deleted {removed}" + (f"; stopped: {error}" if error else ""))
    return 1 if error else 0


def cmd_schedule(ctx: Ctx) -> int:
    staging = ctx.state.folder / "schedule"
    files, commands = hi_schedule.stage(
        ctx.cfg.bank,
        ctx.script,
        ctx.vault,
        ctx.args.env_file,
        ctx.args.at,
        staging,
        python=sys.executable,
    )
    print(f"wrote {', '.join(sorted(files))} to {staging}; nothing was enabled.")
    print(
        f"Create {ctx.args.env_file} (mode 600) with {hi_client.URL_VAR}=... and "
        f"{hi_client.KEY_VAR}=..., then run:"
    )
    for line in commands:
        print(f"  {line}")
    return 0


def cmd_import_state(ctx: Ctx) -> int:
    pilot = hi_state.read_pilot_state(ctx.args.pilot_state)
    imported, left = hi_sync.import_pilot(ctx.vault, ctx.cfg, ctx.state, pilot)
    print(
        f"imported {imported} sent notes without sending; "
        f"{left} left for the next send or sync"
    )
    return 0


COMMANDS = {
    "chunks": cmd_chunks,
    "check": cmd_check,
    "dry-run": cmd_dry_run,
    "preview": cmd_preview,
    "send": cmd_send,
    "status": cmd_status,
    "sync": cmd_sync,
    "init-bank": cmd_init_bank,
    "forget": cmd_forget,
    "schedule": cmd_schedule,
    "import-state": cmd_import_state,
}
