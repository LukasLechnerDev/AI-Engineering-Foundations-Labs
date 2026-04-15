import json

import pandas as pd
from openai import OpenAI

instructions = """
You identify what makes a job posting stand out.
Return up to 3 short bullet points about perks, benefits, or unique selling points.
Focus on things that would excite a candidate: compensation, flexibility, mission, tech stack, growth, etc.
""".strip()

schema = {
    "type": "object",
    "properties": {
        "highlights": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["highlights"],
    "additionalProperties": False,
}


def extract_highlights(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    print("\nStep 6: Extracting highlights and perks...")

    highlights_per_job = []

    for i, (_, job) in enumerate(df.iterrows(), start=1):
        print(f"  Extracting highlights {i}/{len(df)}: {job['title']}")

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=instructions,
            input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
            text={
                "format": {
                    "type": "json_schema",
                    "name": "job_highlights",
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        highlights_per_job.append(json.loads(response.output_text)["highlights"])

    df = df.copy()
    df["highlights"] = highlights_per_job
    return df
