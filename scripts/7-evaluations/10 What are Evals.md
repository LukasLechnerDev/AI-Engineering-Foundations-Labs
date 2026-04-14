# What are evals

## Learning Goals
- 

## Notes
- We created our first real AI-based app
- How do we know if it works correctly?
- How do we know that the classification that the app is according to our ideas / definitions
- How can we "measure" if a change of a prompt is good or bad?
- Should we use a more powerful model to get better results?
- Can we use a cheaper model that has a similar accuracy at less costs and more speed?
- is the "reason" toned in a way we like it to be? Is the tone of voice on point?
- Evals answer that question systematically instead of relying on manual spot-checking or vibe checks.
- Evaluation is the cornerstone of building reliable LLM applications.
- Evals are all about assigning metrics to quantify the quality of our prompt + model combination.

Yes, this is exactly what an eval is! You have a labeled dataset (101 jobs with known is_ai_engineering_role ground truth) and you want to run the real model against it to measure how well your prompt + model combination performs. Swapping the model or tweaking the prompt and re-running lets you compare quality — that's the eval loop.

Let me update the plan to reflect this approach.

## Script

## Sources
- 