---
description: Process and clean up voice memo transcripts through a multi-phase pipeline
---

# /cu:transcript-cleanup

Process and clean up voice memo transcript: **$ARGUMENTS**

---

## Overview

This command processes raw voice memo transcripts through a 4-phase pipeline:

0. **Formatting** - Break long single-line transcripts into readable paragraphs
1. **Disambiguation** - Ask clarifying questions about unclear content
2. **Cleaned Version** - Minimal fixes preserving original style and flow
3. **Structured Version** - Organised into logical sections with proper formatting

---

## Phase 0: Preliminary Formatting

### Purpose

Raw speech-to-text transcripts are often a single long line. This phase breaks them into readable
chunks before human review.

### Execution

**Step 0.1: Check if formatting is needed**

- If input file already ends with `_formatted.md`, skip to Phase 1
- If input file is raw transcript, proceed with formatting

**Step 0.2: Resolve the input, then run the formatting script**

Resolve the transcript path FIRST. Never run the script with an empty argument:

1. If `$ARGUMENTS` names a file, use it.
2. Otherwise, ask the user for the transcript path.
3. Otherwise, pick the newest unprocessed file under `_voice-memos/` (one with no sibling
   `_formatted.md`).

Then run the formatter with the Bash tool, using **`python3`** and the framework tools directory
that exists in THIS deployment. The snippet below auto-detects it , do not hardcode one host's
directory, because each deployment has only its own:

```bash
# Auto-detect the host framework tools dir (${CLAUDE_PLUGIN_ROOT}/tools on Claude Code, else ${CLAUDE_PLUGIN_ROOT}/tools):
TOOLS="$([ -d ${CLAUDE_PLUGIN_ROOT}/tools ] && echo ${CLAUDE_PLUGIN_ROOT}/tools || echo ${CLAUDE_PLUGIN_ROOT}/tools)"
python3 "$TOOLS/format_transcript.py" "<resolved-input>" --sentences 5
```

This creates `[filename]_formatted.md` with line breaks every 5 sentences. If no transcript can be
resolved, stop and ask the user , do not call the script with no input.

**Step 0.3: Continue with formatted file**

All subsequent phases work from the `_formatted.md` version.

---

## Phase 1: Disambiguation Questions

### Identify Ambiguities

Scan for the following types of issues requiring user clarification:

**A. Unclear References**

- Pronouns without clear antecedents ("they", "it", "that thing")
- Vague project/feature names
- Undefined acronyms or abbreviations
- References to people, companies, or tools without context

**B. Potential Transcription Errors**

