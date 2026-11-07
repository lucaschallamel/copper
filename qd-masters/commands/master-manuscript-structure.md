---
description: Set up or audit a long-form writing project's structure , the canon/working/research/archive
  authority separation, file naming, and where a given document belongs, grounded
  in the qd-master-manuscript-structure skill.
---

# /qd-masters:master-manuscript-structure

Set up a new writing project's structure, or audit an existing one for authority ambiguity.

Load the `qd-masters:master-manuscript-structure` skill and apply it to the project.

## Arguments

- `project_path` , the project to set up or audit (required)
- `mode` , optional: `setup` (propose a layout) or `audit` (find authority ambiguity). Defaults to
  `audit` when the path already has content
- `existing_layout` , optional: a layout to preserve or adapt rather than replace

## Output

For setup: a proposed layout with each folder's authority level stated. For audit: documents whose
authority level is ambiguous, same-level contradictions found, and duplicated canon , each with the
document that should win and why. Renaming and moving are proposed, never performed silently.
