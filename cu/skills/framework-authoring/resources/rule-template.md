---
rule_id: NN
title: '[Rule Name]'
description: '[One-sentence description of what this rule governs and its primary purpose]'
category: foundation
scope: '[WHO/WHAT/WHERE/HOW/WHY this rule applies - be specific about when this rule is activated]'
author: ''
version: 0.1.0
last_updated: YYYY-MM-DD
---

## Rule Overview

[Opening paragraph: 2-3 sentences explaining the purpose of this rule, what it governs, and why it's
important for the scaffold/project. Should clearly articulate the value proposition and scope.]

## [Optional: Project or Organisational Alignment]

<!-- Include this section if the rule has strong connection to project or organisational values -->

This rule embodies the project's or organisation's core values through [specific domain]:

- **[COM] Commitment**: [How this rule demonstrates commitment to excellence]
- **[RSP] Respect**: [How this rule shows respect for users/team/environment]
- **[SHR] Sharing**: [How this rule enables knowledge sharing and capability building]
- **[TSP] Team Spirit**: [How this rule supports team culture]
- **[OPT] Optimism**: [How this rule promotes positive outcomes]

**Sustainability**: [Optional: If applicable, explain alignment with sustainability standards]

**Cross-Reference**: Integrates with Rule 00 ([specific aspect]) and Rule 01 ([specific aspect]).

---

## Section 1: [Major Topic Area]

**[Subsection Title]**:

- **[PRINCIPLE] Principle Name**: [Detailed explanation of what this principle requires]

  - [Supporting detail or requirement]
  - [Additional context or guidance]
  - [Example or anti-pattern to avoid]

- **[PRINCIPLE] Second Principle**: [Explanation]
  - [Detail 1]
  - [Detail 2]

**[Second Subsection]**:

- Point 1 with principle tagging **[CODE]**
- Point 2 with cross-reference **[CODE]**
- Point 3 with specific guidance

**Cross-Reference**: [How this section relates to other rules or sections]

---

## Section 2: [Another Major Topic Area]

**Mandatory Requirements** (use this pattern for non-negotiable items):

- **[PRINCIPLE] Requirement Name**: Detailed requirement description
- **Validation Criteria**: How compliance will be verified
- **Exceptions**: Any allowed exceptions and approval process
- **Consequences**: What happens if this requirement is not met

**Best Practices** (use this pattern for recommendations):

- **[PRINCIPLE] Practice Name**: Description of recommended approach
- **Benefits**: Why this practice is valuable
- **Implementation Guidance**: How to implement this practice
- **Examples**: Concrete examples or code snippets

---

## Section 3: [Process or Workflow Section]

<!-- Use flowcharts or step-by-step processes when describing workflows -->

**[Process Name] Workflow**:

1. **[STEP 1 NAME]**: [Description with principle tags]

   - Sub-step A with **[CODE]** tagging
   - Sub-step B with validation criteria

2. **[STEP 2 NAME]**: [Description]

   - Requirements
   - Deliverables
   - Quality gates

3. **[STEP 3 NAME]**: [Description]
   - Inputs from previous step
   - Transformations or activities
   - Outputs and next steps

**Quality Gates**:

- Gate 1: [Criteria] → **[PRINCIPLE]**
- Gate 2: [Criteria] → **[PRINCIPLE]**

**Escalation Path**: [When to escalate and to whom]

---

## Section 4: [Standards or Conventions]

**Naming Conventions** (if applicable):

- **[ISA] Standard**: Use `snake_case` for [context]
- **[ISA] Standard**: Use `PascalCase` for [context]
- **[CMV] Constants**: All caps with underscores `CONSTANT_NAME`

**File Organisation** (if applicable):

```
directory-structure/
├── subdirectory-1/           # Purpose of this directory
│   ├── file-pattern-*.ext    # Naming pattern explanation
│   └── README.md             # Documentation requirement
│
└── subdirectory-2/           # Another organised section
    └── specific-file.ext     # Specific file purpose
```

**Configuration Management** (if applicable):

- **[ENV] Environment Variables**: [How to manage config]
- **[SF] Simplicity**: [Keep configuration simple and clear]
- **[SD] Documentation**: [Document all configuration options]

---

## Section 5: [Integration or Cross-Cutting Concerns]

**Integration with Other Rules**:

- **Rule 00**: [Specific integration point or dependency]
- **Rule 01**: [How this rule uses or depends on structure/governance]
- **Rule 02**: [How this relates to coding standards]
- **[Other Rules]**: [Additional cross-references as needed]

**Tool Integration**:

- **[Tool Name]**: [How this tool supports the rule]
- **Configuration**: [Where config lives, how to customise]
- **Automation**: [What can be automated]

**Team Responsibilities**:

- **[Role 1]**: [What this role is responsible for under this rule]
- **[Role 2]**: [Their specific obligations]
- **Shared**: [Collective team responsibilities]

---

## Validation & Compliance

**How to Verify Compliance**:

1. [Automated check or tool]
2. [Manual review process]
3. [Metric or measurement]

**Success Metrics**:

- **Metric 1**: [Target value] - [How to measure]
- **Metric 2**: [Target value] - [Measurement approach]

**Review Cycle**: [How often this rule should be reviewed - monthly/quarterly/annually]

**Feedback Mechanism**: [How team members can suggest improvements to this rule]

---

## Examples & Anti-Patterns

**Good Example** ✅:

```
[Code, configuration, or process example showing correct application of this rule]

Why this works:
- [Principle 1] **[CODE]**: [Explanation]
- [Principle 2] **[CODE]**: [Explanation]
```

**Anti-Pattern** ❌:

```
[Example of what NOT to do]

Why this fails:
- Violates **[CODE]**: [Explanation]
- Creates risk: [What could go wrong]
- Better approach: [Link to good example or alternative]
```

