# Size-budget evidence , the measured corpus behind the concision rule

Reference for `kit-authoring/SKILL.md`'s concision budget. Split out under US-357 because it is
consulted when AUTHORING an asset, not needed on every load , and because leaving it inline pushed
`SKILL.md` to twice the budget it sets, which would have been the standard failing its own rule.

### Concision , measured house sizes (US-357 corrected)

**Measured across every shipped kit, 2026-09-06** (`wc -l` over `kits/*/skills/*/SKILL.md` and
`kits/*/agents/*.md`, excluding `kits/core/`):

| corpus | n   | min | **median** | mean | max      |
| ------ | --- | --- | ---------- | ---- | -------- |
| skills | 155 | 57  | **131**    | 139  | **651**  |
| agents | 61  | 63  | **69**     | 213  | **1145** |

**Budget: skills ~130 lines, agents ~70 , anchored on the MEDIAN.** The mean is not usable for
agents: one 1,145-line asset drags it to 213, three times the median.

**These numbers replace an earlier figure that was a survivorship sample.** The original ("skills
99-138, n=92; agents ~68, n=14") measured only the `qd-*` and `gd-*` families , the corner of the
corpus that already complies , and presented it as the house standard. The medians survived
re-measurement; the ranges were understated 3-6x and the sample sizes by 4x.

The `qd-*` corpus (92 skills, 93-193 lines, one concern each) remains the **reference partition** ,
the tidy end of the distribution and a legitimate target , but it is not the whole house.

**Existing debt, stated in BOTH scopes because mixing them is how the last figure went wrong:**

| scope                                            | assets over 200 lines |
| ------------------------------------------------ | --------------------- |
| excluding `kits/core/` (matches the table above) | **24 of 216**         |
| all kits including core                          | **38 of 235**         |

The table above excludes core, so **24 of 216** is the figure that belongs beside it. An earlier
draft said "37 of 235" , wrong in value (this story's own edits pushed `kit-authoring/SKILL.md` from
152 to 231 lines, making it one more) and wrong in scope (a core-inclusive denominator sitting under
a core-excluding table). Both errors are recorded rather than quietly corrected: a standard that
mixes scopes in one paragraph is doing the thing it warns against.

That debt is named rather than pretended away. Exceeding the budget is permitted with a recorded
justification: it is a review trigger, not a cap. A cap would fail 37 assets on day one, and a
standard the corpus cannot meet is ignored within one story.

**Re-measure, do not trust.** These figures age as the corpus grows. The command and date are given
above so the next author re-runs them instead of inheriting a stale number , which is exactly how
the survivorship sample propagated.

### Worked example , a justified exceedance

`check-personal-data.py` (US-352) is **~730 lines with 8 exemption surfaces** (673 when first
measured at US-352's S7; **re-run `wc -l` rather than trusting this** , the drift between those two
numbers is itself the Currency rule demonstrating why), five times the median and flagged at its own
S7 review as a `[CA]`/`[SF]` WARN. It ships anyway, and this standard says why that is acceptable:

- Each exemption surface was added by a NAMED review finding, and each carries its rationale in
  place , the file records why it is large.
- The alternatives were considered and rejected on the merits: splitting it would put the
  fail-closed posture in one file and the exemptions in another, where they drift.
- A RULE MATRIX in its docstring gives a reader the whole picture without reading 600 lines.

**The justification is the deliverable, not the exceedance.** An asset over budget with a recorded
reason is compliant; an asset over budget with none is not , regardless of size. A standard whose
author exempts their own most recent work is worthless, which is why the example is drawn from it.

---

## Reference counts (dated , re-measure before relying)

Measured 2026-09-07. These live here rather than in `SKILL.md` because an asserted count in an
always-loaded body is what the Currency rule forbids.

- `qd-coaches` + `qd-masters` + `qd-smes`: **92 skills, 0 agents** , the zero-agent precedent.
- Assets over 200 lines: **24 of 216** excluding `kits/core/`; **38 of 235** including it.
- The anti-pattern agent (`asl-coach-tutor`, vault source): 1,212 lines, ~800 of them reference
  knowledge resident on every invocation.

---

## Worked coverage table (S5 G4)

The MECE rule asks each kit to map every capability to exactly one owning skill. **No shipped kit
carries such a table yet** (measured: 0 of 24), so here is one, retrofitted to a real multi-skill
kit so an author has something to copy rather than a blank page.

**Where it lives**: in the kit's own `README.md`, or in the `kit.md` body beneath the entity
sections. NOT in `kit.md` frontmatter , `kits/SPEC.md` s.5.4 freezes that contract, and a coverage
table is documentation about the kit, not part of its manifest.

### Example , `gd-quality` (4 skills)

| Capability , the thing an agent needs to know                       | Owning skill                |
| ------------------------------------------------------------------- | --------------------------- |
| Is this requirement well-formed, unambiguous, verifiable?           | `gd-quality:requirements-validator` |
| What quality strategy and gates should this project run?            | `gd-quality:qa-coordinator`         |
| How do I write the tests themselves , pyramid, TDD/BDD, frameworks? | `gd-quality:test-suite-generator`   |
| Has the business validated this against real process and personas?  | `gd-quality:uat-coordinator`        |

**Applying the behavioural test** , for each row, name the single skill that must load. If two
answers are defensible, the partition is wrong:

- _"Write a test for this endpoint"_ -> `test-suite-generator`, unambiguously. Not `qa-coordinator`,
  which decides WHAT to test, not how to write it.
- _"Is this acceptance criterion testable?"_ -> `requirements-validator`. Tempting to reach for
  `uat-coordinator`, but UAT validates against BUSINESS process after the fact; this is a property
  of the requirement text itself. **Two defensible answers would mean the boundary needs restating,
  not that the table needs a second owner.**

**What a FAILING table looks like**: two rows resolving to the same skill (merge them , they are one
capability), or a capability the kit's `includes` claims with no owning skill (a gap , the agent
proceeds unaware, which the standard calls worse than overlap).

**Deriving the rows**: take `includes.skills` and each skill's `description`; one row per distinct
thing a skill claims to do. `kit.md`'s one-line `summary` does not enumerate capabilities and is not
the input.
