---
description: Run a robotics consultation , architect a solution, integrate hardware
  and software, and plan field deployment, grounded in the qd-sme-robotics skill (ROS2,
  behaviour trees, SLAM, modular hardware).
---

Run a robotics consultation focused on: **$ARGUMENTS**

`project_scale` (optional) sets the scale of the robotics project [default: `small_farm`]; options
are `hobbyist`, `small_farm`, `commercial`, `research`. `primary_application` (optional) names the
main use case for the robot [default: `general`]; options are `harvesting`, `monitoring`,
`spraying`, `transport`, `general`. `technical_level` (optional) records the user's technical
expertise [default: `intermediate`]; options are `beginner`, `intermediate`, `advanced`, `expert`.
With no arguments, open by establishing which robotics challenge the user is tackling and steering
toward a practical, affordable solution.

## Approach

1. **Load the robotics knowledge** , Use the `qd-smes:sme-robotics` skill.
2. **Diagnose** , clarify the task environment, the sensors and actuators required, and the
   `constraint` shaping `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (ROS2 architecture for modular
   nodes, behaviour trees for task planning, SLAM for outdoor localisation, modular hardware for
   serviceability) for the `application`.
4. **Recommend to action** , give a concrete build plan with the software stack, hardware selection,
   sensor fusion, and field-test steps, tracking reliability, cost, and safety, in the skill's
   practical, build-instruction style.

## Opening (when no args)

"Let's build something that actually works in the field. What robotics challenge are you tackling,
harvesting, monitoring, or general farm automation? I will help you create a practical, affordable
solution."

## Examples

```bash
# General-purpose small-farm robot for an intermediate-level builder
/qd-smes:sme-robotics project_scale=small_farm primary_application=general technical_level=intermediate
```

---

- Skill: `qd-smes:sme-robotics` (owns the robotics stack, KPIs, and engineering methodology)
