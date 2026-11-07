---
description: Track and guide a hardened story delivery pipeline for COPPER work items
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:pipe

Track and guide the lean COPPER story delivery pipeline for: **$ARGUMENTS**

---

## Overview

This command is a **pure orchestrator** (v2.0.0) that manages a hardened delivery pipeline for
COPPER backlog stories. All substantive actions (review, quality gates, capture, closure) are
delegated to standalone commands. cu-pipe handles only YAML state management, stage advancement,
commit discipline, and the hard gate protocol.

**Migration from v1.x**: v2.0.0 is a breaking architectural change. The inline stage implementations
have been extracted into standalone commands. If you previously relied on cu-pipe performing reviews
inline, those reviews now happen via the delegated commands listed in the delegation table below.

State is stored in:

```text
docs-copper/roadmap/pipeline-audit-trail/<story-id>.yaml
```

Stage artefacts are stored in:

```text
docs-copper/roadmap/pipeline-audit-trail/artifacts/<story-id>-s<stage>-<type>.md
```

Any stage that produces a substantive deliverable (challenge log, implementation plan, review
findings, risk register, etc.) MUST write it to the `artifacts/` subfolder using the standardised
naming pattern. This ensures all pipeline deliverables are co-located and discoverable.

Pipeline stages:

```mermaid
flowchart LR
    S0[SELECT] --> S1[KICKOFF]
    S1 --> S2[PLAN]
    S2 --> S3[EXECUTE]
    S3 --> S4[CODE REVIEW]
    S4 --> S5[ARCH SEC COMP REVIEW]
    S5 --> S6[TEST QUALITY VERIFY]
    S6 --> S7[CRITICAL REVIEW]
    S7 --> S8[CAPTURE]
    S8 --> S9[CLOSE]
    S9 --> S10[MERGE]
```

---

## Delegation Reference Table

| Stage | Delegated Command(s)                                       | Expected Inputs                   | Expected Outputs                                                    | Artefact Path                                                      | Verification Method                                              |
| ----- | ---------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------- |
| S1    | `/cu:story-kickoff`                                        | Story ID, review profile          | Challenge log table, implementation plan, risk register             | `pipeline-audit-trail/artifacts/<id>-s1-kickoff.md`                | Challenge log has >= profile minimum entries; story file changed |
| S2    | Agent produces inline                                      | S1 challenge log, story ACs       | Implementation plan with alternatives and "what could go wrong"     | `pipeline-audit-trail/artifacts/<id>-s2-plan.md`                   | At least one alternative considered; risk section present        |
| S4    | `/cu:quality-review`                                       | File paths or scope, review depth | Structured findings table, PASS/FAIL status                         | (optional: `artifacts/<id>-s4-review.md` for significant findings) | `**Overall Status**:` line parsed                                |
| S5    | `/cu:arch-review`                                          | Architecture scope                | Structured findings table, risk register, PASS/FAIL status          | (optional: `artifacts/<id>-s5-review.md` for significant findings) | `**Overall Status**:` line parsed; risk register present         |
| S6    | `/cu:qa-gate`                                              | Change surface, file list         | `quality_gates.status: pass\|fail`, verified_claims with exit codes | (none - evidence captured in YAML)                                 | Exit code 0 on all gates; verified_claims recorded               |
| S7    | `/cu:dod-verify`                                           | Story ID, DoD criteria            | PASS/FAIL/SKIP/WARN per criterion                                   | (none - evidence captured in YAML)                                 | All criteria have definitive status                              |
| S8    | `/cu:dev-journal` + `/cu:memory-update` + `/cu:readme-update` | Story context, change summary     | Journal file artifact, memory-bank updates, README file updates     | `docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-<slug>.md`             | Files exist on disk; closure_checks show pass                    |
| S9    | `/cu:story-update` + `/cu:readme-update`                   | Story ID, review outcomes         | Close docs committed; README updates; story stays In Progress       | (none - evidence captured in YAML)                                 | Close docs committed; story still In Progress (Done at merge)    |
| S10   | `/cu:mr-create` + `/cu:kanban` (post-merge)                | Branch, review outcomes           | MR URL, user confirms merge, then story Done + card DONE            | (none - MR is the deliverable)                                     | MR URL valid; user confirmed merge; story Done; card in DONE     |

---

## Command Forms

```text
/cu:pipe init <story-id>
/cu:pipe status [story-id]
/cu:pipe next [story-id]
/cu:pipe complete [story-id]
/cu:pipe force <stage> "<reason>" [story-id]
```

---

## Phase 1: Parse Intent and Resolve Story

