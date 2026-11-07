#!/usr/bin/env python3
"""No-client-literal gate: kit content must carry no configured client literal.

SEC-001 (EP-108). A BLOCKING, fail-closed pre-publish control over ``kits/``: no
client-confidential codename, project name, customer name, or named individual
may appear in any kit asset (and therefore never reach a published marketplace
artefact). It is the confidentiality half of the marketplace pipeline (US-217 is
the publish mechanism; this gate is the precondition it must call).

WHY HASHES, NOT A PLAINTEXT DENYLIST (S1 D-Storage): this repo is marketplace-
bound (publishable). A committed plaintext denylist of client literals (a
codename, a bank name, a person's name, ...) would itself LEAK the very secrets
the gate exists to keep out , AND this very file lives under ``kits/`` and is
scanned, so it must name NO real literal. So the literal set is stored as SALTED
SHA-256 hashes in ``client-literals.json`` , no plaintext client literal is ever
committed, and every example below is fictional (e.g. "Acme", "Zephyr").

HONEST LIMITATION (S1-1, for S5): the salt is in-tree, so low-entropy tokens are
brute-forceable from the committed config. The control this gate provides is "no
plaintext literal in the repo, and no literal in a shipped kit", NOT cryptographic
secret-hiding against a motivated attacker. Defence-in-depth is the manual
first-publish review checkpoint (Story Risk 1).

MATCHING (S1-2): token-based, case-insensitive. Files are tokenised
(``\\w+``, casefolded). ``word`` literals match a single token at its boundary
(so a fictional "Acme" does NOT match "Acmewidget"). ``ngram`` literals match N
consecutive tokens (so a fictional "Jane Roe" matches the adjacent pair, not the
two words apart). This is a deliberate, documented deviation from white-label's
raw-substring mode , you cannot hash "every substring", and whole-word /
whole-phrase IS the correct semantic for codenames and names, and it is what kills
the generic-token false-positive (R1).

SCOPE (S1-3): scans ``kits/`` text files only; self-exempts this gate's own files
(anchored to their real relative location, S4-#2). The backlog/audit docs that
legitimately name the literals live under ``docs-copper/`` , out of scope.

ACCEPTED RESIDUALS (S5), all backstopped by the manual first-publish review
checkpoint (Story Risk 1):
  - Deliberate intra-token obfuscation (S5-#4) , "Nor-kom", "N0rkom", homoglyphs,
    zero-width chars , evades whole-token matching. An insider deliberately
    obfuscating a codename is out of scope for an automated gate.
  - Non-text assets (S5-#5) , suffixes outside TEXT_SUFFIXES (images, .csv/.svg/...)
    are not scanned. Extend the set as kits gain such assets.
  - Brute-force from the in-tree salt (S5-#6) , bare SHA-256 is used DELIBERATELY,
    not a slow KDF (scrypt/argon2): the matcher hashes EVERY token of EVERY kit file,
    so a per-guess-slow KDF is infeasible at scan volume. The salt is anti-casual-
    disclosure, not credential-grade secrecy; the literals are codenames/names, not
    credentials, and the real control is non-shipment. Acceptable residual.

Usage:
    python3 check-no-client-literals.py [ROOT_DIR]     # scan ROOT/kits/
    python3 check-no-client-literals.py hash "LITERAL" # print a config entry

Exit codes:
    0 - no client literal found (or no literals configured , vacuous, reported)
    1 - a configured client literal was found in a kit asset
    2 - usage error or config missing/unreadable/malformed (FAIL CLOSED)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

CONFIG_NAME = "client-literals.json"
# Tests point this at a controlled config (known salt + literals they generate with
# the same `hash` logic); production resolves the config next to the script.
CONFIG_ENV = "NO_CLIENT_LITERALS_CONFIG"
# Self-exemption is anchored to the gate's OWN LOCATION (its source under kits/core/),
# by path RELATIVE to the scanned kits/ root , NOT by bare filename (S4-#2): a decoy
# named check-no-client-literals.py / client-literals.json ANYWHERE else in kits/ must
# still be scanned, or a literal could be smuggled into it. The compiled .opencode/
# .claude/ copies are outside kits/ and never scanned.
_SCRIPTS_REL = "core/skills/framework-authoring/scripts"
SELF_EXEMPT_RELPATHS = {
    f"{_SCRIPTS_REL}/check-no-client-literals.py",
    f"{_SCRIPTS_REL}/{CONFIG_NAME}",
}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".ts", ".sh"}

_TOKEN_RE = re.compile(r"\w+")


def _tokenise(text: str) -> list[str]:
    """Casefolded word tokens. The SINGLE shared tokeniser used by both the
    matcher and the ``hash`` subcommand, so add-time and match-time never drift
    (pre-mortem P2)."""
    return [t.casefold() for t in _TOKEN_RE.findall(text)]


def _hash(salt: str, normalised: str) -> str:
    """Salted SHA-256 of a normalised (already-casefolded, space-joined) phrase."""
    return hashlib.sha256(f"{salt}\x00{normalised}".encode()).hexdigest()


def _entry_for(literal: str, salt: str) -> dict | None:
    """Build a config entry for a literal: word (1 token) or ngram (N tokens).
    Returns None if the literal has no word tokens (nothing to match)."""
    tokens = _tokenise(literal)
    if not tokens:
        return None
    n = len(tokens)
    mode = "word" if n == 1 else "ngram"
    return {"h": _hash(salt, " ".join(tokens)), "mode": mode, "n": n}


def _config_path(script_dir: Path) -> Path:
    """The config override (env, for tests) else the script's sibling config."""
    override = os.environ.get(CONFIG_ENV)
    return Path(override) if override else script_dir / CONFIG_NAME


