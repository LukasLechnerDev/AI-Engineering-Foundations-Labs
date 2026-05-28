import json
from textwrap import dedent

from profile.student_profile import STUDENT_PROFILE

MODEL = "gpt-5.4-mini"

SKILL_MATCH_INSTRUCTIONS = dedent("""
    You semantically match required job skills to a student's profile skills.

    Rules:
    - Put every required skill into exactly one output list.
    - Use the exact required skill names from the input.
    - Be conservative. Do not match skills just because they are both technical.
                                  
    - Use matched_required_skills when the student profile clearly covers the required skill.
    - Use partial_required_skills when the student profile has related experience but does not fully cover the required skill.
    - Use no_match_skills when the student profile does not cover the required skill.
                                  
    - Match provider-specific skills to broader profile skills when appropriate, for example OpenAI API to LLM APIs.
    - Match cloud subservices to the broader cloud provider when appropriate, for example ECS Fargate or S3 to AWS.
    - Match testing tools to testing when appropriate, for example pytest to testing.
    
    - Do not match different concepts, for example RAG to LLM APIs, Docker to Kubernetes, or prompt engineering to fine-tuning.
""")

SKILL_MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "matched_required_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "partial_required_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "no_match_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "matched_required_skills",
        "partial_required_skills",
        "no_match_skills",
    ],
    "additionalProperties": False,
}


class SkillMatchingStep:
    def __init__(self, client):
        self.client = client

    def run(self, jobs):
        print("\n--- Step 4: Matching skills ---")

        matched_jobs = []
        for i, job in enumerate(jobs, start=1):
            print(f"Matching skills for job {i}/{len(jobs)}: {job['title']}")

            # Use only the skill names from the previous enrichment step.
            required_skills = [item["skill"] for item in job["skills"]]

            # If no skills were extracted, there is nothing to compare.
            if not required_skills:
                job["matched_required_skills"] = []
                job["partial_required_skills"] = []
                job["no_match_skills"] = []
                matched_jobs.append(job)
                continue

            # Ask the model to compare the job skills with the student's profile.
            prompt = dedent(f"""
                Match these required job skills against the student profile skills.

                Required job skills:
                {", ".join(required_skills)}

                Student profile skills:
                {", ".join(STUDENT_PROFILE["skills"])}
            """).strip()

            response = self.client.responses.create(
                model=MODEL,
                instructions=SKILL_MATCH_INSTRUCTIONS,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "semantic_skill_matching",
                        "schema": SKILL_MATCH_SCHEMA,
                        "strict": True,
                    },
                    "verbosity": "low",
                },
            )

            result = json.loads(response.output_text)

            job["matched_required_skills"] = result["matched_required_skills"]
            job["partial_required_skills"] = result["partial_required_skills"]
            job["no_match_skills"] = result["no_match_skills"]
            print(
                "Skill matches: "
                f"{len(job['matched_required_skills'])} matched, "
                f"{len(job['partial_required_skills'])} partial, "
                f"{len(job['no_match_skills'])} no match"
            )
            matched_jobs.append(job)

        return matched_jobs
