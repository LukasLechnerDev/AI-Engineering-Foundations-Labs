import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Allow importing from the parent directory (step_3_classify.py lives there)
sys.path.insert(0, str(Path(__file__).parents[1]))

from step_3_classify import instructions, schema

EVAL_FILE = Path(__file__).parents[1] / "evals/eval-jobs.jsonl"
SAMPLE_SIZE = 20
CLASSIFIER_MODEL = "gpt-4o-mini"
JUDGE_MODEL = "gpt-5-mini"


judge_instructions = f"""
You evaluate whether the reason given for an AI engineering job classification is high quality.

The classifier was given these rules:
{instructions}

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


def classify_single(job: dict, client: OpenAI) -> dict:
    response = client.responses.create(
        model=CLASSIFIER_MODEL,
        instructions=instructions,
        input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
        text={
            "format": {
                "type": "json_schema",
                "name": "job_classification",
                "schema": schema,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


def judge_reason(job: dict, result: dict, client: OpenAI) -> dict:
    input_text = (
        f"Title: {job['title']}\n\n"
        f"Description:\n{job['description']}\n\n"
        f"Classification: is_ai_engineering_role={result['is_ai_engineering_role']}\n"
        f"Reason: {result['reason']}"
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
    client = OpenAI()

    passes = 0
    for i, job in enumerate(jobs, start=1):
        result = classify_single(job, client)
        judgment = judge_reason(job, result, client)

        status = "PASS" if judgment["passes"] else "FAIL"
        print(f"  [{status}] {i}/{len(jobs)} {job['title']}: {judgment['feedback']}")

        if judgment["passes"]:
            passes += 1

    rate = passes / len(jobs)
    print(f"\nReason quality: {passes}/{len(jobs)} ({rate:.1%})")

    assert rate >= 0.80, f"Reason quality {rate:.1%} is below the 80% threshold"
