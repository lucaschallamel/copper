#!/usr/bin/env python3
"""Ingest an Obsidian vault into its own Hindsight bank (US-380). Standard library only.

  python3 -I hindsight_ingest.py [--vault PATH] <command>

Local only (no network): chunks, dry-run <chunk>, preview <note>, status, schedule,
import-state. Network: check, init-bank, send <chunk>, sync [--dry-run], forget
<note|folder>... | --all. Credentials: HINDSIGHT_URL and HINDSIGHT_API_KEY from the
environment, never printed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python3 -I` does not add it

import argparse  # noqa: E402
import os  # noqa: E402

import hi_cli  # noqa: E402


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hindsight_ingest.py", description=__doc__.splitlines()[0]
    )
    p.add_argument(
        "--vault", type=Path, default=Path.cwd(), help="vault root (default: here)"
    )
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("chunks", "check", "status", "init-bank"):
        sub.add_parser(name)
    for name in ("dry-run", "send"):
        sub.add_parser(name).add_argument("chunk")
    sub.add_parser("preview").add_argument("note")
    sync = sub.add_parser("sync")
    sync.add_argument("--dry-run", action="store_true")
    forget = sub.add_parser("forget")
    forget.add_argument("targets", nargs="*")
    forget.add_argument("--all", action="store_true")
    schedule = sub.add_parser("schedule")
    schedule.add_argument("--at", default="02:30")
    schedule.add_argument(
        "--env-file",
        type=Path,
        default=Path.home() / ".config" / "hindsight-ingest" / "env",
    )
    sub.add_parser("import-state").add_argument("pilot_state", type=Path)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return hi_cli.run(args, os.environ, Path(__file__).resolve())


if __name__ == "__main__":
    sys.exit(main())
