# Project Guidance
This repository is a companion repository for the AI Engineering Fundamentals course.

## Core Goal
Everything in this repository should be optimized for students learning the material.

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
- Whenever working on the structure of the course, module outlines, or individual lesson content, first read the whole course in `content/Course AIE Foundations/` to get full context before making changes.
- Do not make scope, sequencing, or lesson-placement decisions based only on the current file or module.
- Use the broader course context to avoid duplication, misplaced topics, and inconsistencies across modules.

## Notebook Priority
- Keep notebook cells focused and easy to scan.
- Prefer explicit code over compact but hard-to-read code.
- Minimize setup and boilerplate.
- Make outputs easy for students to interpret.

## Script and Outline Style
- All lecture and overview markdown files use this section structure, in this order:
  1. `## Learning goals` — concise bullets, no "Students should learn how to" prefix. Write the goal itself: "Measure X" not "Students should learn how to measure X".
  2. `## Notes` — background research, data, platform comparisons, or other supporting context, also very concise
  3. `## Script` — the actual lecture content.
  4. `## Sources` — links or references used to prepare the lecture (optional, omit if empty).
- Apply this structure to every lecture and overview file, including module outline files.

## General Instructions 
- ALWAYS run `.venv/bin/ruff format` after you are done with your task to get the code style right, but only do this if you have added or modified python code.
- Make sure that all python code follows the current python best practices. Make use of mcp servers to fetch information about best practices. Always shout when you see code that doesn't follow best practises. 
