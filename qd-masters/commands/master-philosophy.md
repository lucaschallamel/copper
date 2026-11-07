---
description: Run a philosophical inquiry , clarify concepts, examine assumptions,
  and reason through ethics and meaning, grounded in the qd-master-philosophy skill
  (Socratic method, applied ethics, Eastern and Western traditions).
---

Run a philosophical inquiry focused on: **$ARGUMENTS**

`philosophical_tradition` (optional) sets the primary philosophical approach [options: western,
eastern, integrated, analytical, continental; default: integrated]; `focus_area` (optional) sets the
main area of philosophical inquiry [options: ethics, metaphysics, consciousness, practical_wisdom,
political; default: practical_wisdom]; `engagement_style` (optional) sets the teaching and
discussion approach [options: socratic, academic, contemplative, practical, narrative; default:
socratic]. With no arguments, open by asking which fundamental question has been calling to the
user.

## Approach

1. **Load the philosophical knowledge** , Use the `qd-masters:master-philosophy` skill.
2. **Clarify the question** , untangle what is really being asked in `$ARGUMENTS` and surface the
   hidden assumptions.
3. **Apply a method** , select the fitting approach from the skill (Socratic questioning,
   comparative philosophy, applied ethics, thought experiment) and reason through the traditions
   that bear on it.
4. **Deliver insight** , offer a clear, accessible synthesis that improves how the user thinks and
   lives, in the skill's wise, humble, practical style.

## Opening (when no args)

"Philosophy begins in wonder , that moment when we step back from the rush of life and ask 'why?' or
'what does this mean?' What fundamental question has been calling to you?"

## Examples

```bash
# Explore practical wisdom through Socratic dialogue, drawing on integrated traditions
/qd-masters:master-philosophy philosophical_tradition=integrated focus_area=practical_wisdom engagement_style=socratic
```

---

- Skill: `qd-masters:master-philosophy` (owns the traditions, methods, and philosophical knowledge)
