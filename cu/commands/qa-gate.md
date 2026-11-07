---
description: Run all executable quality gates (tests, linting, formatting, validators)
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:qa-gate

Run all executable quality gates for the COPPER framework: **$ARGUMENTS**

---

## Overview

This command orchestrates the four mandatory quality gates for framework work. It is the
authoritative quality gate runner, used by cu-pipe S6 (TEST QUALITY VERIFY) and available for
standalone ad-hoc checks.

**Delegated from**: cu-pipe S6_TEST_QUALITY_VERIFY **Also callable**: standalone for pre-commit
verification or ad-hoc quality checks

---

## Execution Protocol

Run the four gates **in order**. Stop at the first failure unless the user specifies
`--continue-on-error`. Report pass/fail per gate with clear output.

### Gate 1: Python Test Suite

```bash
uv run pytest tests/ --tb=short -q
```

**What it checks**: All unit and functional tests under `tests/`.

**On failure**:

- Review the failing test names in the pytest output
- Read the test file and the source file it tests
- Fix the code or update the test if requirements changed
- Re-run: `uv run pytest tests/<failing-file>::<failing-test> --tb=long -v`

**Evidence to record**:

```yaml
quality_gates:
  test_suite:
    status: pass|fail
    evidence: 'uv run pytest tests/ --tb=short -q : X passed, Y failed'
```

---

### Gate 2: Python Linting

```bash
npm run lint:ruff
```

(The pinned `uvx ruff@0.15.4` lint and format check CI runs; `uv run ruff` fails where ruff is not a
project dependency.)

**What it checks**: Python syntax, style, and common errors across the codebase.

**On failure**:

- Read the ruff output for file, line, and rule code
- Apply auto-fixes where safe: `npm run format:ruff`
- For remaining issues, manually address each violation
- Re-run: `npm run lint:ruff`

**Evidence to record**:

```yaml
quality_gates:
  python_linting:
    status: pass|fail
    evidence: 'npm run lint:ruff : N issues found' or 'All checks passed!'
```

---

### Gate 3: Markdown/JSON Formatting

```bash
npm run lint:prettier
```

**What it checks**: Formatting consistency of the files the project's `lint:prettier` script names,
so the gate and CI check the same set. (A hard-coded list here named `opencode.jsonc`, git-ignored
since it became host config; prettier then exited 2 although every file it checked passed.)

**On failure**:

- Auto-fix all formatting: `npm run format:prettier`
- Re-run: `npm run lint:prettier`
- If still failing, check `.prettierrc.json` for custom rules

**Evidence to record**:

```yaml
quality_gates:
  formatting:
    status: pass|fail
    evidence: 'npm run lint:prettier : all files formatted correctly'
```

---

### Gate 4: User Story Validator

```bash
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/scripts/user-story-validator.py docs-copper/roadmap/backlog/
```

**What it checks**: All backlog story files conform to the user-story template (frontmatter fields,
Progress updates block, body structure).

**On failure**:

- Read the validator output for the specific error (MISSING_PROGRESS_BLOCK, INVALID_STATUS, etc.)
- Open the flagged story file and add the missing section or fix the invalid field
- Re-run the validator on the single file to confirm the fix
- `no story files found` (exit 2): the backlog holds no story yet, so nothing was validated. This is
  not a pass; record Gate 4 as unverified until the first story exists

**Evidence to record**:

```yaml
quality_gates:
  story_validator:
    status: pass|fail
    evidence: 'user-story-validator: N/N files pass, 0 errors'
```

---

## Summary Report

After running all gates, produce a summary:

```text
=== Quality Gate Summary ===
  [PASS] Gate 1: Python test suite (X tests passed)
  [PASS] Gate 2: Python linting (0 issues)
  [PASS] Gate 3: Markdown/JSON formatting (all files OK)
  [PASS] Gate 4: User story validator (N/N pass)
  Result: ALL GATES PASSED
```

On any failure:

```text
=== Quality Gate Summary ===
  [PASS] Gate 1: Python test suite (X tests passed)
  [FAIL] Gate 2: Python linting (2 issues)
  [SKIP] Gate 3: Markdown/JSON formatting (not reached)
  [SKIP] Gate 4: User story validator (not reached)
  Result: FAILED : fix Gate 2 issues and re-run
```

---

## Pipeline Integration (cu-pipe S6)

When called from cu-pipe S6_TEST_QUALITY_VERIFY:

1. Run `/cu:qa-gate` (this command)
2. Record the summary output in the pipeline YAML `quality_gates` section
3. Record each gate result as a `verified_claim` entry
4. Refuse stage completion on any non-zero exit code unless the stage is formally bypassed

**Minimum verified claims after S6**:

```yaml
verified_claims:
  - claim: 'Framework pytest suite passes'
    command: 'uv run pytest tests/ --tb=short -q'
    expected: 'exit_code=0'
    actual: 'exit_code=0'
    exit_code: 0
    scope: 'framework'
    category: 'test_suite'
  - claim: 'Python linting passes (ruff)'
    command: 'npm run lint:ruff'
    expected: 'exit_code=0'
    actual: 'exit_code=0'
    exit_code: 0
    scope: 'framework'
    category: 'lint'
  - claim: 'Prettier formatting check passes'
    command: 'npm run lint:prettier'
    expected: 'exit_code=0'
    actual: 'exit_code=0'
    exit_code: 0
    scope: 'framework'
    category: 'formatting'
  - claim: 'All backlog stories pass validation'
    command:
      'uv run python ${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/scripts/user-story-validator.py
      docs-copper/roadmap/backlog/'
    expected: 'exit_code=0'
    actual: 'exit_code=0'
    exit_code: 0
    scope: 'framework'
    category: 'validator'
```

---

## Arguments

| Argument              | Default | Description                                            |
| --------------------- | ------- | ------------------------------------------------------ |
| `$ARGUMENTS`          | (none)  | Optional: specific gate number (1-4) or `--fix`        |
| `--fix`               |         | Auto-fix where possible (ruff --fix, prettier --write) |
| `--continue-on-error` |         | Run all gates even if one fails                        |

---

## Related Commands

- `/cu:pipe` S6_TEST_QUALITY_VERIFY: delegates to this command
- `/cu:quality-review`: deeper code quality and security analysis
