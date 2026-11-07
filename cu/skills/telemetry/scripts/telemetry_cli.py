#!/usr/bin/env python3
"""cu-telemetry CLI : summary and health over the fallback-event JSONL.

Read-only consumers of the append-only sink written by ``telemetry_emitter.py``
(US-166). Neither command ever rewrites the sink (NFR-3).

Subcommands
-----------
summary [--days N] [--path P]
    Aggregate per-handler success rate, fall-through rate, mean latency, and
    error-class distribution into a human-readable table (AC4).

health [--days N] [--threshold T] [--path P]
    Flag handlers whose fall-through rate over the window exceeds the threshold
    (default 25% over 7 days) and recommend review (AC5). Exits non-zero when
    any handler is flagged, so it is usable as a CI gate.

Exit Codes
    0: ok / no handler flagged
    1: one or more handlers flagged (health only)
    2: script execution error

Usage
    uv run python .../telemetry/scripts/telemetry_cli.py summary --days 30
    uv run python .../telemetry/scripts/telemetry_cli.py health

Author: COPPER framework
Version: 1.0.0
Language: British English (en-AU)
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

# Import sibling resolver/constants without requiring a package install.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from telemetry_emitter import resolve_sink_path  # noqa: E402

DEFAULT_HEALTH_THRESHOLD = 0.25  # AC5: 25% fall-through
DEFAULT_HEALTH_DAYS = 7
EXIT_OK = 0
EXIT_FLAGGED = 1
EXIT_ERROR = 2


def load_records(path: Path | None) -> list[dict[str, Any]]:
    """Read all parseable JSONL records. Returns [] when sink is absent/disabled."""
    if path is None or not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # tolerate partial trailing writes
    return records


def _within_window(
    records: list[dict[str, Any]], days: int | None
) -> list[dict[str, Any]]:
    # `days is None` means "no window" (keep all); `--days 0` is an explicit
    # zero-day window and must NOT be conflated with no-window (M1).
    if days is None:
        return records
    cutoff = datetime.now(UTC) - timedelta(days=days)
    kept: list[dict[str, Any]] = []
    for rec in records:
        ts = rec.get("timestamp")
        if not ts:
            continue
        try:
            when = datetime.fromisoformat(ts)
        except ValueError:
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        if when >= cutoff:
            kept.append(rec)
    return kept


def _new_agg() -> dict[str, Any]:
    return {
        "total": 0,
        "success": 0,
        "fallthrough": 0,
        "error": 0,
        "latency_sum": 0,
        "errors": defaultdict(int),
    }


def _tally_record(agg: dict[str, Any], rec: dict[str, Any]) -> None:
    """Fold one record into a handler's running aggregate."""
    agg["total"] += 1
    outcome = rec.get("outcome", "")
    if outcome in ("success", "fallthrough", "error"):
        agg[outcome] += 1
    agg["latency_sum"] += int(rec.get("latency_ms", 0) or 0)
    ec = rec.get("error_class")
    if ec:
        agg["errors"][ec] += 1


def _finalise_rates(agg: dict[str, Any]) -> None:
    """Compute derived rate/mean metrics in place."""
    total = agg["total"] or 1
    agg["success_rate"] = agg["success"] / total
    agg["fallthrough_rate"] = agg["fallthrough"] / total
    agg["error_rate"] = agg["error"] / total
    agg["mean_latency_ms"] = agg["latency_sum"] / total


def aggregate(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Per-handler aggregates: counts, rates, mean latency, error distribution."""
    by_handler: dict[str, dict[str, Any]] = defaultdict(_new_agg)
    for rec in records:
        _tally_record(by_handler[rec.get("handler", "unknown")], rec)
    for agg in by_handler.values():
        _finalise_rates(agg)
    return dict(by_handler)


def cmd_summary(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser() if args.path else resolve_sink_path()
    records = _within_window(load_records(path), args.days)
    aggs = aggregate(records)
    if not aggs:
        print("No telemetry records found.")
        return EXIT_OK
    print(
        f"Fallback telemetry summary ({len(records)} records"
        + (f", last {args.days} days" if args.days else "")
        + ")"
    )
    header = (
        f"{'handler':<20} {'n':>5} {'succ%':>7} "
        f"{'fall%':>7} {'err%':>6} {'mean_ms':>8}  errors"
    )
    print(header)
    print("-" * 72)
    for handler in sorted(aggs):
        a = aggs[handler]
        errs = ", ".join(f"{k}:{v}" for k, v in sorted(a["errors"].items())) or "-"
        print(
            f"{handler:<20} {a['total']:>5} {a['success_rate'] * 100:>6.1f}% "
            f"{a['fallthrough_rate'] * 100:>6.1f}% {a['error_rate'] * 100:>5.1f}% "
            f"{a['mean_latency_ms']:>8.1f}  {errs}"
        )
    return EXIT_OK


def cmd_health(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser() if args.path else resolve_sink_path()
    records = _within_window(load_records(path), args.days)
    aggs = aggregate(records)
    flagged = {h: a for h, a in aggs.items() if a["fallthrough_rate"] > args.threshold}
    if not aggs:
        print("No telemetry records in window; nothing to assess.")
        return EXIT_OK
    if not flagged:
        print(
            f"All {len(aggs)} handler(s) healthy "
            f"(fall-through <= {args.threshold * 100:.0f}% over {args.days} days)."
        )
        return EXIT_OK
    print(
        f"FLAGGED: {len(flagged)} handler(s) exceed "
        f"{args.threshold * 100:.0f}% fall-through over {args.days} days:"
    )
    for handler in sorted(flagged):
        a = flagged[handler]
        print(
            f"  - {handler}: {a['fallthrough_rate'] * 100:.1f}% fall-through "
            f"({a['fallthrough']}/{a['total']}) - recommend review"
        )
    return EXIT_FLAGGED


def _add_summary_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("summary", help="Aggregate per-handler telemetry into a table.")
    p.add_argument(
        "--days", type=int, default=None, help="Restrict to the last N days."
    )
    p.add_argument("--path", type=str, default=None, help="Override sink path.")
    p.set_defaults(func=cmd_summary)


def _add_health_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("health", help="Flag handlers over the fall-through threshold.")
    p.add_argument(
        "--days",
        type=int,
        default=DEFAULT_HEALTH_DAYS,
        help=f"Window in days (default {DEFAULT_HEALTH_DAYS}).",
    )
    p.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_HEALTH_THRESHOLD,
        help=f"Fall-through rate threshold 0-1 (default {DEFAULT_HEALTH_THRESHOLD}).",
    )
    p.add_argument("--path", type=str, default=None, help="Override sink path.")
    p.set_defaults(func=cmd_health)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cu-telemetry", description="Fallback telemetry summary and health checks."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    _add_summary_parser(sub)
    _add_health_parser(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:  # pragma: no cover - defensive
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
