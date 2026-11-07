#!/usr/bin/env python3
"""Enforce the precedence-tier constitution across the always-on rule corpus.

Every rule file (00-07) and instructions.md declares a `precedence_tier` in
frontmatter (T1-T5). The tier is the highest tier the file's content reaches
(a file-level ceiling). This validator gates three properties (US-339):

  (a) A missing or invalid `precedence_tier` on a governed file is an ERROR.
  (b) A `[!danger]` / `[!warning]` salience callout may appear only in a T1 file
      (the reserved register stays reserved to the non-negotiable tier).
  (c) A reserved-register PROSE token (MANDATORY / NON-NEGOTIABLE / MUST NOT /
      NEVER) on a T4/T5 file is an ERROR.
  (d) A T1/T2 file that declares `paths` frontmatter is an ERROR: a scoped rule
      loads only after a matching file is touched, and safety never waits (US-378).

The register checks scan PROSE ONLY: fenced code blocks, blockquote/callout
lines, and frontmatter are excluded, so a legitimate token inside an example,
a code fence, or a T1 callout does not trip a false positive.

Usage:
    python3 check-precedence.py [ROOT_DIR]

Exit codes:
    0 - Constitution holds
    1 - Violation detected
    2 - Usage error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

VALID_TIERS = {"T1", "T2", "T3", "T4", "T5"}
# Tiers on which the reserved MANDATORY register is NOT permitted in prose.
LOWER_TIERS = {"T4", "T5"}

# Reserved-register tokens. Word-boundary matched, case-sensitive uppercase.
RESERVED_TOKEN = re.compile(r"\b(MANDATORY|NON-NEGOTIABLE|MUST NOT|NEVER)\b")
CALLOUT = re.compile(r"\[!(danger|warning)\]", re.IGNORECASE)
# A `paths` key in the frontmatter makes Claude Code load the rule only after a
# matching file is touched (ADR-054). T1/T2 content must never be conditional on a
# file match, so such a file is refused (US-378 AC9). The key is read with a YAML
# parser, as the compiler reads it: a line regex missed `"paths":` (S4 finding 5).
PATHS_KEY = "paths"
UNCONDITIONAL_TIERS = {"T1", "T2"}
# Inline code spans (`...`) , stripped from prose before the reserved-token scan
# so a legitimate `MANDATORY` enum reference is not a false positive (R2).
INLINE_CODE = re.compile(r"`[^`]*`")


def governed_files(root: Path) -> list[Path]:
    """The always-on corpus: instructions.md + every numbered rule file.

    Scans `kits/core/` (the committed source of truth), NOT the compiled
    `.opencode/`/`.claude/` trees , identical to check-white-label-core.py.
    The compiled trees have identity slots filled by the org-identity kit, so a
    reserved-register token injected there is the KIT's content, not core's; the
    precedence constitution governs core, so it must scan core.
    """
    core = root / "kits" / "core"
    files: list[Path] = []
    instructions = core / "instructions.md"
    if instructions.is_file():
        files.append(instructions)
    rules_dir = core / "rules"
    if rules_dir.is_dir():
        files.extend(sorted(rules_dir.glob("*.rules.md")))
    return files


def frontmatter_end_line(text: str) -> int:
    """1-indexed line number of the closing frontmatter `---`, or 0 if none."""
    if not text.startswith("---"):
        return 0
    lines = text.splitlines()
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return i
    return 0


def _frontmatter(text: str) -> str | None:
    """The leading frontmatter block, or None when there is none."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return None if end == -1 else text[:end]


class FrontmatterError(ValueError):
    """Frontmatter that is not one YAML mapping with unique keys."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """A safe loader that refuses a repeated key: with duplicates a line regex and a
    YAML parser read different values (S4 re-review F6), so neither is trusted."""


def _construct_unique_mapping(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    repeated = sorted({str(k) for k in keys if keys.count(k) > 1})
    if repeated:
        raise FrontmatterError(f"repeated key(s) {repeated}")
    return loader.construct_mapping(node, deep=deep)


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def frontmatter_meta(text: str) -> dict | None:
    """The frontmatter as a mapping, or None when there is no frontmatter.

    Read with a YAML parser, as the compiler reads it. Raises FrontmatterError when
    the block does not parse, is not a mapping, or repeats a key.
    """
    frontmatter = _frontmatter(text)
    if frontmatter is None:
        return None
    try:
        meta = yaml.load(frontmatter[3:], Loader=_UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise FrontmatterError("does not parse as YAML") from exc
    if meta is None:
        return {}
    if not isinstance(meta, dict):
        raise FrontmatterError("is not a mapping")
    return meta


def read_tier(meta: dict | None) -> str | None:
    """precedence_tier from parsed frontmatter, as written (validated by the caller)."""
    if not meta or meta.get("precedence_tier") is None:
        return None
    return str(meta["precedence_tier"])


def is_path_scoped(meta: dict | None) -> bool:
    """True when the frontmatter declares `paths` (a scoped rule file)."""
    return bool(meta) and PATHS_KEY in meta


def _fence_marker(stripped: str) -> str | None:
    """Return the fence marker run ('```' or '~~~'-family) if the line opens or
    closes a fence, else None. A closing fence must match the opener's char (R3),
    checked by the caller against the tracked opener."""
    for ch in ("`", "~"):
        if stripped.startswith(ch * 3):
            return ch
    return None


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Yield (1-indexed line number, scannable-prose) for prose lines only.

    Excludes from scanning: the leading frontmatter block; fenced code blocks
    (fence close must match the opener's marker char, R3); genuine `[!...]`
    callout blocks (but NOT plain blockquotes , those are un-quoted and scanned,
    R1); and inline-code spans within a line (stripped before scanning, R2).

    A plain blockquote has its leading `>` markers stripped and its content
    scanned , quoting cannot be used to smuggle reserved-register prose (R1).
    """
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    in_frontmatter = False
    fence_char: str | None = None  # the opener's marker char while inside a fence
    in_callout = False  # inside a `> [!...]` callout block

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Leading frontmatter block (--- ... ---) at the very top.
        if i == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue

        # Fenced code blocks , open on any ```/~~~, close only on the SAME char.
        marker = _fence_marker(stripped)
        if fence_char is not None:
            if marker == fence_char:
                fence_char = None
            continue  # inside a fence (or its closing line) , never prose
        if marker is not None:
            fence_char = marker
            continue

        # Blockquote handling. A callout block opens with `> [!...]` and continues
        # while lines start with `>`; those lines are the reserved salience
        # register and are exempt from the token scan. A PLAIN blockquote is not a
        # callout , strip its `>` markers and scan the remaining content (R1).
        if stripped.startswith(">"):
            content = stripped.lstrip(">").strip()
            if in_callout:
                continue  # continuation of an open callout block
            if CALLOUT.search(content):
                in_callout = True
                continue  # the callout's opening line
            # plain blockquote , scan the un-quoted content
            out.append((i, _strip_inline_code(content)))
            continue
        # a blank or non-`>` line ends any open callout block
        in_callout = False

        out.append((i, _strip_inline_code(line)))

    return out


