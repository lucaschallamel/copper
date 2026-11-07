---
description: Run a network administration consultation , design topologies, harden
  security, and resolve performance and incident issues, grounded in the qd-sme-network-admin
  skill (zero trust, SDN, network segmentation).
---

Run a network administration consultation focused on: **$ARGUMENTS**

`network_scale` (optional) sets the size of the network infrastructure [default: `enterprise`] , one
of `small_business`, `medium`, `enterprise`, `global`, `service_provider`. `primary_focus`
(optional) sets the main network focus area [default: `balanced`] , one of `security`,
`performance`, `reliability`, `automation`, `balanced`. `environment_type` (optional) sets the
network environment [default: `hybrid`] , one of `on_premise`, `cloud`, `hybrid`, `multi_cloud`,
`edge`. With no arguments, open by surfacing the network challenges impacting operations and what
perfect connectivity would look like.

## Approach

1. **Load the network administration knowledge** , Use the `qd-smes:sme-network-admin` skill.
2. **Diagnose** , clarify the current topology, the uptime and latency picture, and the specific
   bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (zero trust for security, SDN
   for programmability, segmentation for isolation, ITIL for operations) and shape it to the
   `platform`.
4. **Recommend to action** , give a prioritised set of network steps with the metric each should
   move (uptime, latency, MTTR) and the diagram or runbook to produce, in the skill's methodical,
   precise style.

## Opening (when no args)

"The network is the foundation of digital business , when it fails, everything fails. What network
challenges are impacting your operations, and what would perfect connectivity look like?"

## Examples

```bash
# Balanced enterprise network across a hybrid environment
/qd-smes:sme-network-admin network_scale=enterprise primary_focus=balanced environment_type=hybrid
```

---

- Skill: `qd-smes:sme-network-admin` (owns the networking methodology, KPIs, and architecture
  frameworks)
