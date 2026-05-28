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

ENRICHMENT_INSTRUCTIONS = dedent("""
    You enrich AI engineering job postings for a concise job report.

    Extract only information supported by the posting.
    Use concise normalized skill names like 'python', 'rag', 'sql', 'aws', or 'docker'.
    Return a short, faithful job summary and a separate company summary.
    If the posting does not describe the company, set company_summary to "Not enough company information in the posting."
    Return one concise highlights_and_benefits sentence.
    Include notable role highlights, benefits, or perks only when the posting clearly states them.
    If none are listed, return "None listed".
    For salary, use only explicit compensation text from the description. If no salary is listed in the description, return "Not listed".
    For job_type, return "remote", "hybrid", "on-site", or "unknown" based only on the posting.
    For location, return the location stated in the posting. If no location is listed, return "Unknown".
""")

ENRICHMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "job_summary": {"type": "string"},
        "company_summary": {"type": "string"},
        "salary": {"type": "string"},
        "job_type": {
            "type": "string",
            "enum": ["remote", "hybrid", "on-site", "unknown"],
        },
        "location": {"type": "string"},
        "highlights_and_benefits": {"type": "string"},
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
        },
    },
    "required": [
        "job_summary",
        "company_summary",
        "salary",
        "job_type",
        "location",
        "highlights_and_benefits",
        "skills",
    ],
    "additionalProperties": False,
}


class EnrichmentStep:
    def __init__(self, client):
        self.client = client

    def run(self, jobs):
        print("\n--- Step 3: Enriching jobs ---")

        enriched_jobs = []
        for i, job in enumerate(jobs, start=1):
            print(f"Enriching job {i}/{len(jobs)}: {job['title']}")

            prompt = f"""
Enrich this AI engineering job posting.

Use only these skill categories:
{", ".join(SKILL_CATEGORIES)}

Title: {job["title"]}
Company: {job.get("company", "")}

Description:
{job["description"]}
""".strip()

            response = self.client.responses.create(
                model=MODEL,
                instructions=ENRICHMENT_INSTRUCTIONS,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "job_enrichment",
                        "schema": ENRICHMENT_SCHEMA,
                        "strict": True,
                    },
                    "verbosity": "low",
                },
            )
            enrichment = json.loads(response.output_text)
            enriched_job = {**job, **enrichment}
            enriched_jobs.append(enriched_job)

        return enriched_jobs
