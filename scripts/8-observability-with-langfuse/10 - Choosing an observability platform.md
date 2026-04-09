# 10 - Choosing an observability platform

## Recommendation
- Use Langfuse in the course.

## Why this is the best course choice
- The course teaches the raw OpenAI SDK first, so the observability tool should stay framework-agnostic.
- Langfuse fits that goal well because it is positioned as open source, self-hostable, and not tied to LangChain.
- This keeps the course focused on observability concepts instead of teaching a framework-specific platform.
- It is also easier to justify for students who want a tool they can run cheaply in personal projects.

## What the job dataset suggests
- The strongest signal is not one specific vendor. The strongest signal is that observability in general matters.
- In `3-extracted_skills.jsonl`:
  - `observability` appears in 20 of 101 rows
  - `monitoring` appears in 15 rows
  - `logging` appears in 7 rows
  - `tracing` appears in 3 rows
  - `telemetry` appears in 3 rows
- In `1-scraped_jobs.jsonl`:
  - `monitoring` appears in 54 of 139 descriptions
  - `observability` appears in 37 descriptions

## Named tools seen in the dataset
- LLM-specific tools:
  - `LangSmith`: 2 extracted-skill rows, 3 job descriptions
  - `Langfuse`: 1 extracted-skill row, 1 job description
  - `AgentOps`: 1 extracted-skill row, 1 job description
- Broader observability stacks:
  - `Grafana`: 2 extracted-skill rows, 4 job descriptions
  - `Prometheus`: 1 extracted-skill row, 3 job descriptions
  - `CloudWatch`: 1 extracted-skill row, 2 job descriptions
  - `Application Insights`: 1 extracted-skill row, 1 job description
  - `Splunk`: 1 extracted-skill row, 1 job description
- Adjacent MLOps tools show up often too:
  - `MLflow`: 5 extracted-skill rows, 10 job descriptions

## Interpretation
- In real jobs, developers will often inherit a company-wide observability stack first.
- That usually means tools like Grafana, Prometheus, CloudWatch, or Application Insights.
- On top of that, teams building LLM products may add an AI-specific layer such as LangSmith or Langfuse.
- In this dataset, LangSmith appears more often than Langfuse, so students are probably more likely to encounter LangSmith on LangChain-heavy teams.

## Course stance
- Teach Langfuse in the course.
- Mention LangSmith as another important platform students are likely to see in the wild.
- Emphasize that the transferable skill is not a single vendor UI.
- The transferable skill is tracing runs, inspecting prompts and outputs, tracking latency and cost, and comparing versions over time.
- Also mention OpenTelemetry as the vendor-neutral foundation that makes these tools easier to switch later.
