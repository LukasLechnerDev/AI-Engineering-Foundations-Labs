# Outline

## Learning goals
- Structure a pipeline as composable, typed Nodes with explicit input/output types
- Replace manual JSON schema dicts with Pydantic models and `client.responses.parse()`
- Parallelize independent LLM calls using `asyncio` and `asyncio.gather()`
- Add resilient retry logic with `tenacity`
- Cache pipeline steps locally to avoid redundant API calls during development
- Track token usage and cost per step
- Replace `print()` with structured `logging`
- Validate configuration with `pydantic-settings`
- Unit test deterministic pipeline steps with `pytest` without hitting the API

## Notes
- Refactors the working MVP from a single script into professional-quality Python — same output, better code
- Keep every example grounded in the actual project, no abstract toy code
- The Nodes pattern intentionally mirrors the mental model used in agent frameworks (module 13)
- Pydantic structured output pairs with module 4 (interacting with model endpoints) — reference it
- Logging here is the foundation for Langfuse observability in module 7 — say so explicitly
- Testing deterministic nodes here sets up the evaluation mindset in module 6
- Do NOT cover model routing, fallbacks, or operational rate limit handling — those belong in module 11 (productionizing)
- Streaming and a Node protocol/base class are good stretch exercises if time allows

## Script
- Open with the problem: one long script, no types, no error handling, slow sequential API calls
- Introduce the Nodes pattern — each step becomes a typed function: `input type → output type`
  - `scrape(config) → list[ScrapedJob]`
  - `filter(list[ScrapedJob]) → list[ScrapedJob]`
  - `classify(list[ScrapedJob]) → list[ClassifiedJob]`
  - `enrich(list[ClassifiedJob]) → list[EnrichedJob]`
  - `match(list[EnrichedJob], UserProfile) → list[MatchedJob]`
  - `main()` becomes a clean pipeline of node calls
- Introduce Pydantic models as the contract between nodes (`ScrapedJob`, `ClassifiedJob`, etc.)
- Show how Pydantic replaces manual schema dicts: define a `BaseModel`, pass it to `client.responses.parse()`, get a typed object back — no `json.loads()`, no schema boilerplate
- Refactor the classify, enrich, and match loops to async using `AsyncOpenAI`
- Show `asyncio.gather()` running all jobs in parallel — run the timer, show the speedup
- Add `asyncio.Semaphore` to cap concurrent requests and respect rate limits
- Add a `@retry` decorator from `tenacity` to each async node — exponential backoff, show a failed call recovering
- Add a simple JSONL file cache: skip scraping and classifying if a recent cache exists, load from disk instead — makes dev iteration fast
- Add `pydantic-settings` to replace the hardcoded `USER_SKILLS` dict and scraping params with a validated `AppConfig` loaded from `.env`
- Replace all `print()` calls with `logging` — set log levels, show how to silence verbose output in tests
- Write `pytest` unit tests for `score_skill_match` and the filter logic — fast, no API calls, deterministic
- Run the refactored pipeline end-to-end: same digest output, professional codebase
