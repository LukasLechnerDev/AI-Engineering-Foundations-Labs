import json
from textwrap import dedent

MODEL = "gpt-5.4-mini"

CLASSIFY_INSTRUCTIONS = dedent("""
    You classify whether a job posting is truly for an AI Engineering role.

    AI Engineering definition:
    - AI engineering means building applications on top of foundation models or integrating them into products.
    - Traditional ML engineering focuses on building, training, or tuning models.
    - MLOps and platform engineering focus on infrastructure and tooling, not AI-powered product features.

    Decision rules:
    - Set is_ai_engineering_role to true when the main responsibility is building product or application features on top of foundation models or LLMs.
    - Set is_ai_engineering_role to false when the role is mainly traditional software engineering, data science, analytics, ML research, model training, classical ML engineering, MLOps, or platform work.
    - If the posting is ambiguous or unclear, set is_ai_engineering_role to false.
    - In reason, briefly explain the main evidence for the decision in one sentence.
""")

CLASSIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "is_ai_engineering_role": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": ["is_ai_engineering_role", "reason"],
    "additionalProperties": False,
}


class ClassificationStep:
    def __init__(self, client):
        self.client = client

    def run(self, jobs):
        print("\n--- Step 2: Classifying jobs ---")

        ai_engineering_jobs = []
        for i, job in enumerate(jobs, start=1):
            print(f"Classifying job {i}/{len(jobs)}: {job['title']}")

            prompt = f"Title: {job['title']}\n\nDescription:\n{job['description']}"

            response = self.client.responses.create(
                model=MODEL,
                instructions=CLASSIFY_INSTRUCTIONS,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "job_classification",
                        "schema": CLASSIFY_SCHEMA,
                        "strict": True,
                    },
                    "verbosity": "low",
                },
            )
            classification = json.loads(response.output_text)

            if classification["is_ai_engineering_role"]:
                job["classification_reason"] = classification["reason"]
                ai_engineering_jobs.append(job)
                print(f"  -> Kept: {classification['reason']}")
            else:
                print(f"  -> Skipped: {classification['reason']}")

        print(f"AI engineering roles: {len(ai_engineering_jobs)} / {len(jobs)}")
        return ai_engineering_jobs
