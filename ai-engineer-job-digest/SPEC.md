# Portfolio Project 1: AI Engineer Job Digest (Email-First)

## Summary
A scheduled batch job that scrapes AI Engineer postings from the last 24 hours, classifies and enriches them with LLMs, matches them against a fixed user profile, runs evals, logs to Langfuse, and emails a ranked digest.

## Skills Demonstrated
- OpenAI API in a real pipeline (structured outputs, task-specific models, one tool call)
- Prompt engineering for classification, enrichment, matching, and digest writing
- Evaluations: deterministic, gold-set, and LLM-as-a-judge
- Observability with Langfuse (traces, prompt versions, latency, cost)
- Docker + AWS deployment, light CI
- Product thinking: ranking jobs and surfacing skill gaps

## Pipeline
1. Scrape postings from existing sources (last 24h)
2. Deterministic cleanup: title filter, required fields, dedup, timestamp filter
3. Classify AI vs not-AI; route low-confidence to manual review or fallback model
4. Enrich: summary, benefits/highlights, required skills, seniority
5. Match against user profile via a `score_skill_match(...)` tool call, then write fit explanation and skill-gap notes
6. Render ranked digest (HTML + text)
7. Run evals; gate the send on critical thresholds
8. Save artifacts to S3; send email if gate passes

## Storage
- S3: raw scrapes, curated JSON, rendered emails, eval reports
- Env/config: recipient(s), user profile, API keys
- No database in v1

## Key Types
`ScrapedJob` → `ClassifiedJob` (+ decision, reason, confidence) → `EnrichedJob` (+ summary, highlights, skills, seniority) → `MatchedJob` (+ fit score, reason, gaps). Plus `UserProfileConfig`, `SkillMatchResult` (tool output), `DigestArtifact`, `EvalReport`.

## OpenAI Usage
Use the OpenAI SDK directly (no LangChain). Demonstrate:
- Structured outputs for classification and enrichment
- Separate `instructions` and `input`
- Task-specific model choice
- Prompt versioning and A/B comparison
- One tool call: `score_skill_match(required_skills, user_profile, seniority, prefs) → { score, matched, missing, seniority_fit, notes }`. Deterministic Python logic — no nested model call. The model uses the result to write the fit explanation, skill-gap section, and personalized summary line.

## Evaluations
Eval is a headline feature.

- **Deterministic:** 24h scrape window, dedup, schema parsing, seniority normalization, tool scoring stability, rendering
- **Gold-set:** labeled classification set; small labeled set for seniority/skill extraction
- **LLM-as-a-judge:** summary faithfulness, highlights usefulness, fit explanation, "what to learn next", overall digest quality, prompt A/B on one core stage
- **Operational:** latency, token cost, failure rate, version comparison over time
- **Send gate:** block send on critical failures; always save the failed digest + report

## Langfuse
Trace every OpenAI call, log prompt versions/latency/cost, attach eval scores.

## Teaching Flow
Build product-first; insert theory when it becomes necessary.

1. Define product and daily workflow
2. Reuse scraping/classification from `1-introduction`
3. Notebook → Python modules + CLI
4. Add enrichment prompts
5. Add matching and ranking
6. Render HTML/text digest
7. Eval datasets and baselines
8. LLM-judge + send gate
9. Langfuse instrumentation
10. Dockerize
11. Schedule on AWS

Theory attaches to implementation: LLMs at classification, OpenAI API at structured outputs, prompt engineering at quality bottlenecks, tool calling at matching, evals when prompts start changing, observability when debugging, deployment after local works.

## Deployment & CI
- Docker → ECS Fargate scheduled task → EventBridge schedule
- S3 artifacts, Resend for email, Secrets Manager for keys
- Local: run with fixed config, preview HTML, dry-run mode
- CI: lint, unit tests, Docker build, one smoke test with mocked services
- No CD in v1 — deploy manually

## Test Scenarios
No jobs in 24h; many false positives; malformed descriptions; duplicates; low fit score with clear gaps; tool and model explanation agree; low-quality enrichment fails the gate; successful send; dry-run.

## Acceptance Criteria
- Student can run pipeline end-to-end locally
- One useful digest email sent to fixed recipient
- All OpenAI calls visible in Langfuse
- Eval results saved and visible
- Container runs on AWS on schedule

## Assumptions & Defaults
- v1 is email-only, fixed recipient list, no auth/unsubscribe/DB
- No LangChain, RAG, agents, or PyTorch
- S3 is the only persistent storage
- Resend over SES (less setup)
- Stretch: multiple recipient profiles, preview page, salary extraction, manual rerun endpoint

## Notes
Consider framing the user profile around source roles (ML Engineer, Data Scientist, Backend/Frontend Dev) and what each needs to learn to become an AI Engineer.