---

## Appendix: Principle Codes Quick Reference

<!-- Include this if the rule uses many principle codes -->

**Core Development**:

- [SF] Simplicity First | [RP] Readability Priority | [DM] Dependency Minimalism
- [ISA] Industry Standards | [SD] Strategic Documentation | [TDT] Test-Driven Thinking

**Quality & Architecture**:

- [DRY] Don't Repeat Yourself | [CA] Clean Architecture | [REH] Robust Error Handling
- [CSD] Code Smell Detection | [MOD] Modularity Focus | [ARC] Architecture Stability

**Security & Compliance**:

- [SFT] Security-First | [IV] Input Validation | [RM] Resource Management
- [RL] Rate Limiting | [RLS] Row Level Security | [SPO] Secure Prohibited Operations

**Organisational Values**:

- [COM] Commitment | [RSP] Respect | [SHR] Sharing
- [TSP] Team Spirit | [OPT] Optimism

---

_Rule maintained by [Project Team] | Version 0.1.0 | Last updated: YYYY-MM-DD_

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated rule.** **INSTRUCTIONS FOR
> COMPLETING THIS TEMPLATE**:
>
> 1. Replace all [placeholder text] with actual content
> 2. Remove principle codes from frontmatter that aren't used in this rule
> 3. Tag every decision/requirement with relevant principle code(s) using **[CODE]** format
> 4. Include cross-references to other rules where dependencies exist
> 5. Provide concrete examples for abstract concepts
> 6. Update version following semantic versioning (MAJOR.MINOR.PATCH)
> 7. Move status from "draft" to "active" after review and approval
> 8. Delete optional sections that don't apply to your rule
>
> **STATUS VALUES**:
>
> - `draft` - Rule is being created or refined
> - `active` - Rule is approved and in effect
> - `deprecated` - Rule is outdated but not yet removed
> - `archived` - Rule is no longer in use
>
> **CATEGORY VALUES**:
>
> - `foundation` - Core project/scaffold principles
> - `development` - Coding and implementation rules
> - `architecture` - Design and structural rules
> - `operations` - Deployment and runtime rules
> - `documentation` - Documentation standards
>
> **PRINCIPLE CODE USAGE**:
>
> - Only include codes you actually use in the rule content
> - Tag every requirement/decision with **[CODE]** inline
> - Group related codes in frontmatter with comments
> - Reference the Principle Codes Quick Reference section for full list

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated rule.**
>
> ```yaml
> template_name: 'Rule Template'
> template_description:
>   'Standardised template for creating project rules with comprehensive principle code tagging,
>   cross-references, and validation criteria'
> template_scope:
>   'Use for defining governance, technical, and operational rules across scaffold and project
>   contexts'
> template_version: '1.0.0'
> template_last_updated: '2025-10-26'
> template_status: 'active'
> template_category: 'governance'
> template_maintained_by: '[Project Team]'
>
> principle_codes_available:
>   core_development:
>     - SF # Simplicity First
>     - RP # Readability Priority
>     - DM # Dependency Minimalism
>     - ISA # Industry Standards Adherence
>     - SD # Strategic Documentation
>     - TDT # Test-Driven Thinking
>   quality_architecture:
>     - DRY # Don't Repeat Yourself
>     - CA # Clean Architecture
>     - REH # Robust Error Handling
>     - CSD # Code Smell Detection
>     - MOD # Modularity Focus
>     - ARC # Architecture Stability
>     - IMP # Impact Analysis
>     - PA # Performance Awareness
>   workflow_organization:
>     - ENV # Environment Awareness
>     - ORG # Organisational Clarity
>     - SCM # Script Management
>     - FOC # Focus on Relevant Code
>     - SCP # Scope Protection
>     - TST # Test Coverage
>     - AC # Atomic Changes
>     - CD # Commit Discipline
>   security_compliance:
>     - SFT # Security-First Thinking
>     - IV # Input Validation
>     - RM # Resource Management
>     - CMV # Constants Over Magic Values
>     - RL # Rate Limiting
>     - RLS # Row Level Security
>     - CAP # CAPTCHA Integration
>     - WAF # Web Application Firewall
>     - SPO # Secure Prohibited Operations
>     - QSR # Quarterly Security Review
>     - PKV # Package Verification
>     - DEH # Dependency Hygiene
>     - DCH # Dependency Change Documentation
>   ai_agent_communication:
>     - RAT # Rule Application Tracking
>     - TR # Transparent Reasoning
>     - EDC # Explanation Depth Control
>     - AS # Alternative Suggestions
>     - KBT # Knowledge Boundary Transparency
>     - CWM # Context Window Management
>   organisational_values:
>     - COM # Commitment
>     - RSP # Respect
>     - SHR # Sharing
>     - TSP # Team Spirit
>     - OPT # Optimism
>
> cross_references:
>   - 'User Story Template: user-story-template.md'
>   - 'ADR Template: (to be created)'
>   - 'Memory Bank: docs-copper/memory-bank/'
>
> applies_to:
>   - 'All team members involved in rule creation and governance'
>   - 'Technical leads and architects defining standards'
>   - 'Project managers establishing workflow rules'
>
> usage_pattern:
>   when_to_create_rule:
>     - 'Establishing new governance or technical standards'
>     - 'Codifying recurring decisions into reusable guidance'
>     - 'Preventing repeated anti-patterns or issues'
>     - 'Aligning team on quality, security, or architectural expectations'
>   rule_lifecycle:
>     - 'draft: Initial creation and refinement'
>     - 'active: Reviewed, approved, and enforced'
>     - 'deprecated: Phasing out, but not yet removed'
>     - 'archived: Historical record, no longer applicable'
> ```
