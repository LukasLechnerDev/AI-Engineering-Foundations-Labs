# Portfolio Project 1: AI Engineer Job Digest (Email-First)

## Summary
Build a scheduled AI job digest system that scrapes fresh AI Engineer jobs from the last 24 hours, filters out false positives with LLM classification, enriches the accepted jobs, matches them against a fixed user skill profile, evaluates output quality, logs everything to Langfuse, and sends a polished email digest.

This keeps the teaching focus on AI engineering:
- OpenAI API usage in a real pipeline
- prompt engineering tied to visible product quality
- evaluations, including LLM-as-a-judge
- observability with Langfuse
- Dockerized deployment to AWS
- light CI without turning the course into a DevOps course

## Skills Demonstrated
- Python for scraping, data processing, pipeline orchestration, testing, and CLI code
- OpenAI API usage beyond a single basic prompt
- prompt engineering for classification, enrichment, matching, and digest writing
- structured outputs and schema-driven LLM integration
- LLM evaluations, including gold-set metrics and LLM-as-a-judge
- observability with Langfuse traces, prompt versions, latency, and cost
- deterministic software engineering around retries, validation, and failure handling
- AWS deployment and cloud storage
- Docker containerization
- light CI for linting, tests, and smoke checks
- product thinking: ranking jobs for a user and surfacing skill gaps

Optional advanced skills if time remains:
- prompt A/B testing and regression analysis
- tool calling with deterministic helper functions
- human-in-the-loop review for low-confidence cases
- cost and latency optimization across pipeline stages

## Product And Architecture
The product is a scheduled batch job, not a frontend app.

Pipeline steps:
- Scrape job postings from the last 24 hours from the existing job sources.
- Apply deterministic cleanup: title filter, required-field checks, deduplication, timestamp filter.
- Classify each role as true AI engineering vs not AI engineering.
- Enrich accepted jobs with:
  - short role summary
  - benefits/perks/highlights
  - seniority level
  - required skills
- Compare each job against a fixed user skill profile from config.
- Include one controlled tool-calling step in the matching stage so the model can call a deterministic helper like `score_skill_match(...)` before writing the fit explanation.
- Generate:
  - a ranked digest of the best-fit jobs
  - a concise "what you still need to learn" section
  - HTML and plain-text email versions
- Run evaluations before sending.
- Send the digest only if the eval gate passes.
- Save artifacts to S3.

Minimal storage design:
- `S3` for raw scrape snapshots, curated job JSON, rendered email HTML/text, and eval reports
- environment variables / config for:
  - recipient email(s)
  - user skill profile
  - OpenAI, Langfuse, and email-provider keys
- no database in `v1`

Important interfaces and types:
- `ScrapedJob`: raw posting data
- `ClassifiedJob`: `ScrapedJob` plus AI-engineering decision and reason
- `EnrichedJob`: `ClassifiedJob` plus summary, highlights, benefits, seniority, extracted skills
- `UserProfileConfig`: skills, interests, preferred seniority, optional exclusions
- `MatchedJob`: `EnrichedJob` plus fit score, fit reason, skill gaps
- `SkillMatchResult`: deterministic tool output with overlap score, matched skills, missing skills, seniority fit, and rule-based notes
- `DigestArtifact`: ranked jobs, intro copy, closing copy, HTML/text render
- `EvalReport`: deterministic metrics, judge scores, send/no-send decision

## OpenAI, Prompts, And Evals
Use the OpenAI SDK directly, not LangChain, so students learn the core API first.

OpenAI API usage should intentionally demonstrate:
- structured outputs for classification and enrichment
- separate `instructions` and `input`
- task-specific model choice instead of one default model
- prompt versioning and prompt A/B comparison
- explicit output schemas for reliable downstream code
- different response styles for extraction vs final digest writing
- one controlled tool-calling example for deterministic skill-match scoring before natural-language explanation

Tool-calling example:
- Use tool calling in the matching stage, not in scraping or classification.
- Expose one deterministic helper function, for example `score_skill_match(...)`.
- Inputs to the tool:
  - extracted required skills for the job
  - normalized user skill profile
  - extracted seniority level
  - optional user preferences like remote-only or seniority target