1. Parse `$ARGUMENTS` into: `init` | `status` | `next` | `complete` | `force`
2. Resolve story ID: (a) explicit in args, (b) branch pattern `feature/us-123-...`, (c) ask user
3. Validate story file exists under `docs-copper/roadmap/backlog/`

---

## Phase 2: Ensure Pipeline Location Exists

1. Ensure `docs-copper/roadmap/pipeline-audit-trail/` exists
2. Use `<story-id>.yaml` as state filename

---

## Phase 3: State Model

### YAML Shape

```yaml
schema_version: 2
story_id: US-123
story_path: docs-copper/roadmap/backlog/US-123-slug.md
feature_branch: ''
review_profile: standard
change_surface:
  code: false
  docs: true
  tests: false
  architecture: true
  security_sensitive: false
  compliance_sensitive: false
current_stage: S0_SELECT
status: active
status_reason: ''
initiated_at: '2026-05-07T00:00:00Z'
completed_at: ''
stages:
  S0_SELECT: { status: completed, completed_at: '', evidence: [], commit: '' }
  S1_KICKOFF: { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S2_PLAN: { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S3_EXECUTE: { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S4_CODE_REVIEW: { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S5_ARCH_SEC_COMP_REVIEW:
    { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S6_TEST_QUALITY_VERIFY:
    { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S7_CRITICAL_REVIEW: { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S8_CAPTURE: { status: pending, completed_at: '', reviewers: [], evidence: [], commit: '' }
  S9_CLOSE: { status: pending, completed_at: '', evidence: [], commit: '' }
  S10_MERGE: { status: pending, completed_at: '', evidence: [], commit: '' }
closure_checks:
  backlog_status: { status: pending, reason: '' }
  board_status: { status: pending, reason: '' }
  dev_journal: { status: pending, reason: '' }
  memory_bank: { status: pending, reason: '' }
  readme_review: { status: pending, reason: '' }
  commit_evidence: { status: pending, reason: '' }
  pr_readiness: { status: pending, reason: '' }
  pr_creation:
    { status: pending, reason: 'Created at S10 after all close docs committed and pushed' }
  deliverables_resolved: { status: pending, reason: '' }
  dod_verified: { status: pending, reason: '' }
quality_gates:
  lint: { status: pending, evidence: '' }
  unit_tests: { status: pending, evidence: '' }
  integration_tests: { status: pending, evidence: '' }
  functional_tests: { status: pending, evidence: '' }
  docs_quality: { status: pending, evidence: '' }
  validators: { status: pending, evidence: '' }
verified_claims: []
pr_readiness:
  { status: pending, branch: '', branch_clean: false, ready_for_pr: false, evidence: [] }
bypasses: []
notes: ''
```

### YAML Formatting Convention

The template above uses **flow style** (single-line) for the initial scaffold. When populating
evidence during pipeline execution, always expand to **block style** (multi-line) for readability:

```yaml
# BAD: flow style (hard to read in diffs and editors)
S0_SELECT: { status: completed, evidence: ['Created branch', 'Updated story'], commit: 'abc123' }

# GOOD: block style (readable, diff-friendly)
S0_SELECT:
  status: completed
  completed_at: '2026-05-14T10:00:00Z'
  evidence:
    - 'Created branch'
    - 'Updated story'
  commit: 'abc123'
```

Apply block style to: `stages.*`, `closure_checks.*`, `quality_gates.*`, `verified_claims`, and
`pr_readiness`. This matches the convention established by US-131 onwards.

### Status Enums (Two Levels)

The pipeline uses **two separate status enums** that MUST NOT be conflated:

**1. Pipeline Top-Level Status** (`status` field at YAML root):

`active` | `completed` | `abandoned`

| Value       | Meaning                                       | Transition                |
| ----------- | --------------------------------------------- | ------------------------- |
| `active`    | Story is in progress through the pipeline     | Initial state at `init`   |
| `completed` | All 11 stages done, S10 MERGE succeeded       | Set by Phase 5 `complete` |
| `abandoned` | Story dropped without completing the pipeline | Set by user disposition   |

**Critical rule**: Top-level status becomes `completed` only after S10 MERGE, not S9 CLOSE.

**2. Stage-Level Status** (each `stages.SX_*.status` field):

`pending` | `in_progress` | `completed` | `blocked` | `bypassed` | `abandoned`

| Value         | Meaning                                      | Used For           |
| ------------- | -------------------------------------------- | ------------------ |
| `pending`     | Stage not yet started                        | Initial state      |
| `in_progress` | Stage currently being executed               | Active stage       |
| `completed`   | Stage finished with verified evidence        | Done stage         |
| `blocked`     | Stage cannot proceed (dependency/decision)   | Hard gate hold     |
| `bypassed`    | Stage skipped with recorded justification    | Soft gate skip     |
| `abandoned`   | Stage abandoned (story dropped mid-pipeline) | Pipeline cancelled |

