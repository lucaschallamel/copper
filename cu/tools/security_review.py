"""The S5 security-review evidence check (US-393 AC3, AC9, AC10; D8, D14, D20).

`pipeline_validator.py verify <story> S5_ARCH_SEC_COMP_REVIEW` calls `problems()`.

A record with `change_surface.security_sensitive: true` ran the security-audit skill
in full-audit mode (D7). The full `findings.json` stays outside version control
(D20); the story's artefact folder holds a redacted summary and the coverage ledger:

    Findings summary: <path>        this story's redacted summary (tracked)
    Findings digest: sha256:<hex>   SHA-256 of the full findings.json
    Findings JSON: <path>           where the full file lives (optional, untracked)
    Coverage ledger: <path>         this story's ledger (tracked)
    Audit source ref: <commit>      the commit the audit read

The ledger passes the vendored validator and covers every changed trust-boundary
path; the summary carries no detail and no unfixed Critical or High (D14); when the
full file is present it is untracked, passes its validator, matches the digest and
agrees with the summary. A record that is not security-sensitive states
`no trust boundary touched: <reason>`, or `trust boundary touched, not
security-sensitive: <reason>` when its diff touches a path in the project's list,
read from the default branch so a story cannot edit the list that judges it (D5,
D6, D12). Anything that cannot be checked is an error naming the cause (TD-201);
an absent list, or an absent full findings file, is a warning.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

SUMMARY = "Findings summary:"
DIGEST = "Findings digest:"
FINDINGS = "Findings JSON:"
LEDGER = "Coverage ledger:"
SOURCE_REF = "Audit source ref:"
NO_BOUNDARY = "no trust boundary touched:"
TOUCHED = "trust boundary touched, not security-sensitive:"
PATH_LIST = "trust-boundary-paths.json"
FINDINGS_VALIDATOR = "validate-findings.cjs"
LEDGER_VALIDATOR = "validate-coverage-ledger.cjs"
TIMEOUT_S = 60
MAX_BYTES = 5 * 1024 * 1024  # the vendored validators' own input cap
OPEN_UNITS = {"planned", "in_progress"}
COVERING_UNITS = {"covered", "candidate"}
SUMMARY_KEYS = {"fingerprint", "verdict", "severity", "title", "disposition"}
MUST_FIX = {"critical", "high"}
NO_LIST = f"{PATH_LIST} not on the default branch: the path check did not run"
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}")
_COMMIT = re.compile(r"[0-9a-f]{40}")
_FILED = re.compile(r"filed:[A-Z]{2,4}-\d+")

Problems = tuple[list[str], list[str]]


@dataclass
class Git:
    """The story's view of git: its branch against the default branch."""

    root: Path
    branch: str | None = None
    _base: str | None = field(default=None, repr=False)

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def base(self) -> str:
        """origin/HEAD, else origin/main, else main (a stale local main lags)."""
        if self._base is None:
            head = self.run("symbolic-ref", "--short", "refs/remotes/origin/HEAD")
            remote = self.run("rev-parse", "--verify", "-q", "refs/remotes/origin/main")
            if head.returncode == 0 and head.stdout.strip():
                self._base = head.stdout.strip()
            else:
                self._base = "origin/main" if remote.returncode == 0 else "main"
        return self._base

    def tip(self) -> str:
        return self.branch or "HEAD"

    def changed(self) -> list[str]:
        """Paths the story changed; renames list both sides (`--no-renames`)."""
        span = f"{self.base()}...{self.tip()}"
        proc = self.run("diff", "--name-only", "--no-renames", span)
        if proc.returncode != 0:
            raise RuntimeError(
                f"git diff {span} failed: cannot list the story's changed paths"
                " (is the branch present locally?)"
            )
        paths = [p for p in proc.stdout.splitlines() if p]
        if not paths:
            raise RuntimeError(f"git diff {span} is empty: the branch has no change")
        return paths

    def show_base(self, rel: str) -> str | None:
        """`rel` as the default branch has it; None when the file is not there."""
        proc = self.run("show", f"{self.base()}:{rel}")
        if proc.returncode == 0:
            return proc.stdout
        if self.run("rev-parse", "--verify", "-q", self.base()).returncode != 0:
            raise RuntimeError(f"git cannot resolve {self.base()}: cannot read {rel}")
        return None

    def is_story_commit(self, sha: str) -> bool:
        """On the story branch and not already on the default branch."""
        on_tip = self.run("merge-base", "--is-ancestor", sha, self.tip())
        on_base = self.run("merge-base", "--is-ancestor", sha, self.base())
        return on_tip.returncode == 0 and on_base.returncode != 0

    def ignored(self, path: Path) -> bool:
        return self.run("check-ignore", "-q", str(path)).returncode == 0


