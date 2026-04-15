# Deterministic checks

## Learning goals
- Understand what a deterministic eval is and when to use it.
- Write deterministic checks for the classification step of `ai-engineer-job-digest`.

## Notes
- use "Edit CSV" extension to have a table view
- CSV so that domain experts have an easy way to enter data
- Scrape some jobs with notebook in module 1
- copy that JSONL file to evals folder of current module
- convert JSONL to CSV
- go through job postings and make human-classify
- Get the test set by going through Langfuse
- The classification step outputs `is_ai_engineering_role: bool` and `reason: str`.
- Deterministic checks are the right fit here because the output is structured and the expected answer is knowable in advance.
- Build a small labeled test set from real scraped jobs — a handful of clear positives and clear negatives is enough to start.
- These checks run instantly, require no LLM calls, and can be rerun after every prompt change.
- Keep out: model-graded checks, eval frameworks, anything that requires an LLM to evaluate.

## Script

### What is a deterministic check?
- A check where the expected output is known in advance and the result is always pass or fail.
- No LLM involved in the evaluation — just code comparing actual output to expected output.
- Examples: exact match on a label, schema validation, checking that a required field is present.

### Why start here?
- Fastest feedback loop — runs in milliseconds.
- Zero cost — no API calls needed.
- Easy to debug — when it fails, you know exactly what went wrong.
- A deterministic check failing after a prompt change is a clear signal that something regressed.

### The classification output
The classifier returns:
```json
{
  "is_ai_engineering_role": true,
  "reason": "The role focuses on building LLM-powered features."
}
```
We can write deterministic checks against `is_ai_engineering_role` because the label is binary and verifiable.

### Building the test set
- Pick a small number of jobs from `jobs/1-scraped_jobs.jsonl` where the right answer is obvious.
- Label them by hand: `true` for clear AI engineering roles, `false` for clear non-AI-engineering roles.
- Aim for 5–10 examples to start — enough to catch regressions, small enough to label quickly.

Example cases:
- **True**: "AI Engineer – build and deploy LLM-powered features for our product team"
- **False**: "Senior MLOps Engineer – manage model training infrastructure and CI/CD pipelines"
- **False**: "Data Analyst – build dashboards and reporting for business stakeholders"

### Writing the checks
```python
test_cases = [
    {"title": "AI Engineer – LLM features", "description": "...", "expected": True},
    {"title": "Senior MLOps Engineer", "description": "...", "expected": False},
    {"title": "Data Analyst", "description": "...", "expected": False},
]

passed = 0
for case in test_cases:
    result = classify(case["title"], case["description"])
    actual = result["is_ai_engineering_role"]
    ok = actual == case["expected"]
    status = "PASS" if ok else "FAIL"
    print(f"{status}: {case['title']}")
    if ok:
        passed += 1

print(f"\n{passed}/{len(test_cases)} passed")
```

### What to do when a check fails
- Read the `reason` field — the model usually explains its decision.
- Check if the prompt instructions are ambiguous for this case.
- Update the prompt and rerun all checks before moving on.

## Sources
https://app.datalumina.academy/c/genai-accelerator/sections/578161/lessons/2306558

