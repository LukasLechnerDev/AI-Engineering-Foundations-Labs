# LangChain RAG Example: Jobs and Companies

A RAG agent built with LangChain Deep Agents, following the official
[RAG with Deep Agents tutorial](https://docs.langchain.com/oss/python/deepagents/rag).
Instead of LangChain's docs, it searches our job postings and company profiles
in `../knowledge-base/2026-09-24_0926/`.

## Setup

```bash
cd 9-rag/1-langchain-example
uv sync
cp .env.example .env   # then add your OPENAI_API_KEY
```

## Run

```bash
uv run agent.py
```

Change `EXAMPLE_QUERY` at the bottom of `agent.py` to ask your own question.
See `../0-good-questions.md` for ideas.