- Outputs from the tool:
  - numeric fit score
  - matched skills
  - missing skills
  - seniority fit or mismatch
  - short rule-based notes that explain the score
- The tool should contain transparent, testable scoring logic rather than another model call.
- After the tool returns, the model uses the tool output to write:
  - the fit explanation
  - the "what you still need to learn" section
  - a short personalized summary line for the digest
- This keeps the deterministic part of the system in Python while still demonstrating how models can orchestrate software tools.

Evaluation should be a headline feature of the project.

Deterministic evals:
- scrape window really is last 24 hours
- duplicate removal works
- schema parsing never silently fails
- seniority normalization is stable
- tool-call scoring is stable and produces expected outputs for representative skill profiles
- ranking and email rendering succeed with representative inputs

Gold-set evals:
- labeled classification set for true AI engineering vs false positives
- small labeled set for seniority and skill extraction sanity checks

LLM-as-a-judge evals:
- summary faithfulness to the posting
- usefulness of benefits/highlights
- quality of fit explanation
- usefulness of "what to learn next"
- overall digest usefulness for a job-seeking AI engineer
- prompt A vs prompt B comparisons for at least one core stage like classification or job summary generation

Operational evals:
- latency per step
- token/cost per step
- failure rate per step
- prompt/model version comparison over time

Send gate:
- do not send the email if critical eval thresholds fail
- always save the failed digest and eval report to S3 for inspection

Langfuse usage:
- trace every OpenAI call
- log prompt versions, latency, and cost
- attach eval scores to runs
- make failures reviewable after deployment

## Teaching Flow
Teach this by building the product first and inserting theory exactly when it becomes necessary.

Suggested sequence:
1. Define the product and the daily digest workflow.
2. Reuse the existing scraping and classification ideas from `1-introduction`.
3. Turn the notebook logic into small Python modules and a CLI entrypoint.
4. Add enrichment prompts for summaries, perks, seniority, and skill extraction.
5. Add skill-profile matching and ranking.
6. Add digest rendering to HTML and text.
7. Introduce evaluation datasets and baseline metrics.
8. Add LLM-as-a-judge and the send gate.
9. Add Langfuse instrumentation.
10. Dockerize the job.
11. Deploy the scheduled container on AWS.

Theory lessons should be attached to implementation moments:
- "How LLMs work" when classification first appears
- "How the OpenAI API works" when structured outputs are introduced
- "Prompt engineering" when output quality becomes the bottleneck
- "Tool calling" when the model first combines deterministic match scoring with natural-language reasoning
- "Evaluations" when prompts start changing
- "Observability" when the system needs debugging and comparison
- "Deployment" after the local pipeline already works

## Deployment And CI
Recommended deployment shape:
- Docker container for the batch job
- `ECS Fargate` scheduled task
- `EventBridge` schedule
- `S3` artifact bucket
- `Resend` for email sending
- `Secrets Manager` or ECS task secrets for API keys

Local developer workflow:
- run pipeline locally with a fixed config
- preview HTML email locally before any send
- support a dry-run mode that skips real email sending

CI scope should stay light:
- lint
- unit tests
- Docker build
- one small pipeline smoke test with mocked external services

No full CD in `v1`.
Deploy manually so the infrastructure story stays short and understandable.

## Test Plan
Core scenarios:
- no jobs found in the last 24 hours
- mixed scrape with many false positives
- malformed or incomplete descriptions
- duplicate postings across sources
- tool returns a low fit score with clear missing-skill guidance
- tool and model explanation agree on the core reasons for the match score
- low-quality enrichment output that should fail the send gate
- successful digest generation and send
- dry-run execution that stores artifacts but skips email

Acceptance criteria:
- a student can run the pipeline locally end-to-end
- the system sends one useful digest email for a fixed recipient
- all OpenAI calls are visible in Langfuse
- eval results are saved and visible
- the container runs on AWS on a schedule

## Assumptions And Defaults
- `v1` is email-only
- recipient list is fixed in config
- no subscriber management, auth, unsubscribe flow, or database
- no LangChain, no RAG, no agents, no PyTorch
- S3 is the only persistent project storage
- Resend is preferred over SES to reduce setup friction
- if time remains, the best stretch goals are:
  - multiple recipient profiles
  - digest preview page
  - salary extraction/normalization
  - manual rerun endpoint
