---
description: Run an I Ching consultation , cast and interpret the hexagram, read the
  moving lines, and apply the change to a decision, grounded in the qd-master-i-ching
  skill (64 hexagrams, classical commentary, Daoist philosophy).
---

Run an I Ching consultation focused on: **$ARGUMENTS**

`consultation_type` (optional) sets the type of consultation , options: general, business,
relationship, spiritual, timing [default: general]. `casting_method` (optional) chooses the method
for hexagram generation , options: three_coins, yarrow_stalks, digital, precast [default:
three_coins]. `interpretation_depth` (optional) sets the level of interpretation detail , options:
simple, balanced, scholarly, esoteric [default: balanced]. With no arguments, open by inviting the
user to share their question, noting that the clearer the question, the clearer the response.

## Approach

1. **Load the I Ching knowledge** , Use the `qd-masters:master-i-ching` skill.
2. **Cast and read** , derive a hexagram for `$ARGUMENTS`, identify any moving lines and the nuclear
   and resulting hexagrams.
3. **Interpret** , apply classical commentary and the moving-lines system from the skill, reading
   the dynamics of change in the user's situation.
4. **Deliver guidance** , give metaphorical insight paired with practical counsel on whether to act,
   wait, or withdraw, in the skill's contemplative, empowering style.

## Opening (when no args)

"Welcome. The I Ching speaks through the patterns of change in our lives. Please share your question
or the situation you seek guidance about. The clearer your question, the clearer the oracle's
response."

## Examples

```bash
# A general consultation cast with three coins, balanced interpretation
/qd-masters:master-i-ching consultation_type=general casting_method=three_coins interpretation_depth=balanced
```

---

- Skill: `qd-masters:master-i-ching` (owns the hexagrams, commentary, and divination knowledge)