def problems(
    root: Path,
    pipeline_dir: str,
    yaml_data: dict,
    stage_data: dict,
    skill_dir: Path,
    git: Git,
    *,
    story_id: str,
) -> Problems:
    """Errors and warnings for an S5 record; ([], []) when it passes."""
    lines = [str(line) for line in (stage_data.get("evidence") or [])]
    surface = yaml_data.get("change_surface") or {}
    globs, problem = _globs(git, f"{pipeline_dir}/{PATH_LIST}")
    if problem:
        return [problem], []
    if surface.get("security_sensitive") is True:
        audit = Audit(
            root, f"{pipeline_dir}/artifacts", skill_dir, story_id, git, globs
        )
        errors, warnings = _audit_problems(audit, lines)
        if globs is None:  # D12: an absent list never passes silently
            warnings.append(NO_LIST)
        return errors, warnings
    return _boundary_problems(globs, lines, git)


def _value(lines: list[str], prefix: str) -> str | None:
    """The rest of the first evidence line that STARTS with `prefix` (quotes
    stripped) and carries a real value: empty or `<placeholder>` does not count."""
    for line in lines:
        text = line.strip().strip("`'\"").strip()
        if not text.startswith(prefix):
            continue
        value = text[len(prefix) :].strip().strip("`'\"").strip()
        if value and not (value.startswith("<") and value.endswith(">")):
            return value
    return None


def _read_bytes(path: Path) -> bytes:
    """One capped, no-follow read: what the validator accepted is what is used."""
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path.name} exceeds {MAX_BYTES} bytes")
    return data


def _read_json(path: Path) -> object:
    return json.loads(_read_bytes(path).decode("utf-8"))


# --- security-sensitive: ledger, summary, source ref, full findings -------


@dataclass(frozen=True)
class Audit:
    """What the security-sensitive check needs to know about the story."""

    root: Path
    artefacts: str
    skill_dir: Path
    story_id: str
    git: Git
    globs: list[str] | None


def _audit_problems(audit: Audit, lines: list[str]) -> Problems:
    errors: list[str] = []
    for prefix, check in ((LEDGER, _ledger_problem), (SUMMARY, _summary_problem)):
        value = _value(lines, prefix)
        if not value:
            errors.append(
                f"security-sensitive S5 evidence lacks a '{prefix} <path>' line"
            )
            continue
        path, problem = _contained(audit, value)
        problem = problem or check(audit, path)
        if problem:
            errors.append(f"{prefix} {value}: {problem}")
    errors += _ref_problems(audit, lines)
    digest = _value(lines, DIGEST)
    if not digest or not _SHA256.fullmatch(digest):
        errors.append(
            f"security-sensitive S5 evidence lacks a '{DIGEST} sha256:<hex>' line"
        )
        return errors, []
    if errors:
        return errors, []
    return _full_findings(audit, lines, digest)


