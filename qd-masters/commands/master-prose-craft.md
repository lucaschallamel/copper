---
description: Run a line-level prose revision pass , diagnose abstraction, filter words,
  sensory balance, rhythm and register, grounded in the qd-master-prose-craft skill.
---

# /qd-masters:master-prose-craft

Revise a passage at the line, naming each defect class before proposing a change.

Load the `qd-masters:master-prose-craft` skill and apply it to the supplied material.

## Arguments

- `passage` , the text to revise (required)
- `revision_focus` , optional: one of abstraction, filter-words, sensory, rhythm, show-tell, register
- `authorial_intent` , optional: what the passage is meant to achieve, so deliberate choices are preserved

## Output

A diagnosis-first revision: defect class, quoted line, proposed revision, and what the revision changes.
Deliberate authorial choices are identified and left alone.
