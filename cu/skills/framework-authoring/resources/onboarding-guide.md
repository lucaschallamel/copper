---
title: 'Onboarding Guide , Humans Using the Framework'
version: '1.0.1'
last_updated: '2026-10-18'
maintained_by: 'Lucas Challamel'
---

# Onboarding Guide , Humans Using the Framework

Guidance for human developers and team leads, moved out of the always-on `instructions.md` by US-378
(ADR-054): it describes how people adopt the framework, not how an agent behaves.

### For Human Developers

**First-Time Setup**:

1. Read `instructions.md` completely
2. Review Foundation Rules (00-03) in order
3. Scan Documentation & Architecture Rules (04-05) for awareness
4. Bookmark principle codes registry for quick reference

**Daily Usage**:

- Tag decisions with principle codes in: code comments, PR descriptions, ADRs, documentation
- Reference specific rules by number when needed (e.g., "per Rule 02 security mandates...")
- Use README.md files for human-readable guides (not part of agentic framework)

**Quality Gates** (from Rule 01 & 02):

- ≥80% unit test coverage | ≥70% integration test coverage
- All linters pass (Semgrep, MegaLinter) | Code review approval
- Documentation updated | Principle codes applied

### For Team Leads

**Onboarding**:

- Week 1: Instructions.md + Foundation Rules (00-03)
- Week 2: Documentation & Architecture Rules (04-05) + specific domain rules
- Ongoing: README files for development/testing workflows

**Quality Assurance**:

- Audit principle code usage in ADRs and code
- Review cross-reference compliance across rules
- Track metrics from Rule 02 quality standards

---