**3. Story Frontmatter Status** (in the Markdown story file under `docs-copper/roadmap/backlog/`):

The canonical story-lifecycle set , defined ONCE in `tools/status-vocabulary.json` and loaded by
both `pipeline_validator.py` and `user-story-validator.py` (TD-171 AC3):

`Draft` | `Ready` | `In Progress` | `Done` | `Blocked` | `Cancelled`

| Value         | Meaning                          | Pipeline Mapping                             |
| ------------- | -------------------------------- | -------------------------------------------- |
| `Draft`       | Story not yet groomed            | No pipeline record                           |
| `Ready`       | Groomed, actionable, not started | No pipeline record (or parked pre-S1)        |
| `In Progress` | Story being worked on            | Pipeline `active`, some stages `in_progress` |
| `Done`        | Story fully delivered and merged | Pipeline `completed`                         |
| `Blocked`     | Story cannot proceed             | Pipeline `active`, stage `blocked`           |
| `Cancelled`   | Story dropped                    | Pipeline `abandoned` (if one exists)         |

**Cross-Reference Consistency Rule**: When the pipeline top-level status is `completed`, the story
frontmatter status MUST be `Done`. When the story frontmatter is `Done`, the pipeline top-level
status MUST be `completed` (records quarantined as `schema_version: 1` are exempt , they are legacy
histories, skipped and counted by the audit). Violations are caught by TWO independent mechanisms:
`tests/regression/test_pipeline_status_consistency.py` (self-contained corpus test in the pytest
suite) and the `pipeline-validator audit` gate line in `deploy/local_ci.py`, mirrored in
`.github/workflows/quality.yml` (TD-171 AC5).

### Bypass Record

```yaml
bypasses:
  - stage: S5_ARCH_SEC_COMP_REVIEW
    reason: 'Docs-only release path accepted'
    risk_accepted: 'Lightweight review performed'
    approved_by: 'Maintainer'
    timestamp: '2026-05-07T00:00:00Z'
```

### Verified Claim Shape

```yaml
verified_claims:
  - claim: 'Framework pytest suite passes'
    command: 'uv run pytest tests/ --tb=short -q'
    expected: 'exit_code=0'
    actual: 'exit_code=0'
    exit_code: 0
    scope: 'framework'
    category: 'test_suite'
```

Required fields: `claim`, `command`, `expected`, `actual`, `exit_code`, `scope`, `category`.

---

## Phase 4: Stage Definitions

| Stage | Purpose                                     | Evidence Expectation                                                           |
| ----- | ------------------------------------------- | ------------------------------------------------------------------------------ |
| S0    | Confirm story, create branch, create YAML   | branch created, story status In Progress, Kanban TODO -> DOING                 |
| S1    | Critically refine scope, ACs, dependencies  | challenge log (per profile minimum), story file updated                        |
| S2    | Define execution approach with alternatives | implementation plan with alternatives and "what could go wrong"                |
| S3    | Produce working artefacts                   | changed files linked to story intent, AC self-review                           |
| S4    | Formal code/content review                  | `/cu:quality-review` output with PASS/FAIL status                              |
| S5    | Architecture, security, compliance review   | `/cu:arch-review` output with findings table and risk register                 |
| S6    | Test and quality verification               | `/cu:qa-gate` output with verified_claims and exit codes                       |
| S7    | Critical readiness review                   | `/cu:dod-verify` output, challenge log, distinct perspectives                  |
| S8    | Capture continuity and narrative            | dev-journal + memory-bank + readme-update executed                             |
| S9    | Close internal bookkeeping                  | close docs committed (no push yet); story stays In Progress                    |
| S10   | Push, create MR, await merge, then close    | push, MR created, user confirms merge; POST-MERGE story -> Done + card -> DONE |

---

## Phase 4.1: Critical Thinking Protocol

Before advancing any stage from S1 onward, answer these four mandatory questions:

1. **Challenge**: What assumption am I making that could be wrong?
2. **Sceptic**: What would a reasonable sceptic say?
3. **Gap**: What am I not seeing?
4. **Downstream**: If this is wrong, what breaks?

### Challenge Log Format

```markdown
| #   | Aspect | Challenge             | Disposition              | Status                     |
| --- | ------ | --------------------- | ------------------------ | -------------------------- |
| 1   | Scope  | <question or concern> | <resolution or decision> | resolved / open / deferred |
```

### Minimum Entries by Profile

