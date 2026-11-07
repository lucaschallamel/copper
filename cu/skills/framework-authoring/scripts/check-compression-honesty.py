#!/usr/bin/env python3
"""Compression-honesty gate (US-341, Axis B) , a prose edit must not silently
weaken a spec.

Axis A (the S5 semantic-preservation council) proves "nothing weakened" by
judgement. Axis B proves it mechanically: for each rule file changed against
`main`, every DIRECTIVE (MUST/SHOULD/NEVER/...) and every GOVERNING NUMERIC
THRESHOLD BOUND TO A RECOGNISED UNIT (a number + a unit from the closed list
below , 30 lines, >=80%, 5 methods) present in the BEFORE version must still be
present in the AFTER version (or in a resource the block was relocated to). A
threshold that vaguens into prose ("Max function lines: 30" -> "keep functions
small") is CAUGHT.

Axis B is one axis of a DUAL-axis gate, not a total guarantee on its own. It
covers directive tokens (by count) and unit-bound numeric thresholds (by
presence); it does NOT see ratio thresholds ("4.5:1"), bare-metric-name
thresholds ("cyclomatic complexity < 10"), or a single directive softened in
place while its token count holds (see the WORD_UNITS scope note and the extract()
docstring). Those residuals are the province of Axis A. A green Axis B means "no
covered directive/threshold was dropped", NOT "no governance was weakened".

Extraction is PROSE-ONLY (frontmatter, fenced code, and inline-code spans are
excluded, reusing the check-precedence approach) and GOVERNING-NUMBERS-ONLY (a
bare number like a date/ID/PR-number is ignored , only numbers bound to a
threshold unit count). This avoids a false-fail when an example carrying
`Sprint 002` / `PC123456` is relocated (US-341 S2 D-3).

Comparison is by PRESENCE (set membership), not count: every directive and
governing threshold that appears in BEFORE must appear at least once in AFTER
(or in a relocated resource). This is deliberate , US-341's method includes
"collapse a restated Summary/Reminder block to a pointer", which legitimately
removes DUPLICATE statements of a threshold; that must pass as long as the
threshold still appears once elsewhere. Only the LAST copy going missing (the
spec genuinely disappearing / vaguening) is a failure.

Whatever files the caller names, the gate also checks every governed file
(`kits/core/rules/*.rules.md`, `kits/core/instructions.md`) that git reports
changed since the branch point (TD-201 A9): a renamed rule is compared with its
source path, and a deleted one with empty text. A deleted rule's text counts as
moved only into a changed rule or a resource a changed rule newly references,
and the corpus net backs that credit as it backs any relocation. The comparison
point is `git merge-base <base> HEAD`, so a rule merged to the base after the
branch point is not this change's to answer for.

Usage:
    python3 check-compression-honesty.py <rule-file> [<rule-file> ...]
    python3 check-compression-honesty.py --base <git-ref> <rule-file> ...

Exit codes:
    0 - every directive + governing threshold round-trips
    1 - a directive or threshold was lost (a spec was weakened)
    2 - usage error
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

# Directive tokens (word-boundary, case-sensitive uppercase).
DIRECTIVE = re.compile(r"\b(MUST NOT|MUST|SHOULD NOT|SHOULD|NEVER|SHALL|REQUIRED)\b")

# Governing numeric threshold: a number bound to a RECOGNISED threshold UNIT.
# Written in the corpus in several shapes, all normalised to a canonical (num,
# unit) key so they compare equal regardless of wording (dates/IDs have no unit
# -> ignored):
#   "30 lines", ">=80%", "2 levels"          (num then unit, adjacent)
#   "5 public methods", "<=2 nesting levels" (num then unit, INTERVENING NOUN , C2)
#   "Max function lines: 30"                 (unit then num, label form)
#   "<10 seconds", "retention >=30 days"     (time units , C2 / Finding A)
# `%` binds tight (no space, no intervening word: "80%"); word-units may have an
# intervening noun ("5 public methods") and need a trailing word boundary.
#
# SCOPE (honest limit , S7 C4/C5): the unit set below is a CLOSED allow-list.
# Thresholds whose unit is NOT in it are invisible to this gate , specifically
# RATIO forms ("4.5:1" contrast) and BARE-METRIC-NAME forms ("cyclomatic
# complexity < 10", where the unit is an implicit metric name, not a word-unit).
# These are deliberately out of scope here (like dates/IDs): a ratio/bare-metric
# threshold that vaguens would PASS Axis B. The dual-axis design covers this , the
# Axis A semantic council (S5) is the backstop for any threshold class Axis B does
# not mechanically see. Extend WORD_UNITS (or add a ratio pattern) if such a
# threshold ever migrates into compressible rule prose; today they live only in
# instructions.md's YAML config block, which _prose() excludes and which US-341
# did not compress.
WORD_UNITS = (
    r"(?:lines?|methods?|levels?|classes|characters|chars|seconds?|"
    r"minutes?|hours?|days?|weeks?|MB|GB|KB)"
)
# num, then either `%` (adjacent) OR <=3 intervening words then a word-unit + \b.
THRESHOLD_NUM_UNIT = re.compile(
    r"(?:<=|>=|≤|≥|<|>)?\s*(\d+)\s*"
    r"(?:(%)|(?:[A-Za-z-]+\s+){0,3}?(" + WORD_UNITS + r")\b)",
    re.IGNORECASE,
)
# "Max <noun> <unit>: <num>" or "<unit>: <num>" , unit precedes the number.
THRESHOLD_UNIT_NUM = re.compile(
    r"(" + WORD_UNITS + r")\**\s*[:=]\s*(\d+)\b",
    re.IGNORECASE,
)

INLINE_CODE = re.compile(r"`[^`]*`")
# A one-line reference to a relocated block (a markdown link, a bare path or an
# inline-code path), so Axis B can follow the block that moved. Four homes count
# (ADR-054 D4): a skill resource, a sibling rule file (anchor -> scoped), a skill's
# SKILL.md and a command. Any other .md is not followed. A followed home credits only
# the directives it GAINED against the base (S4 finding 1): pointing at a home that
# already held MUSTs cannot pay for a MUST deleted here.
RESOURCE_REF = re.compile(
    r"(?:\]\(|\s|`)("
    r"[\w./-]*resources/[\w./-]+\.md"
    r"|[\w./-]*rules/[\w.-]+\.rules\.md"
    r"|[\w./-]*skills/[\w.-]+/SKILL\.md"
    r"|[\w./-]*commands/[\w.-]+\.md"
    r")"
)


def _prose(text: str) -> str:
    """Return the file's prose , frontmatter, fenced code, and inline-code spans
    removed (so a threshold inside a code example is not extracted)."""
    lines = text.splitlines()
    out: list[str] = []
    in_fm = False
    fence: str | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and stripped == "---":
            in_fm = True
            continue
        if in_fm:
            if stripped == "---":
                in_fm = False
            continue
        marker = None
        if stripped.startswith("```"):
            marker = "```"
        elif stripped.startswith("~~~"):
            marker = "~~~"
        if fence is not None:
            if marker == fence:
                fence = None
            continue
        if marker is not None:
            fence = marker
            continue
        out.append(INLINE_CODE.sub("", line))
    return "\n".join(out)


def _normalise_threshold(num: str, unit: str) -> str:
    """Canonical `{num} {unit}` key. Units are lowercased and singularised so
    `5 methods` / `5 method` and `30 line` / `30 lines` compare equal."""
    u = unit.lower()
    if u not in ("chars", "characters") and u.endswith("s"):
        u = u[:-1]  # methods->method, lines->line, days->day, seconds->second
    return f"{num} {u}"


def extract(text: str) -> tuple[Counter, set]:
    """Extract (directive-counts, threshold-presence-set) from PROSE.

    Two different signals, two different comparisons (S4 rework):

    - DIRECTIVES are prose mandates (rewordable), so a lexical phrase-key either
      false-fails on a legit reword or misses a softened mandate. The honest
      heuristic is a per-token COUNT: the file must not end up with FEWER of a
      directive token than before , that catches wholesale mandate deletion
      (incl. losing 2 of 3 MUSTs) without lying about reword-equivalence.
      Residual (documented): softening ONE mandate in place while the token count
      holds is not caught , inherent to a prose heuristic; Axis A (the S5 council)
      is the backstop for that.
    - THRESHOLDS are precise values, so they are compared by PRESENCE of a
      canonical (num, unit) key (C2 , covers the several written forms; a moved
      threshold is found via the newly-referenced resource union, C1).
    """
    prose = _prose(text)
    directives: Counter = Counter(DIRECTIVE.findall(prose))
    thresholds: set = set()
    for m in THRESHOLD_NUM_UNIT.finditer(prose):
        # group 2 = '%' (tight) or group 3 = a word-unit (possibly with an
        # intervening noun); exactly one is set.
        unit = m.group(2) or m.group(3)
        thresholds.add(_normalise_threshold(m.group(1), unit))
    for m in THRESHOLD_UNIT_NUM.finditer(prose):
        thresholds.add(_normalise_threshold(m.group(2), m.group(1)))
    return directives, thresholds


def git_show(ref: str, path: str) -> str | None:
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def git_ref_exists(ref: str) -> bool:
    """Whether `ref` resolves to a commit , distinguishes 'file is new on a valid
    base' (pass) from 'the base ref itself does not exist' (a hard error, so a
    typo'd --base cannot silently make every file look new)."""
    r = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


