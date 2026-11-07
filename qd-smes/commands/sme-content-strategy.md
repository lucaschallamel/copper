---
description: Run a content strategy consultation , design content systems, develop
  brand voice, and plan editorial, grounded in the qd-sme-content-strategy skill (content
  strategy quad, topic cluster model, content maturity model).
---

# /qd-smes:sme-content-strategy

Run a content strategy consultation focused on: **$ARGUMENTS**

`content_focus` (optional) sets the primary content domain , options `marketing`, `product`,
`technical`, `brand`, `enterprise` [default: `marketing`]. `organization_size` (optional) sets the
company scale , options `startup`, `growth`, `enterprise`, `agency`, `nonprofit` [default:
`growth`]. `content_maturity` (optional) sets the current content sophistication , options `ad_hoc`,
`developing`, `managed`, `optimized`, `strategic` [default: `developing`]. With no arguments, open
by surfacing the story the content currently tells and whether it is the story the brand wants.

## Approach

1. **Load the content strategy knowledge** , Use the `qd-smes:sme-content-strategy` skill.
2. **Diagnose** , clarify the current content landscape, the brand voice, the audience journey, and
   the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (content strategy quad for
   systems, topic cluster model for SEO, content maturity model for capability) for the user's
   channel.
4. **Recommend to action** , give a prioritised set of steps with the engagement or conversion
   metric each should move and the strategy or style guide to produce, in the skill's purposeful
   style.

## Opening (when no args)

"Content is how your brand shows up in the world, every word shapes perception and drives action.
What story is your content telling, and is it the story you want?"

## Examples

```
/qd-smes:sme-content-strategy content_focus=marketing organization_size=growth content_maturity=developing
```

---

- Skill: `qd-smes:sme-content-strategy` (owns the content strategy methodology, KPIs, and
  frameworks)
