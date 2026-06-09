import json
from textwrap import dedent

MODEL = "gpt-5.4-mini"

SKILL_CATEGORIES = [
    "ai-engineering",
    "machine-learning",
    "programming-languages",
    "frontend",
    "backend",
    "databases",
    "cloud",
    "dev-ops",
    "other",
]

SKILLS_INSTRUCTIONS = dedent(f"""
    You extract required skills from AI engineering job postings.

    Return concise normalized skill names like 'python', 'rag', 'langchain', 'aws', or 'docker'.
    Return all skill names in lowercase.

    Only include skills that are clearly important for the role.

    Assign each skill to one of these categories:
    {", ".join(SKILL_CATEGORIES)}
""")

SKILLS_SCHEMA = {
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


class SkillExtractionStep:
    def __init__(self, client):
        self.client = client

    def run(self, jobs):
        print("\n--- Step 3: Extracting required skills ---")

        results = []
        for i, job in enumerate(jobs, start=1):
            print(f"Extracting skills for job {i}/{len(jobs)}: {job['title']}")

            prompt = job["description"]

            skills_response = self.client.responses.create(
                model=MODEL,
                instructions=SKILLS_INSTRUCTIONS,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "ai_engineering_skill_extraction",
                        "schema": SKILLS_SCHEMA,
                        "strict": True,
                    },
                    "verbosity": "low",
                },
            )
            skills = json.loads(skills_response.output_text)["skills"]
            print(f"  -> Extracted {len(skills)} skills")

            results.append(
                {
                    "title": job["title"],
                    "company": job.get("company", ""),
                    "job_url": job["job_url"],
                    "skills": skills,
                }
            )

        return results