def _resource_refs(text: str) -> set:
    """The set of relocation paths (resources, rules, skills, commands) a text
    references."""
    return {m.group(1) for m in RESOURCE_REF.finditer(text)}


def _resolve(ref: str, root: Path) -> Path | None:
    for cand in (root / ref, root / "kits" / "core" / ref):
        if cand.is_file():
            return cand.resolve()
    return None


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def git_toplevel() -> Path | None:
    r = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    return Path(r.stdout.strip()).resolve() if r.returncode == 0 else None


def rename_sources(base: str, root: Path) -> dict[str, tuple[str, str]]:
    """Map each path renamed (`R`) or copied (`C`) since `base` to its status and
    the path it came from, so a home moved or duplicated in this change is compared
    with its origin, not treated as new (S4 re-review F2). Covers tracked files: the
    gate runs on a commit, where every home is tracked."""
    # -z keeps paths unquoted; a failed diff is an error, never "nothing moved"
    # (S4 re-review R2: either fell back to "new home", crediting everything).
    return {
        new: (status, old)
        for status, old, new in name_status(
            root, base, "-M", "-C", "--find-copies-harder"
        )
        if status in ("R", "C")
    }


def name_status(root: Path, base: str, *opts: str):
    """Yield (status letter, path at base, path now) from `git diff -z
    --name-status`; a rename or copy carries two paths, anything else one."""
    fields = _git(root, "diff", "-z", *opts, "--name-status", base).split("\0")
    i = 0
    while i < len(fields) and fields[i]:
        status = fields[i][:1]
        if status in ("R", "C"):
            yield status, fields[i + 1], fields[i + 2]
            i += 3
        else:
            yield status, fields[i + 1], fields[i + 1]
            i += 2


