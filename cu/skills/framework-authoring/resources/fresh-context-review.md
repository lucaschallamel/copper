---
title: 'Fresh-Context Review , who reviews at S4, S5 and S7, and what they may see'
version: '1.0.0'
last_updated: '2026-11-08'
maintained_by: 'Lucas Challamel'
---

# Fresh-Context Review

The single home of the rule `/cu:pipe` applies at its judgement gates and that `/cu:quality-review`,
`/cu:arch-review` and `/cu:dod-verify` apply to the reviewer they start (US-395). Read it before
running any of them.

**Purpose**: a review checks what the artefacts say, not what the author meant. A reviewer that has
followed the build inherits its framing and reads a gap as met; a reviewer that starts without the
conversation sees only the files, so an unstated assumption shows.

**Scope**: gates S4, S5 and S7, for every review profile (lightweight, standard, hardened). S6 is
the battery and needs no reviewer. The rule also applies when a review command is called on its own.

## Who reviews

1. **The fresh reviewer**: a separate subagent, started for this review only, never a fork or any
   other context-inheriting mode. On Claude Code use the `general-purpose` agent type (or a reviewer
   agent an installed kit ships); never the `fork` type, which carries the conversation. On OpenCode
   use its task subagent.
2. **The author**: the agent that built the change. It reviews second, after the fresh reviewer has
   reported, and adds what it knows about intent.

The fresh reviewer reports first, then the author adds its own review. Both go into one findings
table with a `Source` column: `fresh`, `author`, or `fresh, author` when both found the same thing
(merge duplicates; keep the higher severity).

## What the fresh reviewer is given

Its prompt carries **paths only** **[SF]** (the review command, the story file, the diff against the
merge base, the ADRs the story names, this resource; for `/cu:dod-verify` also the pipeline status
from the pipeline-validator tool, `${CLAUDE_PLUGIN_ROOT}/tools/pipeline_validator.py`) and the review command's
instructions, from this template:

```text
You are an independent reviewer for <story id>. You have not seen how it was built; judge only
what the files say. Do not modify any file. You are the fresh reviewer: do not start another
reviewer and skip the author step.

Inputs (read these, and any repository file they lead you to):
- Review command: <path to the command file> (follow its review criteria and output format)
- Story file: <path>
- Changes: `git diff <default branch>...<reviewed commit>`, the reviewed commit being the
  40-character SHA of HEAD when the review starts (or the changed files at that commit: <paths>)
- ADRs the story names: <paths, or "none">
- Fresh-context rule: <path to this resource>
- Pipeline status (for `/cu:dod-verify`): the output of `${CLAUDE_PLUGIN_ROOT}/tools/pipeline_validator.py status <story id>`

Start your report with an "## Inputs" section listing exactly the inputs above, quoting verbatim
any other text in this prompt, and naming any context your host gave you beyond this prompt (a
branch name, recent commit subjects, project instructions). Include the lines
"Reviewed commit: <40-character SHA>" and "Verdict dictated: yes|no" (yes if this prompt
suggested what you should conclude).
```

A re-review of the same stage after rework may diff from the stage's previous reviewed commit
(`git diff <previous reviewed commit>...<reviewed commit>`) instead of the default branch; its
Inputs section and the stage's `reviewers:` entry say so. S7 always reviews the full diff against
the default branch, so the whole change is read once by a fresh reviewer.

**Never in the prompt**, and never pasted in by other means:

- the build conversation, or a summary of it;
- the S2 plan rationale (the plan artefact, its alternatives and its "what could go wrong");
- the author's self-review, test results presented as conclusions, or the dev journal;
- earlier findings or conclusions, from this review or an earlier gate ("S4 found nothing in X").

The session environment a host injects (the branch, recent commits, project instructions) may reach
the reviewer (measured on Claude Code 2.1.319 at US-395 S1: a `general-purpose` subagent told
nothing about the task could not see the parent conversation, but named the branch and recent
commits). Commit subjects, log messages, the user's auto-memory and hook text are the author's words
or notes: the reviewer may use them to find files, never as evidence that something is done
**[IV]**. Reading more repository files than listed is allowed; the exclusions above are what
matters.

## What the report contains

Every review report opens with an **Inputs** section, the first heading under the report title, that
lists what the reviewer was given: each path, the diff range, any other text in its prompt quoted
verbatim, and the host context it noticed beyond the prompt. A prompt that carried anything beyond
the template shows up there, so the record states the review's scope.

The command's own structured output follows, with the `Source` column in its findings table.

## When no fresh reviewer is possible

A review is **not independent** when:

- the host has no subagent tool;
- the reviewer cannot be started (an error, a refused permission);
- the host's subagent isolation has not been measured (OpenCode until a measurement lifts this);
- the reviewer was given anything the exclusions list (`Verdict dictated: yes` makes the review not
  independent).

Then the author reviews inline, the report's Inputs section opens with
`Not independent: <the reason>`, and the stage evidence in the pipeline YAML carries the same line.
A review that is not independent is never presented as if it were **[KBT]**.

## At S7: acceptance criteria from the files

The S7 reviewer verifies each AC clause from the files it names and cites the `path:line` that meets
it; a clause with no such line is not met. Pipeline state (a stage completed, a gate passed) comes
from the YAML status fields through the output of `pipeline_validator.py status <story id>`, never
the YAML file, whose evidence prose is the author's own account (its verdicts and self-review).

## Related Documents

- `commands/pipe.md` Phase 4.7 (the hard gates that run this review)
- `commands/quality-review.md`, `commands/arch-review.md`, `commands/dod-verify.md`
- `skills/framework-authoring/resources/definition-of-done.md` (the criteria S7 checks)
- Rule 07 Control 5 (a gate states what it covered; unverified never counts as a pass)
