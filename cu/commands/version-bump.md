---
description: Bump the COPPER framework version consistently across all files, then
  commit, tag, and push
---

# /cu:version-bump

Bump the framework version for: **$ARGUMENTS** (one of `major` | `minor` | `patch` | `X.Y.Z`).

This command makes a version bump **consistent and repeatable**. The single source of truth is
`pyproject.toml` `[project] version`; `deploy/__init__.py` derives `__version__` from it. A backing
script rewrites the mechanical files; you (the agent) write the CHANGELOG and AGENTS.md prose; then
a gated flow commits, tags, and pushes.

> **Git-safety**: this command performs commit, tag, and push. Each is behind an explicit
> stop-and-confirm gate. Never proceed past a gate without the user's go-ahead.

---

## Inputs

- `$ARGUMENTS` = the bump kind: `major`, `minor`, `patch`, or an explicit semver like `4.0.0`.
- If `$ARGUMENTS` is empty, ask the user which bump kind and stop.

---

## Phase 0: Pre-flight

1. **Branch check**: run `git rev-parse --abbrev-ref HEAD`. Releases are cut from `main` (or a
   release branch). If on an unexpected branch, surface it and ask before continuing.
2. **Clean tree check**: run `git status --short`. If there are unrelated uncommitted changes,
   surface them and ask whether to proceed (the bump should be its own commit).
3. **Read current version**: `uv run python -m deploy --version` (or read `pyproject.toml`). Record
   it.
4. **Determine the release date** (today, `YYYY-MM-DD`) for the changelog and README footer.

## Phase 1: Mechanical file bump (script)

Run the backing script with the chosen bump and date:

```bash
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/scripts/bump-version.py BUMP --date YYYY-MM-DD --dry-run
```

- **Always run `--dry-run` first** and show the user the planned edits (old -> new across
  pyproject.toml, README badge/zip/footer, AGENTS.md frontmatter).
- Then run **without** `--dry-run` to apply:

```bash
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/scripts/bump-version.py BUMP --date YYYY-MM-DD
```

The script rewrites: `pyproject.toml` version, `README.md` (badge, `copper-X.Y.Z.zip` examples,
footer version+date), and `AGENTS.md` (frontmatter version on its own track + `last_updated`).

## Phase 2: CHANGELOG + AGENTS prose (agent judgement)

These need human-readable narrative, so the agent writes them (the script intentionally does not):

1. **CHANGELOG.md**: add a new `## [X.Y.Z] - YYYY-MM-DD` entry at the top (above the previous
   release), following Keep a Changelog. Summarise the release in one lead paragraph, then
   `### Added` / `### Changed` / `### Fixed` / `### Deferred` / `### Notes` as appropriate. Use only
   plain hyphens (no en/em dashes - house rule).
2. **AGENTS.md**: add a new changelog entry at the top of its `changelog:` list whose **version is
   the new AGENTS.md frontmatter version** (already bumped by the script) and whose first line reads
   `'Release vX.Y.Z: <one-line summary>'`, followed by the salient changes.

Choose the semver level honestly: MAJOR = breaking changes, MINOR = new capability /
backward-compatible, PATCH = fixes only.

## Phase 3: Validate

1. **Version consistency**: confirm the same `X.Y.Z` appears in `pyproject.toml`, the README badge,
   and `uv run python -m deploy --version`; and that `CHANGELOG.md` has the new top entry.
2. **No dashes**: check the edited files for en/em dashes (U+2013 / U+2014) and replace any the bump
   introduced with plain hyphens.
3. **Tests**: run `.venv/bin/python -m pytest -q`. Must stay green. Run `prettier --write` on the
   edited markdown.

## Phase 4: Commit (GATE 1)

Stage the version files and show the user the staged diff. **STOP and ask for explicit approval**
before committing. On approval:

```bash
git add pyproject.toml README.md AGENTS.md CHANGELOG.md
git commit -m "chore(release): bump framework to vX.Y.Z

<short summary of what's in this release>"
```

(`deploy/__init__.py` no longer needs editing - it derives the version from pyproject.toml.)

## Phase 5: Tag (GATE 2)

**STOP and confirm the tag** with the user (name and that it should point at the release commit). On
approval, create an **annotated** tag on the release commit:

```bash
git tag -a vX.Y.Z -m "COPPER vX.Y.Z - <summary>"
```

Verify the tag points at `HEAD` (`git rev-parse vX.Y.Z^{commit}` == `git rev-parse HEAD`).

## Phase 6: Push (GATE 3)

**STOP and confirm push** with the user (this is outward-facing and hard to reverse). On approval:

```bash
git push origin <branch>
git push origin vX.Y.Z
```

Confirm the remote has both the commit and the tag.

## Phase 7: Report

Summarise: old version -> new version, files changed, commit SHA, tag, and remote push status.
Remind the user of any release follow-ups (e.g. GitHub release notes, distribution zip via
`uv run python -m deploy --package`).

---

## Example Usage

```bash
/cu:version-bump patch # 3.8.0 -> 3.8.1 (fixes only)
/cu:version-bump minor # 3.8.0 -> 3.9.0 (new capability)
/cu:version-bump major # 3.8.0 -> 4.0.0 (breaking)
/cu:version-bump 4.0.0 # explicit version
```

---

## Cross-References

- **Script**: `${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/scripts/bump-version.py` (mechanical files)
- **Source of truth**: `pyproject.toml` `[project] version`; `deploy/__init__.py` derives from it
- **Tests**: `tests/unit/test_bump_version.py`
- **Convention**: forward-only semver; annotated tags on `main`; merges/pushes require explicit
  approval
