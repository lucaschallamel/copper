#!/usr/bin/env python3
"""White-label core invariant: Tier-2 core (/kits/core/) must be org-identity-free.

Enforces ADR-019's white-label Tier-2 core boundary (US-178). The neutral kit
core (`/kits/core/`) must contain no organisation identity and no per-target
asset prefix, so any organisation can install its own identity-kit (Tier 3)
onto the same core.

Checks over every asset under `/kits/core/`:
  1. prefix-free names   : no `rg-` / `ta-` / `cu-` (prefixes are applied per-target at
                           compile time by the adapter, ADR-018), so neutral
                           source names must not carry it.
  2. denylist backstop   : no org token in core content, matched CASE-INSENSITIVELY
                           (a backstop bypassed by lowercasing is worthless).
                           Distinctive brand tokens (Regdata, REGDATA Protection
                           Suite) match as substrings; short/common tokens (RPS,
                           FINMA, exec/board surnames) match on WORD BOUNDARIES to
                           avoid false-positives.
  2c. kit-agent/skill    : (TD-166 S7) no CONTENT reference to a specific `rg-`/`ta-`
      content coupling     kit agent or skill (`@rg-foo` delegation form or bare
                           `rg-foo` grant/reference form). Check 1 only covers the
                           FILENAME; this catches config grants, subagent_type
                           values, delegation lists, and consumer references in the
                           BODY. `cu-` (the core emission prefix) and `rg-prefix*`
                           (the naming-scheme discussion) are NOT flagged. Core names
                           the ROLE / capability; the installed kit supplies the agent.
  3. marker convention   : core institutional slots use markers, not concrete org
                           values (ADR-019 Q3, SPEC 9.2). Both marker forms
                           (`{{...}}` placeholders and `<!-- identity:slot -->`
                           HTML-comment markers) must be non-empty; a concrete org
                           value (check 2) is itself a value-where-a-marker-belongs
                           violation.

NOTE ON SCOPE (US-178 S3): `/kits/core/` is populated by US-183 (ADR-018 P2).
Until then this check finds zero core assets and reports that VACUOUS state
explicitly (it does NOT silently pass as if it had enforced anything). It bites
automatically the moment `/kits/core/` is populated. It deliberately does NOT
scan `.opencode/` (compiled output: prefixes are applied there, and Tier-2/
Tier-3/example content is intermixed).

Usage:
    python3 check-white-label-core.py [ROOT_DIR]

Exit codes:
    0 - Core is white-label (or no core assets to scan yet)
    1 - A white-label violation was found
    2 - Usage error
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Org identity tokens that must never appear in white-label core content.
# This list is DATA for the check; the check file itself is not under
# /kits/core/, so it never scans itself.
#
# Two match modes: distinctive multi-word/brand tokens match as plain substrings;
# short or common-word tokens (acronyms, surnames) match on WORD BOUNDARIES to
# avoid false-positives (e.g. "RPS" inside an unrelated acronym, or "Prince" as an
# ordinary word). All matching is CASE-INSENSITIVE (finding S7-#1): a backstop
# bypassed by lowercasing ("regdata", "rps") would be worthless.
DENYLIST_SUBSTRING = [
    "Regdata",
    "REGDATA Protection Suite",
]
DENYLIST_WORD = [
    "RPS",
    "FINMA",
    # executive / board names (ADR-019 Q3 example set)
    "Prince",
    "Ducret",
    "Martino",
    "Kalfon",
    "Jacquier",
]
_SUBSTRING_LOWER = [(t, t.casefold()) for t in DENYLIST_SUBSTRING]
_WORD_RES = [
    (t, re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE)) for t in DENYLIST_WORD
]

# ADR-046 decision 12: the LEGACY framework name must not silently re-enter core.
# Checked PER LINE so documented legacy-compat forms (dual-read fallbacks,
# migration notes) stay legal. This tuple mirrors
# deploy/copper_rename_map.GLOBAL_LEGACY_FORMS; a unit test asserts it is a
# superset so the two cannot drift apart silently (US-258 lesson). Kept inline
# because this script also ships to hosts where deploy/ does not exist.
LEGACY_BRAND = "rahan"
LEGACY_ALLOWED_FORMS = (
    ".rahan/",
    ".rahan-",
    '".rahan"',
    "RAHAN:BEGIN",
    "RAHAN:END",
    "RAHAN_TELEMETRY_PATH",
    "Documents/RAHAN",
    '"Documents" / "RAHAN"',
    "RAHAN-era",
    "legacy RAHAN",
    "Legacy RAHAN",
)

# cu- is the COPPER EMISSION prefix (ADR-046); core SOURCE names stay neutral.
# US-375: `ra` is the vendor prefix; the retired `rg` stays refused too.
PREFIX_RE = re.compile(r"^(ra|rg|ta|cu)-")

# CONTENT coupling to a specific kit agent/skill (TD-166 S7): a core asset must not
# NAME a vendor/kit-prefixed agent or skill in its body/frontmatter (config grants,
# subagent_type values, delegation lists, consumer references), whether written as
# `@rg-foo` (delegation form) or bare `rg-foo` (grant/reference form). `cu-` is the
# core's OWN emission prefix (legitimate in content, e.g. `cu-cascade-handler`,
# `/cu-init`) and is NOT flagged. `rg-prefix`/`rg-prefixed` is the English
# discussion of the naming SCHEME itself (not a concrete agent) , exempted via the
# negative lookahead. Core must name the ROLE / capability; the installed kit
# supplies the concrete `rg-`/`ta-` agent or skill.
KIT_REF_RE = re.compile(r"@?\b(?:ra|rg|ta)-(?!prefix)[a-z][a-z-]*")

# Marker convention (AC2): core institutional slots use markers, not concrete org
# values. SPEC 9.2 names two forms: `{{...}}` placeholders and `<!-- identity:slot -->`
# HTML-comment markers. Both must be non-empty/well-formed. A concrete org value
# (the denylist) appearing in core IS a "value where a marker belongs" violation,
# so the denylist doubles as the marker-convention enforcement proxy.
MARKER_RE = re.compile(r"\{\{\s*([^}]*?)\s*\}\}")
IDENTITY_SLOT_RE = re.compile(r"<!--\s*identity:\s*([^>]*?)\s*-->")

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".ts", ".sh"}

# Self-exemption (US-183 WS1): once framework-authoring is migrated into
# /kits/core/, this checker scans itself , and it MUST contain the org tokens it
# bans (the denylist is the enforcement mechanism, not org identity). Exempt this
# one file from the DENYLIST scan only (prefix + marker checks still apply). This
# is the single unavoidable exemption: every OTHER core file is genuinely de-org'd.
# The token here is DATA the tool operates on, not identity the tool asserts.
#
# CHANGELOG.md (US-339): the per-kit changelog lives at the kit root and is NEVER
# compiled into a host tree or loaded into agent context (asset folders are
# glob-loaded; the kit root is not). Its historical entries legitimately cite
# `regdata-*` kit names as change provenance (e.g. "US-340 evicted content to the
# regdata-consulting kit"). Like `.opencode/` (deliberately unscanned, line ~30),
# never-shipped historical metadata is not the white-label surface , exempt it
# from the denylist scan (prefix/marker checks still apply).
# check-identity-drift.py (SP-119): the RAHAN-identity-drift guard MUST name the
# RAHAN/Regdata tokens it detects and allowlists (rahan.regdata.ch is the ADR-046
# documented exception). Like check-white-label-core.py, the tokens are DATA the
# tool operates on, not identity it asserts , exempt from the denylist scan only.
DENYLIST_SELF_EXEMPT = {
    "check-white-label-core.py",
    "check-identity-drift.py",
    "instructions.md",
}


def find_core_root(root: Path) -> Path | None:
    """Return /kits/core/ if it exists, else None (not yet populated by US-183)."""
    core = root / "kits" / "core"
    return core if core.is_dir() else None


def _is_denylist_exempt(path: Path, core: Path) -> bool:
    """Whether `path` is exempt from the org-token denylist scan.

    The checker and instructions.md are exempt by basename (they legitimately
    name the banned tokens). CHANGELOG.md is exempt ONLY at the core ROOT
    (`kits/core/CHANGELOG.md`) , the per-kit changelog whose never-shipped
    historical entries cite `regdata-*` provenance (R5: NOT any CHANGELOG.md
    nested under an asset folder, which the never-loaded rationale does not cover
    and which would be a real leak surface)."""
    if path.name in DENYLIST_SELF_EXEMPT:
        return True
    if path.name == "CHANGELOG.md" and path.parent == core:
        return True
    return False


# US-330 / ADR-051 , the bare-command allowlist.
#
# ADR-046 gives core assets the `cu-` emission prefix; a command escapes it by
# carrying `namespace: core`. That is a SINGLE FRONTMATTER LINE, so the bare
# namespace , whose entire value is being small and deliberate , could grow by
# accident with nothing to notice.
#
# This check makes `namespace: core` necessary but NOT SUFFICIENT: the slug must
# also appear in tools/universal-commands.json under `active`.
#
# It lives inside THIS gate rather than a sibling script on purpose. A new script
# is a second thing to wire into ci:local and a second thing to forget , the
# "what runs it?" failure this repo has hit five times. Here, the runner already
# exists.
# S4 R1/R2/R3 , three defects in the first version of this guard, all found by
# attacking it rather than reading it:
#
#   R1  the regex string-matched `namespace: core`, while the COMPILER YAML-parses
#       the value and tests membership. `namespace: "core"`, `'core'` and
#       `core # comment` all ship bare and all slipped past , a guard defeated by
#       two quote characters.
#   R2  it checked `core` ALONE, but FOUR namespaces are prefix-free. A core
#       command declaring `cm`, `gd` or `qd` ships bare unguarded , three of the
#       four routes to a bare command were blind. Written against ADR-051's
#       WORDING instead of against what the compiler actually does.
#   R3  the regex was MULTILINE over the WHOLE FILE, so `namespace: core` in a body
#       or code fence raised a violation. ADR-051 exists to document this
#       mechanism, so commands quoting it are likely, not hypothetical.
#
# PREFIX_FREE_NAMESPACES is INLINED rather than imported because this script ships
# to hosts where `deploy/` does not exist (same reason as LEGACY_ALLOWED_FORMS
# above). tests/unit/test_check_white_label_core.py pins it against
# deploy.targets.base via AST, so the two cannot drift apart silently.
PREFIX_FREE_NAMESPACES = frozenset({"core", "cm", "gd", "qd"})

# A frontmatter `namespace:` value, tolerant of what YAML tolerates: optional
# single/double quotes and a trailing comment. Applied to the FRONTMATTER BLOCK
# ONLY (see _frontmatter_block), never the whole file.
_NAMESPACE_RE = re.compile(
    r"""^namespace:\s*['"]?([A-Za-z0-9_-]+)['"]?\s*(?:\#.*)?$""", re.MULTILINE
)


