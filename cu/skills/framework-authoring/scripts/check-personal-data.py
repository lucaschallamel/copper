#!/usr/bin/env python3
"""US-352 , the personal-data boundary gate: no kit ships a person's identity.

A BLOCKING, fail-closed control over every kit tree. It exists because the vault
migration (EP-108) moves assets that were authored for one person's private workspace
into a PUBLIC marketplace, and an inventory of that corpus found special-category
personal data (political affiliation, religious belief, dietary stance, family
composition) woven through the directive layer , including already propagated into an
agent body, so removing it from one rule file would not have removed it at all.

TWO DETECTORS, DELIBERATELY DIFFERENT SEVERITIES (US-352 S2, C3 disposition)

  REFUSE (fails the gate) , unambiguous:
    - an absolute /Users/<name>/ or /home/<name>/ path (a real login, not a heuristic)
    - a salted denylist hit (finite, curated, high confidence , SEC-001's model)
    - a rules/00-*.md file inside kit content (Rule 00 IS the user-profile file)
    - a reference to a `never_migrate` path (US-352 AC6)

  FLAG (counted, reported, NEVER fatal) , heuristic:
    - a values/personal/identity/background heading (legitimate in a brand kit)
    - an author/owner frontmatter key with a non-placeholder value

The split is not invented here , `deploy/kit/publish_gate.py` already separates REFUSE
from FLAG on the grounds that "heuristic suspicion is for humans to judge, and a
permanently red gate only trains click-through". Applying one blanket verdict would
break that: all-REFUSE goes permanently red on legitimate brand kits, all-FLAG makes
the gate non-blocking.

WHAT THIS GATE DOES NOT DO , no pattern here claims to detect religion, politics or
diet SEMANTICALLY. Those are open classes; a regex for belief either misses or
over-fires. A gate that claims semantic detection and quietly misses converts an
unknown risk into a FALSE ASSURANCE, which is worse than no gate. The denylist carries
known instances as salted hashes; the structural half catches the SHAPE that carries
them. Neither over-promises, and the output never issues a clean bill of health.

DIVERGENCE FROM SEC-001 (deliberate , do not "fix" it back for consistency):

  ZERO FILES SCANNED IS A FAILURE (exit 2), because a gate that passes while scanning
  nothing is the exact defect AC4 exists to prevent. `check-no-client-literals.py`
  used to return 0 when the tree was absent; TD-201 brought it in line (exit 2).

  SEC-001 reads with `errors="ignore"`; this gate uses `errors="strict"`, so a file
     with invalid UTF-8 becomes a REFUSAL rather than being silently mangled and
     partially scanned. A latin-1 encoded name-and-path refuses here and would slip
     past SEC-001.

Also note this gate does NOT exempt its own files (S4 F0). Whole-file self-exemption
made them an unscanned write channel inside the published tree; only the
self-referential CONSTRUCTS are excluded , pattern-source lines in this script, and the
salt/token values in the config (structurally, not by line: a minified one-line JSON
would otherwise carry a payload out with the salt).

RULE MATRIX , the single statement of what this gate does (S7 C4).

There are 8 exemption surfaces and 6 refusal sites. Each was added by a named review
finding and is individually defensible, but predicting whether a given file is scanned
should not require reading 600 lines plus three review artefacts. This table is that
map; keep it correct when changing a rule.

  SCANNED                kits/ and docs-copper/            (SCAN_ROOTS, C7)
  NOT SCANNED            tests/ and .obsidian/ fixtures    (EXCLUDED_PREFIXES, C7)
                         .DS_Store and friends             (EXCLUDED_NAMES, C7)
                         binary/Office containers          (BINARY_SUFFIXES, F2/F17)

  REFUSE (exit 1)                                 kits/    docs-copper/roadmap/
    absolute home path (POSIX + Windows)          yes      yes, except dated records
    FILLED Rule 00 (user-profile file)            yes      yes
    salted denylist hit                           yes      yes
    never-migrate path reference                  yes      EXEMPT (prose, C7)
    unsupported personal-profile slot reference   yes      EXEMPT (prose, C1)
    symlink                                       yes      yes            (F3)
    unreadable in-scope asset                     yes      yes            (fail closed)

  FLAG (counted, never fatal)
    values/personal/identity heading              yes      yes
    authorship key naming an individual           yes      yes  (aggregated, T3)

  EXIT 2 (fail closed)   absent tree | empty tree | zero files scanned | bad config
                         , DIVERGES from SEC-001, which returns 0 here (AC4)

WHY THE EXEMPTIONS EXIST , each is a distinction, not a hole:
  * self-referential (F0)  , this gate's own script and config SHIP in kits/core, so a
    blanket exemption made them an unscanned write channel. Only the CONSTRUCTS are
    excluded (pattern source; salt and token hashes, dropped structurally from the JSON
    because a minified one-line config would otherwise carry a payload out with them).
  * governance prose (C7) , a document that DISCUSSES a forbidden path is not an asset
    that REFERENCES one for use; without this the control could not be documented.
    Narrow: only the two REFERENCE-shaped rules are exempt. Every CONTENT-shaped rule
    still applies, so prose cannot become a hiding place.
  * dated records (C7)    , dev journals and closed audit trails are immutable by
    convention; their logins are already public in git history, so redacting them would
    destroy an accurate record without un-publishing anything.
  * placeholder logins    , `<name>`, `${VAR}`, XXX, and documentation personas are
    conventions, not machine paths. Must consume the WHOLE segment (F1: `USERNAME2` is
    a real login that merely starts with a placeholder word).

TUNING A FALSE POSITIVE: prefer narrowing the RULE over adding a path to an exemption
list. Four false positives were fixed that way (core's own Rule 00 template, a prose
ellipsis, a sibling gate's pattern source, the never-migrate declaration matching
itself); only one needed a new exemption surface.

Exit codes: 0 clean (flags permitted) | 1 refusal(s) | 2 usage/config/empty-scan.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

CONFIG_NAME = "personal-data.json"
# Tests point this at a controlled config (known salt + fictional tokens generated with
# the same `hash` logic); production resolves the config next to the script.
CONFIG_ENV = "PERSONAL_DATA_CONFIG"

# F0 (S4, CRITICAL) , THE GATE'S OWN FILES ARE SCANNED. The first version exempted
# them wholesale, which made them an unscanned WRITE CHANNEL inside the very tree
# being published: personal data in the config's free-text `reason` field scanned
# clean. That exemption was copied from SEC-001 without re-examining WHY it was safe
# there , SEC-001 matches only hashes, so its payload surface is a few bytes; this
# config carries free-text fields BY DESIGN.
#
# Instead of exempting the files, we exempt only the CONSTRUCTS that would
# self-trigger: the regex source lines in this script, and the salt/token values in
# the config. Everything else in both files is scanned like any other asset.
# Repo-relative since C7 widened the scan roots (paths were kits/-relative before).
_SCRIPTS_REL = "kits/core/skills/framework-authoring/scripts"
SELF_REFERENTIAL_RELPATHS = {
    f"{_SCRIPTS_REL}/check-personal-data.py",
    f"{_SCRIPTS_REL}/{CONFIG_NAME}",
    # A SIBLING gate whose job is to detect hardcoded home paths necessarily carries
    # the pattern in its source (check-portability.py:56 already handles C:\Users\ ,
    # it solved this before we did). Same class as self-reference: line-filtered, not
    # whole-file exempt, so only the pattern lines are excluded.
    f"{_SCRIPTS_REL}/check-portability.py",
}
# Lines in the gate's own source that legitimately contain pattern text.
_SELF_PATTERN_MARKER = re.compile(
    r"_RE\s*=\s*re\.compile|_PLACEHOLDER_LOGIN|_SEP\s*=|^\s*#|^\s*(?:\"|')"
)

# F2 (S4): an ALLOWLIST omitted the formats personal prose actually lives in , .rst,
# .mdx, .csv, .svg, .html, .toml, extensionless README/Dockerfile. Inverted to a
# BINARY denylist: read everything EXCEPT known-binary suffixes, so a new text format
# is covered by default instead of silently unscanned. SEC-001's own residual said
# "extend the set as kits gain such assets" , they already had.
# US-352 C7 (S5 A4): the egress boundary is the PUBLIC GIT REMOTE, not `kits/`.
# `kits/` was inherited from SEC-001 without asking where the boundary actually is ,
# `docs-copper/` is 1,677 tracked files, equally public, and already contains a
# never-migrate vault path (the US-352 story itself).
#
# NOT widened to the whole repo, for a measured reason: test suites and detector
# sources must CONTAIN the patterns they detect (`crates/.../detect/username.rs`,
# `test_check_portability.py`, this gate's own tests). Scanning them would make the
# gate permanently red on its own machinery , the F0 lesson generalised. The boundary
# is public CONTENT trees; machinery-that-describes-content is excluded by
# construction and named here rather than left implicit.
# TD-178: the documentation half of the scan set is DISCOVERED, not hardcoded. The
# gate ALREADY fails closed (exit 2) when a scan root is absent or empty , that
# contract is preserved exactly; only how the directory is FOUND changes.
SCAN_ROOTS_STATIC = ("kits",)
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
DOCS_ROOT_MARKERS = ("roadmap", "dev-journal", "memory-bank")


def _resolve_docs_root_name(root: Path) -> str:
    """The documentation directory NAME, by DISCOVERY ONLY (TD-178 S5 A1).

    **`COPPER_DOCS_ROOT` is deliberately NOT honoured here.** Every other guard
    accepts it, because for them the root is a portability question. For this gate it
    is a SECURITY BOUNDARY: `scan_roots` decides what the privacy gate looks at, and
    an env var that shrinks it is a bypass, not a convenience.

    Measured before this change: with a refusal payload (an absolute home path) under
    `docs-copper/`, the baseline scan REFUSED at exit 1; pointing `COPPER_DOCS_ROOT`
    at an in-tree decoy made the same tree PASS at exit 0. Both runs reported "2 of 2
    walked" , identical arithmetic over different sets, which is why a count did not
    reveal it and a refusal payload did.

    `PERSONAL_DATA_CONFIG` is NOT a precedent for this: it selects detection TOKENS,
    never the SCOPE that is scanned.
    """
    for name in DOCS_ROOT_CANDIDATES:
        candidate = root / name
        if candidate.is_dir() and any(
            (candidate / m).is_dir() for m in DOCS_ROOT_MARKERS
        ):
            return name
    return DOCS_ROOT_CANDIDATES[0]


# Excluded within those roots: vendored third-party bundles (their build artefacts
# carry the plugin authors' paths, not ours) and test/fixture trees.
EXCLUDED_PREFIXES = (
    ".obsidian/",
    "tests/",
)
# Untracked OS artefacts (.DS_Store) are gitignored, so they never cross the egress
# boundary this gate defends. Scanning them produced fail-closed refusals for files
# git will never ship , a false positive that would train click-through.
EXCLUDED_NAMES = (".DS_Store", "Thumbs.db", ".localized")
# GOVERNANCE PROSE (C7): a document that DISCUSSES a forbidden path is not a kit asset
# that REFERENCES one for use. The story, its review artefacts and the spec must be
# able to name what they govern , otherwise the control cannot be documented at all.
# Narrow by design: this exempts ONLY the two reference-shaped rules. Every
# content-shaped rule (a real login, a filled Rule 00, a denylist hit) applies here
# exactly as it does in a kit, so governance prose cannot become a hiding place.
# Generalises the single-file SPEC.md carve-out rather than accumulating special cases.
_PROSE_PREFIXES = (
    "docs-copper/roadmap/",
    # A dev journal narrating a privacy control must be able to NAME what the control
    # blocks , same distinction as the roadmap: a document that DISCUSSES a forbidden
    # path is not an asset that REFERENCES one for use. Found when this gate refused
    # the journal entry describing its own delivery. `dev-journal/` was already treated
    # as a narrative record for the home-path rule; this makes the treatment consistent.
    "docs-copper/dev-journal/",
    "kits/SPEC.md",
)

# HISTORICAL RECORDS (C7): dated records , dev journals, closed pipeline audit trails ,
# are immutable by convention: they record what was true then, and rewriting them
# falsifies the record. The ~18 real logins they contain are already public in git
# history, so redaction here would not un-publish anything; it would only destroy an
# accurate record while leaving the disclosure intact.
#
# They are therefore EXEMPT FROM THE HOME-PATH RULE ONLY, and the exemption is
# deliberately dated: anything created from 2026-09 onward is NOT exempt, so the gate
# binds all new writing while leaving the archive intact. Every other rule still
# applies. Recorded as residual R12 with an owner, not silently dropped.
_HISTORICAL_PREFIXES = (
    "docs-copper/dev-journal/",
    "docs-copper/roadmap/pipeline-audit-trail/",
    "docs-copper/roadmap/analysis/",
)


def _is_historical_record(rel: str) -> bool:
    """A dated record whose accuracy outranks redaction (see R12)."""
    return rel.startswith(_HISTORICAL_PREFIXES)


def _is_governance_prose(rel: str) -> bool:
    return rel.startswith(_PROSE_PREFIXES)


BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".bmp",
    ".tiff",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".bz2",
    ".xz",
    ".7z",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp3",
    ".mp4",
    ".wav",
    ".mov",
    ".avi",
    ".webm",
    ".pyc",
    ".pyo",
    ".so",
    ".dylib",
    ".dll",
    ".exe",
    ".bin",
    # Office/OpenDocument containers are ZIPs , read_text raises, which the
    # unreadable branch then reports as a REFUSAL. They are binary, not unclearable.
    # (Their CONTENT is out of scope for a text scanner; flagged as a residual.)
    ".docx",
    ".xlsx",
    ".pptx",
    ".odt",
    ".ods",
    ".odp",
    ".sig",
    ".key",
    ".pem",
    ".der",
}

# --- structural signals -------------------------------------------------------
# REFUSE: an absolute home-directory path. `\w[\w.-]*` is the login segment; a
# trailing separator is required so `/Users/` alone (a generic mention) does not fire.
# Tuning finding T2: an anonymised login (XXX, USER, YOUR_NAME, <name>, ${USER}) is a
# documentation placeholder, not a real person's machine path.
#
# F1 (S4): the first version was case-sensitive, single-separator and forward-slash
# only, and its placeholder exclusion was unanchored on the right , so /users/,
# a doubled separator, a Windows root, a tilde, a missing trailing slash, and a real
# login that merely STARTS with a placeholder word) all passed. Each is now covered,
# and the placeholder must consume the WHOLE segment.
_PLACEHOLDER_LOGIN = (
    r"(?:X{2,}|USER|USERNAME|YOUR[-_]?NAME|NAME|ME"
    # Conventional documentation personas , a home path built on one of these in a
    # worked example is a placeholder, not a machine path (found in US-174).
    r"|alice|bob|carol|dave|eve|jane|john|foo|bar|example"
    r"|<[^>]+>|\$\{[^}]+\}|%[A-Z]+%)"
)
_SEP = r"[\\/]"
# POSIX and Windows home roots, with the login as the following path segment.
_HOME_PATH_RE = re.compile(
    rf"(?:[A-Za-z]:)?{_SEP}+(?:Users|home){_SEP}+"
    rf"(?!{_PLACEHOLDER_LOGIN}(?:{_SEP}|$))"  # whole-segment placeholder only
    rf"(?![<{{\[])"  # not a <name> / {{var}} / [var]
    rf"(?!\.\.\.)"  # not a prose ellipsis, /Users/...
    rf"[\w.-]+",  # the login , trailing sep optional
    re.IGNORECASE,
)
# US-352 C1 (S5 A3): SPEC 9.4 specifies that an unfilled `personal-profile` slot
# DEGRADES to a placeholder. `IdentityResolver` does the opposite , it fail-closes on
# any unfilled slot , and no `personal-profile` branch exists. Rather than leave a
# normative contract with no implementation (the pattern that produced the `/cu-init`
# fiction in Rule 00), the gap is ENFORCED: referencing the slot is refused until the
# resolver supports it. Same move AC6 made , a claim becomes a control.
_UNSUPPORTED_SLOT_RE = re.compile(
    r"<!--\s*identity:slot:\s*personal-profile\s*-->", re.IGNORECASE
)
# Zero-width and BOM characters defeat `[\w.-]+` mid-login. Stripped before matching.
_ZERO_WIDTH = dict.fromkeys(
    map(ord, "\u200b\u200c\u200d\u200e\u200f\ufeff\u2060"), None
)

# REFUSE: a FILLED Rule 00 inside kit content. Rule 00 IS the user-profile file, but
# core's own is the WHITE-LABEL TEMPLATE carrying the `identity:slot` marker , the very
# mechanism this story extends. Tuning finding T1: refuse only when the file has no slot
# marker and no `[TO BE CONFIGURED]` placeholders, i.e. when it has been FILLED IN.
# F9 (S4): the first version matched only `rules/00-*.md` lowercase, so `00-...MD`,
# `persona/00-...`, `rules/00-user.yaml` and `persona-00-the-user.rules.md` all dodged
# it. And the "unfilled" exemption fired on a bare `{{` ANYWHERE , one Jinja example
# in an otherwise FILLED Rule 00 disabled the whole detector. The exemption now
# requires the identity:slot marker specifically, or explicit [TO BE CONFIGURED]
# placeholders, and is refused outright if the file also carries filled identity fields.
# S5 follow-up: F9 widened this to any `00-*` file in any segment, which over-shot ,
# ordinary numbered documents (`00-design-brief.md`, `00-extracted-index.md`) tripped
# it. The signal is a USER-PROFILE file, so the name must indicate one: `00-the-user`,
# `00-user`, `00-profile`, or a `rules/`-located `00-*`. A numbered analysis doc is not
# a Rule 00. Content still decides , _FILLED_IDENTITY_RE gates the refusal.
_RULE00_RE = re.compile(
    r"(?:^|[/-])00[-_](?:the[-_])?(?:user|profile|persona)[^/]*\.(?:md|ya?ml|txt)$"
    r"|(?:^|/)rules/00[-_][^/]*\.(?:md|ya?ml|txt)$",
    re.IGNORECASE,
)
_UNFILLED_RULE00_RE = re.compile(
    r"<!--\s*identity:slot:|\[TO BE CONFIGURED\]", re.IGNORECASE
)
# Fields that indicate a Rule 00 has been FILLED IN with a real person.
# The value must be a REAL one , `**Full Name**: [TO BE CONFIGURED]` is the
# white-label template, not a filled profile (false positive on core's own Rule 00).
_FILLED_IDENTITY_RE = re.compile(
    r"^\s*(?:\*\*)?(?:Full Name|Primary Identity|Alias|Nationality|Religion|"
    r"Political|Marital|Family)(?:\*\*)?\s*:\s*(?!\[|\{\{|<|TO BE|TBD|N/A)\S",
    re.IGNORECASE | re.MULTILINE,
)
# FLAG: a heading that typically introduces personal content.
_PERSONAL_HEADING_RE = re.compile(
    r"^#{1,6}\s+.*\b(values|personal|identity|background|beliefs)\b",
    re.IGNORECASE | re.MULTILINE,
)
# FLAG: an author/owner frontmatter key carrying a non-placeholder value.
_AUTHOR_KEY_RE = re.compile(
    r"^(author|owner|maintained_by|assignee)\s*:\s*['\"]?([^'\"\n]+)", re.MULTILINE
)
# F11 (S4): every branch was a PREFIX test under re.match, so `-Sam Real`,
# `N/Amelia` and `TBDavid` all classified as placeholders , and any author value
# starting with `-` (a YAML list item) was silently dropped. Anchored with \Z.
_PLACEHOLDER_RE = re.compile(
    r"^\s*(?:\[[^\]]*\]|\{\{[^}]*\}\}|<[^>]*>|TO BE\b.*|TBD|N/A|-|''|\"\")\s*\Z"
    r"|^\s*\Z",
    re.IGNORECASE,
)

_TOKEN_RE = re.compile(r"\w+")


def _tokenise(text: str) -> list[str]:
    """Casefolded word tokens , the SINGLE shared tokeniser used by both the matcher
    and the `hash` subcommand, so add-time and match-time never drift."""
    return [t.casefold() for t in _TOKEN_RE.findall(text)]


def _hash(salt: str, normalised: str) -> str:
    return hashlib.sha256(f"{salt}\x00{normalised}".encode()).hexdigest()


def _entry_for(literal: str, salt: str) -> dict | None:
    tokens = _tokenise(literal)
    if not tokens:
        return None
    n = len(tokens)
    return {
        "h": _hash(salt, " ".join(tokens)),
        "mode": "word" if n == 1 else "ngram",
        "n": n,
    }


def _config_path(script_dir: Path) -> Path:
    override = os.environ.get(CONFIG_ENV)
    return Path(override) if override else script_dir / CONFIG_NAME


def _load_config(script_dir: Path) -> dict:
    """Load + validate the config. FAIL CLOSED (raise) on any problem , a missing or
    malformed config must never silently pass."""
    cfg_path = _config_path(script_dir)
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "salt" not in data or "tokens" not in data:
        raise ValueError(f"{cfg_path}: missing 'salt' or 'tokens'")
    if not isinstance(data["salt"], str) or not data["salt"]:
        raise ValueError(f"{cfg_path}: 'salt' must be a non-empty string")
    if not isinstance(data["tokens"], list):
        raise ValueError(f"{cfg_path}: 'tokens' must be a list")
    if not isinstance(data.get("never_migrate", []), list):
        raise ValueError(f"{cfg_path}: 'never_migrate' must be a list")
    # F10 (S4): entries were only checked as a LIST, and the loops skipped anything
    # malformed with `if isinstance(nm, dict) and nm.get("path")` , so a string entry,
    # a typo'd key or an empty path was SILENTLY IGNORED. `tokens` fails closed on the
    # same shape; never_migrate must too.
    for nm in data.get("never_migrate", []):
        if not isinstance(nm, dict):
            raise ValueError(
                f"{cfg_path}: never_migrate entry is not an object: {nm!r}"
            )
        if not isinstance(nm.get("path"), str) or not nm["path"].strip():
            raise ValueError(f"{cfg_path}: never_migrate entry has no 'path': {nm!r}")
        if not isinstance(nm.get("reason"), str) or not nm["reason"].strip():
            raise ValueError(f"{cfg_path}: never_migrate entry has no 'reason': {nm!r}")
    return data


def _norm_path(value: str) -> str:
    """Casefold and normalise separators , F10: matching was case-sensitive plain
    `in`, so a lower-cased spelling of a configured path evaded it."""
    return value.replace("\\", "/").casefold()


def _index(tokens: list[dict]) -> tuple[set[str], dict[int, set[str]]]:
    """Split configured hashes into the word set and the per-n ngram sets. A
    hand-edited config must fail closed, never mask a token with n=0 or a bad mode."""
    word_hashes: set[str] = set()
    ngram_by_n: dict[int, set[str]] = {}
    for tok in tokens:
        if not isinstance(tok, dict):
            raise ValueError(f"token entry is not an object: {tok!r}")
        h, mode, n = tok.get("h"), tok.get("mode"), tok.get("n")
        if not h or mode not in ("word", "ngram") or not isinstance(n, int) or n < 1:
            raise ValueError(f"malformed token entry: {tok!r}")
        if mode == "word":
            word_hashes.add(h)
        else:
            ngram_by_n.setdefault(n, set()).add(h)
    return word_hashes, ngram_by_n


# US-353 S3: an AUTHORSHIP key value is not a leak , it is the credit line, and the
# house convention carries the maintainer's name in 439 shipped files. The denylist is
# a REFUSE detector, so seeding it with the maintainer's own name would refuse the
# entire corpus for crediting its author. US-352 already classifies an authorship key
# as FLAG (aggregated, T3, never fatal); this keeps the two consistent by removing the
# authorship VALUE from the denylist's input.
#
# Scoped BY KEY, not by line (the US-352 F0 lesson: a line filter is defeated by
# anything that puts the payload on a different line). Only the value of a recognised
# authorship key is dropped; the same literal ANYWHERE else still REFUSES, so the
# detector keeps its meaning for prose , which is the class it exists to catch.
_AUTHORSHIP_KEYS = ("author", "owner", "maintained_by", "assignee")

# US-353 S7 P2 , ALLOWLIST, not a denylist of shapes. Three rounds of this exemption
# were bypassed in turn: a line regex (S4) fell to a value YAML wrapped onto the next
# line; a block parser (S5) fell to a list-form key; and that fell to flow-style
# mappings
# (`key: {a: '...'}`) and spaced colons (`key   : '...'`). Each fix enumerated one more
# shape to exclude, which is unwinnable , a fourth form always exists.
#
# Inverted here: exempt ONLY the exact shape the corpus uses, measured , `key: value` on
# ONE line, value a bare or quoted scalar (443 `maintained_by`, 11 `author`, 6
# `assignee`; ZERO use any other form). Everything else , lists, flow mappings, block
# scalars, wrapped values , falls through to the detector. A new YAML form cannot bypass
# an allowlist; at worst it is a false REFUSE on an authorship line, which fails CLOSED
# and is the correct direction to err.
# The two shapes the corpus measurably uses, and nothing else (US-353 S7 remediation:
# the first allowlist rejected 4 of 460 real authorship lines , a flow-sequence
# placeholder `assignee: [User Name]` and three values carrying a trailing `# comment`.
# Neither held a denylisted literal today, so it was LATENT not live , but `assignee` is
# exactly where a real name lands, so it would have become a false REFUSE on ordinary
# usage. Fail-closed is the right direction; a gate that predictably reds on normal work
# trains click-through, which is the failure US-357 warns about).
# BOUNDED BY LENGTH as well as by shape. Widening to accept `assignee: [User Name]`
# re-opened the flow-form channel , a sequence absorbed a full Article 9 sentence, the
# same abuse the flow MAPPING allowed. Measured: the longest real authorship value in
# the corpus is 23 characters (n=460, p99=17). A name or placeholder is short; a
# sentence is not. 64 gives ~3x headroom and still closes the channel.
_AUTHORSHIP_MAX_VALUE = 64
_AUTHORSHIP_SCALAR = re.compile(
    r"^(?:author|owner|maintained_by|assignee)[ \t]*:[ \t]*"
    r"(?:'[^'\n]*'|\"[^\"\n]*\"|\[[^\[\]\n]*\]|[^\n{}\[\]|>&*]*?)"
    r"[ \t]*(?:#[^\n]*)?$"
)


def _is_authorship_line(line: str) -> bool:
    """An authorship line is exempt only if it matches an allowlisted SHAPE and its
    value is short enough to be a name rather than prose."""
    if not _AUTHORSHIP_SCALAR.match(line):
        return False
    value = line.split(":", 1)[1]
    value = re.sub(r"\s*#.*$", "", value).strip()
    return len(value) <= _AUTHORSHIP_MAX_VALUE


def _strip_authorship_values(text: str) -> str:
    """Blank the VALUE of an authorship key, keeping the key so US-352's separate
    authorship FLAG detector still sees it.

    Only the FRONTMATTER block is considered , an `author:`-shaped line in the BODY is
    prose and stays subject to the denylist.
    """
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    head, body = text[: end + 4], text[end + 4 :]
    out = []
    for line in head.split("\n"):
        if _is_authorship_line(line):
            out.append(line.split(":", 1)[0] + ":")
        else:
            out.append(line)
    return "\n".join(out) + body


def _denylist_hits(text: str, salt: str, words: set[str], ngrams: dict[int, set[str]]):
    """Return the hash-classes present. Reports the CLASS, never the literal ,
    printing the plaintext would re-leak exactly what the gate protects."""
    hits: list[str] = []
    tokens = _tokenise(_strip_authorship_values(text))
    if words:
        for t in tokens:
            if _hash(salt, t) in words:
                hits.append("denylist:word")
                break
    for n, hset in ngrams.items():
        for i in range(len(tokens) - n + 1):
            if _hash(salt, " ".join(tokens[i : i + n])) in hset:
                hits.append(f"denylist:ngram-{n}")
                break
    return hits


SCAN_RECORD_ENV = "PERSONAL_DATA_SCAN_RECORD"


def _emit_scan_record(**fields) -> None:
    """US-352 C4 (S5 A2) , retain evidence that the scan RAN, over what, and with
    what result.

    Rule 07 Control 5 requires an effectful action to be traceable to the decision that
    authorised it. Printing counts to stdout leaves the only record in a CI log with a
    default retention, which asserts the scan happened rather than evidencing it.
    One JSONL line per run, appended where `PERSONAL_DATA_SCAN_RECORD` points; a no-op
    when unset, so local runs stay silent and CI can archive the file.
    """
    dest = os.environ.get(SCAN_RECORD_ENV)
    if not dest:
        return
    record = {
        "utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "gate": "check-personal-data",
        "root": str(fields.pop("root")),
        **fields,
    }
    try:
        with open(dest, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
    except OSError as exc:
        # Evidence-keeping must not become a new failure mode for the control itself.
        print(f"personal-data: could not write scan record: {exc}", file=sys.stderr)


def _scannable_config_text(text: str) -> str:
    """The gate's own config, minus ONLY the salt and the token hashes.

    F0: everything else , `never_migrate` paths and reasons, `$comment` prose, any
    key a maintainer adds , is free text inside a file that ships in `kits/core`, so
    it is scanned like any other asset. Falls back to the raw text if the config does
    not parse, because an unparseable config must not become an exemption.
    """
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return text
    if not isinstance(data, dict):
        return text
    scannable = {k: v for k, v in data.items() if k not in ("salt", "tokens")}
    # Keep the REASONS (free prose, must be scanned) but drop the declared PATHS,
    # which would otherwise match themselves.
    if isinstance(scannable.get("never_migrate"), list):
        scannable["never_migrate"] = [
            {k: v for k, v in nm.items() if k != "path"}
            for nm in scannable["never_migrate"]
            if isinstance(nm, dict)
        ]
    return json.dumps(scannable, ensure_ascii=False)


def check_file(path: Path, root: Path, cfg: dict, words, ngrams) -> tuple[list, list]:
    """Return (refusals, flags) for one asset. FAIL CLOSED on an unreadable in-scope
    asset , an asset the gate cannot READ is an asset it cannot clear."""
    rel = path.relative_to(root).as_posix()
    # F3 (S4): skip symlinks. `deploy/registry.py kit_source_files` , the canonical
    # walk this gate should match , deliberately skips them so a kit cannot pull
    # out-of-tree bytes. Following them let a link to /etc/passwd be scanned as kit
    # content, and a symlinked DIRECTORY would hide a subtree from the scan entirely.
    if path.is_symlink():
        return [f"{rel}: symlink in kit content (cannot clear out-of-tree bytes)"], []
    self_ref = rel in SELF_REFERENTIAL_RELPATHS
    refusals: list[str] = []
    flags: list[str] = []

    # Path-shaped signals apply to any file, text or not.
    rule00 = bool(_RULE00_RE.search(rel))
    prose = _is_governance_prose(rel)
    rel_norm = _norm_path(rel)
    if not prose:
        for nm in cfg.get("never_migrate", []):
            if _norm_path(nm["path"]) in rel_norm:
                refusals.append(f"{rel}: never-migrate path ({nm['reason']})")

    # F2: read everything except known-binary suffixes.
    if path.suffix.lower() in BINARY_SUFFIXES:
        return refusals, flags
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeDecodeError):
        return (
            refusals
            + [f"{rel}: unreadable in-scope asset (cannot clear , FAIL CLOSED)"],
            flags,
        )
    if self_ref:
        # F0: the gate's own files stay IN SCOPE , only the self-referential
        # CONSTRUCTS are excluded, never the whole file.
        #
        # The config is excluded STRUCTURALLY, not by line: a minified one-line JSON
        # puts `"salt"` and a payload on the SAME line, so line-filtering would drop
        # the payload with it (found by re-testing the first fix). Parse it and scan
        # every value except the salt and the token hashes.
        if path.suffix.lower() == ".json":
            # `never_migrate` is EXCLUDED too: it is the DECLARATION of the blocked
            # paths, so scanning it for those paths refuses the very list that defines
            # them. Its `reason` prose is retained and scanned , only the paths go.
            text = _scannable_config_text(text)
        else:
            text = "\n".join(
                ln for ln in text.splitlines() if not _SELF_PATTERN_MARKER.search(ln)
            )
    # F1: zero-width characters defeat the login character class.
    text = text.translate(_ZERO_WIDTH)

    if rule00 and (
        _FILLED_IDENTITY_RE.search(text) or not _UNFILLED_RULE00_RE.search(text)
    ):
        refusals.append(f"{rel}: FILLED rule-00 user-profile file inside kit content")
    # SPEC.md DOCUMENTS the marker (in the warning that forbids its use); a kit asset
    # would PLACE it for resolution. Narrow, path-anchored, and scoped to THIS rule
    # only , everything else in SPEC.md is still scanned (the F0 lesson: never exempt
    # a shipped file wholesale).
    if not prose and _UNSUPPORTED_SLOT_RE.search(text):
        refusals.append(
            f"{rel}: references identity:slot personal-profile, which the resolver "
            "does not yet support (SPEC 9.4 is a CONTRACT, not current behaviour)"
        )
    if _HOME_PATH_RE.search(text) and not _is_historical_record(rel):
        refusals.append(f"{rel}: absolute home-directory path (a real login)")
    for cls in _denylist_hits(text, cfg["salt"], words, ngrams):
        refusals.append(f"{rel}: {cls}")
    if not prose:
        text_norm = _norm_path(text)
        for nm in cfg.get("never_migrate", []):
            if _norm_path(nm["path"]) in text_norm:
                refusals.append(
                    f"{rel}: references never-migrate path ({nm['reason']})"
                )
    if _PERSONAL_HEADING_RE.search(text):
        flags.append(f"{rel}: personal-content heading")
    for m in _AUTHOR_KEY_RE.finditer(text):
        if not _PLACEHOLDER_RE.match(m.group(2).strip()):
            # Tuning finding T3: authorship attribution is normal in published
            # software and fires on 431 files. Tagged so the reporter can COLLAPSE it
            # to one aggregate line , suppressing it entirely would hide a real
            # publisher decision, listing each would bury every other signal.
            flags.append(f"ATTRIBUTION\t{rel}: {m.group(1)} key names an individual")
            break
    return refusals, flags


def _cmd_hash(literal: str, script_dir: Path) -> int:
    """Print a paste-ready config entry for a literal , so a maintainer never has to
    put the plaintext in the config (or in a commit message) to add it."""
    cfg = _load_config(script_dir)
    entry = _entry_for(literal, cfg["salt"])
    if entry is None:
        print("no word tokens in that literal , nothing to match", file=sys.stderr)
        return 2
    print(json.dumps(entry))
    return 0


def main(argv: list[str]) -> int:
    script_dir = Path(__file__).resolve().parent
    if len(argv) >= 2 and argv[1] == "hash":
        if len(argv) != 3:
            print(f'usage: {argv[0]} hash "LITERAL"', file=sys.stderr)
            return 2
        return _cmd_hash(argv[2], script_dir)

    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    docs_name = _resolve_docs_root_name(root)
    scan_roots = [root / r for r in (*SCAN_ROOTS_STATIC, docs_name)]
    kits = scan_roots[0]
    try:
        cfg = _load_config(script_dir)
        words, ngrams = _index(cfg["tokens"])
    except Exception as exc:  # noqa: BLE001  (config problems FAIL CLOSED)
        print(f"personal-data: config error: {exc}", file=sys.stderr)
        return 2

    if not kits.is_dir():
        # DIVERGENCE FROM SEC-001 (US-352 AC4): it returns 0 here. A gate that passes
        # while scanning nothing is the defect this AC exists to prevent.
        print(
            f"personal-data: {kits} not present , NOTHING SCANNED (fail closed).",
            file=sys.stderr,
        )
        return 2

    assets = []
    for sr in scan_roots:
        if not sr.is_dir():
            continue
        for p in sr.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
            if any(seg in rel for seg in EXCLUDED_PREFIXES):
                continue
            if p.name in EXCLUDED_NAMES:
                continue
            assets.append(p)
    if not assets:
        print(
            f"personal-data: 0 files under {kits} , NOTHING SCANNED (fail closed).",
            file=sys.stderr,
        )
        return 2

    refusals: list[str] = []
    flags: list[str] = []
    n_read = 0
    for asset in assets:
        r, f = check_file(asset, root, cfg, words, ngrams)
        # F16 (S4): the scanned count included files never OPENED (binary, symlink),
        # overstating coverage , a 10-file tree reported "10 scanned" with 4 unread.
        # AC4's breadth claim is only honest if it counts what was actually read.
        if not asset.is_symlink() and asset.suffix.lower() not in BINARY_SUFFIXES:
            n_read += 1
        refusals.extend(r)
        flags.extend(f)

    # Collapse the ATTRIBUTION class to one aggregate line (tuning T3): it fires on
    # every file carrying a `maintained_by:`/`author:` key, which is routine in
    # published software. Kept VISIBLE as a count , shipping a real person's name is a
    # publisher decision, not a defect , but never as N separate lines.
    attribution = [f for f in flags if f.startswith("ATTRIBUTION\t")]
    flags = [f for f in flags if not f.startswith("ATTRIBUTION\t")]

    n_tok = len(words) + sum(len(s) for s in ngrams.values())
    if n_tok == 0:
        # F12 (S4): the empty denylist was buried mid-sentence in a line ending in
        # reassuring prose, while the docstring advertised it as a live control.
        # SEC-001 prints an explicit warning; so does this.
        print(
            "personal-data: WARNING , 0 denylist token(s) configured. The denylist "
            "detector is INERT; only the structural signals are enforcing.",
            file=sys.stderr,
        )
    if attribution:
        print(
            f"personal-data: {len(attribution)} file(s) carry an authorship key naming "
            f"an individual (routine in published software; a publisher "
            f"decision, not a "
            f"defect , `grep -rl maintained_by kits/` to review)"
        )
    if refusals:
        print(f"personal-data: {len(refusals)} refusal(s) under {kits}:")
        for v in refusals:
            print(f"  REFUSE {v}")
        if flags:
            print(f"personal-data: {len(flags)} flag(s) for review")
        return 1
    if flags:
        print(f"personal-data: {len(flags)} flag(s) for review:")
        for v in flags:
            print(f"  flag   {v}")
    _emit_scan_record(
        root=kits,
        read=n_read,
        walked=len(assets),
        refusals=len(refusals),
        flags=len(flags) + len(attribution),
        tokens=n_tok,
    )
    # US-353 S5 A1: with ZERO tokens the denylist DID NOT RUN , the result is
    # indistinguishable from a run that checked and found nothing. A count buried in the
    # summary is not enough: "0 refusals" reads as a pass. Say it in its own line, so a
    # reader does not have to know to ask. (This is the standing state in CI, where no
    # PERSONAL_DATA_CONFIG is set and the committed config ships no tokens by design.)
    if n_tok == 0:
        print(
            "personal-data: NOTE , 0 denylist tokens configured, so the DENYLIST HALF "
            "DID NOT RUN. Only the structural detectors and the never-migrate list "
            "were applied. A prose-form personal literal would NOT be caught by this "
            "run. Point PERSONAL_DATA_CONFIG at a seeded config to enable it."
        )
    print(
        f"personal-data: {n_read} text asset(s) READ of {len(assets)} walked, against "
        f"{n_tok} configured token(s) + structural signals, 0 refusals, "
        f"{len(flags)} flag(s) , never a clean bill of health (open classes are not "
        f"semantically detectable; binary assets are not read)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
