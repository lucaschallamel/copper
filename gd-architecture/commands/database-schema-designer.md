---
description: Run a database schema-design session , produce a performant, integrity-preserving
  schema with an indexing and migration plan, grounded in the gd-database-schema-designer
  skill.
---

Design a database schema for: **$ARGUMENTS**

All arguments are optional. `database_type` (default `postgresql`; options: `postgresql`, `mysql`,
`oracle`, `sqlserver`, `mongodb`, `cassandra`); `schema_complexity` (default `standard`; options:
`simple`, `standard`, `advanced`, `enterprise`); `optimization_focus` (default `performance`;
options: `performance`, `storage`, `integrity`, `scalability`); `migration_strategy` (default
`incremental`; options: `incremental`, `blue_green`, `shadow_table`, `zero_downtime`);
`validation_level` (default `standard`; options: `basic`, `standard`, `strict`, `enterprise`). With
no arguments, open by drawing out the entities, the access patterns, and the integrity rules.

## Approach

1. **Load the schema-design knowledge** , Use the `gd-architecture:database-schema-designer` skill.
2. **Frame the problem** , clarify the entities and relationships behind `$ARGUMENTS`, the read/write
   access patterns, the data-integrity rules, and the expected volume and growth.
3. **Design the schema** , apply the fitting models from the skill (normalisation 1NF-6NF with
   justified denormalisation, indexing strategy, constraints, temporal and multi-tenant patterns) to
   the chosen `database_type` and `optimization_focus`.
4. **Validate and migrate** , at the requested `validation_level`, check query plans, constraint
   compliance, and the rollback path, then deliver the schema with an indexing plan and a
   `migration_strategy` for zero-downtime evolution.

## Opening (when no args)

"Let's design a schema that keeps your data correct and your queries fast as it grows. What entities
and relationships are involved, what are the main read and write patterns, and what integrity rules
must hold?"

## Examples

```bash
# PostgreSQL schema optimised for performance
/gd-architecture:database-schema-designer database_type=postgresql optimization_focus=performance

# Enterprise schema with zero-downtime migration
/gd-architecture:database-schema-designer schema_complexity=enterprise migration_strategy=zero_downtime

# Enterprise-level validation strictness
/gd-architecture:database-schema-designer validation_level=enterprise
```

---

- Skill: `gd-architecture:database-schema-designer` (owns the methodologies, patterns, and schema-design
  knowledge)
- Related agent: the proactive `gd-architecture:database-schema-designer` agent loads the same skill
  autonomously.
