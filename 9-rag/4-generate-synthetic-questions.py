"""Generate synthetic user questions for the job postings RAG app.

We generate questions in two steps. First we pick combinations of dimension
values (we call them tuples), then we write one question per tuple. Asking for
both in a single prompt gives questions that all sound the same.
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langfuse import get_client
from pydantic import BaseModel, Field

MODEL = "gpt-5.6-luna"
EXTRA_TUPLES = 10
DATASET_NAME = "rag/ai-engineering-jobs"

RAG_DIRECTORY = Path(__file__).resolve().parent
OUTPUT_FILE = RAG_DIRECTORY / "synthetic-questions.json"

load_dotenv(RAG_DIRECTORY / ".env", override=True)

# A short summary of the knowledge base, used when we generate the tuples.
KNOWLEDGE_BASE = """
The knowledge base has 18 AI engineering job postings and 14 company profiles.
All jobs are in the United States. The companies are Capital One, American
Express, Optum, Amgen, Toyota North America, Trinity Industries (railcars),
Realtor.com, iManage (software for law firms), WRITER (enterprise AI agents),
Blue Cross and Blue Shield of Nebraska, RA Capital Management (healthcare
investing), Alvarez & Marsal (consulting), and two recruiting firms, Purple Cow
Recruiting and J2B Global. Seniority ranges from campus hire to staff level.
"""

DIMENSIONS = """
question_type: what the user wants.
  Values: values_mission, domain_interest, career_transition, constraint_filter,
  comparison, aggregate, direct_fact
corpus_support: how well the knowledge base can answer the question.
  Values: strong, partial, none
clarity: how well formed the question is.
  Values: well_specified, vague, conflicting
user_focus: the industry, topic, or requirement the user anchors the question on.
  Values: healthcare, finance, legal, automotive, real_estate, manufacturing,
  enterprise_ai, sustainability, education, gaming, academia, remote_work,
  location, seniority, compensation, employer_type, skills
"""

# The 20 combinations we reviewed by hand. The LLM adds more on top of these.
# We added user_focus after a first run: without it, most questions ended up
# being about healthcare.
REVIEWED_TUPLES = [
    ("values_mission", "strong", "well_specified", "healthcare"),
    ("values_mission", "partial", "vague", "sustainability"),
    ("values_mission", "none", "well_specified", "education"),
    ("domain_interest", "strong", "well_specified", "automotive"),
    ("domain_interest", "strong", "vague", "real_estate"),
    ("domain_interest", "partial", "well_specified", "manufacturing"),
    ("domain_interest", "none", "well_specified", "gaming"),
    ("career_transition", "strong", "well_specified", "legal"),
    ("career_transition", "strong", "vague", "enterprise_ai"),
    ("career_transition", "partial", "vague", "healthcare"),
    ("career_transition", "none", "well_specified", "academia"),
    ("constraint_filter", "strong", "well_specified", "remote_work"),
    ("constraint_filter", "strong", "vague", "seniority"),
    ("constraint_filter", "partial", "well_specified", "compensation"),
    ("constraint_filter", "none", "well_specified", "location"),
    ("constraint_filter", "strong", "conflicting", "seniority"),
    ("comparison", "strong", "well_specified", "finance"),
    ("comparison", "strong", "vague", "employer_type"),
    ("aggregate", "strong", "well_specified", "skills"),
    ("direct_fact", "partial", "well_specified", "employer_type"),
]

TUPLE_PROMPT = """
We are testing a chatbot that answers questions about a knowledge base of AI
engineering job postings.
{knowledge_base}
Generate {count} combinations of these dimensions:
{dimensions}

We already have these combinations, so generate different ones:
{reviewed}

Vary the values across all four dimensions.
"""

QUESTION_PROMPT = """
We are generating synthetic user questions for a chatbot that answers questions
about a knowledge base of AI engineering job postings from many companies.

Write one realistic question for these dimension values:
- question_type: {question_type}
- corpus_support: {corpus_support}
- clarity: {clarity}
- user_focus: {user_focus}

Users do not know what is in the knowledge base. So never name a company and
never hint at which posting you mean. Users describe their own background, their
interests, or what they care about.

