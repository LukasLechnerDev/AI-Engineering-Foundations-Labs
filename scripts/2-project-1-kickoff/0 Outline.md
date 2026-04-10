# Outline

## Learning goals
- Understand what `ai-engineer-job-digest` does and why it is a strong first portfolio project.
- Explain, that this is a AI Workflow or AI Pipeline and what's different to AI Agents
- Understand when a no-code tool is enough and when a custom Python app is the better choice.
- See the MVP path before the course adds optional tooling and deeper production topics.
- Understand where prompt work, evals, deployment, and later post-MVP modules fit into the build.

## Notes
- This module sets the course story for the rest of the project.
- The MVP path should stay simple: build the product, improve prompts, add local evals, ship it, then expand.
- Keep the no-code comparison lightweight and practical, not as a tool deep dive.
- Basic observability with Langfuse stays in the MVP path.
- Langfuse-based evaluation workflows come later, after the MVP is complete.

## Script
- Introduce the project and the end user value.
- Walk through the pipeline from raw job postings to the final digest output.
- Briefly compare no-code automation tools like `n8n` and `Zapier` with building a custom Python app.
- Explain that the course will build first and only add theory when the project needs it.
- Place the later modules on the timeline:
  - prompt engineering when output quality becomes the bottleneck
  - evaluations when we need evidence that prompt changes helped
  - observability with Langfuse when we want to inspect traces and failures in the working pipeline
  - deployment when the product is ready to ship
  - project recap once the MVP works end to end
  - productionizing when we want to harden the system after the MVP
  - evaluations with Langfuse when we want a later operational workflow on top of the local eval suite

## Sources
https://pro.academind.com/courses/ai-agents-workflows-the-practical-guide/lectures/62110718
