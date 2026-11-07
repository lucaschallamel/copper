---
description: Run a performance-optimisation session , find bottlenecks and apply measured
  optimisations for latency, throughput, or resource use, grounded in the gd-performance-optimizer
  skill (Big O, profiling, caching, scalability laws).
---

Run a performance-optimisation session for: **$ARGUMENTS**

All arguments are optional. `optimization_target` (default `general`; options: `latency`,
`throughput`, `memory`, `cpu`, `general`) sets the primary concern; `performance_target` (default
`significant`; options: `incremental`, `significant`, `order-of-magnitude`) sets the ambition;
`constraint` (default `maintainability`; options: `maintainability`, `cost`, `time`,
`compatibility`) sets what must be respected; `validation_level` (default `standard`; options:
`basic`, `standard`, `strict`, `enterprise`). With no arguments, ask what is slow and what the
workload looks like.

## Approach

1. **Load the performance knowledge** , Use the `gd-development:performance-optimizer` skill.
2. **Measure** , establish a baseline for the target behind `$ARGUMENTS` with a representative
   workload, then profile to locate the real bottleneck.
3. **Optimise** , apply the fitting techniques (algorithmic, memory, query, concurrency, caching)
   for the chosen `optimization_target` and `performance_target`, respecting `constraint`.
4. **Validate** , re-measure at the requested `validation_level`, keep the before/after evidence
   (flame graph, benchmark, metric), and confirm correctness is preserved.

## Examples

```text
# Latency-focused optimisation aiming for order-of-magnitude gains
/gd-development:performance-optimizer optimization_target=latency performance_target=order-of-magnitude

# Enterprise-grade validation of a performance optimisation
/gd-development:performance-optimizer validation_level=enterprise
```

## Opening (when no args)

"Let's make this faster with evidence, not guesswork. What is slow , an endpoint, a query, a job ,
what load does it see, and is your priority latency, throughput, or resource use?"

---

- Skill: `gd-development:performance-optimizer` (owns the methodologies, the analysis frameworks, and
  the safety rules)
- Related agent: the proactive `gd-development:performance-optimizer` agent loads the same skill autonomously.
