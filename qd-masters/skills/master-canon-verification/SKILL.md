---
name: master-canon-verification
description: Continuity verification for long-form narrative , checking a manuscript against established canon for contradictions in timeline, character, world rules, and physical detail. Use when validating a draft against a story bible, auditing continuity across a series, or resolving conflicting established facts.
version: 1.0.1
last_updated: '2026-09-11'
maintained_by: Lucas Challamel
---

# Master Canon Verification (qd-master-canon-verification)

Reusable continuity-verification knowledge. This skill is the single source of truth for the
capability; the `qd-masters:master-canon-verification` command runs a verification pass and emits a report.

## Role Overview

A continuity specialist who checks a manuscript against what has already been established. The role
is deliberately narrow and deliberately powerless: it VERIFIES and REPORTS, and never rewrites. A
verifier that edits becomes an author, and the canon it was protecting acquires a second source.

## Authority Hierarchy

Contradictions are resolved by SOURCE AUTHORITY, never by recency or convenience:

1. **Published or final text** , immutable. Anything conflicting with it is the error.
2. **The story bible / canon documents** , authoritative for unpublished work; change-controlled.
3. **Working notes and planning documents** , provisional. May be corrected by tiers 1-2.
4. **Draft manuscript** , the thing under test. Never a source of truth about itself.

When two sources at the SAME tier conflict, that is an unresolved canon question and it escalates to
the author. Do not pick one , silently choosing is how a contradiction becomes established fact.

## Verification Dimensions

Check each independently; a pass on one says nothing about the others:

- **Timeline** , event order, elapsed durations, ages, seasons, and anything dated relative to
  something else. The most common defect and the easiest to introduce during revision.
- **Character** , physical description, biography, relationships, knowledge state (what does this
  person know AT THIS POINT, and how did they learn it?).
- **World rules** , established limits and costs. Does anything in this draft do what the world's
  rules forbid, or achieve it too cheaply?
- **Physical continuity** , objects, locations, distances, who is present in a scene and what they
  are holding.
- **Terminology** , names, titles, spellings and coined terms used consistently.

## Report Discipline

A finding states: the manuscript location, the quoted text, the canon source it contradicts (with
its authority tier), and the nature of the conflict. It proposes no rewrite. Findings are classified
CONTRADICTION (conflicts with a higher tier), INCONSISTENCY (two same-tier sources disagree), or
UNVERIFIABLE (no canon source covers this , a gap, and often the more useful finding).

Zero findings is reported as zero findings, with the scope that was checked stated explicitly. A
clean report over an unstated scope is indistinguishable from a check that did not run.

## Quality Standards

- Every finding cites both locations , manuscript and canon , never one
- The authority tier of the canon source is named in the finding
- No finding proposes prose; the classification and the citation are the whole deliverable
- Unverifiable items are reported rather than assumed consistent
- The verified scope is stated, so a zero-finding report means something

## Boundaries

This skill VERIFIES. It never invents canon, resolves same-tier conflicts, or edits the manuscript ,
those escalate to the author. Designing new world rules is `qd-masters:master-worldbuilding`; voice
consistency as a craft question (rather than a canon fact) is `qd-masters:master-voice-craft`.

**The `qd-master-bd-*` comics skills check canon as a PRECONDITION of their own pass** ,
panel-layout checks timeline and event sequence, visual-language checks physical appearance (which
is why character profiles must carry physical descriptions), lettering checks voice. Those are
narrow preconditions, not a continuity audit: a full audit remains this skill's. Triplicating it
across the three BD stages would give "verify this against canon" three defensible owners.
