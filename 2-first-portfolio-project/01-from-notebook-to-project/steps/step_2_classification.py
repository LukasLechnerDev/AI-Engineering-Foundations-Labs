import json
from textwrap import dedent

MODEL = "gpt-5.4-mini"

CLASSIFY_INSTRUCTIONS = dedent("""
    You classify whether a job posting is truly for an AI Engineering role.

    AI Engineering definition:
    - AI engineering means building applications on top of foundation models or in other words integrating them into products.
    - Traditional ML engineering focuses on building, training, or tuning models; AI engineering primarily leverages existing models.
    - MLOps and platform engineering are not AI engineering, as they focus on infrastructure and tooling rather than building AI-powered features.

    Decision rules:
    - Set is_ai_engineering_role to true when the main responsibility is building product or application features on top of foundation models or LLMs.
    - Set is_ai_engineering_role to false when the role is mainly traditional software engineering, data science, analytics, ML research, model training, classical ML engineering, MLOps or platform work, or something else where AI application work is not the core responsibility.
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
            title = job["title"]
            description = job["description"]
            job_url = job["job_url"]

            print(f"Classifying job {i}/{len(jobs)}: {title}")

            classify_response = self.client.responses.create(
                model=MODEL,
                instructions=CLASSIFY_INSTRUCTIONS,
                input=f"Classify this job posting.\n\nTitle: {title}\n\nDescription:\n{description}",
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "ai_engineering_job_screening",
                        "schema": CLASSIFY_SCHEMA,
                        "strict": True,
                    },
                    "verbosity": "low",
                },
            )
            classification = json.loads(classify_response.output_text)

            if classification["is_ai_engineering_role"]:
                print(f"  -> Kept (AI Engineer): {classification['reason']}")
                ai_engineering_jobs.append(
                    {"title": title, "job_url": job_url, "description": description}
                )
            else:
                print(f"  -> Skipped (not AI Engineer): {classification['reason']}")

        print(
            f"\n{len(ai_engineering_jobs)}/{len(jobs)} jobs classified as AI engineering roles"
        )
        return ai_engineering_jobs
