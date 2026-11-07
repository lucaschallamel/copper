#!/usr/bin/env python3
"""No-Talan gate: shipped kit content must carry no prior-org "Talan" brand token.

US-219 (EP-108), sibling of the SEC-001 no-client-literal gate. COPPER's
white-label core was extracted from a Talan-era origin; this BLOCKING, fail-closed
pre-publish control over ``kits/`` keeps the prior-org brand token "talan" out of
every shipped (marketplace-bound) kit asset.

WHY A PLAINTEXT LITERAL (unlike SEC-001's hashes): "Talan" is a public company
name, not a confidential client literal, so naming it in this gate leaks nothing.
A simple, readable, case-insensitive substring check is sufficient and is the
right tool for a single known brand token.

SCOPE: scans ``kits/`` text files only and self-exempts THIS gate's own source
file (anchored to its real relative location, so a decoy named check-no-prior-org.py
elsewhere under kits/ is still scanned). The compiled ``.opencode/`` / ``.claude/``
copies live outside ``kits/`` and are never scanned. Backlog/audit docs that
legitimately discuss the de-branding live under ``docs-copper/`` , out of scope.

The gate's own file is the single justified occurrence of the token under
``kits/`` (a literal gate must name what it checks for); it is self-exempted, so
the gate reports a true zero over every other asset.

DOCUMENTED RESIDUAL (I-1): only TEXT_SUFFIXES are scanned. Non-text assets
(images, fonts, .svg) are not, so a future binary brand asset whose name or bytes
carry the token would need a name-based check , or removal at source, as US-219
did for the Talan logo binaries. Extend this gate when such assets reappear.

SCOPE OF ASSURANCE (S5 F-2): this gate catches the single literal brand TOKEN
"talan". It does NOT catch UNTOKENED prior-org corporate claims (partner tiers,
awards, head-counts, slogans) that name no token , a green gate is NOT a complete
de-brand. Those are handled by a separate content sweep (the M-1b follow-up story)
and by the manual first-publish review. Likewise, this gate scans the WORKING TREE
only; prior-org data removed here remains in GIT HISTORY until a history rewrite
(a publish-precondition, S5 F-1).

Usage:
    python3 check-no-prior-org.py [ROOT_DIR]   # scan ROOT/kits/ (default: cwd)

Exit codes:
    0 - no "talan" token found in any scanned kit asset
    1 - the token was found in a kit asset (or an in-scope asset was unreadable)
    2 - usage error, or the scan root has no kits/ dir (fail closed, S5 F-3)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LITERAL = "talan"
_LITERAL_RE = re.compile(re.escape(LITERAL), re.IGNORECASE)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".ts", ".sh", ".css"}

# Self-exemption is anchored to the gate's OWN LOCATION (its source under
# kits/core/), by path RELATIVE to the scanned kits/ root , NOT by bare filename:
# a decoy named check-no-prior-org.py ANYWHERE else under kits/ must still be scanned.
_SCRIPTS_REL = "core/skills/framework-authoring/scripts"
SELF_EXEMPT_RELPATHS = {f"{_SCRIPTS_REL}/check-no-prior-org.py"}


def check_file(path: Path, kits_root: Path) -> list[str]:
    """Return violation messages for one kit asset."""
    if path.suffix not in TEXT_SUFFIXES:
        return []
    if path.relative_to(kits_root).as_posix() in SELF_EXEMPT_RELPATHS:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        # FAIL CLOSED: an in-scope asset the gate cannot READ is one it cannot
        # clear. Treat it as a blocking violation, never a silent skip.
        return [f"{path}: unreadable in-scope asset (cannot clear , FAIL CLOSED)"]
    if _LITERAL_RE.search(text):
        return [f"{path}: prior-org brand token present"]
    return []


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print("usage: check-no-prior-org.py [ROOT_DIR]", file=sys.stderr)
        return 2

    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    kits = root / "kits"
    if not kits.is_dir():
        # FAIL CLOSED (S5 F-3): a publish gate with no scan root is suspicious,
        # not benign. A wrong CWD or a refactor that moves kits/ must fail loudly,
        # never silently pass.
        print(f"no-prior-org: {kits} not present (FAIL CLOSED)", file=sys.stderr)
        return 2

    assets = [p for p in kits.rglob("*") if p.is_file()]
    violations: list[str] = []
    for asset in assets:
        violations.extend(check_file(asset, kits))

    if violations:
        print(f"no-prior-org: {len(violations)} violation(s) under {kits}:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(
        f"no-prior-org: {len(assets)} asset(s) scanned, prior-org brand token absent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
