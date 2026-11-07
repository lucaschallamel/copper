---
description: Run a continuity verification pass , check a manuscript against canon
  for timeline, character, world rule, physical and terminology contradictions, grounded
  in the qd-master-canon-verification skill.
---

# /qd-masters:master-canon-verification

Verify a draft against established canon and emit a findings report. Verification only , never edits.

Load the `qd-masters:master-canon-verification` skill and apply it to the supplied material.

## Arguments

- `manuscript` , the draft under test (required)
- `canon_sources` , the canon documents and their authority tier (required)
- `scope` , optional: which dimensions to check. Defaults to all five

## Output

A findings report: each item cites manuscript AND canon location, names the canon source's authority
tier, and is classified CONTRADICTION / INCONSISTENCY / UNVERIFIABLE. The verified scope is stated so a
zero-finding result means something. No prose is proposed.