def _contained(audit: Audit, value: str) -> tuple[Path, str | None]:
    """This story's tracked file, inside the artefact folder, no symlink on the way."""
    root = audit.root.resolve()
    folder = (root / audit.artefacts).resolve()
    path = (root / value).resolve()
    if Path(value).is_absolute() or not path.is_relative_to(folder):
        return path, f"must be a file inside the artefact folder {audit.artefacts}/"
    if Path(os.path.normpath(root / value)) != path:
        return path, "must not pass through a symbolic link"
    if not Path(value).name.startswith(f"{audit.story_id}-s5-"):
        return (
            path,
            f"must be this story's file ({audit.story_id}-s5-...), not another's",
        )
    if not path.is_file():
        return path, "not found"
    return path, None


def _validate(root: Path, script: Path, path: Path) -> str | None:
    node = shutil.which("node")
    if node is None:
        return f"node not found on PATH: cannot run {script.name} (install node)"
    if not script.is_file():
        return f"validator not found: {script}"
    try:
        proc = subprocess.run(
            [node, str(script), str(path)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
            cwd=root,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"{script.name} timed out after {TIMEOUT_S}s"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()[-1:] or [""]
        return f"{script.name} rejected it (exit {proc.returncode}): {tail[0][:200]}"
    return None


def _ledger_problem(audit: Audit, path: Path) -> str | None:
    problem = _validate(audit.root, audit.skill_dir / LEDGER_VALIDATOR, path)
    if problem:
        return problem
    units = _read_json(path)
    return _coverage_problem(units) or _scope_problem(units, audit)


def _coverage_problem(units: list) -> str | None:
    """The ledger must show coverage: units exist, none open, one covering (D8)."""
    statuses = {unit.get("status") for unit in units}
    if not statuses:
        return "no coverage unit: the ledger must show what the audit covered"
    if OPEN_UNITS & statuses:
        return f"units still open {sorted(OPEN_UNITS & statuses)}: audit unfinished"
    if not COVERING_UNITS & statuses:
        return "no unit covered: every unit is deferred, blocked or out of scope"
    return None


def _scope_problem(units: list, audit: Audit) -> str | None:
    """Reviewed paths meet the diff and include every changed boundary path (M2)."""
    # A unit's reviewed_paths already hold every check's paths (the validator
    # refuses a check path missing from them), so the units are enough.
    reviewed = {p for unit in units for p in unit.get("reviewed_paths") or []}
    try:
        diff = audit.git.changed()
    except RuntimeError as error:
        return str(error)
    if not reviewed & set(diff):
        return "the ledger reviews none of the story's changed paths"
    globs = audit.globs or []
    missing = [
        p
        for p in diff
        if any(fnmatch.fnmatch(p, g) for g in globs) and p not in reviewed
    ]
    if missing:
        return f"changed trust-boundary paths not reviewed: {', '.join(missing[:5])}"
    return None


def _summary_problem(audit: Audit, path: Path) -> str | None:
    """Redacted (allowed keys only) and no unfixed Critical or High (D14, D20)."""
    entries = _read_json(path)
    if not isinstance(entries, list):
        return "must be a JSON list of summary entries"
    for entry in entries:
        problem = _entry_problem(entry)
        if problem:
            return problem
    return None


def _entry_problem(entry: object) -> str | None:
    if not isinstance(entry, dict) or set(entry) != SUMMARY_KEYS:
        return f"each entry holds exactly {sorted(SUMMARY_KEYS)} (no finding detail)"
    fp, verdict, severity = entry["fingerprint"], entry["verdict"], entry["severity"]
    disposition = str(entry["disposition"])
    if verdict == "confirmed":
        if severity in MUST_FIX and disposition != "fixed":
            return (
                f"{fp}: a confirmed {severity} finding must be fixed before the merge"
            )
        if disposition != "fixed" and not _FILED.fullmatch(disposition):
            return f"{fp}: a confirmed finding is 'fixed' or 'filed:<STORY-ID>'"
    elif verdict not in ("needs_validation", "rejected"):
        return f"{fp}: unknown verdict {verdict!r}"
    elif severity is not None:
        return f"{fp}: only a confirmed finding carries a severity"
    return None


def _ref_problems(audit: Audit, lines: list[str]) -> list[str]:
    ref = _value(lines, SOURCE_REF)
    if not ref or not _COMMIT.fullmatch(ref):
        return [f"security-sensitive S5 evidence lacks a '{SOURCE_REF} <40-hex>' line"]
    if not audit.git.is_story_commit(ref):
        return [f"{SOURCE_REF} {ref}: not a commit of this story's branch"]
    return []


def _full_findings(audit: Audit, lines: list[str], digest: str) -> Problems:
    """When the full file is here: untracked, valid, matching the digest and summary."""
    value = _value(lines, FINDINGS)
    path = Path(value).expanduser() if value else None
    if path is not None and not path.is_absolute():
        path = audit.root / path
    if path is None or not path.is_file():
        return [], [
            "full findings.json not present here: digest and summary not compared"
        ]
    resolved = path.resolve()
    if resolved.is_relative_to(audit.root.resolve()) and not audit.git.ignored(
        resolved
    ):
        return [
            f"{FINDINGS} {value}: the full findings must stay out of version control"
        ], []
    problem = _validate(audit.root, audit.skill_dir / FINDINGS_VALIDATOR, resolved)
    if problem:
        return [f"{FINDINGS} {value}: {problem}"], []
    data = _read_bytes(resolved)
    if f"sha256:{hashlib.sha256(data).hexdigest()}" != digest:
        return [f"{FINDINGS} {value}: does not match {DIGEST} {digest}"], []
    records = json.loads(data.decode("utf-8"))
    summary = _read_json((audit.root / (_value(lines, SUMMARY) or "")).resolve())
    full = {(r["fingerprint"], r["verdict"], _severity(r)) for r in records}
    told = {(e["fingerprint"], e["verdict"], e["severity"]) for e in summary}
    if full != told:
        return [
            f"{SUMMARY} disagrees with the full findings"
            " (fingerprint, verdict, severity)"
        ], []
    return [], []


def _severity(record: dict) -> str | None:
    return (record.get("severity") or {}).get("overall_severity")


# --- not security-sensitive: the boundary claim ---------------------------


def _boundary_problems(globs: list[str] | None, lines: list[str], git: Git) -> Problems:
    if globs is None:
        return _claim(lines, NO_BOUNDARY, []), [NO_LIST]
    try:
        touched = [
            p for p in git.changed() if any(fnmatch.fnmatch(p, g) for g in globs)
        ]
    except RuntimeError as error:
        return [str(error)], []
    if touched:
        return _claim(lines, TOUCHED, touched[:5]), []
    return _claim(lines, NO_BOUNDARY, []), []


def _globs(git: Git, rel: str) -> tuple[list[str] | None, str | None]:
    """The trust-boundary globs as the default branch has them (D12, M3)."""
    try:
        text = git.show_base(rel)
    except RuntimeError as error:
        return None, str(error)
    if text is None:
        return None, None
    try:
        data = json.loads(text)
    except ValueError as error:
        return None, f"{PATH_LIST} is unreadable: {error}"
    data = data if isinstance(data, dict) else {}
    paths = data.get("paths")
    if not isinstance(data.get("version"), str):
        return None, f"{PATH_LIST} must carry a 'version' string"
    globs_ok = isinstance(paths, list) and all(isinstance(p, str) for p in paths)
    if not (globs_ok and paths):
        return None, f"{PATH_LIST} must hold a non-empty 'paths' list of globs"
    return paths, None


def _claim(lines: list[str], prefix: str, touched: list[str]) -> list[str]:
    if _value(lines, prefix):
        return []
    because = f" (the diff touches {', '.join(touched)})" if touched else ""
    return [f"S5 evidence lacks a '{prefix} <reason>' line{because}"]
