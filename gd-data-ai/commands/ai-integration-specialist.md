---
description: Run an AI-integration design session , architect LLM, RAG, agent, or
  search systems with prompt optimisation and production guardrails, grounded in the
  gd-ai-integration-specialist skill.
---

Run an AI-integration design session for: **$ARGUMENTS**

All arguments are optional. `integration_type` (default `rag`; options: `chatbot`, `rag`, `agent`,
`search`, `generation`, `analysis`); `llm_provider` (default `openai`; options: `openai`,
`anthropic`, `google`, `azure`, `opensource`); `complexity` (default `standard`; options: `simple`,
`standard`, `advanced`, `enterprise`); `optimization_focus` (default `accuracy`; options:
`accuracy`, `speed`, `cost`, `scalability`). With no arguments, open by drawing out the use case,
the data sources, and the accuracy, latency, and cost constraints.

## Approach

1. **Load the AI-integration knowledge** , Use the `gd-data-ai:ai-integration-specialist` skill.
2. **Frame the problem** , clarify the use case behind `$ARGUMENTS`, the data sources, the expected
   query volume, and the non-functional requirements (accuracy, latency, cost, compliance).
3. **Design the integration** , apply the fitting patterns from the skill (RAG architecture, prompt
   templates, orchestration framework, vector store, and evaluation harness) to the chosen
   `integration_type` and `llm_provider`.
4. **Optimise and harden** , tune for the requested `optimization_focus`, add guardrails against
   hallucination and prompt-injection, define provider fallbacks, and instrument accuracy, latency,
   and cost.

## Opening (when no args)

"Let's design an AI integration that is accurate, fast, and cost-aware. What are you building, what
data does it draw on, and what accuracy, latency, and cost constraints must it respect?"

## Examples

```bash
# Enterprise RAG system on Anthropic
/gd-data-ai:ai-integration-specialist integration_type=rag llm_provider=anthropic complexity=enterprise

# Agent integration tuned for response speed
/gd-data-ai:ai-integration-specialist integration_type=agent optimization_focus=speed

# Chatbot on a self-hosted open-source model
/gd-data-ai:ai-integration-specialist integration_type=chatbot llm_provider=opensource
```

---

- Skill: `gd-data-ai:ai-integration-specialist` (owns the methodologies, patterns, and
  AI-integration knowledge)
- Related agent: the proactive `gd-data-ai:ai-integration-specialist` agent loads the same skill
  autonomously.