def _frontmatter_block(text: str) -> str:
    """The YAML frontmatter only , the text between the first two `---` fences.

    Line-anchored and deliberately simple (the shared deploy/frontmatter.py split
    from TD-169 is not importable on a host without deploy/). Returns "" when there
    is no frontmatter, so a body-only file is never scanned for directives.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return ""  # unterminated frontmatter , treat as none rather than guess


def load_universal_allowlist(core: Path) -> set[str] | None:
    """The `active` bare-command slugs, or None when the allowlist is absent.

    Returns None rather than an empty set so the caller can distinguish "no
    command may be bare" from "the allowlist is missing" , the second is a
    wiring failure and must not silently enforce an empty policy.
    """
    path = core / "tools" / "universal-commands.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    active = data.get("active")
    return set(active) if isinstance(active, list) else None


def check_bare_command(path: Path, core: Path, allowlist: set[str] | None) -> list[str]:
    """ADR-051 D2: a bare core command must be on the allowlist.

    ONE DIRECTION ONLY. Bare-but-unlisted fails; listed-but-not-yet-bare is
    LEGAL, which is what makes ADR-051's `reserved` rows expressible at all
    (`dream`/`distill`/`learn` are named before they ship). Checking both
    directions would force every future member to ship the moment it was named.
    """
    if path.suffix != ".md" or path.parent != core / "commands":
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    match = _NAMESPACE_RE.search(_frontmatter_block(text))
    if match is None or match.group(1) not in PREFIX_FREE_NAMESPACES:
        # No namespace, or a vendor namespace , the command wears a prefix and is
        # none of this check's business.
        return []
    if allowlist is None:
        return [
            f"{path}: declares a prefix-free `namespace:` but "
            "tools/universal-commands.json "
            "is missing or unreadable , the bare-command allowlist cannot be checked"
        ]
    slug = path.stem
    if slug in allowlist:
        return []
    return [
        f"{path}: ships UNPREFIXED (`namespace: {match.group(1)}` is prefix-free) "
        f"but '{slug}' is not in the ADR-051 universal allowlist. Amend ADR-051 "
        "first, then kits/core/tools/universal-commands.json (in that order)"
    ]


def check_asset(path: Path, core: Path) -> list[str]:
    """Return a list of violation messages for a single core asset file."""
    violations: list[str] = []
    # 1. prefix-free name (AC3)
    if PREFIX_RE.match(path.name):
        violations.append(f"{path}: prefixed name (core must be prefix-free)")
    # text-content checks only on known text suffixes (binary/unknown are skipped)
    if path.suffix not in TEXT_SUFFIXES:
        return violations
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return violations
    # 2. denylist backstop (AC4): substring + word-boundary, both case-insensitive.
    # The denylist-bearing file itself is exempt (it MUST name the tokens it bans).
    if not _is_denylist_exempt(path, core):
        text_lower = text.casefold()
        for token, token_lower in _SUBSTRING_LOWER:
            if token_lower in text_lower:
                violations.append(
                    f"{path}: denylist token '{token}' in white-label core"
                )
        for token, pattern in _WORD_RES:
            if pattern.search(text):
                violations.append(
                    f"{path}: denylist token '{token}' in white-label core"
                )
        # 2b. legacy framework name (ADR-046): per-line, legacy-compat forms OK.
        for line_no, line in enumerate(text.splitlines(), start=1):
            if LEGACY_BRAND in line.casefold() and not any(
                form in line for form in LEGACY_ALLOWED_FORMS
            ):
                violations.append(
                    f"{path}:{line_no}: legacy brand 'RAHAN' in white-label core"
                )
        # 2c. kit-agent/skill CONTENT coupling (TD-166 S7): core must not NAME a
        # specific `rg-`/`ta-` kit agent or skill in its content (check #1 only
        # covers the FILENAME). Core names the role; the kit supplies the agent.
        for ref in sorted(set(KIT_REF_RE.findall(text))):
            violations.append(
                f"{path}: kit-agent/skill reference '{ref}' in white-label core "
                "(name the role/capability; the installed kit supplies it)"
            )
    # 3. marker convention (AC2): both marker forms must be non-empty/well-formed
    for m in MARKER_RE.finditer(text):
        if not m.group(1).strip():
            violations.append(f"{path}: empty marker slot '{m.group(0)}' (AC2)")
    for m in IDENTITY_SLOT_RE.finditer(text):
        if not m.group(1).strip():
            violations.append(f"{path}: empty identity slot '{m.group(0)}' (AC2)")
    return violations


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    core = find_core_root(root)
    if core is None:
        # Nothing scanned is not a pass (TD-201 A20).
        print(
            f"white-label-core: {root / 'kits' / 'core'} not present , NOTHING "
            "SCANNED (FAIL CLOSED). Pass the root that holds kits/core/.",
            file=sys.stderr,
        )
        return 2

    assets = [p for p in core.rglob("*") if p.is_file()]
    if not assets:
        # Dir exists but is empty (e.g. US-183 mid-population): still vacuous, say so
        # explicitly rather than claim enforcement over nothing (finding S7-#3).
        print(
            f"white-label-core: {core} exists but contains no assets , NOTHING "
            "SCANNED (FAIL CLOSED).",
            file=sys.stderr,
        )
        return 2

    # US-330: loaded ONCE, not per asset , the allowlist is one file and re-reading
    # it per asset would be both wasteful and a chance for the two reads to differ.
    allowlist = load_universal_allowlist(core)

    violations: list[str] = []
    for asset in assets:
        violations.extend(check_asset(asset, core))
        violations.extend(check_bare_command(asset, core, allowlist))

    if violations:
        print(f"white-label-core: {len(violations)} violation(s) under {core}:")
        for v in violations:
            print(f"  - {v}")
        return 1

    print(f"white-label-core: {len(assets)} core asset(s) scanned, all white-label.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
