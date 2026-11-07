# SP - Spike Story Type Guidance

**Story Type**: Spike | **Prefix**: SP-NNN | **Version**: 1.2.0 | **Last Updated**: 2026-05-07

---

## Progress Update Block

Spikes should include a **collapsible progress update callout** immediately after the YAML
frontmatter and before the spike heading or overview content.

### Recommended Format

```markdown
> [!note]- Progress updates
>
> - **2026-05-07**: Spike scoped and awaiting research execution.
> - **2026-05-06**: Investigation scope refined and decision framing clarified.
> - **2026-05-05**: Spike created with research question and expected outcome.
```

### Usage Guidance

- Use the collapsible callout syntax: `[!note]-`
- Track research lifecycle milestones: scoped, investigated, analysed, concluded
- Keep entries tied to actual research framing or findings rather than implementation claims

---

## Definition

**Spike**: Time-boxed investigation to answer a technical question, evaluate alternatives, or reduce
uncertainty before implementation. Does not deliver production functionality but enables informed
decision-making.

---

## When to Use SP Stories

- **Technology evaluation** (comparing frameworks, tools, platforms)
- **Architecture decision research** (design alternatives analysis)
- **Performance analysis** and bottleneck investigation
- **Proof-of-concept** development for unknowns
- **Complexity estimation** for large features
- **Feasibility assessment** for technical approaches

---

## Required YAML Fields

```yaml
---
story_id: SP-015
story_type: spike
title: 'Evaluate Kafka vs RabbitMQ for event streaming'
research_question: 'Which message broker best fits our scalability and operational requirements?'
time_box: '16 hours' # e.g., "16 hours", "2 days"
expected_outcome: 'ADR documenting choice with pros/cons, follow-up implementation stories'
decision_deadline: 2025-02-10 # when decision is needed
spike_outcome: '' # actual findings (added post-completion)
priority: High
story_points: 0 # spikes don't earn velocity points
status: Done
created: 2025-01-25
last_modified: 2025-02-05
---
```

---

## Time-Boxing Guidelines

### Quick Investigation: 4-8 hours

- Simple comparison or analysis
- Binary technology choice
- Performance profiling of known bottleneck

### Standard Spike: 16 hours / 2 days

- Typical research scope
- Technology evaluation with POC
- Architecture design exploration

### Complex Research: 24-40 hours / 3-5 days

- Comprehensive evaluation (3+ alternatives)
- Performance analysis with benchmarking
- Feasibility assessment for complex feature

### Maximum Time-Box: 5 days

- If research requires >5 days, break into multiple spikes or reconsider approach

---

## Spike Template Structure

```markdown
# Spike: [Research Question]

## Time Box: [X hours/days]

## Decision Deadline: [YYYY-MM-DD]

## Research Question

[What we need to learn or decide]

## Success Criteria

[What constitutes sufficient research to make informed decision]

- Specific questions to answer
- Data/metrics to collect
- Options to evaluate

## Deliverables

- [ ] Technical findings document
- [ ] Recommendation with pros/cons analysis
- [ ] ADR if architecture decision required
- [ ] Follow-up implementation stories

## Expected Outcomes

[What decisions or knowledge we expect to gain]

## Spike Outcome (Post-Completion)

[Actual findings, recommendation, decision made]

- Research findings summary
- Recommendation with justification
- Pros/cons comparison
- Follow-up stories created: US-XXX, TD-YYY

## Next Steps

[Follow-up stories based on findings]
```

---

## Examples

### Example 1: Technology Evaluation Spike

```markdown
---
story_id: SP-015
story_type: spike
title: 'Evaluate Kafka vs RabbitMQ for event streaming'
research_question: 'Which message broker best fits our scalability and operational requirements?'
time_box: '16 hours'
expected_outcome: 'ADR with technology choice, implementation roadmap'
decision_deadline: 2025-02-10
spike_outcome: 'Recommendation: Kafka. ADR created with full analysis.'
priority: High
story_points: 0
status: Done
---

# Spike: Event Streaming Technology Evaluation

## Time Box: 16 hours (2 days)

## Decision Deadline: 2025-02-10

## Research Question

Which message broker (Kafka vs RabbitMQ) best supports:

- 10,000 events/second throughput requirement
- Event replay capability for analytics
- Operational complexity acceptable for 3-person ops team
- Cost-effectiveness for our scale

## Success Criteria

Research delivers:

- [ ] Performance benchmark results (throughput, latency)
- [ ] Operational complexity assessment
- [ ] Cost analysis (infrastructure + operational)
- [ ] Proof-of-concept implementation (4 hours each)
- [ ] Clear recommendation with justification

## Deliverables

- [x] Technical findings document
- [x] Benchmark results spreadsheet
- [x] ADR created: Event Streaming Technology Choice
- [x] Follow-up implementation stories created

## Spike Outcome

**Recommendation**: Apache Kafka

**Key Findings**:

1. **Performance**: Kafka 50,000 msg/s vs RabbitMQ 15,000 msg/s (our POC)
2. **Event Replay**: Kafka native support, RabbitMQ requires workarounds
3. **Operational Complexity**: Kafka higher (Zookeeper), but manageable with managed service
4. **Cost**: Kafka $800/month (AWS MSK), RabbitMQ $400/month (self-managed) - Kafka worth premium

**Pros (Kafka)**:

- Superior throughput and scalability
- Event replay built-in (analytics requirement)
- Strong ecosystem and community
- Industry standard for event streaming

**Cons (Kafka)**:

- Higher operational complexity
- Steeper learning curve
- Higher infrastructure cost

**Decision**: Choose Kafka based on:

- Performance headroom for 5-year growth (10× current volume)
- Event replay critical for analytics roadmap
- Managed service (AWS MSK) mitigates operational complexity
- Industry momentum (easier hiring, better tooling)

**Next Steps**:

- [x] ADR created and approved
- [ ] US-125: Set up Kafka cluster (AWS MSK) - 8 pts
- [ ] US-126: Implement event producer service - 5 pts
- [ ] US-127: Implement event consumer service - 5 pts
- [ ] TD-080: Migrate existing RabbitMQ events to Kafka - 13 pts
```

