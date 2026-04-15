import json
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

sys.path.insert(0, str(Path(__file__).parents[1]))

from step_3_classify import classify, instructions

EVAL_FILE = Path(__file__).parents[1] / "evals/1-scraped_jobs.jsonl"
SAMPLE_SIZE = 20
JUDGE_MODEL = "gpt-5.4-mini"


judge_instructions = f"""
You evaluate whether the reason given for an AI engineering job classification is high quality.

The classifier was given these rules:
<classification rules>
{instructions}
</classification rules>

A good reason must satisfy all three criteria:
1. Grounded: it references specific details from the job description (no hallucinations).
2. Rule-aligned: it correctly applies the classification rules above.
3. Consistent: it logically supports the predicted classification decision.

Return passes=true only if all three criteria are met.
""".strip()

judge_schema = {
    "type": "object",
    "properties": {
        "passes": {"type": "boolean"},
        "feedback": {"type": "string"},
    },
    "required": ["passes", "feedback"],
    "additionalProperties": False,
}


def load_eval_jobs():
    return [json.loads(line) for line in EVAL_FILE.read_text().splitlines() if line]


def judge_reason(job: dict, client: OpenAI) -> dict:
    input_text = (
        f"Title: {job['title']}\n\n"
        f"Description:\n{job['description']}\n\n"
        f"Classification: is_ai_engineering_role={job['is_ai_engineering_role']}\n"
        f"Reason: {job['reason']}"
    )
    response = client.responses.create(
        model=JUDGE_MODEL,
        instructions=judge_instructions,
        input=input_text,
        text={
            "format": {
                "type": "json_schema",
                "name": "reason_judgment",
                "schema": judge_schema,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


# Execute with: uv run pytest tests/test_reason_eval.py -s
def test_reason_quality():
    jobs = load_eval_jobs()[:SAMPLE_SIZE]
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
    result_df = classify(df, client)

    passes = 0
    for _, row in result_df.iterrows():
        judgment = judge_reason(row.to_dict(), client)

        status = "PASS" if judgment["passes"] else "FAIL"
        print(f"  [{status}] {row['title']}: {judgment['feedback']}")

        if judgment["passes"]:
            passes += 1

    total = len(result_df)
    rate = passes / total
    print(f"\nReason quality: {passes}/{total} ({rate:.1%})")

    assert rate >= 0.80, f"Reason quality {rate:.1%} is below the 80% threshold"
