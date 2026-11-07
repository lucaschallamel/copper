"""The secret gate: notes that must not be sent at all (US-380 AC5).

1. gitleaks (local, redacted report) flags a note -> skipped and listed. It scans a
   private temporary copy of exactly the notes about to be sent, never the vault in
   place, so it cannot wander into forbidden folders or large attachments.
2. Private keys, API tokens and Luhn-valid card numbers -> skipped and listed. IBANs and
   payment references longer than any card number are removed before the card check.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

TOKEN_RE = (
    r"\b(sk-[A-Za-z0-9_-]{20,}|sk_(?:live|test)_[A-Za-z0-9]{16,}"
    r"|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}"
    r"|AKIA[0-9A-Z]{16}|xox[bpa]-[A-Za-z0-9-]{10,})"
)
SKIP_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("api-token", re.compile(TOKEN_RE)),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(api[_ -]?key|secret[_ -]?key|token)\s*[:=]\s*[A-Za-z0-9_\-]{16,}"
        ),
    ),
)
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?\b")
DIGIT_RUN_RE = re.compile(r"\d+(?:[ .-]\d+)*")
SEPARATOR_RE = re.compile(r"[ .-]")
CARD_MIN, CARD_MAX = 13, 19
# Groupings real cards are written in (Visa/Mastercard/Discover, Amex, Diners), and the
# leading digits card networks use. Anything else (decimals, timestamps, coordinates in
# drawings, reference numbers) is not tried, which keeps the Luhn check's one-in-ten
# chance from flagging ordinary numbers (measured on a real vault at S7).
CARD_LAYOUTS = ((4, 4, 4, 4), (4, 4, 4, 4, 3), (4, 6, 5), (4, 6, 4))
CARD_LEADS = "23456"


class GateError(Exception):
    """The gate cannot run (gitleaks missing or failing): nothing may be sent."""


def luhn_ok(digits: str) -> bool:
    total, parity = 0, len(digits) % 2
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == parity:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def secret_reason(text: str) -> str | None:
    """Why this (already redacted) text must not be sent, or None."""
    for label, pattern in SKIP_PATTERNS:
        if pattern.search(text):
            return label
    for run in DIGIT_RUN_RE.finditer(IBAN_RE.sub(" ", text)):
        groups = SEPARATOR_RE.split(run.group())
        if any(luhn_ok(c) for c in _candidates(groups) if c[0] in CARD_LEADS):
            return "card-number"
    return None


def _candidates(groups: list[str]):
    """Card-shaped digit strings in a run: one unbroken 13-19 digit group, or groups
    laid out as cards are written, starting at any group of the run."""
    for start, group in enumerate(groups):
        if CARD_MIN <= len(group) <= CARD_MAX:
            yield group
        for layout in CARD_LAYOUTS:
            window = groups[start : start + len(layout)]
            if tuple(len(g) for g in window) == layout:
                yield "".join(window)


def require_gitleaks() -> str:
    path = shutil.which("gitleaks")
    if not path:
        raise GateError("gitleaks not found on PATH; refusing to run without it")
    return path


def gitleaks_version() -> str:
    """The gitleaks version that gates the sends, for the run record (S5-4)."""
    try:
        out = subprocess.run(
            [require_gitleaks(), "version"], capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return (out.stdout.strip().splitlines() or ["unknown"])[0][:40]


def gitleaks_identity() -> str:
    """What the sends were judged by: the version text and a hash of the binary. Some
    builds print the same version text for every release (Arch 8.30.1: "version is set
    by build process"), so the text alone never changes on an upgrade (BUG-018 S4)."""
    binary = Path(require_gitleaks()).resolve()
    try:
        sha = hashlib.sha256(binary.read_bytes()).hexdigest()[:16]
    except OSError as exc:
        raise GateError(f"gitleaks unreadable ({type(exc).__name__})") from None
    return f"{gitleaks_version()}|{sha}"


def gitleaks_flagged(notes: dict[str, bytes]) -> dict[str, set[str]]:
    """Run gitleaks over a private copy of `notes` ({note id: the bytes that will be
    sent}); return {note id: rule ids}. The bytes, not the files: a note saved after it
    was read is not what gitleaks must judge (BUG-018 AC1). Each note gets its own
    numbered folder, so two ids that one file system folds together (`A.md`, `a.md` on
    a case-insensitive temp folder) are never written to the same file (BUG-018 S4)."""
    binary = require_gitleaks()
    if not notes:
        return {}
    names = list(notes)
    with tempfile.TemporaryDirectory(prefix="hindsight-gate-") as tmp:
        mirror = Path(tmp) / "m"
        for i, note in enumerate(names):
            dest = mirror / str(i) / note
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(notes[note])
        report = Path(tmp) / "report.json"
        _run(binary, mirror, report)
        return _parse(report, mirror, names)


def _run(binary: str, mirror: Path, report: Path) -> None:
    args = [
        binary,
        "dir",
        ".",
        "--no-banner",
        "--redact",
        "--exit-code",
        "0",
        "--log-level",
        "error",
        "--report-format",
        "json",
        "--report-path",
        str(report),
    ]
    try:
        subprocess.run(
            args, cwd=mirror, check=True, stdout=subprocess.DEVNULL, timeout=600
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GateError(
            f"gitleaks failed ({type(exc).__name__}); nothing sent"
        ) from None


def _parse(report: Path, mirror: Path, names: list[str]) -> dict[str, set[str]]:
    try:
        findings = json.loads(report.read_text() or "[]")
    except (OSError, json.JSONDecodeError):
        raise GateError("gitleaks report unreadable; nothing sent") from None
    flagged: dict[str, set[str]] = {}
    for finding in findings:
        name = finding.get("File")
        if not name:
            raise GateError("gitleaks finding without a file; nothing sent")
        path = Path(name) if Path(name).is_absolute() else mirror / name
        try:
            index = path.resolve().relative_to(mirror.resolve()).parts[0]
        except (ValueError, IndexError):  # outside the mirror, or the mirror itself
            index = ""
        if not index.isdigit() or int(index) >= len(names):
            raise GateError("gitleaks finding outside the mirror; nothing sent")
        flagged.setdefault(names[int(index)], set()).add(finding.get("RuleID", "?"))
    return flagged
