import json
from textwrap import dedent

from models import OverallJobMatch
from profile.student_profile import STUDENT_PROFILE

MODEL = "gpt-5.4-mini"

OVERALL_MATCH_INSTRUCTIONS = dedent("""
    You evaluate how well an AI engineering job fits a student.

    Consider:
    - role type
    - additional student preferences
    - skill match results

    Decision categories:
    - Apply this week: strong role fit, enough matched skills, aligned with student requirements, worth near-term application effort.
    - Consider applying: plausible fit with useful upside, but has notable gaps or uncertainty.
    - Not ready yet: not a near-term application priority, but useful for identifying skills to build.
    - No fit: the role has a hard mismatch with the student's requirements or goals. The student should not apply and should not use this role as a learning target.

    Rules:
    - Return an overall match score from 0 to 1, where 1 is the strongest fit.
    - Be conservative and grounded in the provided data.
    - Do not invent facts about the student, company, or role.
    - Do not mention numeric scores or percentages in the reasoning.
    - Use the additional student preferences as plain text guidance.
    - Choose exactly one decision category.
    - Keep the reason under 70 words.
    - Keep the mismatch summary under 50 words.
    - Keep the recommended action under 50 words.
""")


class OverallMatchingStep:
    def __init__(self, client):
        self.client = client

    def run(self, jobs):
        print("\n--- Step 5: Calculating overall match ---")

        matched_jobs = []
        for i, job in enumerate(jobs, start=1):
            print(f"Calculating overall match {i}/{len(jobs)}: {job['title']}")

            prompt = dedent(f"""
                Evaluate the overall match between this job and the student profile.

                Job:
                - title: {job["title"]}
                - company: {job.get("company", "")}
                - job_type: {job["job_type"]}
                - location: {job["location"]}
                - salary: {job["salary"]}
                - job_summary: {job["job_summary"]}
                - company_summary: {job["company_summary"]}
                - highlights_and_benefits: {job["highlights_and_benefits"]}
                - required_skills: {json.dumps([item["skill"] for item in job["skills"]], indent=2)}
                - posting_description: {job["description"]}

                Student profile:
                {json.dumps(STUDENT_PROFILE, indent=2)}

                Skill match result:
                - matched_required_skills: {job["matched_required_skills"]}
                - partial_required_skills: {job["partial_required_skills"]}
                - no_match_skills: {job["no_match_skills"]}
            """).strip()

            response = self.client.responses.parse(
                model=MODEL,
                instructions=OVERALL_MATCH_INSTRUCTIONS,
                input=prompt,
                text_format=OverallJobMatch,
                verbosity="low",
            )
            match = response.output_parsed
            if match is None:
                raise ValueError("The model did not return an overall job match.")

            job["overall_match_score"] = match.overall_match_score
            print(f"Overall match score: {job['overall_match_score']:.2f}")

            job["application_decision"] = match.application_decision.value
            print(f"Application decision: {job['application_decision']}")

            job["application_decision_reason"] = match.application_decision_reason
            job["mismatch_summary"] = match.mismatch_summary
            job["recommended_action"] = match.recommended_action
            matched_jobs.append(job)

        return sorted(
            matched_jobs,
            key=lambda job: job["overall_match_score"],
            reverse=True,
        )