### Example 2: Performance Investigation Spike

```markdown
---
story_id: SP-020
story_type: spike
title: 'Investigate database performance bottleneck in reporting queries'
research_question: 'Why are monthly reports taking 45 seconds when requirement is <5 seconds?'
time_box: '8 hours'
expected_outcome: 'Root cause identified, optimisation recommendations'
decision_deadline: 2025-02-05
spike_outcome: 'Root cause: missing indexes. Recommendations implemented.'
priority: High
story_points: 0
status: Done
---

# Spike: Reporting Performance Investigation

## Time Box: 8 hours (1 day)

## Decision Deadline: 2025-02-05

## Research Question

Why do monthly revenue reports take 45 seconds to generate when requirement is <5 seconds?

- Is it database query performance?
- Is it data volume issue?
- Is it application code inefficiency?

## Success Criteria

Research identifies:

- [ ] Performance bottleneck (query, code, or infrastructure)
- [ ] Root cause with evidence (query plans, profiling data)
- [ ] Optimisation recommendations (quick wins + long-term)
- [ ] Estimated improvement from each recommendation

## Spike Outcome

**Root Cause**: Missing database indexes on report queries

**Investigation Findings**:

1. **Query Analysis**: Explain plan shows full table scans on 3M row table
2. **Missing Indexes**:
   - `transactions.created_at` (used in date range filter)
   - `transactions.customer_id` (used in aggregation)
   - `transactions.status` (used in WHERE clause)
3. **Query Optimisation**: Current query uses 3 subqueries (rewritable as JOINs)

**Performance Testing Results**:

- **Current**: 45 seconds average
- **With indexes**: 3.2 seconds (-93%)
- **With indexes + query rewrite**: 1.8 seconds (-96%)

**Recommendations**:

1. **Immediate** (TD-085, 2 pts): Add 3 missing indexes - 1 hour
2. **Short-term** (TD-086, 3 pts): Rewrite query to use JOINs - 2 hours
3. **Long-term** (US-150, 8 pts): Implement materialised view for common reports - 1 sprint

**Next Steps**:

- [x] TD-085: Add missing indexes (DONE - 1.5h actual)
- [ ] TD-086: Optimise report query structure
- [ ] US-150: Implement report caching with materialised views
```

### Example 3: Feasibility Spike (component evaluation context)