# The files this gate governs, whatever the caller names (TD-201 A9): the callers
# pass a glob of the rules that exist now, so a renamed rule read as new and a
# deleted one was never named.
GOVERNED_DIR = "kits/core/rules/"
GOVERNED_SUFFIX = ".rules.md"
GOVERNED_FILES = ("kits/core/instructions.md",)


def governed(rel: str) -> bool:
    return rel in GOVERNED_FILES or (
        rel.startswith(GOVERNED_DIR) and rel.endswith(GOVERNED_SUFFIX)
    )


def governed_changes(
    base: str, root: Path
) -> tuple[dict[str, str], list[str], set[str]]:
    """Governed files changed since `base`: {path now: path at base} for every one
    still present (a rename maps to its source), the base paths deleted, and the
    paths a governed file was renamed out to (judged as a deletion, so its new
    file is a home that gained all of its text)."""
    present: dict[str, str] = {}
    deleted: list[str] = []
    moved_out: set[str] = set()
    for status, old, new in name_status(root, base, "-M"):
        if status == "D":
            if governed(old):
                deleted.append(old)
        elif governed(new):
            present[new] = old
        elif status == "R" and governed(old):
            deleted.append(old)
            moved_out.add(new)
    return present, deleted, moved_out


class GitError(RuntimeError):
    """A git query the gate depends on failed: the gate cannot run (exit 2)."""


