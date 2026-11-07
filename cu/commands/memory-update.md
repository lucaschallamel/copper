---
description: Comprehensive memory bank synchronisation across all 6 core files
---

# /cu:memory-update

Initiate comprehensive memory update for: **$ARGUMENTS**

---

## Overview

This command synchronises project knowledge across the **Memory Bank** (`/memory-bank/`) - the 6
core files that maintain AI session continuity.

---

## Phase 1: Context Gathering

Before updating, gather current session context:

1. **Read Current State**:

   - `activeContext.md` (current work focus)
   - `progress.md` (milestones)
   - Check git status for recent changes

2. **Identify Update Scope**:
   - What was worked on? (proposal, project, analysis)
   - What was completed? (deliverables, decisions)
   - What decisions were made? (with principle codes)
   - What was learned? (insights, process improvements)

---

## Phase 2: Memory Bank Update

Rule 03's review questions (moved here by US-378), asked of every file even when nothing changes:

- **Current state**: what was just completed, what is in progress, what changed about our
  understanding?
- **Next steps**: what is the immediate priority, are there blockers, what decisions need to be
  made?
- **Insights**: new patterns discovered, lessons learned, gotchas to remember?

Focus particularly on `activeContext.md` and `progress.md`, which track current state.

Update the 6 memory bank files in hierarchical order:

### Update Sequence (Respecting Dependencies)

```
projectbrief.md    → Rarely changes (only if scope/objectives change)
       ↓
productContext.md  → Rarely changes (only if market/positioning changes)
       ↓
systemPatterns.md  → When architecture evolves (new ADRs, patterns)
       ↓
techContext.md     → When tech stack changes (new dependencies, versions)
       ↓
activeContext.md   → EVERY SESSION (current work, recent changes, next steps)
       ↓
progress.md        → Weekly (milestones, decision log)
```

### File-by-File Update Guidelines

#### 1. activeContext.md (ALWAYS UPDATE)

- Update "Last Updated" date
- Update "Current Phase" and "Status"
- Add the new session block
  - Format: `## Session YYYY-MM-DD: <STORY-ID> , <one-line framing>`
  - Include: Focus, Delivered, Key decisions, Learnings
- **Roll the previous session block to `archive/activeContext-archive.md`** (US-261), keeping the
  live head at the **last 1-2 blocks** per the Rule 03a budget. Blocks move **VERBATIM**, newest
  first, and the block is **appended to the archive BEFORE it is removed from the live file**, never
  the reverse
- Update "Next Steps" section
- Clear resolved "Active Decisions"

#### 2. progress.md (UPDATE IF MILESTONE REACHED)

- Add milestone to "Achievements" section
- Update decision log with new decisions
- **Roll milestones older than the rolling head to `archive/progress-archive.md`** (US-262), same
  rules: verbatim, newest first, append before remove

> [!warning] The archives are NOT `progress.md`
>
> History leaves `activeContext.md` for `archive/activeContext-archive.md`, and leaves `progress.md`
> for `archive/progress-archive.md`. It does **not** move from one live file into another: both are
> budgeted (Rule 03a), so that only relocates the cost. The archives are **excluded from the
> mandatory session-start read**, mechanically , the read enumerates the six core files BY NAME, so
> a subdirectory is outside it , which is why moving history there removes its per-session cost
> entirely.

#### 3. systemPatterns.md (UPDATE IF ARCHITECTURE CHANGED)

**Trigger Checklist** - Update if ANY of these occurred:

- [ ] New ADR created or existing ADR modified
- [ ] New integration pattern added
- [ ] New data flow or component interaction
- [ ] Architecture decision affecting multiple components

**A new pattern** is written as `## <pattern> (<STORY-ID>[, ...])`, the story id inside the
parenthetical that ENDS the heading (Rule 03a, section 4, gives the full grammar). Phase 2.5 rolls
it to `archive/systemPatterns-archive.md` and leaves one line in `## Pattern index (archived)`
(TD-194). Only the title stays live: a lesson every session must apply goes in a must-include
section (Anti-Patterns to Avoid), edited in place; those never roll.

#### 4. techContext.md (UPDATE IF TECH STACK CHANGED)

**Trigger Checklist** - Update if ANY of these occurred:

- [ ] New dependencies added
- [ ] New tools or quality gates added
- [ ] Version updates to major dependencies
- [ ] New environment requirements

#### 5. productContext.md (RARELY UPDATE)

- Only if market positioning or product vision changes

#### 6. projectbrief.md (RARELY UPDATE)

