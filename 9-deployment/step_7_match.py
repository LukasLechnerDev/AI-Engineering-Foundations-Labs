import json

import pandas as pd
from langfuse import observe
from openai import OpenAI

# Edit this to match your own background.
# In a later lesson we'll extract this automatically from a CV PDF.
USER_PROFILE = """
Skills: Python, LLMs, OpenAI API, FastAPI, Docker, REST APIs, Git
Experience: 3 years as a backend developer, 1 year building LLM-powered features
Education: Bachelor's in Computer Science
"""

instructions = """
You evaluate how well a candidate fits a job based on their profile and the required skills.

- matched_skills: the required skills the candidate has. Use semantic matching — treat equivalent
  terms as the same skill (e.g. "JS" and "JavaScript", "LLM" and "LLMs", "Postgres" and "PostgreSQL").
  Only return skills that appear in the required skills list.
- match_score: an integer from 0 to 100 reflecting overall fit, considering skills, experience level,
  and background — not just skill count.
- match_reasoning: 2–3 concise bullet points explaining why the candidate is or isn't a strong fit.
""".strip()

schema = {
    "type": "object",
    "properties": {
        "matched_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "match_score": {"type": "integer"},
        "match_reasoning": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["matched_skills", "match_score", "match_reasoning"],
    "additionalProperties": False,
}


@observe(name="match-skills")
def match_skills(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    print("\nStep 7: Matching skills against your profile...")

    scores = []
    matched_skills_per_job = []
    match_reasoning_per_job = []

    for i, (_, job) in enumerate(df.iterrows(), start=1):
        print(f"  Matching {i}/{len(df)}: {job['title']}")

        required_skills = job["extracted_skills"] or []
        required_skill_names = [item["skill"] for item in required_skills]

        if not required_skill_names:
            scores.append(0)
            matched_skills_per_job.append(set())
            match_reasoning_per_job.append([])
            continue

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=instructions,
            input=f"Candidate profile:\n{USER_PROFILE}\n\nRequired skills:\n{', '.join(required_skill_names)}",
            text={
                "format": {
                    "type": "json_schema",
                    "name": "skill_match",
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        result = json.loads(response.output_text)
        scores.append(result["match_score"])
        matched_skills_per_job.append(set(result["matched_skills"]))
        match_reasoning_per_job.append(result["match_reasoning"])

    df = df.copy()
    df["match_score"] = scores
    df["matched_skills"] = matched_skills_per_job
    df["match_reasoning"] = match_reasoning_per_job

    # Rank by score (highest first)
    df = df.sort_values("match_score", ascending=False).reset_index(drop=True)

    print(f"  Top score: {df['match_score'].max()}")
    return df