| Profile       | S1 minimum | S7 minimum                     |
| ------------- | ---------- | ------------------------------ |
| `lightweight` | 2          | 2 perspectives, 1 entry each   |
| `standard`    | 3          | 2 perspectives, 2 entries each |
| `hardened`    | 5          | 3 perspectives, 2 entries each |

### Anti-Patterns

- Confirmation bias, mechanical review, deferred criticality, vague evidence

---

## Phase 4.5: Story Document Maintenance

Pipeline commands (`init`, `complete`, `force`) are explicit permission to update the story document
and Kanban board via `/cu:story-update` and `/cu:kanban`.

### Progress Update Checkpoints

| Stage | Progress Entry                                     |
| ----- | -------------------------------------------------- |
| S0    | Story selected, branch created, pipeline initiated |
| S1    | Scope refined, ACs reviewed, profile chosen        |
| S3    | Execution completed, artefacts produced            |
| S8    | Dev-journal, memory-bank, readme-update captured   |
| S9    | Close docs committed (status/board flip at merge)  |
| S10   | Pushed, MR created, merged; story Done, card DONE  |

Format: `> - **YYYY-MM-DD**: [SX_STAGE] One-line summary`

### Kanban Board Transitions

Delegate to `/cu:kanban`:

| Transition     | From    | To        | Character                                                      |
| -------------- | ------- | --------- | -------------------------------------------------------------- |
| Work started   | `TODO`  | `DOING`   | `- [ ]` -> `- [/]`                                             |
| Work merged    | `DOING` | `DONE`    | `- [/]` -> `- [x]` (post-merge, with the status flip , TD-173) |
| Work abandoned | `DOING` | `CARPARK` | `- [/]` -> `- [-]`                                             |

### Story Frontmatter Status

| Event               | `status`                                                        |
| ------------------- | --------------------------------------------------------------- |
| init (S0)           | `In Progress`                                                   |
| complete at S9      | `In Progress` (unchanged , close docs only)                     |
| **after the merge** | `Done`, together with top-level `status: completed` in the YAML |
| force abandon       | `Blocked`                                                       |

**A story is `Done` only when its pipeline is `completed`, which happens at or after the merge**
(TD-173). S9 commits the close documentation; it does not assert delivery. Setting `Done` at S9 was
unsatisfiable: `verify S9_CLOSE` demanded it while `audit` refuses `Done` whilst the pipeline is
active, and with S10 pending the pipeline cannot be `completed`. The status flip belongs in the
post-merge close commit on `main`, which is what practice already did (SEC-005 `51862d3a`, SEC-006
`bc343404`).

---

## Phase 4.6: Commit Discipline

### Commit Checkpoint Stages

| Stage | Commit Message Pattern                               |
| ----- | ---------------------------------------------------- |
| S1    | `docs(<story-id>): complete S1 : <one-line summary>` |
| S3    | `docs(<story-id>): complete S3 : <one-line summary>` |
| S6    | `docs(<story-id>): complete S6 : <one-line summary>` |
| S9    | `docs(<story-id>): S9 close documentation`           |

### Commit Procedure

For each checkpoint stage:

1. Stage all changed files with `git add`
2. If no files changed: record `commit: skipped (no changes)` in evidence
3. Create commit: `git commit -m "docs(<story-id>): complete S<stage> : <summary>"`
4. Record commit hash in pipeline YAML stage entry under `commit`

### Test tiers (TD-195)

Run the cheapest check that can catch what the stage changed; the full battery is for the stages
that assert merge-readiness.

| Stage              | Tier                                                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| S0-S2, S8          | none required (state and documentation); run any guard the change touches                                                                              |
| S3, S4, S5, S7, S9 | **fast tier**: `npm run ci:local:fast` (governance gates, plus pytest without `slow` and `battery_duplicate`, no coverage), plus the tests you changed |
| S6, S10            | **full battery**: `npm run ci:local` on the exact commit, all green                                                                                    |

A test marked `battery_duplicate` re-runs a battery gate verbatim, so the battery skips it and plain
`pytest` still runs it; the comment above each marker names the gate. A test marked `slow` is
skipped by the fast tier only, never by the battery.

### S10 Merge Readiness

**Final full-quality-battery re-run (MANDATORY, before push).** The S6 quality gate ran earlier in
the story; commits at S7 (review fixes), S8 (capture), and S9 (close) have since changed the tree,
so the S6 evidence is stale relative to the exact commits about to be pushed. Before pushing, run
`npm run ci:local` on current HEAD. It runs every gate (tests and coverage, lint, validators, the
determinism gates) and must exit 0: exit 1 is a failure, and exit 2 means a gate could not be run
(for example capability kits are installed), so neither is a pass.

