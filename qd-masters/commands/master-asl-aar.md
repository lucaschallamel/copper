---
description: Produce an ASL after-action report , the fixed template covering plan
  versus execution, critical decisions, what worked, rules learned and next steps.
---

# /qd-masters:master-asl-aar

Emit a structured after-action report. The template is fixed, which is why this is a command rather
than an agent.

## Arguments

- `scenario` , the scenario played (required)
- `outcome` , the result and how it was reached (required)
- `notes` , optional: turn-by-turn observations

## Output

A report with fixed sections: Scenario Overview, Pre-Game Plan vs Execution, Critical Decisions,
What Worked, What Did Not Work, Rules Learned, Lessons Learned, Next Steps. Findings name the
DECISION, not the die roll.
