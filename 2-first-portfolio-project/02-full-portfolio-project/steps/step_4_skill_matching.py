import json
from textwrap import dedent

from profile.student_profile import STUDENT_PROFILE

MODEL = "gpt-5.4-mini"

SKILL_MATCH_INSTRUCTIONS = dedent("""
    Compare each required job skill with the student's profile skills.

    Return three lists:
    - matched_required_skills: the profile clearly covers the required skill.
    - partial_required_skills: the profile has related experience, but not a clear match.
    - no_match_skills: the profile does not show this skill.

    Rules:
    - Put every required skill into exactly one list.
    - Use only the exact required skill names from the input.
    - Do not add profile skills, explanations, or new skill names.
    - Be conservative. If you are unsure, use no_match_skills.
    - Use partial_required_skills for related but different skills.

    Matching examples:
    - OpenAI API can match LLM APIs.
    - ECS Fargate or S3 can match AWS.
    - pytest can match testing.
    - RAG does not match LLM APIs.
    - Docker does not match Kubernetes.
    - prompt engineering does not match fine-tuning.
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
