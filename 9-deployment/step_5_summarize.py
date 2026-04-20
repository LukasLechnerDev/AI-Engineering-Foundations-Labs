import json

import pandas as pd
from langfuse import observe
from openai import OpenAI

instructions = """
You write a 2-sentence summary of an AI engineering job posting.
Focus on the role's main responsibilities and the type of product or system being built.
""".strip()

schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
    },
    "required": ["summary"],
    "additionalProperties": False,
}


@observe(name="summarize")
def summarize(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    print("\nStep 5: Generating summaries...")

    summaries = []

    for i, (_, job) in enumerate(df.iterrows(), start=1):
        print(f"  Summarizing {i}/{len(df)}: {job['title']}")

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=instructions,
            input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
            text={
                "format": {
                    "type": "json_schema",
                    "name": "job_summary",
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        summaries.append(json.loads(response.output_text)["summary"])

    df = df.copy()
    df["summary"] = summaries
    return df
