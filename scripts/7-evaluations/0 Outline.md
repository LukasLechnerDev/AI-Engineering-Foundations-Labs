# Outline

## Learning goals
- Measure whether the AI system is actually working before shipping it.
- Add a safety net to the project, not academic benchmarking.
- Understand three practical evaluation levels:
  - deterministic checks / code based grading
  - human-annotated data / human based grading
  - LLM as a judge / model grading
- Components of an Eval
   - Input
   - Golden Answer (defined by a human or generated synthetically)
   - Model Output
   - Score
Synthetic Test Set Generation
online vs offline evaluations
when to execute evals - guardrails, retries, ...

## Notes
- Students have already improved their prompts in the previous module.
- The question now is: "How do I know my prompts still work after I change them?"
- Evals answer that question systematically instead of relying on manual spot-checking or vibe checks.
- Anchor the module on the classification and extraction steps in the project.
- Start with deterministic checks (does the output match the expected label?).
- Add a model-graded / LLM as a judge check for the summary quality.
- The goal is a runnable eval script students can reuse as the project evolves.
- Keep out: eval frameworks and platforms (Langfuse, LangSmith, Braintrust, and similar tools), statistical significance, large-scale benchmarking, fine-tuning, dataset curation, and A/B testing in production.
- Langfuse-based eval inspection belongs later, after students already have local evals running in code.
- How can the OpenAI API help with evals?

## Questions that Evals can answer
- "Which LLM is the best choice for our needs?"
- "Can we achieve high performance without excessive costs?"


## Script
1. Why evals matter: the cost of finding failures late vs. early
2. What makes a good eval: representative inputs, clear expected outputs, and a pass/fail signal
3. Three levels of evals and when to use each:
   - Deterministic checks (exact match, regex, schema validation)
   - Heuristic checks (word count, structure, keyword presence)
   - Model-graded checks (LLM-as-judge for open-ended outputs)
4. Building a small eval set from real project outputs
5. Writing and running evals against the `ai-engineer-job-digest` pipeline
6. Interpreting results and deciding when something is good enough to ship
7. Clarify the boundary: local eval code is part of the MVP, while Langfuse-based eval workflows come later

Evals are all about assigning metrics to quantify the quality of our prompt + model combination.
with promptfoo we can define multiple prompts, models, etc. and have a nice dashboard to analyze the results of our evals
We have a nice overview of model+prompt combinations and their eval scores

## AI as a judge
- use the most powerful model you can afford
- but the AIE book also mentions that cheaper/faster models can be used as judges

## Sources
- https://app.datalumina.academy/c/genai-accelerator/sections/578161/lessons/2306553
- Anthropic prompt evaluation course: https://github.com/anthropics/courses
- OpenAI on Evals: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Langfuse on Evals: https://langfuse.com/docs/evaluation/core-concepts
- https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app
- https://hamel.dev/notes/llm/evals/flashcards/?ajs_uid=900710
- https://hamel.dev/blog/posts/evals-faq/evals-faq.pdf?ajs_uid=900710
- https://hamel.dev/blog/posts/evals-faq/
