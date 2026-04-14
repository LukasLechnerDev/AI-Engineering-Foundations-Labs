# Outline

## Learning goals
- What are evals?
- Why evals are important
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
- Go through Langfuse traces and search for errors
- Anchor the module on the classification and extraction steps in the project.
- Start with deterministic checks (is the classification right?).
- Add a model-graded / LLM as a judge check for the summary quality or reason string.
- Keep out: eval frameworks and platforms (Langfuse, LangSmith, Braintrust, and similar tools), statistical significance, large-scale benchmarking, fine-tuning, dataset curation, and A/B testing in production.
- Langfuse-based eval inspection belongs later, after students already have local evals running in code.
- How can the OpenAI API help with evals?


## Script
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
