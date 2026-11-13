---
description: Verify Definition of Done criteria for a story against pipeline state
  and deliverables. Loads DoD from framework-authoring skill resource and checks evidence
  per criterion.
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:dod-verify

Verify Definition of Done criteria for: **$ARGUMENTS**

---

## Overview

This command checks all applicable Story-Level Definition of Done criteria for a given story by
verifying evidence against the pipeline state, deliverables, and story file. It loads DoD criteria
from the `cu:framework-authoring` skill resource and filters them based on the story's declared change
surface.

**Callable**: standalone for ad-hoc DoD verification **Integrated**: cu-pipe S7 (CRITICAL REVIEW)
delegates DoD verification to this command; S9's closure checklist uses its verdict

**Scope**: Level 1 (Story-Level DoD) only. Sprint, Release, and Epic levels are out of scope.

**Execution model** (US-395, single home:
`${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/resources/fresh-context-review.md`): on every call (S7 or
standalone) the verification runs as a fresh-context review. A separate subagent, never a fork or
other context-inheriting mode, verifies first with a prompt of paths only (this command, the story
file, the diff against the merge base, the ADRs the story names, the output of
`pipeline_validator.py status <story id>`, never the YAML file, the resource above); the author then
adds what it knows. Never pass the build conversation, the plan rationale, the author's self-review
or earlier findings. When no fresh reviewer is possible (no subagent tool, it cannot start, the
host's isolation is not measured, or the reviewer was given anything the exclusions list), the
author verifies alone and the report says `Not independent: <reason>`; a verification that is not
independent is never presented as independent.

If your prompt names you as the fresh reviewer, do not start another reviewer and skip the author
step: review, and report as the fresh reviewer.

---

## Arguments

Parse `$ARGUMENTS` as: `<story-id>`

**Example**: `/cu:dod-verify US-139`

**Valid story IDs**: Match the prefix of files in `docs-copper/roadmap/backlog/` (e.g., `US-139`,
`TD-101`).

---

## Step 0: Gate - Input Validation

**Mandatory**: Resolve the story file before proceeding.

1. Parse `$ARGUMENTS` to extract the story ID
2. If no argument provided, **FAIL** with: "Usage: /cu:dod-verify <story-id>"
3. Glob for `docs-copper/roadmap/backlog/<story-id>*.md`
4. If 0 matches: **FAIL** with: "No story file found for ID: <story-id>"
5. If >1 matches: **FAIL** with: "Multiple story files match ID: <story-id> - be more specific"
6. If exactly 1 match: record the resolved path and proceed

---

## Step 1: Load Context

### 1a. Load Pipeline State

1. Run `pipeline_validator.py status <story-id>` (the pipeline-validator tool,
   `${CLAUDE_PLUGIN_ROOT}/tools/pipeline_validator.py`) and read its `details`: `change_surface`,
   `current_stage`, `stages` (each stage's status), `stage_commits`, `stage_reviewed_commits`,
   `stage_reviewers`, `quality_gates`, `closure_checks` and `pr_readiness`. These are status fields
   only.
2. If it finds no pipeline record: **WARN** - "No pipeline record found. DoD verification will run
   without change_surface filtering."
3. Never open the pipeline YAML file itself: its evidence and reasons are the author's own account
   of the work (US-395).

### 1b. Load DoD Resource

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/resources/definition-of-done.md`
2. Extract the **Level 1: Story-Level Definition of Done** section only
3. Parse criteria into structured checklist with categories:
   - Code Quality & Implementation (7 criteria)
   - Testing Requirements (5 criteria)
   - Documentation Standards (6 criteria)
   - Code Review & Quality Gates (4 criteria)
   - Version Control & Deployment (4 criteria)

---

## Step 2: Filter Criteria by Change Surface

Apply relevance filtering based on the status output's `change_surface`:

| Category                          | Applies When                                     |
| --------------------------------- | ------------------------------------------------ |
| **Code Quality & Implementation** | `code: true` OR `docs: true` (commands are docs) |
| **Testing Requirements**          | `tests: true`                                    |
| **Documentation Standards**       | Always applies                                   |
| **Code Review & Quality Gates**   | Always applies                                   |
| **Version Control & Deployment**  | Always applies                                   |

**Override**: If no pipeline record was found, evaluate ALL criteria (no filtering).

---

## Step 3: Verify Each Criterion

For each applicable criterion, check evidence and assign a status:

| Status   | Meaning                                          |
| -------- | ------------------------------------------------ |
| **PASS** | Criterion met with supporting evidence           |
| **FAIL** | Criterion not met; specific issue identified     |
| **SKIP** | Criterion not applicable to this story type      |
| **WARN** | Evidence is ambiguous; manual review recommended |

### Acceptance Criteria: From the Files, at `path:line`

Verify each AC clause from the files it names and cite the `path:line` that meets it; a clause with
no such line is FAIL, not WARN. Pipeline state (a stage completed, a gate passed) is read from the
YAML status fields only, through `pipeline_validator.py status <story id>`, never the YAML file: its
evidence prose is the author's own account and never verifies an AC.

### Verification Checks

#### Code Quality & Implementation (when code or docs changed)

| #   | Criterion                       | Verification Method                                                |
| --- | ------------------------------- | ------------------------------------------------------------------ |
| CQ1 | **[CA] Clean Architecture**     | Deliverable files exist and follow project conventions             |
| CQ2 | **[SF] Simplicity First**       | No unnecessary complexity in deliverable (review scope reasonable) |
| CQ3 | **[RP] Readability Priority**   | Clear naming, no ambiguity in command structure                    |
| CQ4 | **[DRY] Don't Repeat Yourself** | No duplication with existing commands                              |
| CQ5 | **[REH] Robust Error Handling** | Command includes failure states (gates with FAIL conditions)       |
| CQ6 | **[IV] Input Validation**       | Command validates story ID (glob resolution with 0/>1 rejection)   |
| CQ7 | **Principle Tagging**           | Deliverable references principle codes in decisions                |

#### Testing Requirements (when tests: true)

| #   | Criterion              | Verification Method                                           |
| --- | ---------------------- | ------------------------------------------------------------- |
| TE1 | **Unit Tests**         | Status output `quality_gates.unit_tests == passed`            |
| TE2 | **Integration Tests**  | Status output `quality_gates.integration_tests`               |
| TE3 | **Test Documentation** | Test file has clear test names and assertions                 |
| TE4 | **All Tests Pass**     | Status output: every test gate in `quality_gates` is `passed` |
| TE5 | **Edge Cases Covered** | Functional test covers declared framework counts              |

#### Documentation Standards (always)

| #   | Criterion                        | Verification Method                                                                                |
| --- | -------------------------------- | -------------------------------------------------------------------------------------------------- |
| DS1 | **[SD] Strategic Documentation** | Command file has clear sections with purpose                                                       |
| DS2 | **API Documentation**            | N/A for framework commands (SKIP)                                                                  |
| DS3 | **README Updates**               | Status output `closure_checks.readme_review == passed` (an S8 field: WARN at S7, re-checked at S9) |
| DS4 | **Code Comments**                | Complex logic explained inline in command                                                          |
| DS5 | **CHANGELOG**                    | CHANGELOG.md entry if version bump involved                                                        |
| DS6 | **Deliverable Completeness**     | Each AC clause cited at its `path:line` (Step 3); ticks alone do not count                         |

#### Code Review & Quality Gates (always)

| #   | Criterion             | Verification Method                                                                                                                                                                               |
| --- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CR1 | **Peer Review**       | Status output: S4 and S5 `completed`; `stage_reviewed_commits` has a commit for each; `stage_reviewers` names the fresh reviewer with `Verdict dictated: no`, or says `Not independent: <reason>` |
| CR2 | **Linters Pass**      | Status output `quality_gates.lint == passed`                                                                                                                                                      |
| CR3 | **Security Scan**     | N/A for docs-only commands unless `security_sensitive: true`                                                                                                                                      |
| CR4 | **Performance Check** | N/A for framework commands (SKIP)                                                                                                                                                                 |

#### Version Control & Deployment (always)

| #   | Criterion                  | Verification Method                                                                           |
| --- | -------------------------- | --------------------------------------------------------------------------------------------- |
| VC1 | **[CD] Commit Discipline** | Status output `stage_commits` has a commit for each completed stage                           |
| VC2 | **Branch Clean**           | Run `git status --porcelain` - must be empty                                                  |
| VC3 | **Deployment Ready**       | Status output `pr_readiness.ready_for_pr == true` (an S9 field: WARN at S7, re-checked at S9) |
| VC4 | **Rollback Plan**          | N/A for framework commands (SKIP)                                                             |

---

## Step 4: Compile Report

Generate a Markdown report with the following structure:

```markdown
## DoD Verification: <story-id>

### Inputs

- Reviewer: fresh subagent | Not independent: <reason>
- Command, story file, diff range, ADRs, pipeline status output, any other prompt text

**Change Surface**: code=<bool>, docs=<bool>, tests=<bool>, architecture=<bool> **Pipeline Stage**:
<current_stage> **DoD Level**: Story-Level (Level 1) **Result**: <X> PASS / <Y> FAIL / <Z> SKIP /
<W> WARN

### Criteria Summary

| #   | Criterion          | Category     | Status | Source | Evidence                                                 |
| --- | ------------------ | ------------ | ------ | ------ | -------------------------------------------------------- |
| CQ1 | Clean Architecture | Code Quality | PASS   | fresh  | Command file at <harness-root>/commands/cu-dod-verify.md |
| AC1 | (story AC clause)  | Story AC     | PASS   | fresh  | `path/to/file.md:42`                                     |
| ... | ...                | ...          | ...    | ...    | ...                                                      |

### Failed Criteria

> List each FAIL with:
>
> - **Criterion**: [code] description
> - **Evidence**: what was found (or missing)
> - **Recommendation**: specific action to resolve

### Warnings

> List each WARN with:
>
> - **Criterion**: [code] description
> - **Concern**: what is ambiguous
> - **Recommendation**: what to verify manually

### Skipped Criteria

> List each SKIP with reason (e.g., "N/A for docs-only command")

### Summary

- **Overall**: PASS / FAIL (PASS if zero FAIL items)
- **Recommendation**: Ready for closure / Address failures before closing
```

---

## Step 5: Return Verdict

After generating the report:

1. Count FAIL items
2. If **zero FAIL**: return **PASS** - "All applicable DoD criteria verified. Story is ready for
   closure."
3. If **any FAIL**: return **FAIL** - "<N> DoD criteria not met. Address before closing."
4. Print the full report for the user
5. If called from cu-pipe S7: the pipeline uses this verdict as evidence for the DoD gate (and S9's
   closure checklist reads it)

---

## Usage Examples

### Standalone Usage

```
/cu:dod-verify US-139
```

Verifies all applicable DoD criteria for story US-139 against its pipeline state and deliverables.

### Integration with cu-pipe

cu-pipe S7 (CRITICAL REVIEW) delegates DoD verification to this command; S9's closure checklist
reads the verdict. The pipeline records the verdict in `closure_checks.dod_verified`.

---

## Anti-Patterns

- **Do not** run actual test suites or linters - this command checks evidence, not execution
- **Do not** modify any files - this is a read-only verification command
- **Do not** skip criteria without justification - every SKIP needs a reason
- **Do not** rubber-stamp - each criterion must reference specific, verifiable evidence

---

## Dependencies

- **DoD Resource**: `${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/resources/definition-of-done.md` (Level 1
  only)
- **Pipeline state**: `pipeline_validator.py status <story-id>` over
  `docs-copper/roadmap/pipeline-audit-trail/<story-id>.yaml` (optional but recommended; the file is
  not opened)
- **Story File**: `docs-copper/roadmap/backlog/<story-id>*.md`

---

## Related Commands

- `/cu:pipe` - Story delivery pipeline that delegates to this command at S7
- `/cu:qa-gate` - Runs executable quality gates (tests, linters, validators)
- `/cu:story-update` - Maintains story file content (ACs, status, progress)
