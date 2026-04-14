import json

import pandas as pd
from openai import OpenAI

SKILL_CATEGORIES = [
    "ai-engineering",
    "ml",
    "data",
    "backend",
    "cloud",
    "ops",
    "languages",
    "frontend",
    "other",
]

skill_instructions = """
You extract required skills from AI engineering job postings.

Return concise normalized skill names like 'python', 'rag', 'sql', 'aws', or 'docker'.
Only include skills that are clearly important for the role.
Assign each skill to one of the provided categories.
""".strip()

skill_schema = {
    "type": "object",
    "properties": {
        "skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "skill": {"type": "string"},
                    "category": {"type": "string", "enum": SKILL_CATEGORIES},
                },
                "required": ["skill", "category"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["skills"],
    "additionalProperties": False,
}


def extract_skills(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    print("\nStep 4: Extracting required skills...")

    category_text = "\n".join(f"- {c}" for c in SKILL_CATEGORIES)
    extracted_skills_per_job = []

    for i, (_, job) in enumerate(df.iterrows(), start=1):
        print(f"  Extracting skills {i}/{len(df)}: {job['title']}")

        prompt = f"""
Extract the required skills for this AI engineering job posting.

Use only these categories:
{category_text}

Description:
{job["description"]}
""".strip()

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=skill_instructions,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ai_engineering_skill_extraction",
                    "schema": skill_schema,
                    "strict": True,
                },
            },
        )

        result = json.loads(response.output_text)
        extracted_skills_per_job.append(
            [
                {"skill": item["skill"].strip().lower(), "category": item["category"]}
                for item in result["skills"]
            ]
        )

    df = df.copy()
    df["extracted_skills"] = extracted_skills_per_job
    return df
