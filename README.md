# AI Engineering Foundations — Labs

Companion code for the **AI Engineering Foundations** course. You'll build an
`ai-engineer-job-digest`: a small app that scrapes AI engineering job postings,
classifies and summarizes them with an LLM, and emails you a digest.

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Create the environment:
   ```bash
   uv sync
   ```
3. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```
4. Verify the setup:
   ```bash
   uv run python 1-what-is-ai-engineering/0-uv-check.py
   ```

In notebooks, select the repo `.venv` as the Jupyter kernel.

## Modules

- `1-what-is-ai-engineering/` — first LLM calls, scraping and classifying jobs.
- `2-first-portfolio-project/` — from notebook to a structured project.
- `3-interacting-with-llm-apis/` — model parameters, prompting, structured
  output, and analyzing images and files.

## Requirements

- Python 3.12+
- An OpenAI API key (see `.env.example` for all supported variables)
