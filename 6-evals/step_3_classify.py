import json

import pandas as pd
from openai import OpenAI

model = "gpt-4o-mini"

instructions = """
You classify whether a job posting is truly for an AI Engineering role.

AI Engineering definition:
- AI engineering means building applications on top of foundation models or in other words integrating them into products.
- Traditional ML engineering focuses on building, training, or tuning models; AI engineering primarily leverages existing models.
- MLOps and platform engineering are not AI engineering, as they focus on infrastructure and tooling rather than building AI-powered features.

Decision rules:
- Set is_ai_engineering_role to true when the main responsibility is building product or application features on top of foundation models or LLMs.
- Set is_ai_engineering_role to false when the role is mainly traditional software engineering, data science, analytics, ML research, model training, classical ML engineering, MLOps or platform work, or something else where AI application work is not the core responsibility.
- If the posting is ambiguous or unclear, set is_ai_engineering_role to false.
""".strip()

schema = {
    "type": "object",
    "properties": {
        "is_ai_engineering_role": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": ["is_ai_engineering_role", "reason"],
    "additionalProperties": False,
}


def classify(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    print("\nStep 3: Classifying with LLM...")

    results = []

    for i, (_, job) in enumerate(df.iterrows(), start=1):
        print(f"  Classifying {i}/{len(df)}: {job['title']}")

        response = client.responses.create(
            model=model,
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

        results.append(json.loads(response.output_text))

    results_df = pd.DataFrame(results)

    # Add the classification columns next to the original job data.
    df = pd.concat([df.reset_index(drop=True), results_df], axis=1)

    ai_count = df["is_ai_engineering_role"].sum()
    print(f"\n  AI engineering roles: {ai_count} / {len(df)} screened")

    return df
