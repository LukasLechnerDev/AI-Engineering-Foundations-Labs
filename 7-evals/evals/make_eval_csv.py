"""
Convert a scraped jobs JSONL file to a CSV for human classification in VS Code.

Workflow:
  1. Run: uv run python evals/make_eval_csv.py evals/1-scraped_jobs.jsonl
  2. Open the generated CSV in VS Code and fill in 'human_classification' (True / False)
  3. Run: uv run pytest tests/test_classify_eval.py -s
"""

import json
import sys
from pathlib import Path

import pandas as pd

jsonl_path = Path(sys.argv[1])
csv_path = jsonl_path.with_suffix(".csv")

jobs = [json.loads(line) for line in jsonl_path.read_text().splitlines() if line]

rows = [
    {"title": j["title"], "job_url": j["job_url"], "human_classification": ""}
    for j in jobs
]

pd.DataFrame(rows).to_csv(csv_path, index=False)
print(f"Created {csv_path} with {len(rows)} jobs")
print("Fill in 'human_classification' (True / False), then run the tests.")