def _git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def _corpus_scope(root: Path) -> str:
    """Where a moved directive can land: the kit tree, or the repository without one."""
    return "kits" if (root / "kits").is_dir() else "."


def tracked(root: Path) -> set[str]:
    """Paths in the index (what a commit of this change would hold)."""
    return set(filter(None, _git(root, "ls-files", "-z").split("\0")))


def corpus_directives(
    base: str, root: Path, now_tracked: set[str]
) -> tuple[Counter, Counter]:
    """Directive totals over every tracked Markdown file in the corpus scope, at the
    base and now. A move between homes nets to zero whatever git calls it (rename,
    copy, delete plus add); a real deletion shows as a negative net (S4 re-review R1).
    """
    scope = _corpus_scope(root)
    names = _git(root, "ls-tree", "-r", "-z", "--name-only", base, "--", scope)
    before_paths = [n for n in names.split("\0") if n.endswith(".md")]
    batch = subprocess.run(
        ["git", "-C", str(root), "cat-file", "--batch"],
        input="".join(f"{base}:{n}\n" for n in before_paths).encode(),
        capture_output=True,
        check=True,
    ).stdout
    before: Counter = Counter()
    pos = 0
    for _ in before_paths:
        nl = batch.index(b"\n", pos)
        size = int(batch[pos:nl].split()[2])
        before += extract(batch[nl + 1 : nl + 1 + size].decode("utf-8", "replace"))[0]
        pos = nl + 1 + size + 1
    now: Counter = Counter()
    prefix = "" if scope == "." else scope + "/"
    for n in sorted(now_tracked):
        if n.endswith(".md") and n.startswith(prefix) and (root / n).is_file():
            now += extract((root / n).read_text(encoding="utf-8", errors="replace"))[0]
    return before, now


class HomePool:
    """Directives each relocation home GAINED against the base, spent at most once.

    A home credits a rule only with what it gained in this change (S4 finding 1),
    and that gain is one shared pool for the whole run: two spellings of one home,
    or two rules pointing at it, cannot spend the same gained MUST twice (S4
    re-review F1). Homes are keyed by resolved path.
    """

    def __init__(self, base: str, root: Path) -> None:
        self.base, self.root = base, root
        self.sources = rename_sources(base, root)
        self.moved_out: set[str] = set()
        self.left: dict[Path, Counter] = {}
        self.paid: Counter = Counter()

    def _origin(self, rel: str) -> str | None:
        """The text a home's directives are measured against.

        A renamed home against its source at the base: the rename moved nothing in.
        A copied home against its source AS IT IS NOW: what the source still holds
        is a duplicate, what it gave up moved here (a block relocated out of a rule
        is reported as a copy of that rule). Otherwise the home's own base version.
        """
        if rel in self.moved_out:
            return None  # a rule renamed out of the governed set: all of it moved here
        status, source = self.sources.get(rel, ("", rel))
        if status == "C":
            current = self.root / source
            if current.is_file():
                return current.read_text(encoding="utf-8")
        return git_show(self.base, source)

    def gain(self, home: Path) -> Counter:
        if home not in self.left:
            after = extract(home.read_text(encoding="utf-8"))[0]
            origin = self._origin(_rel(home, self.root))
            if origin is not None:
                after -= extract(origin)[0]
            self.left[home] = after
        return self.left[home]

    def spend(self, homes: list[Path], token: str, need: int) -> int:
        """Draw up to `need` of `token` from `homes`; return what stays unpaid."""
        for home in homes:
            pool = self.gain(home)
            take = min(pool[token], need)
            pool[token] -= take
            self.paid[token] += take
            need -= take
            if not need:
                break
        return need


