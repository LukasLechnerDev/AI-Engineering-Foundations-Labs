import json
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Allow importing from the parent directory (step_3_classify.py lives there)
sys.path.insert(0, str(Path(__file__).parents[1]))

from step_3_classify import classify

EVAL_FILE = Path(__file__).parents[1] / "evals/eval-jobs.jsonl"


def load_eval_jobs():
    return [json.loads(line) for line in EVAL_FILE.read_text().splitlines() if line]


# Execute with uv run pytest -s
def test_classify_eval():
    jobs = load_eval_jobs()
    df = pd.DataFrame(
        [
            {
                "title": j["title"],
                "job_url": j["job_url"],
                "description": j["description"],
            }
            for j in jobs
        ]
    )

    client = OpenAI()
    result = classify(df, client)

    # Jobs returned by classify() were predicted true; all others were predicted false.
    predicted_true_urls = set(result["job_url"])
    correct = sum(
        1
        for j in jobs
        if (j["job_url"] in predicted_true_urls) == j["is_ai_engineering_role"]
    )
    total = len(jobs)
    accuracy = correct / total

    print(f"\nAccuracy: {correct}/{total} ({accuracy:.1%})")

    assert accuracy >= 0.85, f"Accuracy {accuracy:.1%} is below the 85% threshold"