If the battery is not exit 0, S10 STOPS: fix on the branch and re-run before pushing. Record the
result (commit, passed/failed/skipped, exit code) in S10 evidence AND in the PR body. GitHub Actions
is disabled (ADR-007): no check runs after the push, so this battery on the pushed commit IS the
merge verification, not a pre-check before one.

Then:

1. `git rev-list --count main..HEAD` must be > 0
2. Record `commit_count: <N>` in S10 evidence

---

## Phase 4.7: Hard Gate Protocol (S4-S7)

### Stop-and-Present Protocol

At stages S4 through S7, cu-pipe MUST:

1. **Delegate** the stage to the appropriate command (see delegation table)
2. **Collect** the structured output from the command
3. **STOP** and present findings to the user with:
   - Summary of findings (severity, count)
   - The PASS/FAIL status
   - Numbered options for user disposition
4. **Wait** for user response before advancing

### Mandatory Question Format

```
## S4 CODE REVIEW - Hard Gate

**Status**: PASS | FAIL
**Findings**: <count> (Critical: <n>, High: <n>, Medium: <n>, Low: <n>)

[Findings table from delegated command]

What would you like to do?
[A] Accept findings and advance to S5
[B] Review specific finding in detail (specify which)
[C] Block advancement - require fixes before S5
[D] Bypass with accepted risk (requires reason)
```

### Evidence Recording

After user disposition, record in pipeline YAML:

```yaml
S4_CODE_REVIEW:
  evidence:
    - 'Delegated to /cu:quality-review: PASS, 2 medium findings'
    - 'User disposition: [A] Accept and advance'
    - 'Findings: 0 critical, 0 high, 2 medium, 1 low, 3 info'
```

---

## Phase 4.8: Stage-End Evidence Presentation (ALL stages)

Every stage completion MUST present evidence to the user. The interaction depth varies:

### S0-S3, S8-S10: Acknowledgement Only

Present a summary of what was accomplished, then wait for the user to acknowledge ("continue" or
equivalent) before advancing. No mandatory questions required.

### S4-S7: Full Hard Gate

Present evidence AND mandatory questions with numbered options per Phase 4.7. Block advancement
until user responds.

---

## Two-Layer Enforcement

### Layer 1: Individual Commands

Each delegated command independently enforces quality and presents structured output with PASS/FAIL
status. This is the command's own enforcement, built into its instruction text.

### Layer 2: cu-pipe Verification

cu-pipe verifies that: (a) the delegated command was invoked, (b) structured output was produced,
(c) the PASS/FAIL status is acceptable. Both layers must pass for a stage to advance.

If either layer fails, cu-pipe blocks stage advancement and reports the failure.

---

## Phase 4.9: Mandatory Evidence Verification Protocol

**This protocol is the primary hardening mechanism.** No stage may be marked `completed` until its
evidence has been verified on disk. Self-attestation without disk-level proof is rejected.

### Tool: `pipeline-validator`

Evidence verification is enforced by the `pipeline-validator` engine,
`${CLAUDE_PLUGIN_ROOT}/tools/pipeline_validator.py` (OpenCode also registers it as a custom tool). cu-pipe MUST
invoke this tool at every stage boundary.

**Three actions**:

| Action   | Invocation                                                                | When Used                                                                                                                                                                                                                      |
| -------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `verify` | `pipeline-validator(action="verify", story_id="<id>", stage="S<X>_NAME")` | Before marking any stage `completed`                                                                                                                                                                                           |
| `status` | `pipeline-validator(action="status", story_id="<id>")`                    | At `status` command, before advancing                                                                                                                                                                                          |
| `audit`  | `pipeline-validator(action="audit")`                                      | At `init` to check overall health; also a standing CI gate (`deploy/local_ci.py` + `quality.yml`, TD-171 AC5) over the FULL corpus (`*.yaml`, all story-id prefixes; `schema_version: 1` records reported as `legacy_skipped`) |

### Verification Procedure

Before recording any stage as `completed`, cu-pipe MUST:

1. **Invoke**: Call `pipeline-validator` with `action="verify"`, passing the story ID and current
   stage key
2. **Inspect**: Review the JSON output - specifically `passed`, `errors`, and `warnings`
3. **Decide**:

   - If `passed == true`: mark stage `completed`, record `completed_at`
   - If `passed == false` and `errors` is non-empty: REJECT stage completion, report to user:

     ```
     ## S<X> EVIDENCE VERIFICATION FAILED

     Missing evidence:
     - [ ] <errors[0]>
     - [ ] <errors[1]>

     Stage completion REJECTED. Resolve the missing evidence before retrying.
     ```

