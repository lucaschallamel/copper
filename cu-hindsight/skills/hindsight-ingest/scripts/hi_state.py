"""What this machine has sent (US-380 AC8; per machine, Q28).

State lives in the user's state directory, one folder per bank, with the run log beside
it: `{note id: {"mtime": float, "sha256": hex, "rules": hex}}`, plus the vault it
belongs to. A note is re-sent when its outgoing (redacted) text changes; an unchanged
mtime skips the hashing only while the redaction rules (`rules`) are unchanged too.
Every id in state was sent by this tool, which is what lets sync delete only its own
documents (Q27). One run at a time holds the folder's lock; writes are atomic.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows: no scheduler support, no lock
    fcntl = None

APP = "hindsight-ingest"
STATE_FILE = "state.json"
LOG_FILE = "ingest.log"
LOCK_FILE = ".lock"
FORMAT = 1
PRIVATE = 0o700


def state_dir(
    bank: str,
    environ=os.environ,
    platform: str = sys.platform,
    home: Path | None = None,
) -> Path:
    home = home or Path.home()
    if platform == "darwin":
        base = home / "Library" / "Application Support"
    else:
        base = Path(environ.get("XDG_STATE_HOME") or home / ".local" / "state")
    return base / APP / bank


def private_dir(folder: Path) -> Path:
    """Create the folder readable by this user only: state and logs list note paths."""
    folder.mkdir(parents=True, exist_ok=True)
    folder.chmod(PRIVATE)
    return folder


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@contextlib.contextmanager
def locked(folder: Path):
    """Hold the state folder for one run; refuse if another run holds it."""
    private_dir(folder)
    with (folder / LOCK_FILE).open("w") as handle:
        if fcntl is not None:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise ValueError(
                    "another run is using this bank's state; try again when it ends"
                ) from None
        yield


class State:
    def __init__(self, folder: Path, vault: str = "") -> None:
        self.folder = folder
        self.path = folder / STATE_FILE
        self.vault = vault
        self.notes: dict[str, dict] = {}

    @classmethod
    def load(cls, folder: Path, vault: str = "") -> State:
        """Load, refusing state that belongs to another vault (two vaults, one bank)."""
        state = cls(folder, vault)
        try:
            raw = json.loads(state.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return state
        if not isinstance(raw, dict) or raw.get("format") != FORMAT:
            raise ValueError(f"{state.path}: not a {APP} state file (format {FORMAT})")
        owner = raw.get("vault", "")
        if vault and owner and owner != vault:
            raise ValueError(
                f"this bank's state belongs to the vault '{owner}', not '{vault}': "
                "one vault per bank"
            )
        state.notes = dict(raw.get("notes", {}))
        return state

    def save(self) -> None:
        private_dir(self.folder)
        body = {
            "format": FORMAT,
            "vault": self.vault,
            "notes": dict(sorted(self.notes.items())),
        }
        fd, tmp = tempfile.mkstemp(dir=self.folder, prefix=".state-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(body, ensure_ascii=False, indent=1))
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, self.path)

    def get(self, note: str) -> dict:
        return self.notes.get(note, {})

    def record(self, note: str, mtime: float, sha: str, rules: str = "") -> None:
        self.notes[note] = {"mtime": mtime, "sha256": sha, "rules": rules}

    def forget(self, note: str) -> None:
        self.notes.pop(note, None)


def log(folder: Path, line: str) -> None:
    private_dir(folder)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with (folder / LOG_FILE).open("a", encoding="utf-8") as fh:
        fh.write(f"{stamp} {line}\n")


def read_pilot_state(path: Path) -> dict[str, float]:
    """A pilot script's state file: `{vault-relative path: mtime}`."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not all(
        isinstance(v, (int, float)) for v in raw.values()
    ):
        raise ValueError(f"{path}: not a pilot state file ({{path: mtime}})")
    return {str(k): float(v) for k, v in raw.items()}