def check_file(
    path: Path,
    base: str,
    root: Path,
    now_tracked: set[str] | None = None,
    before_rel: str | None = None,
) -> tuple[list[str], Counter, list[Path], str]:
    """Threshold errors now; the directive deficit and the newly referenced homes
    for main() to settle against the shared pool once every file is read. A renamed
    file is compared with its source path at the base (`before_rel`)."""
    after_text = path.read_text(encoding="utf-8")
    before_text = git_show(base, before_rel or _rel(path, root))
    if before_text is None:
        # New file on a valid base , nothing to weaken. (The base itself is
        # validated in main() so this cannot be a typo'd ref.)
        return [], Counter(), [], ""

    before_dir, before_thr = extract(before_text)
    after_dir, after_thr = extract(after_text)

    # C1: union AFTER only with homes NEWLY referenced by this compression (a
    # genuinely relocated block), NOT every resource the file happens to link. A
    # coincidental threshold in a pre-existing referenced example must NOT mask a
    # real loss of that threshold from the rule's own prose. Thresholds stay
    # presence: an exact value in the pointed-at home is that value's one home.
    # An untracked home is invisible to the rename map and the corpus net, so it
    # earns no credit (fail closed, S4 re-review R4); a commit tracks every home.
    homes: list[Path] = []
    for ref in sorted(_resource_refs(after_text) - _resource_refs(before_text)):
        res = _resolve(ref, root)
        if res is not None and now_tracked is not None:
            if _rel(res, root) not in now_tracked:
                res = None
        if res is not None and res not in homes:
            homes.append(res)
            after_thr |= extract(res.read_text(encoding="utf-8"))[1]

    errors = [
        f"{path.name}: lost governing threshold '{value}' "
        f"(present in {base}, absent after compression)"
        for value in sorted(before_thr - after_thr)
    ]
    # Directives , the count must not drop (catches wholesale mandate deletion);
    # any shortfall is settled against the homes' gains in main().
    deficit = before_dir - after_dir
    summary = ", ".join(
        f"{t} {before_dir[t]} in {base} -> {after_dir[t]} after"
        for t in sorted(deficit)
    )
    return errors, deficit, homes, summary


def check_deleted(
    rel: str, base: str, landing: list[Path], pool: HomePool
) -> tuple[list[str], Counter]:
    """A governed file deleted since the base, checked against empty text. Its text
    counts as moved only into `landing`: the changed governed files and the homes
    they newly reference (S4: the same words added to an unrelated file covered
    it). Each threshold must be present there; each directive is paid from their
    gains, which the corpus net then backs. Returns the errors and what stays unpaid."""
    before_dir, before_thr = extract(git_show(base, rel) or "")
    found: set = set()
    for path in landing:
        found |= extract(path.read_text(encoding="utf-8"))[1]
    errors = [
        f"{Path(rel).name}: deleted, and its governing threshold '{value}' is in no "
        "changed rule and no resource a changed rule newly references"
        for value in sorted(before_thr - found)
    ]
    unpaid: Counter = Counter()
    for token in sorted(before_dir):
        lost = pool.spend(landing, token, before_dir[token])
        if lost:
            unpaid[token] += lost
            errors.append(
                f"{Path(rel).name}: deleted, {lost}x directive '{token}' lost"
            )
    return errors, unpaid


