from langfuse import Evaluation
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

from rag_app import MODEL, answer_question, langfuse

DATASET_NAME = "eval-1-simple-lookup"
JUDGE_MODEL = "openai:gpt-5.6-luna"

correctness_evaluator = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    feedback_key="correctness",
    model=JUDGE_MODEL,
)


def evaluate_correctness(*, input, output, expected_output, **kwargs) -> Evaluation:
    """Evaluate one answer and return a Langfuse score."""
    result = correctness_evaluator(
        inputs=input,
        outputs=output,
        reference_outputs=expected_output,
    )
    return Evaluation(
        name="correctness",
        value=result["score"],
        comment=result["comment"],
        data_type="BOOLEAN",
    )


def run_rag_app(*, item, **kwargs) -> str:
    """Run the RAG application for one Langfuse experiment item."""
    return answer_question(item.input)


def run_langfuse_experiment():
    """Run an experiment on the hosted Langfuse dataset."""
    dataset = langfuse.get_dataset(DATASET_NAME)

    return dataset.run_experiment(
        name="rag-correctness",
        description="Evaluate RAG answers against reviewed reference answers.",
        task=run_rag_app,
        evaluators=[evaluate_correctness],
        max_concurrency=4,
        metadata={"rag_model": MODEL, "judge_model": JUDGE_MODEL},
    )


if __name__ == "__main__":
    if not langfuse.auth_check():
        raise RuntimeError("Check the Langfuse credentials in 7-rag/.env")

    try:
        experiment = run_langfuse_experiment()
        print(experiment.format())
    finally:
        langfuse.flush()
