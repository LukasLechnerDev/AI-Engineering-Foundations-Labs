import csv
from pathlib import Path

import pytest
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

from rag_app import answer_question

DATASET_PATH = Path(__file__).with_name("eval_dataset.csv")
REQUIRED_COLUMNS = {
    "id",
    "category",
    "question",
    "reference_answer",
    "source_documents",
}


def load_eval_cases() -> list[dict[str, str]]:
    with DATASET_PATH.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing columns in {DATASET_PATH.name}: {missing}")

        cases = list(reader)

    case_ids = [case["id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError(f"Each case in {DATASET_PATH.name} needs a unique id")

    return cases


EVAL_CASES = load_eval_cases()

correctness_evaluator = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    feedback_key="correctness",
    model="openai:gpt-5.6-luna",
)


@pytest.mark.parametrize("case", EVAL_CASES, ids=lambda case: case["id"])
def test_correctness(case: dict[str, str]):
    question = case["question"]
    reference_answer = case["reference_answer"]
    answer = answer_question(question)

    evaluation = correctness_evaluator(
        inputs=question,
        outputs=answer,
        reference_outputs=reference_answer,
    )

    assert evaluation["score"] is True, evaluation["comment"]
