# Project Guidance
This repository is a companion repository for the AI Engineering Fundamentals course.

## Core Goal
Everything in this repository should be optimized for students learning the material.

## MVP Release Priority
- Ship the first MVP of the course as fast as possible.
- Center the MVP around building the `ai-engineer-job-digest` project together with the student.
- Teach only the minimum theory students need to understand and complete the project.
- If a topic is not needed for the MVP, cut it or defer it to a later version of the course.
- Prefer practical project progress over broad or comprehensive theory coverage.
- Add deeper explanations only when they are clearly necessary for the current lesson.

## Development Principles
- Keep code short.
- Keep code readable.
- Keep code easy to understand.
- Prefer simple solutions over clever ones.
- Avoid unnecessary abstraction.
- Avoid unnecessary optimizations.
- Use straightforward variable names.
- Add comments only when they make the code easier for students to follow.

## Teaching Priority
When choosing between a more advanced solution and a simpler solution, prefer the simpler solution unless the advanced approach is clearly necessary for the lesson.

When choosing between broader theory coverage and faster progress toward the MVP, prefer faster progress toward the MVP.

## Course Context Workflow
- Whenever working on the structure of the course, module outlines, or individual lesson content, first read the whole course in `scripts/` to get full context before making changes.
- Do not make scope, sequencing, or lesson-placement decisions based only on the current file or module.
- Use the broader course context to avoid duplication, misplaced topics, and inconsistencies across modules.

## Environment Workflow
- Use `uv sync` to create or refresh the project environment when dependencies or the notebook kernel are missing.
- In notebooks, use the repo `.venv` as the Jupyter kernel.
- Preserve the existing project-output flow between lessons. If a notebook depends on files from an earlier step such as `jobs/1-scraped_jobs.jsonl`, keep that dependency explicit instead of hiding it.

## Notebook Priority
- Keep notebook cells focused and easy to scan.
- Prefer explicit code over compact but hard-to-read code.
- Minimize setup and boilerplate.
- Make outputs easy for students to interpret.

## Script and Outline Style
- Keep teaching goals in outline files very concise — drop "Students should learn how to" and similar prefixes. Write the goal itself, not a sentence about the goal.
- Instead of "Students should learn how to measure X", write "Measure X".
- Apply to all Teaching goal / Teaching goals sections in outline and lecture scripts.

## General Instructions 
- ALWAYS run `.venv/bin/ruff format` after you are done with your task to get the code style right, but only do this if you have added or modified python code.
- Make sure that all python code follows the current python best practices. Make use of mcp servers to fetch information about best practices. Always shout when you see code that doesn't follow best practises. 
