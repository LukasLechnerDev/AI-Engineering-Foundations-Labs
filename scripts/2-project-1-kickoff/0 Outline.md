# Outline

## Learning goals
- Present what we are going to build with `ai-engineer-job-digest` 
- why it is a strong first portfolio project => which skills it demonstrates
- email => so no frontend experience necessary
- Explain, that this is a AI Workflow or AI Pipeline and what's different to AI Agents
- Understand when a no-code tool like n8n is enough and when a custom Python app is the better choice.

## Storyline
- first lecture presents what we are going to build for the MVP
- from notebook to python file: Create first version of pipeline
  - that does SCRAPING - FILTERING - CLASSIFICATION - HTML RENDER
- basically just the code that we have written in the notebooks
- then extend with enriching and skill matching
- then the user already has the first nice project early in the course

Next steps: 
- Now that we have our first nice project finished, at least one that we can trigger locally, its time for the next 2 modules to talk about how LLMs work in general, and then some more information about how we can interact with the openAI api and prompt engineering
- later we will come back to the project and talk about how we can make it more professional / improve the architecture / add pydantic for Structured Output to not have everything in a big main file
- later we will also add evaluations, monitoring and deploy it so that we get daily emails automatically

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