4. **No bypass**: Evidence verification failures cannot be bypassed with `force`

### Per-Stage Verification Rules (Implemented in pipeline_validator.py)

| Stage | Checks Performed by `pipeline-validator verify`                                                    |
| ----- | -------------------------------------------------------------------------------------------------- |
| S0    | Feature branch exists; YAML state file parseable; story status is In Progress                      |
| S1    | Kickoff artefact file exists; story file changed since S0; evidence non-empty                      |
| S2    | Plan artefact file exists; evidence non-empty                                                      |
| S3    | Evidence non-empty; commits exist since S2                                                         |
| S4    | Evidence contains PASS/FAIL status indicator                                                       |
| S5    | Evidence contains PASS/FAIL status indicator                                                       |
| S6    | Evidence contains PASS/FAIL; `quality_gates` all pass                                              |
| S7    | Evidence contains PASS/FAIL/SKIP/WARN status indicator                                             |
| S8    | Dev-journal file exists on disk (extracted from `closure_checks.dev_journal`); evidence non-empty  |
| S9    | Story frontmatter status is `In Progress` (TD-173 , `Done` is asserted at S10); evidence non-empty |
| S10   | Evidence non-empty (MR URL, user confirmation)                                                     |

### S8-Specific Hardening

S8 has historically been the stage where evidence gaps accumulate. For S8 specifically.

**S8 is documentation capture, and it is delegated, not improvised. The three capture commands MUST
be INVOKED, in this order:**

1. **`/cu:dev-journal`** , create the session journal entry.
2. **`/cu:memory-update`** , synchronise the Memory Bank (the command performs its own full review of
   all 6 files; do NOT substitute ad-hoc hand-edits to one or two files).
3. **`/cu:readme-update`** , review and update README.md files affected by the story's changes (run
   it against the folder(s) the story touched).

**Anti-shortcut rule**: producing an _equivalent_ artefact by hand (writing the journal inline,
hand-editing `activeContext.md`, manually tweaking a README) does NOT satisfy S8. The commands carry
their own rigour (memory-update reviews all 6 bank files; readme-update sweeps a folder hierarchy
and checks cross-references); skipping the command skips that rigour. If a capture command cannot be
invoked in the current environment, record WHY in the stage evidence and flag it to the user , do
not silently substitute manual work.

**Disk-level verification (a stage may not be marked completed until all pass):**

1. **Dev-journal**: the file path recorded in `closure_checks.dev_journal` MUST resolve to an
   existing file. Verification: `test -f <path>` returns 0.
2. **Memory-bank**: `/cu:memory-update` was invoked AND at least `activeContext.md` and `progress.md`
   were modified during this pipeline run. Verification:
   `git diff --name-only HEAD~1 -- memory-bank/` includes these files.
3. **README update**: `/cu:readme-update` was invoked for the story's touched folder(s).
   Verification: README files changed in working tree or last commit (or, if none needed changing,
   the stage evidence records that `/cu:readme-update` ran and found nothing to update).

If any of these three checks fail, S8 completion is REJECTED regardless of other evidence.

---

## S5 Formal Review Protocol

S5 delegates to `/cu:arch-review` which produces:

1. **Structured findings table**: severity, category, issue, recommendation
2. **Risk register**: risk ID, description, probability, impact, mitigation
3. **PASS/FAIL status**

cu-pipe presents the full findings table and risk register to the user with disposition options.
User disposition is recorded in pipeline YAML evidence.

---

## S8 User Hold Protocol

Before advancing past S8, cu-pipe MUST perform disk-level verification of all S8 deliverables, then
present the verified evidence:

1. **Verify dev-journal**: Confirm `test -f docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-<slug>.md`
   returns 0. If the file does not exist, REJECT S8 completion.
2. **Verify memory-bank**: Confirm `activeContext.md` and `progress.md` have been modified during
   this pipeline run.
3. **Verify readme-update**: Confirm `/cu:readme-update` was executed (README files changed).

Only after all three verifications pass, present the hold:

- Dev-journal location and file existence
- Memory-bank files updated
- `/cu:readme-update` execution and files changed

Then asks:

```
## S8 CAPTURE - User Hold

Evidence:
- Dev-journal: docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-<slug>.md (VERIFIED: file exists on disk)
- Memory bank: activeContext.md, progress.md, systemPatterns.md (VERIFIED: files modified)
- README update: N files updated via /cu:readme-update (VERIFIED: command executed)

What would you like to do?
[A] Confirm and advance to S9 (CLOSE)
[B] Review capture artefacts before advancing
[C] Hold - do not advance yet
```

Record user decision in pipeline YAML evidence before advancing.

