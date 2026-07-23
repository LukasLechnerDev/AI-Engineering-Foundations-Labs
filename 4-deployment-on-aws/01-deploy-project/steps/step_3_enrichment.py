from textwrap import dedent

from models import JobEnrichment, SkillCategory

MODEL = "gpt-5.4-mini"

ENRICHMENT_INSTRUCTIONS = dedent("""
    You enrich AI engineering job postings for a concise job report.

    Extract only information supported by the posting.
    Use concise normalized skill names like 'python', 'rag', 'sql', 'aws', or 'docker'.
    
    Return a short, faithful job summary and a separate company summary.
    If the posting does not describe the company, set company_summary to "Not enough company information in the posting."
    
    Return one concise highlights_and_benefits sentence.
    Include notable role highlights, benefits, or perks only when the posting clearly states them.
    If none are listed, return "None listed".
    
    For salary, use only explicit compensation text from the description. 
    If no salary is listed in the description, return "Not listed".
    
    For job_type, return "remote", "hybrid", "on-site", or "unknown" based only on the posting.
                                 
    For location, return the location stated in the posting. 
    If no location is listed, return "Unknown".
""")


class EnrichmentStep:
    def __init__(self, client):
        self.client = client

    def run(self, jobs):
        print("\n--- Step 3: Enriching jobs ---")

        enriched_jobs = []
        for i, job in enumerate(jobs, start=1):
            print(f"Enriching job {i}/{len(jobs)}: {job['title']}")

            prompt = dedent(f"""
                Enrich this AI engineering job posting.

                Use only these skill categories:
                {", ".join(category.value for category in SkillCategory)}

                Title: {job["title"]}
                Company: {job.get("company", "")}

                Description:
                {job["description"]}
            """).strip()

            response = self.client.responses.parse(
                model=MODEL,
                instructions=ENRICHMENT_INSTRUCTIONS,
                input=prompt,
                text_format=JobEnrichment,
                verbosity="low",
            )
            enrichment = response.output_parsed
            if enrichment is None:
                raise ValueError("The model did not return a job enrichment.")

            enriched_job = {**job, **enrichment.model_dump(mode="json")}
            enriched_jobs.append(enriched_job)

        return enriched_jobs
