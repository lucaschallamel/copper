"""Per-vault configuration: `<vault>/.hindsight-ingest.json` (US-380 AC1).

No config, no run. Required keys are `bank` and `forbidden`; every other key has a
default, and a key this module does not know is an error (a typo must not silently
disable a guard).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

CONFIG_NAME = ".hindsight-ingest.json"
BANK_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
REQUIRED = ("bank", "forbidden")
LIST_KEYS = ("forbidden", "pilot", "exclude_dirs", "exclude_files", "detectors", "tags")


class ConfigError(Exception):
    """The vault config is missing or invalid; `errors` lists every problem found."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


@dataclass(frozen=True)
class Config:
    bank: str
    forbidden: tuple[str, ...]
    pilot: tuple[str, ...] = ()
    exclude_dirs: tuple[str, ...] = ()
    exclude_files: tuple[str, ...] = ()
    detectors: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    batch_size: int = 5
    pause_s: float = 20.0
    timeout_s: float = 300.0
    max_chars: int = 200_000
    sync_host: str | None = None
    max_delete_ratio: float = 0.10
    allow_insecure_transport: bool = False
    include_drawings: bool = False


KNOWN_KEYS = frozenset(Config.__dataclass_fields__)


def load(vault: Path, known_detectors: tuple[str, ...]) -> Config:
    """Read and validate the vault's config; raise ConfigError listing every problem."""
    path = vault / CONFIG_NAME
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ConfigError(
            [f"no {CONFIG_NAME} in {vault}: this vault has not opted in"]
        ) from None
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(
            [f"{CONFIG_NAME}: unreadable ({type(exc).__name__})"]
        ) from None
    if not isinstance(raw, dict):
        raise ConfigError([f"{CONFIG_NAME}: must be a JSON object"])
    errors = _check(raw, known_detectors)
    if errors:
        raise ConfigError(errors)
    values = {k: (tuple(v) if k in LIST_KEYS else v) for k, v in raw.items()}
    return Config(**values)


def _check(raw: dict, known_detectors: tuple[str, ...]) -> list[str]:
    errors = [f"missing required key '{k}'" for k in REQUIRED if k not in raw]
    errors += [f"unknown key '{k}'" for k in sorted(set(raw) - KNOWN_KEYS)]
    if "bank" in raw and not (
        isinstance(raw["bank"], str) and BANK_RE.match(raw["bank"])
    ):
        errors.append("'bank' must be 1-64 characters: letters, digits, '.', '_', '-'")
    for key in LIST_KEYS:
        if key in raw and not _str_list(raw[key]):
            errors.append(f"'{key}' must be a list of non-empty strings")
    errors += _check_numbers(raw) + _check_paths(raw)
    unknown = [d for d in raw.get("detectors", []) if d not in known_detectors]
    if unknown and _str_list(raw.get("detectors")):
        errors.append(f"unknown detector(s) {unknown}; known: {list(known_detectors)}")
    return errors


def _check_numbers(raw: dict) -> list[str]:
    errors = []
    rules = {
        "batch_size": (int, 1, 100),
        "pause_s": ((int, float), 0, 3600),
        "timeout_s": ((int, float), 1, 3600),
        "max_chars": (int, 1, 10_000_000),
        "max_delete_ratio": ((int, float), 0, 1),
    }
    for key, (kind, low, high) in rules.items():
        value = raw.get(key)
        if key in raw and (isinstance(value, bool) or not isinstance(value, kind)):
            errors.append(f"'{key}' must be a number")
        elif key in raw and not low <= value <= high:
            errors.append(f"'{key}' must be between {low} and {high}")
    for flag in ("allow_insecure_transport", "include_drawings"):
        if flag in raw and not isinstance(raw[flag], bool):
            errors.append(f"'{flag}' must be true or false")
    if raw.get("sync_host") is not None and not (
        isinstance(raw["sync_host"], str) and raw["sync_host"]
    ):
        errors.append("'sync_host' must be a host name")
    return errors


PATH_KEYS = ("forbidden", "exclude_dirs", "pilot")


def _bad_path(rule: str) -> bool:
    """A folder rule that could silently match nothing: '.', '..', '\\', blanks."""
    parts = rule.strip("/").split("/")
    return "\\" in rule or any(p in ("", ".", "..") or p != p.strip() for p in parts)


def _check_paths(raw: dict) -> list[str]:
    errors = []
    for key in PATH_KEYS:
        values = raw.get(key, [])
        bad = [v for v in values if isinstance(v, str) and _bad_path(v)]
        if _str_list(values) and bad:
            errors.append(f"'{key}' has malformed folder rule(s) {bad}")
    files = raw.get("exclude_files", [])
    if _str_list(files) and any("/" in f or "\\" in f for f in files):
        errors.append("'exclude_files' takes file names, not paths")
    return errors


def _str_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) and v for v in value)