---

## Phase 5: Intent Behaviour

### `init <story-id>`

1. Resolve the story
2. Call `pipeline-validator(action="audit")` to check overall pipeline health
3. Ensure pipeline directory exists
4. Create feature branch: `feature/<story-id>-<slug>` (skip if already on matching branch)
5. Create YAML state file on the feature branch
6. Record branch name in YAML
7. Mark S0 completed, set current_stage to S1
8. Call `pipeline-validator(action="verify", story_id, stage="S0_SELECT")` to confirm S0 evidence
9. Delegate to `/cu:story-update`: insert S0 progress entry, set status In Progress, update
   last_modified
10. Delegate to `/cu:kanban`: move card TODO -> DOING
11. Present S0 evidence (acknowledgement mode per Phase 4.8)

### `status [story-id]`

1. Resolve the story
2. Call `pipeline-validator(action="status", story_id)` to get validated pipeline state
3. Present: current stage, completed stages, pending stages, bypass history, next expected evidence,
   any warnings from the validator

### `next [story-id]`

1. Resolve the story
2. Read YAML state file
3. Present checklist for the next pending stage with expected evidence

### `complete [story-id]`

1. Resolve the story, read YAML state file
2. Treat as **advance and complete the current stage**
3. **Call `pipeline-validator(action="verify", story_id, stage)` for the current stage**. If
   `passed == false`, REJECT stage completion immediately and present the `errors` array to the
   user. Do not proceed to step 4.
4. **Stage-specific delegation and verification**:

| Stage | Action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| S1    | Delegate to `/cu:story-kickoff`. **Story update gate (AC14)**: verify story file has changed since S0 (`git diff` on story file); if unchanged, REJECT S1 and require challenge findings to be applied. Verify challenge log has >= profile minimum entries. Write artifact to `pipeline-audit-trail/artifacts/<story-id>-s1-kickoff.md`. Delegate to `/cu:story-update` for progress entry.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| S2    | Agent produces implementation plan inline (no delegation needed). Verify: at least one alternative considered, "what could go wrong" section present. Write artifact to `pipeline-audit-trail/artifacts/<story-id>-s2-plan.md`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| S3    | Agent produces deliverables inline. Self-review against each AC. Record deviation log if execution diverged from plan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| S4    | Delegate to `/cu:quality-review`. Collect structured output. Apply hard gate protocol (Phase 4.7).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| S5    | Delegate to `/cu:arch-review`. Collect findings table + risk register. Apply hard gate protocol (Phase 4.7) AND formal review protocol.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| S6    | Delegate to `/cu:qa-gate`. Collect verified_claims. Apply hard gate protocol (Phase 4.7). Block on any non-zero exit code.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| S7    | Delegate to `/cu:dod-verify`. Collect PASS/FAIL/SKIP/WARN per criterion. Apply hard gate protocol (Phase 4.7).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| S8    | **INVOKE** `/cu:dev-journal`, then `/cu:memory-update`, then `/cu:readme-update` (in that order , do NOT hand-author equivalents; see S8-Specific Hardening anti-shortcut rule). Verify file artefacts exist on disk. Apply user hold protocol (Phase 4.8).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| S9    | Delegate to `/cu:story-update` (progress entry; status stays In Progress) and `/cu:readme-update`. Commit all close docs. Verify: close docs committed. The status/board flip to Done/DONE happens POST-MERGE (TD-173) , setting it here is unsatisfiable against the audit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| S10   | **Re-run the full quality battery on current HEAD (S10 Merge Readiness, MANDATORY) , all green before push.** Then **push** branch to origin (requires user confirmation). Delegate to `/cu:mr-create`, present merge readiness summary, **stop and ask user to confirm merge**. After user confirms: merge, then in ONE post-merge close commit on `main` set story `status: Done`, delegate to `/cu:kanban` (DOING -> DONE), set top-level `status: completed` and populate `completed_at`. **Atomically** , the audit refuses a `completed` pipeline over a story that is not `Done`, and refuses a `Done` story over an `active` pipeline, so the three must move together (TD-173). In the same commit, update the parent epic's stated counters (and its status, if this was its last open child): `epic-validator.py` recounts them from the children and fails the battery otherwise (TD-202). |

5. For checkpoint stages (S1, S3, S6, S9): execute commit procedure (Phase 4.6)
6. Record timestamp, reviewers, evidence
7. Apply stage-end evidence presentation (Phase 4.8)
8. Move current_stage to next pending
9. If S10 complete: set top-level status to `completed`, populate `completed_at`

### `force <stage> "<reason>" [story-id]`

