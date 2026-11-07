---
description: Run a data-architecture design session , produce a governed, scalable
  data platform with modelling, pipelines, and a roadmap, grounded in the gd-data-architect
  skill.
---

Design a data architecture for: **$ARGUMENTS**

All arguments are optional. `architecture_type` (default `lakehouse`; options: `warehouse`, `lake`,
`lakehouse`, `mesh`, `streaming`, `multi-tenant`, `hybrid`); `scale_level` (default `enterprise`;
options: `departmental`, `enterprise`, `web-scale`); `compliance_requirements` (default `general`;
options: `gdpr`, `ccpa`, `hipaa`, `pci`, `sox`, `multi-regulatory`, `general`);
`modernization_focus` (default `balanced`; options: `legacy-migration`, `cloud-native`, `real-time`,
`cost-optimization`, `governance`, `balanced`); `technical_depth` (default `balanced`; options:
`strategic`, `balanced`, `detailed`, `implementation`); `industry_focus` (default `cross-industry`;
options: `financial`, `healthcare`, `retail`, `manufacturing`, `technology`, `public-sector`,
`cross-industry`). With no arguments, open by drawing out the data sources, the analytics goals, and
the governance constraints.

## Approach

1. **Load the data-architecture knowledge** , Use the `gd-architecture:data-architect` skill.
2. **Frame the problem** , clarify the data sources and consumers behind `$ARGUMENTS`, the volume and
   velocity, the analytics and ML goals, and the governance and compliance constraints.
3. **Design the platform** , apply the fitting models from the skill (Kimball dimensional, Data
   Vault 2.0, Lambda/Kappa, Data Mesh, medallion zones) to the chosen `architecture_type` and
   `scale_level`, and capture the modelling, pipelines, and isolation strategy.
4. **Validate and roadmap** , at the requested `technical_depth`, check the scalability path,
   lineage and quality controls, and the `compliance_requirements`, then deliver a phased
   implementation roadmap with cost and trade-off analysis.

## Opening (when no args)

"Let's design a data platform that serves your analytics and ML needs and stays governed and
cost-effective. What are your data sources and volumes, what do you need to get out of it, and what
governance and compliance constraints apply?"

## Examples

```bash
# Lakehouse platform for financial services
/gd-architecture:data-architect architecture_type=lakehouse industry_focus=financial
```

---

- Skill: `gd-architecture:data-architect` (owns the methodologies, patterns, and data-architecture
  knowledge)
- Related agent: the proactive `gd-architecture:data-architect` agent loads the same skill autonomously.
