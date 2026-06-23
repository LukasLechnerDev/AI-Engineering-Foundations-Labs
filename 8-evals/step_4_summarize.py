import json

import pandas as pd
from openai import OpenAI

model = "gpt-4o-mini"

instructions = """
You summarize AI engineering job postings into a concise 2-3 sentence overview.

The summary must:
- Capture what the company builds and what the role's core responsibility is.
- Mention the primary technical focus (e.g. RAG pipelines, LLM agents, model integration).
- Be written in plain, neutral prose — no marketing language or superlatives.
- Never exceed three sentences.
""".strip()

schema = {
    "type": "object",
    "properties": {"summary": {"type": "string"}},
    "required": ["summary"],
    "additionalProperties": False,
}


def summarize(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    print("\nStep 4: Summarizing with LLM...")

    results = []

    for i, (_, job) in enumerate(df.iterrows(), start=1):
        print(f"  Summarizing {i}/{len(df)}: {job['title']}")

        response = client.responses.create(
            model=model,
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

        results.append(json.loads(response.output_text))

    results_df = pd.DataFrame(results)

    return pd.concat([df.reset_index(drop=True), results_df], axis=1)