def settle(
    checked: list[tuple[Path, Counter, list[Path], str]], pool: HomePool
) -> tuple[list[str], Counter]:
    """Pay each file's directive deficit from the gains of the homes it newly
    references. Files citing fewer homes pay first and draw from the homes the
    fewest files cite, so a shared gain goes where it is the only cover. The greedy
    order can only refuse a cover that exists (fail closed), never invent one."""
    cited = Counter(h for _, _, homes, _ in checked for h in homes)
    errors: list[str] = []
    unpaid: Counter = Counter()
    for path, deficit, homes, summary in sorted(
        checked, key=lambda c: (len(c[2]), c[0].as_posix())
    ):
        order = sorted(homes, key=lambda h: (cited[h], h.as_posix()))
        for token in sorted(deficit):
            lost = pool.spend(order, token, deficit[token])
            if lost:
                unpaid[token] += lost
                errors.append(
                    f"{path.name}: lost {lost}x directive '{token}' ({summary})"
                )
    return errors, unpaid


def main(argv: list[str]) -> int:
    args = argv[1:]
    base = "main"
    if args and args[0] == "--base":
        if len(args) < 2:
            print("usage: check-compression-honesty.py [--base REF] FILE ...")
            return 2
        base = args[1]
        args = args[2:]
    if not args:
        print("usage: check-compression-honesty.py [--base REF] FILE ...")
        return 2

    if not git_ref_exists(base):
        print(f"FAIL: base ref '{base}' does not resolve to a commit.")
        print("(A missing base would make every file look new and silently pass.)")
        return 2

    # Paths are taken relative to the repository, whatever the working directory: a
    # run from a subdirectory made every file look new and pass (S4 re-review F8).
    root = git_toplevel()
    if root is None:
        print("FAIL: not inside a git repository.")
        return 2
    # Compare from the branch point, not the base tip: a rule merged to the base
    # after branching is not this change's to answer for (S4: it read as deleted
    # on a branch that was behind).
    label = base
    try:
        point = _git(root, "merge-base", base, "HEAD").strip()
        if point != _git(root, "rev-parse", f"{base}^{{commit}}").strip():
            base = point[:12]
        pool = HomePool(base, root)
        now_tracked = tracked(root)
        present, deleted, pool.moved_out = governed_changes(base, root)
    except GitError as exc:
        print(f"FAIL: {exc}")
        return 2
    targets: dict[str, Path] = {}
    for a in args:
        p = Path(a)
        if not p.is_file():
            print(f"FAIL: not a file: {a}")
            return 2
        targets.setdefault(_rel(p, root), p)
    # Every governed file the base diff reports is checked, named or not.
    for rel in present:
        targets.setdefault(rel, root / rel)
    all_errors: list[str] = []
    checked: list[tuple[Path, Counter, list[Path], str]] = []
    landing = [root / rel for rel in sorted(present) if (root / rel).is_file()]
    for rel, p in sorted(targets.items()):
        errors, deficit, homes, summary = check_file(
            p, base, root, now_tracked, present.get(rel)
        )
        all_errors.extend(errors)
        landing += [h for h in homes if h not in landing]
        if deficit:
            checked.append((p, deficit, homes, summary))
    errors, unpaid = settle(checked, pool)
    all_errors.extend(errors)
    for rel in sorted(deleted):
        errors, lost = check_deleted(rel, base, landing, pool)
        all_errors.extend(errors)
        unpaid += lost
    # A home's gain is real only if it did not come out of another file in the corpus:
    # every credited token must not have shrunk across the corpus as a whole. A loss
    # already reported above is not reported again (S4).
    if pool.paid:
        try:
            before, now = corpus_directives(base, root, now_tracked)
        except GitError as exc:
            print(f"FAIL: {exc}")
            return 2
        for token in sorted(pool.paid):
            lost = before[token] - now[token] - unpaid[token]
            if lost > 0:
                all_errors.append(
                    f"corpus ({_corpus_scope(root)}): {lost}x '{token}' gone overall "
                    f"({before[token]} in {base} -> {now[token]} now), yet "
                    f"{pool.paid[token]} were credited as moved: "
                    "the credit is not backed"
                )

    if all_errors:
        print("FAIL: compression weakened a spec (Axis B):")
        for e in all_errors:
            print(f"  {e}")
        print()
        print("Remediation: restore the lost directive/threshold verbatim in")
        print("intent, or (if it moved) reference the resource it relocated to.")
        return 1

    print(f"PASS: all directives + governing thresholds round-trip vs {label}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