1. Resolve the story
2. Validate stage exists, require non-empty reason, risk_accepted, approved_by
3. Refuse bypasses for S8, S9, and S10
4. Append bypass entry, mark stage as `bypassed`
5. Advance current_stage
6. Delegate to `/cu:story-update` for progress entry noting bypass
7. Delegate to `/cu:kanban` if abandoned (DOING -> CARPARK)

---

## Phase 6: Evidence Heuristics

When giving guidance, inspect the most relevant artefacts:

- **Story source**: `docs-copper/roadmap/backlog/`
- **Analysis notes**: `docs-copper/roadmap/analysis/`
- **Pipeline artifacts**: `docs-copper/roadmap/pipeline-audit-trail/artifacts/` (stage deliverables)
- **Implementation changes**: working tree or recent commits
- **Review evidence**: delegated command output (structured findings, PASS/FAIL)
- **Test and quality evidence**: `/cu:qa-gate` output, verified_claims
- **Capture evidence**: `docs-copper/dev-journal/`, `docs-copper/memory-bank/`
- **Close evidence**: `/cu:mr-create` output, story status, board status, MR confirmation

### Closure Checklist

Each item includes a verification method. S9 completion is REJECTED if any mandatory item fails
verification.

| #   | Item                                   | Verification Method                                      | Mandatory |
| --- | -------------------------------------- | -------------------------------------------------------- | --------- |
| 1   | backlog story status -> Done           | Story frontmatter `status: Done` (verified POST-MERGE)   | S10       |
| 2   | board status -> DONE                   | `/cu:kanban` confirms card in DONE (verified POST-MERGE) | S10       |
| 3   | dev-journal created (file on disk)     | `test -f <journal-path>` returns 0                       | YES       |
| 4   | memory-bank updated                    | `git diff --name-only HEAD~N -- memory-bank/` non-empty  | YES       |
| 5   | `/cu:readme-update` executed           | README files changed in working tree or last commit      | YES       |
| 6   | close docs committed (S9)              | `git log --oneline -1` matches S9 commit message pattern | YES       |
| 7   | DoD verified via `/cu:dod-verify`      | All DoD criteria have definitive status (PASS/SKIP/WARN) | YES       |
| 8   | verified_claims recorded for exec work | `verified_claims` array non-empty in YAML                | CONDITION |
| 9   | branch pushed to origin (S10)          | `git log --oneline origin/main..HEAD` shows commits      | S10       |
| 10  | MR created after push (S10)            | MR URL recorded in S10 evidence                          | S10       |
| 11  | user confirmed merge explicitly (S10)  | User response recorded in evidence                       | S10       |

**CONDITION**: Item 8 is mandatory only when `change_surface.code: true` or
`change_surface.tests: true`.

**Enforcement**: Items 1-7 are verified at S9 completion. Items 9-11 are verified at S10 completion.
Any failed mandatory item blocks stage advancement with a clear error message listing the missing
evidence.

### Testing Scope

- **Framework self-testing** (`scope: framework`): command/skill/rule integrity, governance,
  validators
- **Project delivery guidance** (`scope: project_delivery_guidance`): methodology guidance only

---

## Phase 7: Reporting Format

Return a single Markdown report with:

1. **Story**: resolved ID and file path
2. **Pipeline State**: current stage and status
3. **Profile and Surface**: review profile, change surface
4. **Completed Stages**: with timestamps
5. **Open Gates**: review, quality, readiness items
6. **Next Action**: exact next stage and checklist
7. **Bypasses**: recorded bypass log
8. **Follow-up**: recommended next command

---

## Boundaries

- cu-pipe is a pure orchestrator: all substantive actions delegated to standalone commands
- No backing skill in v2; post-pilot extraction may be considered later
- Feature branch creation mandatory at init; MR creation at S10 after close docs committed
- Merge-to-main and push-to-origin never automatic: user must explicitly confirm
- Intermediate commits at S1, S3, S6, S9 mandatory (Phase 4.6)
- Pipeline commands are explicit permission to update story document and Kanban via delegation
- S8, S9, and S10 are never bypassable
- Hard gates at S4-S7 require user disposition before advancement
- Stage-end evidence presentation at ALL stages (acknowledgement for S0-S3/S8-S10, full gate for
  S4-S7)
- Evidence verification failures at ANY stage cannot be bypassed with `force` (Phase 4.9)
- No stage may be marked `completed` without disk-level verification of its evidence artefacts

---

## Example Usage

```text
/cu:pipe init US-123
/cu:pipe status US-123
/cu:pipe next
/cu:pipe complete US-123
/cu:pipe force S4_CODE_REVIEW "Maintainer accepted review bypass for urgent release" US-123
```

---
