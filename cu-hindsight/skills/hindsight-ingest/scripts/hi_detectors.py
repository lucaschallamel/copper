"""Redaction before send (US-380 AC5, AC6), shared with the US-381 hooks.

Password/PIN phrases are always redacted. National identifiers and IBANs are masked only
when the vault names their detector in `detectors` (opt-in, Q9 and Q25). Redaction keeps
the note: the masked text is what gets sent. Notes that must not be sent at all are the
gate's job (hi_gate).
"""

from __future__ import annotations

import re
from collections.abc import Callable

LABELS = r"password|passwd|pwd|mot de passe|mdp|passcode|code secret|code pin"
PASSWORD_RE = re.compile(rf"(?i)\b({LABELS})\b[^\n]*|\bPIN\s*[:=][^\n]*")
# A label alone on its line: the secret is on the next non-empty line.
LABEL_LINE_RE = re.compile(
    rf"(?im)^([ \t]*(?:{LABELS}|pin)[ \t]*:?[ \t]*\n)(\s*)([^\n]+)"
)
# French NIR: sex, YY, MM, department (incl. 2A/2B), commune, order, optional key.
NIR_RE = re.compile(
    r"\b[12][ .]?\d{2}[ .]?(?:0[1-9]|1[0-2]|[2-9]\d)[ .]?(?:\d{2}|2[ABab])"
    r"[ .]?\d{3}[ .]?\d{3}(?:[ .]?\d{2})?\b"
)
NIR_NOT_AFTER = re.compile(r"(?i)(facture|invoice|r[ée]f[ée]rence|\bref\b|\bréf\b)")
NIR_LOOKBEHIND = 30
CODE_GLUE = (
    "./-_#"  # a digit run glued to these is part of a code or filename, not a NIR
)
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?\b")

PASSWORD = "password"
FR_NIR = "fr-nir"
IBAN = "iban"


def _passwords(text: str) -> tuple[str, int]:
    text, below = LABEL_LINE_RE.subn(r"\1\2[REDACTED]", text)
    text, inline = PASSWORD_RE.subn(
        lambda m: f"{m.group(1) or 'PIN'}: [REDACTED]", text
    )
    return text, below + inline


def _fr_nir(text: str) -> tuple[str, int]:
    count = 0

    def mask(m: re.Match) -> str:
        nonlocal count
        if NIR_NOT_AFTER.search(
            m.string[max(0, m.start() - NIR_LOOKBEHIND) : m.start()]
        ):
            return m.group()  # an invoice or reference number
        if m.start() > 0 and m.string[m.start() - 1] in CODE_GLUE:
            return m.group()  # part of a code or a filename
        count += 1
        return "[NIR masked]"

    return NIR_RE.sub(mask, text), count


def _iban(text: str) -> tuple[str, int]:
    return IBAN_RE.subn("[IBAN masked]", text)


NAMED: dict[str, Callable[[str], tuple[str, int]]] = {IBAN: _iban, FR_NIR: _fr_nir}
KNOWN = tuple(NAMED)


def redact(text: str, detectors: tuple[str, ...]) -> tuple[str, dict[str, int]]:
    """Apply the password rule and the named detectors; return text and counts.

    IBANs go first so a NIR pattern cannot fire inside an IBAN's digits."""
    counts: dict[str, int] = {}
    for name in (n for n in KNOWN if n in detectors):
        text, counts[name] = NAMED[name](text)
    text, counts[PASSWORD] = _passwords(text)
    return text, {k: v for k, v in counts.items() if v}
