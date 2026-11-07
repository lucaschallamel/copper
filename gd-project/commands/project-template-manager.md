---
description: Run a project-scaffolding session , select and compose templates, then
  deploy a complete, production-ready project structure with best practices baked
  in, grounded in the gd-project-template-manager skill.
---

Scaffold and deploy a project structure for: **$ARGUMENTS**

All arguments are optional. `project_type` (default `auto-detect`; the primary project category;
options: `web-app`, `mobile`, `data-platform`, `saas`, `e-commerce`, `analytics`, `hybrid`);
`deployment_speed` (default `balanced`; the speed-versus-customisation trade-off; options: `rapid`,
`balanced`, `customized`, `comprehensive`); `industry_vertical` (default `general`; the
industry-specific customisations; options: `general`, `finance`, `healthcare`, `retail`,
`education`, `government`); `validation_level` (default `standard`; the validation strictness;
options: `basic`, `standard`, `strict`, `enterprise`). With no arguments, open by drawing out the
project type, the target environment, and the standards the scaffold must enforce.

## Approach

1. **Load the scaffolding knowledge** , Use the `gd-project:project-template-manager` skill.
2. **Select and compose** , analyse `$ARGUMENTS` to pick the right base templates and combine them for
   the chosen `project_type` and `industry_vertical`, identifying any composite needs.
3. **Customise to context** , apply the fitting models from the skill (domain-driven templates,
   composable architecture, convention-over-configuration, progressive enhancement) at the chosen
   `deployment_speed`, adapting defaults while preserving standards.
4. **Validate and deploy** , at the requested `validation_level`, validate the generated structure
   against the project's standards, avoid overwriting existing files without a rollback path, and
   deliver a deployment manifest, configuration summary, and usage guide.

## Opening (when no args)

"Let's stand up a project you can build on from day one. What kind of project is it, where will it
run, and which industry standards and conventions does the scaffold need to enforce?"

## Examples

```bash
# Rapid SaaS scaffold for healthcare
/gd-project:project-template-manager project_type=saas deployment_speed=rapid industry_vertical=healthcare

# Enterprise-validated web application scaffold
/gd-project:project-template-manager project_type=web-app validation_level=enterprise

# Comprehensive scaffold with full customisation
/gd-project:project-template-manager deployment_speed=comprehensive
```

---

- Skill: `gd-project:project-template-manager` (owns the template architecture, patterns, and KPIs)
- Related agent: the proactive `gd-project:project-template-manager` agent loads the same skill
  autonomously.
