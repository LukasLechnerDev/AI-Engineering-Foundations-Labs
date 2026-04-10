# Outline

## Teaching goals
- Measure whether the AI system is actually working before shipping it.
- Add a safety net to the project, not academic benchmarking.

## Where this fits
- Students have already improved their prompts in the previous module.
- The question now is: "How do I know my prompts still work after I change them?"
- Evals answer that question systematically instead of relying on manual spot-checking.

## What to cover
1. Why evals matter — the cost of finding failures late vs. early
2. What makes a good eval: representative inputs, clear expected outputs, a pass/fail signal
3. Three levels of evals and when to use each:
   - Deterministic checks (exact match, regex, schema validation)
   - Heuristic checks (word count, structure, keyword presence)
   - Model-graded checks (LLM-as-judge for open-ended outputs)
4. Building a small eval set from real project outputs
5. Writing and running evals against the `ai-engineer-job-digest` pipeline
6. Interpreting results and deciding when something is good enough to ship

## Project fit
- Anchor the module on the classification and extraction steps in the project.
- Start with deterministic checks (does the output match the expected label?).
- Add a model-graded check for the summary quality.
- The goal is a runnable eval script students can reuse as the project evolves.

## Keep out of this module
- eval frameworks and platforms (LangSmith evals, Braintrust, etc.)
- statistical significance and large-scale benchmarking
- fine-tuning and dataset curation
- A/B testing in production