def _load_config(script_dir: Path) -> dict:
    """Load + validate the literal config. FAIL CLOSED (raise) on any problem ,
    a missing/malformed config must never silently pass (S1-4)."""
    cfg_path = _config_path(script_dir)
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "salt" not in data or "literals" not in data:
        raise ValueError(f"{cfg_path}: missing 'salt' or 'literals'")
    if not isinstance(data["salt"], str) or not data["salt"]:
        raise ValueError(f"{cfg_path}: 'salt' must be a non-empty string")
    if not isinstance(data["literals"], list):
        raise ValueError(f"{cfg_path}: 'literals' must be a list")
    return data


def _index(literals: list[dict]) -> tuple[set[str], dict[int, set[str]]]:
    """Split configured hashes into the word set and the per-n ngram sets."""
    word_hashes: set[str] = set()
    ngram_by_n: dict[int, set[str]] = {}
    for lit in literals:
        # S4-#3/#4: validate the shape (a hand-edited config must fail closed, not
        # raise an uncaught AttributeError or silently mask a literal with n=0 / a
        # bad mode).
        if not isinstance(lit, dict):
            raise ValueError(f"literal entry is not an object: {lit!r}")
        h, mode, n = lit.get("h"), lit.get("mode"), lit.get("n")
        if not h or mode not in ("word", "ngram") or not isinstance(n, int) or n < 1:
            raise ValueError(f"malformed literal entry: {lit!r}")
        if mode == "word":
            word_hashes.add(h)
        else:
            ngram_by_n.setdefault(n, set()).add(h)
    return word_hashes, ngram_by_n


def check_file(
    path: Path,
    kits_root: Path,
    salt: str,
    word_hashes: set[str],
    ngram_by_n: dict[int, set[str]],
) -> list[str]:
    """Return violation messages for one kit asset (file path + hash-class, NEVER
    the literal , reporting the plaintext would re-leak it)."""
    if path.suffix not in TEXT_SUFFIXES:
        return []
    if path.relative_to(kits_root).as_posix() in SELF_EXEMPT_RELPATHS:
        return []
    try:
        tokens = _tokenise(path.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        # FAIL CLOSED (S4-#1): an in-scope asset the gate cannot READ is an asset it
        # cannot clear. Treat it as a blocking violation, never a silent skip.
        return [f"{path}: unreadable in-scope asset (cannot clear , FAIL CLOSED)"]
    violations: list[str] = []
    if word_hashes:
        for tok in tokens:
            if _hash(salt, tok) in word_hashes:
                violations.append(
                    f"{path}: a configured client literal (word) is present"
                )
                break
    for n, hashes in ngram_by_n.items():
        hit = any(
            _hash(salt, " ".join(tokens[i : i + n])) in hashes
            for i in range(len(tokens) - n + 1)
        )
        if hit:
            violations.append(
                f"{path}: a configured client literal ({n}-gram) is present"
            )
    return violations


def _cmd_hash(literal: str) -> int:
    """Print a paste-ready config entry for a literal so the maintainer never puts
    plaintext in the repo (living data, S1-5)."""
    script_dir = Path(__file__).resolve().parent
    try:
        salt = _load_config(script_dir)["salt"]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"no-client-literals: config error: {exc}", file=sys.stderr)
        return 2
    entry = _entry_for(literal, salt)
    if entry is None:
        print("no-client-literals: literal has no word tokens", file=sys.stderr)
        return 2
    print(json.dumps(entry))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "hash":
        if len(argv) != 3:
            print('usage: check-no-client-literals.py hash "LITERAL"', file=sys.stderr)
            return 2
        return _cmd_hash(argv[2])

    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    kits = root / "kits"
    script_dir = Path(__file__).resolve().parent
    try:
        cfg = _load_config(script_dir)
        word_hashes, ngram_by_n = _index(cfg["literals"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        # FAIL CLOSED: a publish gate must never pass on a broken config.
        print(f"no-client-literals: config error (FAIL CLOSED): {exc}", file=sys.stderr)
        return 2

    if not word_hashes and not ngram_by_n:
        print("no-client-literals: 0 literals configured , nothing enforced yet.")
        return 0
    if not kits.is_dir():
        # Nothing scanned is not a pass (TD-201 A20): run it from the repository
        # root or pass the root that holds kits/.
        print(
            f"no-client-literals: {kits} not present , NOTHING SCANNED (FAIL CLOSED). "
            "Pass the root that holds kits/.",
            file=sys.stderr,
        )
        return 2

    assets = [p for p in kits.rglob("*") if p.is_file()]
    violations: list[str] = []
    for asset in assets:
        violations.extend(check_file(asset, kits, cfg["salt"], word_hashes, ngram_by_n))

    n_lit = len(word_hashes) + sum(len(s) for s in ngram_by_n.values())
    if violations:
        print(f"no-client-literals: {len(violations)} violation(s) under {kits}:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(
        f"no-client-literals: {len(assets)} kit asset(s) scanned against "
        f"{n_lit} configured literal(s), none present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
