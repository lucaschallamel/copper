---
description: Run a context-optimisation session , compress, structure, or hand off
  conversation context with high retention, grounded in the gd-context-manager skill
  (token economics, hierarchical memory, semantic compression).
---

Optimise conversation context for: **$ARGUMENTS**

All arguments are optional. `context_operation` (default `optimize`; options: `optimize`, `handoff`,
`compress`, `analyze`, `recover`, `archive`); `session_scope` (default `current`; options:
`current`, `project`, `multi-project`, `enterprise`); `target_format` (default `summary`; options:
`summary`, `detailed`, `technical`, `executive`, `gendev-standard`) sets the output format;
`optimization_level` (default `balanced`; options: `minimal`, `balanced`, `aggressive`, `maximum`);
`handoff_style` (default `comprehensive`; options: `quick`, `standard`, `comprehensive`,
`archival`); `focus_area` (default `all`; options: `all`, `code-changes`, `decisions`,
`architecture`); `compression_ratio` (float, default `0.7`; range `0.1`-`0.9`) sets how aggressively
context is compressed; `quality_threshold` (float, default `0.85`; range `0.5`-`1.0`) sets the
minimum retention quality to hold; `gendev_compliance` (boolean, default `true`) keeps output
aligned to ecosystem standards. With no arguments, open by assessing the current context size and
the operation needed.

## Approach

1. **Load the context knowledge** , Use the `gd-framework:context-manager` skill.
2. **Assess** , gauge the context behind `$ARGUMENTS`, its size and health, and confirm the
   `context_operation` and `session_scope`.
3. **Operate** , at the chosen `optimization_level`, apply the fitting model from the skill
   (hierarchical layering, semantic compression, lifecycle pruning) to the `focus_area`, preserving
   decision rationale.
4. **Deliver** , produce the optimised context or a `handoff_style` handoff, validating that no
   load-bearing context was lost.

## Opening (when no args)

"Let's get your context under control. How large is the conversation now, and do you want to
optimise the active session, compress it, or hand it off for a clean resumption later?"

## Examples

```bash
# Optimise the current session into a summary
/gd-framework:context-manager context_operation=optimize session_scope=current target_format=summary
```

---

- Skill: `gd-framework:context-manager` (owns the methodologies, patterns, and context knowledge)
- Related agent: the proactive `gd-framework:context-manager` agent loads the same skill autonomously.
