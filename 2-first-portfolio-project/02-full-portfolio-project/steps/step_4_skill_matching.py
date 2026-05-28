import json
from textwrap import dedent

from profile.student_profile import STUDENT_PROFILE

MODEL = "gpt-5.4-mini"

MATCH_TYPES = ["full-match", "partial-match", "no-match"]

SKILL_MATCH_INSTRUCTIONS = dedent("""
    You semantically match required job skills to a student's profile skills.

    Rules:
    - Return exactly one match decision for every required skill.
    - Be conservative. Do not match skills just because they are both technical.
                                  
    - Use "full-match" when the student profile clearly covers the required skill.
    - Use "partial-match" when the student profile has related experience but does not fully cover the required skill.
    - Use "no-match" when the student profile does not cover the required skill.
                                  
    - Match provider-specific skills to broader profile skills when appropriate, for example OpenAI API to LLM APIs.
    - Match cloud subservices to the broader cloud provider when appropriate, for example ECS Fargate or S3 to AWS.
    - Match testing tools to testing when appropriate, for example pytest to testing.
    
    - Do not match different concepts, for example RAG to LLM APIs, Docker to Kubernetes, or prompt engineering to fine-tuning.
""")

SKILL_MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "matches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "required_skill": {"type": "string"},
                    "matched_profile_skill": {"type": ["string", "null"]},
                    "match_type": {"type": "string", "enum": MATCH_TYPES},
                    "reason": {"type": "string"},
                },
                "required": [
                    "required_skill",
                    "matched_profile_skill",
                    "match_type",
                    "reason",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["matches"],
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

            # The model returns a list of match decisions.
            # Convert that list into a dictionary where each required skill is the key.
            # This makes it easy to find the model's decision for each skill below.
            decisions_by_skill = {
                item["required_skill"]: item for item in result["matches"]
            }

            match_decisions = []
            for required_skill in required_skills:
                decision = decisions_by_skill.get(required_skill)

                # If the model missed a skill, mark it as no-match
                if decision is None:
                    decision = {
                        "required_skill": required_skill,
                        "matched_profile_skill": None,
                        "match_type": "no-match",
                        "reason": "The model did not return a decision for this skill.",
                    }
                else:
                    decision["required_skill"] = required_skill

                match_decisions.append(decision)

            # Split the skill decisions into simple lists for the next step.
            matched = [
                item["required_skill"]
                for item in match_decisions
                if item["match_type"] == "full-match"
            ]
            partial = [
                item["required_skill"]
                for item in match_decisions
                if item["match_type"] == "partial-match"
            ]
            no_match = [
                item["required_skill"]
                for item in match_decisions
                if item["match_type"] == "no-match"
            ]

            job["matched_required_skills"] = matched
            job["partial_required_skills"] = partial
            job["no_match_skills"] = no_match
            matched_jobs.append(job)

        return matched_jobs