def _strip_inline_code(line: str) -> str:
    """Remove inline-code spans so a `MANDATORY`-in-backticks reference is not a
    false positive (R2)."""
    return INLINE_CODE.sub("", line)


def check_file(path: Path) -> list[str]:
    """Return a list of violation messages for one governed file."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    rel = path.name

    try:
        meta = frontmatter_meta(text)
    except FrontmatterError as exc:
        # Fail closed: a tier or `paths` that cannot be read reliably is not trusted.
        errors.append(f"{rel}: frontmatter {exc}")
        return errors
    tier = read_tier(meta)
    if tier is None:
        errors.append(f"{rel}: missing `precedence_tier` frontmatter field")
        return errors  # cannot evaluate tier-dependent rules without a tier
    if tier not in VALID_TIERS:
        errors.append(
            f"{rel}: invalid precedence_tier '{tier}' "
            f"(expected one of {sorted(VALID_TIERS)})"
        )
        return errors

    # Rule (d): T1/T2 is never path-scoped (US-378 AC9, SP-126 S5).
    if tier in UNCONDITIONAL_TIERS and is_path_scoped(meta):
        errors.append(
            f"{rel}: {tier} file declares `paths` , safety and prohibited-operation "
            "directives must load in every session, never on a file match"
        )

    prose = prose_lines(text)
    body_start = frontmatter_end_line(text)

    # Rule (b): danger/warning salience callouts are the reserved register , they
    # may mark T1-T3 content (non-negotiable safety, prohibited-op gates, and
    # mandatory governance) but never advisory T4/T5 prose. Callouts live on
    # blockquote lines, so scan the raw BODY (past the frontmatter) for them.
    if tier in LOWER_TIERS:
        for i, line in enumerate(text.splitlines(), start=1):
            if i <= body_start:
                continue  # skip the frontmatter block (may quote a callout)
            if CALLOUT.search(line):
                errors.append(
                    f"{rel}:{i}: `[!danger]`/`[!warning]` callout on a {tier} file "
                    f"(the salience register is reserved to T1-T3)"
                )

    # Rule (c): reserved-register prose tokens only outside T4/T5.
    if tier in LOWER_TIERS:
        for lineno, line in prose:
            match = RESERVED_TOKEN.search(line)
            if match:
                errors.append(
                    f"{rel}:{lineno}: reserved-register token '{match.group(1)}' "
                    f"in prose on a {tier} file (reserved to T1-T3)"
                )

    return errors


def find_repo_root(start: Path) -> Path:
    """Walk up from `start` to the directory that contains `kits/core/`.

    Location-independent: this script ships to BOTH kits/core/... and the
    compiled .opencode/... /.claude/... trees (at different depths), and CI
    invokes the compiled copy. Fixed parent-counting would break for one of
    them; searching for the kits/core marker works from any copy.
    """
    for candidate in [start, *start.parents]:
        if (candidate / "kits" / "core").is_dir():
            return candidate
    return start


def main() -> int:
    root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else find_repo_root(Path(__file__).resolve())
    )

    files = governed_files(root)
    if not files:
        print(f"FAIL: no governed files found under {root / 'kits' / 'core'}")
        print("Expected kits/core/instructions.md and kits/core/rules/*.rules.md")
        return 2

    all_errors: list[str] = []
    for path in files:
        all_errors.extend(check_file(path))

    if all_errors:
        print("FAIL: precedence-constitution violations:")
        for err in all_errors:
            print(f"  {err}")
        print()
        print("Remediation:")
        print("  - Add `precedence_tier: T1|T2|T3|T4|T5` to each governed file.")
        print("  - Keep `[!danger]`/`[!warning]` callouts out of T4/T5 files.")
        print("  - Never put `paths` on a T1/T2 file; keep that content in an anchor.")
        print("  - Keep MANDATORY-register prose out of T4/T5 files (put a")
        print("    legitimate example inside a code fence or callout).")
        return 1

    print(f"PASS: precedence constitution holds across {len(files)} governed files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