What the dimension values mean:
- values_mission: the user cares about the impact of the work
- domain_interest: the user is interested in an industry or a product
- career_transition: the user is switching career
- constraint_filter: the user has hard requirements like location or seniority
- comparison: the user wants two or more options weighed against each other
- aggregate: the user wants a count or a statistic over all postings
- direct_fact: the user asks about one posting or one company
- strong: several postings clearly fit
- partial: only one posting fits, or it fits only loosely
- none: nothing in the knowledge base fits, so a good answer says so
- well_specified: clear and easy to act on
- vague: the user leaves out important details
- conflicting: the requirements contradict each other
- user_focus: the question should be about this topic or requirement

Keep the question to one or two sentences.

Examples of the tone we want:
"I wanna work for a company that makes a positive impact on the world."
"I am a lawyer turned developer, is there a job for me?"

Write only the question, nothing else.
"""


class QuestionTuple(BaseModel):
    question_type: str = Field(description="One of the question_type values")
    corpus_support: str = Field(description="One of the corpus_support values")
    clarity: str = Field(description="One of the clarity values")
    user_focus: str = Field(description="One of the user_focus values")


class QuestionTuples(BaseModel):
    tuples: list[QuestionTuple]


def generate_extra_tuples(llm, count: int, reviewed: list[tuple]) -> list[tuple]:
    """Ask the LLM for additional dimension combinations."""
    prompt = TUPLE_PROMPT.format(
        knowledge_base=KNOWLEDGE_BASE,
        count=count,
        dimensions=DIMENSIONS,
        reviewed="\n".join(str(tuple_) for tuple_ in reviewed),
    )
    result = llm.with_structured_output(QuestionTuples).invoke(prompt)
    return [
        (t.question_type, t.corpus_support, t.clarity, t.user_focus)
        for t in result.tuples
    ]


def write_questions(llm, tuples: list[tuple]) -> list[str]:
    """Turn every tuple into one natural language question."""
    prompts = [
        QUESTION_PROMPT.format(
            question_type=question_type,
            corpus_support=corpus_support,
            clarity=clarity,
            user_focus=user_focus,
        )
        for question_type, corpus_support, clarity, user_focus in tuples
    ]
    # batch sends all prompts in parallel instead of one after the other
    return [response.content.strip() for response in llm.batch(prompts)]


def upload_to_langfuse(items: list[dict]):
    """Put the questions into the Langfuse dataset we run experiments on.

    We only upload the questions. The expected answers are written by hand
    afterwards in Langfuse, because they have to be checked against the
    documents in the knowledge base.
    """
    langfuse = get_client()
    langfuse.create_dataset(name=DATASET_NAME)

    for item in items:
        langfuse.create_dataset_item(
            dataset_name=DATASET_NAME,
            id=item["id"],  # same id twice updates the item instead of adding one
            input=item["question"],
            metadata={key: value for key, value in item.items() if key != "question"},
        )

    langfuse.flush()
    print(f"Uploaded {len(items)} questions to the '{DATASET_NAME}' dataset")


def main():
    llm = ChatOpenAI(model=MODEL, temperature=1.0)

    tuples = REVIEWED_TUPLES + generate_extra_tuples(llm, EXTRA_TUPLES, REVIEWED_TUPLES)
    questions = write_questions(llm, tuples)

    items = []
    for number, (question, tuple_) in enumerate(zip(questions, tuples, strict=True), 1):
        question_type, corpus_support, clarity, user_focus = tuple_
        items.append(
            {
                "id": f"syn-{number:02d}",
                "question": question,
                "question_type": question_type,
                "corpus_support": corpus_support,
                "clarity": clarity,
                "user_focus": user_focus,
            }
        )

    OUTPUT_FILE.write_text(json.dumps(items, indent=2) + "\n")
    print(f"Wrote {len(items)} questions to {OUTPUT_FILE.name}")
    print(
        "Read the file, fix or drop weak questions, then run this script with 'upload'"
    )


if __name__ == "__main__":
    if "upload" in sys.argv:
        upload_to_langfuse(json.loads(OUTPUT_FILE.read_text()))
    else:
        main()