- Only if project scope or objectives change

---

## Phase 2.5: Prune and archive (MANDATORY , US-264)

Roll closed history out of the live files **before** validating, so the consistency check runs
against the file that will actually be committed.

```bash
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/scripts/prune-memory-bank.py .
```

| Invocation  | Use                                                                              |
| ----------- | -------------------------------------------------------------------------------- |
| (no flag)   | Perform the roll: append to the archive, confirm, then remove from the live file |
| `--check`   | Gate mode , exit 1 if a roll is needed or a live file is over its budget         |
| `--dry-run` | Report what would move, change nothing                                           |

**Why a script and not instructions.** This command carried archive instructions from v2.2.0 that
pointed at `progress.md`, which is itself budgeted, so following them breached that budget while
moving nothing to either archive. It went unnoticed for two months because **prose has no gate**.
The script makes the invariants executable: it appends to the archive and **confirms the block is
there before removing it from the live file**, never the reverse, so an interrupted run leaves a
duplicate rather than a hole. Running it twice is a no-op.

It reads the budgets from Rule 03a's own table and the ratcheted exemptions from the guard that
enforces them, so it cannot disagree with
`tests/regression/test_memory_bank_archive_losslessness.py`. Durable sections (`Next Steps`,
`Active Decisions`, `Blockers`, `Known follow-ups`, `In Progress`, and `systemPatterns.md`'s
must-include sections) are never candidates. Since TD-194 it also rolls every story-tagged pattern
section out of `systemPatterns.md`, leaving an index line. If a bank does not have an archive file,
the script skips that file rather than fails.

---

## Documentation and the memory bank

Moved from Rule 04a by US-378 S7. **Cross-Reference**: see Rule 03 - The Memory-Bank for AI agent
persistent knowledge structure.

**Documentation → Memory Bank Flow**:

- Major project decisions → `memory-bank/progress.md`
- Architecture changes → `memory-bank/systemPatterns.md`
- Technology selections → `memory-bank/techContext.md`
- Active work context → `memory-bank/activeContext.md`

**Memory Bank → Documentation Flow**:

- Memory bank references link to full documentation
- Memory bank provides quick reference, detailed docs provide depth
- Memory bank updated when documentation changes

## Phase 3: Validation (MANDATORY , do not skip)

After updates, verify consistency. This step is easy to skip and has caused stale headers/counts to
slip through , treat it as a required gate, not advisory.

### Consistency Checks

1. **Date Alignment**: every file's `**Last Updated**` is refreshed to today where it changed
2. **Cross-References**: links between documents work
3. **Data Consistency**: the `**Framework counts**` line (agents/skills/commands) matches the actual
   repo , historical-snapshot counts in Prior Work / Recent Changes / Session N blocks are NOT
   edited (they record what was true then)
4. **Completeness**: no TODO placeholders left

### Automated self-check (run it)

```bash
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/scripts/check-memory-bank-consistency.py .
```

This guards the current-state `**Framework counts**` line + `**Last Updated**` dates (the automated
form of checks 1 + 3). Exit 0 = consistent. Run it before reporting the update complete.

---

## Phase 4: Summary Report

Generate a summary of all updates made:

```markdown
## Memory Update Summary

**Session**: [Date] - [Focus] **Scope**: [Brief description]

### Files Updated

- [ ] activeContext.md - [Updated/Skipped]
- [ ] progress.md - [Updated/Skipped]
- [ ] systemPatterns.md - [Updated/Skipped]
- [ ] techContext.md - [Updated/Skipped]
- [ ] productContext.md - [Updated/Skipped]
- [ ] projectbrief.md - [Updated/Skipped]

### Key Changes

1. [Change 1]
2. [Change 2]

### Consistency Self-Check

- `check-memory-bank-consistency.py`: [PASS / FAIL with remediation] (Phase 3, MANDATORY)

### Next Memory Update Triggers

- [Condition that would trigger next update]
```

---

## Example Usage

```bash
# After completing a proposal
/cu:memory-update Completed [Client] data platform proposal - submitted for review

# After architecture changes
/cu:memory-update Architecture decision recorded for API authentication strategy

# Weekly progress update
/cu:memory-update Weekly progress - Q1 proposals at 75% completion

# End of session update
/cu:memory-update Session complete - refined the release plan for the next milestone
```

---

## Cross-References

- **Rule**: `03-memory-bank.rules.md` - Memory bank governance
- **Location**: `/memory-bank/` - 6 core files

---
