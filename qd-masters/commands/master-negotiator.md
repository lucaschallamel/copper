---
description: Run a deal-strategy session , prepare the negotiation, build leverage,
  and design value-creating moves, grounded in the qd-master-negotiator skill (Harvard
  method, BATNA/ZOPA, game theory, cross-cultural tactics).
---

Run a negotiation-strategy session focused on: **$ARGUMENTS**

`negotiation_type` (optional) sets the type of negotiation [options: business, international,
crisis, personal, legal; default: business]; `complexity_level` (optional) sets the negotiation
complexity [options: simple, moderate, complex, extreme; default: complex]; `cultural_context`
(optional) sets the cultural considerations [options: western, asian, middle_eastern, latin, mixed;
default: western]. With no arguments, open by asking what is at stake and what an ideal outcome
would look like for all parties.

## Approach

1. **Load the negotiation knowledge** , Use the `qd-masters:master-negotiator` skill.
2. **Prepare** , map the interests, parties, and constraints of `$ARGUMENTS`; develop the BATNA and
   estimate the ZOPA.
3. **Apply a framework** , select the fitting method from the skill (principled negotiation, game
   theory, Seven Elements, cultural patterns) and design the opening, the concession path, and the
   leverage.
4. **Deliver the plan** , give a prioritised sequence of moves that expands value before dividing
   it, with contingencies for deadlock, in the skill's firm-yet-flexible style.

## Opening (when no args)

"Every negotiation is an opportunity to create value, not just claim it. What's at stake in your
negotiation, and what would an ideal outcome look like for all parties?"

## Examples

```bash
# Prepare a complex business partnership negotiation in a Western context
/qd-masters:master-negotiator negotiation_type=business complexity_level=complex cultural_context=western
```

---

- Skill: `qd-masters:master-negotiator` (owns the frameworks, tactics, and negotiation knowledge)
