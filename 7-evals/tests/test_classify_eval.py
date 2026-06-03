import json
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

sys.path.insert(0, str(Path(__file__).parents[1]))

from step_3_classify import classify

CSV_FILE = Path(__file__).parents[1] / "evals/1-scraped_jobs.csv"
JSONL_FILE = CSV_FILE.with_suffix(".jsonl")


def load_eval_jobs() -> pd.DataFrame:
    labels = pd.read_csv(CSV_FILE)
    unlabeled = labels["human_classification"].isna().sum()
    if unlabeled:
        raise ValueError(
            f"{unlabeled} rows are missing a human_classification — fill them in before running the test."
        )
    labels["human_classification"] = (
        labels["human_classification"].astype(str).str.strip().str.lower().map({"true": True, "false": False})
    )

    jobs = [json.loads(line) for line in JSONL_FILE.read_text().splitlines() if line]
    descriptions = pd.DataFrame(
        [{"job_url": j["job_url"], "description": j["description"]} for j in jobs]
    )

    return labels.merge(descriptions, on="job_url")


# Execute with: uv run pytest tests/test_classify_eval.py -s
def test_classify_eval():
    eval_df = load_eval_jobs()

    client = OpenAI()
    result = classify(eval_df[["title", "job_url", "description"]], client)

    predicted_true_urls = set(result["job_url"])
    url_to_reason = dict(zip(result["job_url"], result["reason"]))

    correct = 0
    for _, row in eval_df.iterrows():
        predicted = row["job_url"] in predicted_true_urls
        if predicted == row["human_classification"]:
            correct += 1
        else:
            reason = url_to_reason.get(row["job_url"], "filtered out as non-AI-engineering role")
            print(f"  MISMATCH: {row['title']}")
            print(f"    human={row['human_classification']}, llm={predicted}")
            print(f"    reason={reason}")
            print(f"    url={row['job_url']}")

    total = len(eval_df)
    accuracy = correct / total

    print(f"\nAccuracy: {correct}/{total} ({accuracy:.1%})")

    assert accuracy >= 0.85, f"Accuracy {accuracy:.1%} is below the 85% threshold"
