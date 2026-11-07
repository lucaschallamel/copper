#!/usr/bin/env python3
"""No-prior-org-claims gate: kit content must not assert prior-org corporate claims
as the current organisation's own.

US-241 (EP-108), the content-accuracy sibling of US-219's no-prior-org TOKEN gate.
US-219 removed the literal prior-org brand token; this gate catches a NARROW, curated
set of UNAMBIGUOUS prior-org corporate claims that carry no token (partner tiers,
awards, slogans) and are FALSE for a small scale-up.

ORG-AGNOSTIC (white-label core): this file lives in `kits/core/` and must name NO
current-organisation identity and NO instance kit path. Exemption is therefore keyed
on an org-neutral GUARD MARKER, not on hardcoded kit names.

WHY NARROW (S2 decision): the broad claim space is context-dependent , e.g. bare
"EcoVadis" is a legitimate CLIENT assessment framework, but "EcoVadis Platinum"
asserted as the org's medal is false. A broad single-pattern lint would false-positive.
So this gate matches ONLY phrases that are never legitimate as the org's own; the
ambiguous/contextual cases are covered by the first-publish review checklist
(docs-copper/architecture/first-publish-prior-ocu-review-checklist.md).

PATTERNS (case-insensitive): partner TIERS ("Gold Partner", "Diamond Partner"),
awards ("Great Place to Work", "EcoVadis Platinum/Platine"), and the prior-org slogan
("Positive Innovation"). NOT matched: bare framework/tool names or any figure , too
false-positive-prone, checklist-covered.

SCOPE: scans kits/ text files line by line. A matched phrase is EXEMPT only when an
org-neutral de-brand GUARD MARKER ("prior-org", "legacy", "do not cite/use/reuse/claim",
"ne pas") appears WITHIN GUARD_WINDOW lines of it , i.e. the phrase is named inside a
"do not cite ..." note. This line-proximity rule (S5 hardening) is tighter than a
file-level allowlist: an unrelated guard word elsewhere in the file no longer exempts a
real claim. Residual (narrow, checklist-backstopped): a real claim placed within
GUARD_WINDOW lines of an unrelated marker. This gate's own source is exempt (anchored to
its real core-relative location). The compiled .opencode/ / .claude/ copies are outside
kits/ and never scanned.

Usage:
    python3 check-no-prior-org-claims.py [ROOT_DIR]   # scan ROOT/kits/ (default: cwd)

Exit codes:
    0 - no prior-org claim phrase found in any non-exempt kit asset
    1 - a phrase was found (or an in-scope asset was unreadable)
    2 - usage error, or the scan root has no kits/ dir (fail closed)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Unambiguous prior-org claim phrases (never legitimate as the current org's own).
PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"gold partner",
        r"diamond partner",
        r"positive innovation",
        r"great place to work",
        r"ecovadis\s+platin(?:um|e)",
    )
]

# Org-neutral de-brand guard markers. A matched phrase is exempt only when one of these
# appears within GUARD_WINDOW lines (a "do not cite ..." note legitimately names it). No
# organisation name or kit path is hardcoded , keeps the gate white-label-core-clean.
GUARD_MARKER = re.compile(
    r"prior-org|legacy|do not (?:cite|use|reuse|claim)|ne pas", re.IGNORECASE
)

# Lines of context around a matched phrase searched for a guard marker. Genuine guard
# notes place the marker on the same or an adjacent line; 3 covers a marker heading that
# precedes a short multi-line warning block.
GUARD_WINDOW = 3

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".ts", ".sh", ".css"}

# This gate's own source, by path RELATIVE to kits/ (an org-neutral core location).
_SELF_RELPATH = "core/skills/framework-authoring/scripts/check-no-prior-org-claims.py"


def check_file(path: Path, kits_root: Path) -> list[str]:
    """Return violation messages for one kit asset."""
    if path.suffix not in TEXT_SUFFIXES:
        return []
    if path.relative_to(kits_root).as_posix() == _SELF_RELPATH:
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        # FAIL CLOSED: an in-scope asset the gate cannot read is one it cannot clear.
        return [f"{path}: unreadable in-scope asset (cannot clear , FAIL CLOSED)"]
    violations: list[str] = []
    for i, line in enumerate(lines):
        for pat in PATTERNS:
            if not pat.search(line):
                continue
            lo = max(0, i - GUARD_WINDOW)
            hi = min(len(lines), i + GUARD_WINDOW + 1)
            if GUARD_MARKER.search("\n".join(lines[lo:hi])):
                continue  # guard context , phrase named to warn against it
            violations.append(
                f"{path}:{i + 1}: prior-org claim phrase present ({pat.pattern})"
            )
    return violations


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print("usage: check-no-prior-org-claims.py [ROOT_DIR]", file=sys.stderr)
        return 2

    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    kits = root / "kits"
    if not kits.is_dir():
        print(f"no-prior-org-claims: {kits} not present (FAIL CLOSED)", file=sys.stderr)
        return 2

    assets = [p for p in kits.rglob("*") if p.is_file()]
    violations: list[str] = []
    for asset in assets:
        violations.extend(check_file(asset, kits))

    if violations:
        print(f"no-prior-org-claims: {len(violations)} violation(s) under {kits}:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"no-prior-org-claims: {len(assets)} asset(s) scanned, no claim present.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
