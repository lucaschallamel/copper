---
description: Generate technical documentation , API references, tutorials, README
  files, or a full documentation set, grounded in the gd-documentation-generator skill
  (Diataxis, Docs-as-Code, OpenAPI) with a bundled heading-extraction helper.
---

Generate documentation for: **$ARGUMENTS**

All arguments are optional. `doc_type` (default `comprehensive`; options: `api-reference`,
`tutorial`, `readme`, `architecture`, `user-guide`, `comprehensive`, `sdk-docs`); `audience_level`
(default `mixed`; options: `beginner`, `intermediate`, `expert`, `mixed`); `format_style` (default
`markdown`; options: `markdown`, `asciidoc`, `restructuredtext`, `html`, `pdf`, `interactive`);
`validation_level` (default `standard`; options: `basic`, `standard`, `strict`, `enterprise`,
`automated`); `content_strategy` (default `user-focused`; options: `user-focused`, `seo-optimized`,
`performance-driven`, `comprehensive`). With no arguments, ask what to document and for whom.

## Workflow

1. **Load the documentation knowledge** , Use the `gd-docs:documentation-generator` skill.
2. **Survey the existing structure** , run the bundled helper to ground generation in the real
   hierarchy before writing:
   ```bash
   python scripts/extract_headings.py < existing-doc-or-readme > .md
   ```
   Use the outline so new content fits the existing structure rather than an invented one.
3. **Plan with Diataxis** , map the `doc_type` to the right quadrant (tutorial, how-to, reference,
   explanation) and the `audience_level`, then outline the document set.
4. **Generate** , produce the documentation in `format_style`, applying the `content_strategy` and
   the skill's example-rich, progressive-disclosure style.
5. **Validate** , at the requested `validation_level`, check coverage, link integrity, and
   code-example accuracy per the skill's quality-assurance practice.

## Examples

```bash
# API reference for an intermediate developer audience
/gd-docs:documentation-generator doc_type=api-reference audience_level=intermediate

# Enterprise-grade validation of a documentation set
/gd-docs:documentation-generator validation_level=enterprise
```

## Opening (when no args)

"Let's create documentation that reduces support load and speeds onboarding. What are we documenting
, an API, a project README, a user guide , and who is the audience?"

---

- Skill: `gd-docs:documentation-generator` (owns the frameworks, the helper script, and the
  documentation knowledge)
- Helper: `scripts/extract_headings.py` (deterministic Markdown heading-outline extractor)