```markdown
---
story_id: SP-025
story_type: spike
title: 'Evaluate component library options for enterprise web interface'
research_question:
  'Which UI component library best supports theming, complex data tables, and accessibility
  requirements?'
time_box: '24 hours'
expected_outcome: 'Feasibility assessment, component library recommendation'
decision_deadline: 2025-03-01
spike_outcome: 'Selected library recommended. ADR created.'
priority: High
story_points: 0
status: Done
---

# Spike: UI Component Library Evaluation

## Time Box: 24 hours (3 days)

## Decision Deadline: 2025-03-01 (Sprint 2 planning)

## Research Question

Which UI component library best supports project requirements:

- Design token and theming compatibility
- Complex data table requirements (collapsible rows, column configuration)
- Autocomplete with advanced search patterns
- Accessibility (WCAG 2.1 AA compliance)
- Long-term maintainability with the chosen frontend stack

## Success Criteria

Research delivers:

- [ ] Evaluation of 2 candidate component libraries
- [ ] Theming feasibility for each
- [ ] Component coverage for project requirements
- [ ] Accessibility compliance assessment
- [ ] Architecture recommendation

## Project Context

- The project uses a defined design system or branding layer
- Users expect a consistent and accessible interface
- Complex data tables are core to the target workflows
- Existing UI patterns may need to be preserved or modernised

## Spike Outcome

**Recommendation**: Candidate library A with targeted theme customisation

**Feasibility**: YES - with theming effort

**Options Evaluated**:

1. **Candidate Library A**: ⚠️ POSSIBLE but challenging

   - Strong base components, but theming may conflict with the project's design approach
   - Limited support for advanced data-table interactions
   - Theming requires significant override effort
   - Good accessibility, but visual alignment is harder

2. **Candidate Library B**: ✅ RECOMMENDED
   - Better theming compatibility
   - Rich data table features (expandable rows, column toggles, filtering)
   - Strong support for advanced search and admin workflows
   - Active development and framework compatibility
   - WCAG 2.1 AA compliant components

**Component Coverage Analysis**:

| Requirement            | Candidate A      | Candidate B      |
| ---------------------- | ---------------- | ---------------- |
| Collapsible table rows | ⚠️ Custom build  | ✅ Native        |
| Column configuration   | ❌ Not available | ✅ Native        |
| Autocomplete           | ✅ Basic         | ✅ Rich features |
| Sticky save bar        | ✅ Toolbar       | ✅ Toolbar       |
| Design-system theming  | ⚠️ Difficult     | ✅ Compatible    |

**Cost Analysis**:

- Candidate A: Lower setup cost, higher adaptation effort
- Candidate B: Moderate setup cost, lower adaptation effort
- Recommendation: Candidate B reduces custom theming and wrapper effort

**Next Steps**:

- [x] ADR created: UI Component Library Decision
- [ ] US-175: Create project theme integration - 8 pts
- [ ] US-176: Implement core component wrappers - 13 pts
- [ ] US-177: Build project-specific table component - 8 pts
- [ ] TD-040: Document component library usage patterns - 3 pts
```

---

## Anti-Patterns

### ❌ Spikes Without Time Boxes

**Wrong**: "Research microservices architecture" (open-ended) **Right**: "16-hour spike: Evaluate 3
microservices frameworks"

### ❌ Implementation During Spike

**Wrong**: Building production-ready feature during spike **Right**: Proof-of-concept only,
implementation in follow-up US stories

### ❌ Spikes Without Documented Outcomes

**Wrong**: Spike completes, but no ADR or follow-up stories **Right**: Always document findings,
create ADR, spawn implementation stories

### ❌ Using Spikes to Avoid Estimation

**Wrong**: "Story too complex to estimate, make it a spike" **Right**: Spikes reduce uncertainty,
then estimate properly

---

## Spike Outcomes Must Document

1. Research findings and technical analysis
2. Recommendation with justification
3. Pros/cons comparison if evaluating alternatives
4. Follow-up implementation stories created
5. Architecture Decision Record (ADR) if significant decision

---

## Related Story Types

**SP outcomes spawn**:

- **US (User Stories)**: Implementation based on spike findings
- **EP (Epics)**: Large initiatives requiring spikes for planning
- **TD (Technical Debt)**: Technical issues discovered during research
- **SEC (Security)**: Security implications identified

**SP preceded by**:

- **EP (Epics)**: Epics often require spikes for uncertainty reduction

---

## Project Considerations

### Common Spike Topics

- **Legacy Integration**: How to interface with existing Java 11 backend
- **IAM Authentication**: SSO integration patterns with enterprise identity services
- **Data Migration**: Strategies for migrating from legacy interfaces or platforms
- **Performance**: API response time optimisation for complex queries
- **Component Selection**: UI library or shared component evaluation

### Technology Evaluation Criteria

- **Angular LTS Compatibility**: Must work with current Angular LTS
- **Design System Integration**: Compatibility with the project's theming and token system
- **Accessibility**: WCAG 2.1 AA compliance required
- **Maintainability**: Long-term support and community activity
- **Governance Standards**: Alignment with the client's or project's technology guidelines

### Spike Outcomes

- All spikes should produce ADR if architecture decision required
- Document findings in `/docs-copper/architecture/ADR/`
- Create follow-up implementation stories with clear acceptance criteria
- Consider impact on critical users, operations, and maintainers when evaluating options

---

## References

- **Story Type System**: See [story-types/README.md](README.md) for the complete type reference
- **Spike Research Dashboard**: `roadmap/dashboards/spike-research-board.md` (create when needed)
- **ADR Template**: `${CLAUDE_PLUGIN_ROOT}/skills/architecture-documentation/resources/adr-template.md` (owning
  skill) `cu:architecture-documentation` skill resource)
- **Related Types**: [US](US-user-story-guidance.md), [EP](EP-epic-guidance.md),
  [TD](TD-technical-debt-guidance.md)
- **Memory Bank**: `docs-copper/memory-bank/` for project context

---

_SP-spike-guidance.md | Version 1.2.0 | Last Updated: 2026-05-07 | COPPER Project Documentation_