- Words that seem out of context (speech-to-text misrecognition)
- Technical terms that may be misspelled phonetically
- Homophone confusions (their/there/they're, effect/affect)
- Proper nouns that may be transcribed incorrectly

**C. Logical Gaps**

- Incomplete thoughts or sentences
- Missing context for decisions mentioned
- Unclear relationships between topics

**D. Intent Clarification**

- Statements that could be interpreted multiple ways
- Action items vs observations (is this a TODO or just a note?)
- Priority indicators that are ambiguous

### Pre-Research

Before asking any questions, **search the codebase** (grep, file search, existing meeting notes,
previous transcripts) to resolve ambiguities autonomously. Only ask the user about items where no
clue exists in the project.

### Present Questions

**Format: One question at a time, with multiple choices.**

For each unresolved ambiguity:

1. Quote the relevant text passage
2. Explain what's unclear
3. Offer **multiple-choice options** (A, B, C, ...) with your best guesses
4. Wait for the user's answer before asking the next question
5. If the user provides a bulk answer covering several items, apply all corrections at once

**Rules:**

- Do NOT dump all questions at once - ask them **sequentially, one by one**
- Always provide **at least 2 options** to choose from (plus "other" if appropriate)
- If codebase research resolved all ambiguities, skip Phase 1 entirely and explain what was
  auto-resolved
- Group trivially similar items (e.g. 3 garbled proper nouns) into a single question only if they
  share the same context

---

## Phase 2: Cleaned Version (\_cleaned.md)

### Cleaning Principles

**PRESERVE:**

- Original speaking style and voice
- Natural flow and thought progression
- Personal expressions and emphasis
- The order of topics as presented

**FIX (Minimal):**

- Obvious transcription errors (speech-to-text mistakes)
- Missing or incorrect punctuation
- Run-on sentences (add periods/commas where natural pauses occur)
- Filler words ONLY if excessive (um, uh, like, you know)
- Repeated words from stuttering/restarts

**DO NOT:**

- Rewrite sentences for "better" grammar
- Reorganise content or change topic order
- Add formal language or remove casual tone
- Remove tangents or asides (they may be important context)

### Output Format

Save as: `[original_filename]_cleaned.md`

---

## Phase 3: Structured Version (\_structured.md)

### Structuring Process

**Step 3.1: Identify Topics**

- Group content into logical themes/topics
- Identify main subjects discussed
- Note action items, decisions, and questions

**Step 3.2: Create Sections**

Possible section types:

- `## Summary` - Brief overview of main points (2-3 sentences)
- `## Key Points` - Main ideas as bullet points
- `## Decisions Made` - Any decisions mentioned
- `## Action Items` - TODOs with assignee if mentioned
- `## Questions/Open Items` - Unresolved questions raised
- `## Ideas & Exploration` - Brainstorming, possibilities discussed
- `## Technical Notes` - Technical details, specifications
- `## Follow-ups` - Items needing future attention

**Step 3.3: Extract Metadata**

Add frontmatter:

```yaml
---
date: [date from filename or content]
type: voice-memo
topics: [list of main topics]
action_count: [number of action items]
---
```

### Output Format

Save as: `[original_filename]_structured.md`

---

## File Naming Convention

```
Original:    20251130.md
Formatted:   20251130_formatted.md  (from format_transcript.py)
Cleaned:     20251130_cleaned.md    (this command - Phase 2)
Structured:  20251130_structured.md (this command - Phase 3)
```

---

## Example Usage

```bash
# Process a voice memo transcript
/cu:transcript-cleanup _voice-memos/20251130.md

# Process already-formatted transcript
/cu:transcript-cleanup _voice-memos/20251130_formatted.md
```

---

## Notes

- **Automatic formatting**: Raw transcripts are automatically formatted before processing
- If input already ends with `_formatted.md`, formatting step is skipped
- Questions in Phase 1 are critical - do not skip or rush them
- The cleaned version should be usable as-is for reference
- The structured version is for quick scanning and action tracking
- All output files are saved in the same directory as the original

---

## Ecosystem Split

This command relies on components from two different locations:

| Component                     | Location                                                        | Owner      | Installed By   |
| ----------------------------- | --------------------------------------------------------------- | ---------- | -------------- |
| `/cu:transcript-cleanup`      | `<harness-root>/commands/cu-transcript-cleanup.md`              | Framework  | Clone          |
| `format_transcript.py`        | `${CLAUDE_PLUGIN_ROOT}/tools/` (OpenCode) or `${CLAUDE_PLUGIN_ROOT}/tools/` (Claude Code) | Framework  | Regenerated    |
| `voice-memo-processing` skill | `~/.claude/skills/voice-memo-processing/`                       | User-level | Manual install |

**Key points:**

- The command and formatting utility ship with the framework repository. They work out of the box
  after cloning.
- The `voice-memo-processing` skill lives at user-level (`~/.claude/skills/`) and must be installed
  separately. It is not part of the framework `<harness-root>/skills/` directory.
- Phase 0 formatting uses the shipped `format_transcript.py` from the active host's tools directory
  (`${CLAUDE_PLUGIN_ROOT}/tools/` on OpenCode, `${CLAUDE_PLUGIN_ROOT}/tools/` on Claude Code; both are generated from
  `kits/core/tools/` by `deploy.regenerate`, US-193/US-194). Phases 1-3 (disambiguation, cleaning,
  structuring) are performed by the AI agent and may reference the user-level skill for additional
  context.

---

**Output**: \_formatted.md + \_cleaned.md + \_structured.md
