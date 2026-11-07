---
description: Run a dependency analysis , audit security, resolve conflicts, plan updates,
  and check licences across an ecosystem, grounded in the gd-dependency-manager skill
  (SBOM, risk scoring, semver, zero-trust dependencies).
---

Run a dependency analysis for: **$ARGUMENTS**

All arguments are optional. `analysis_focus` (default `comprehensive`; options: `security`,
`performance`, `compatibility`, `licensing`, `comprehensive`); `update_strategy` (default
`conservative`; options: `conservative`, `balanced`, `aggressive`, `security-only`); `ecosystem`
(default `auto-detect`; options: `npm`, `pip`, `maven`, `gradle`, `cargo`, `composer`, `nuget`);
`validation_level` (default `standard`; options: `basic`, `standard`, `strict`, `enterprise`). With
no arguments, ask which project and ecosystem to analyse.

## Approach

1. **Load the dependency knowledge** , Use the `gd-development:dependency-manager` skill.
2. **Inventory** , read the manifests and lock files for the target behind `$ARGUMENTS`, detect the
   `ecosystem`, and build the dependency picture (direct and transitive).
3. **Assess** , per `analysis_focus`, score vulnerabilities, surface version conflicts, check
   licences, and flag bundle-size or supply-chain risk.
4. **Plan** , produce a prioritised, `update_strategy`-aligned remediation plan with a tested
   migration and rollback path, validated at the requested `validation_level`, keeping the lock file
   authoritative.

## Examples

```text
# Security-focused analysis with a balanced update strategy
/gd-development:dependency-manager analysis_focus=security update_strategy=balanced

# Enterprise-grade validation of an npm ecosystem
/gd-development:dependency-manager ecosystem=npm validation_level=enterprise
```

## Opening (when no args)

"Let's get your dependencies under control. Which project and package ecosystem should I analyse,
and is the priority security, conflicts, licences, or bundle size?"

---

- Skill: `gd-development:dependency-manager` (owns the methodologies, the risk scoring, and the safety
  rules)
- Related agent: the proactive `gd-development:dependency-manager` agent loads the same skill autonomously.
