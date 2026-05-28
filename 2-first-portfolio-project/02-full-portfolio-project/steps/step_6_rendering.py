from datetime import date
from html import escape
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).parent.parent
REPORT_DIR = PROJECT_DIR / "report"
TEMPLATE_PATH = REPORT_DIR / "report-template.html"
OUTPUT_PATH = REPORT_DIR / "job-agent-report.html"
TOP_JOB_LIMIT = 10

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


class RenderingStep:
    def run(self, jobs):
        print("\n--- Step 6: Rendering HTML report ---")

        visible_jobs = jobs[:TOP_JOB_LIMIT]
        cards = [
            self._render_job_card(rank, job)
            for rank, job in enumerate(visible_jobs, start=1)
        ]

        report_date = date.today()
        job_label = "Job" if len(visible_jobs) == 1 else "Jobs"
        report_title = (
            f"Your Top {len(visible_jobs)} AI Engineering {job_label} of the Week"
        )
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        html = (
            template.replace("{{ report_date }}", report_date.strftime("%B %d, %Y"))
            .replace("{{ calendar_week }}", str(report_date.isocalendar().week))
            .replace("{{ report_title }}", report_title)
            .replace("{{ cards }}", "".join(cards))
        )

        OUTPUT_PATH.write_text(html, encoding="utf-8")
        print(f"Saved report with {len(visible_jobs)} jobs to {OUTPUT_PATH}")

    def _render_job_card(self, rank, job):
        escaped = {
            "job_url": "" if pd.isna(job["job_url"]) else escape(str(job["job_url"])),
            "title": "" if pd.isna(job["title"]) else escape(str(job["title"])),
            "company": ""
            if pd.isna(job.get("company", ""))
            else escape(str(job.get("company", ""))),
            "job_type": ""
            if pd.isna(job["job_type"])
            else escape(str(job["job_type"])),
            "location": ""
            if pd.isna(job["location"])
            else escape(str(job["location"])),
            "application_decision": ""
            if pd.isna(job["application_decision"])
            else escape(str(job["application_decision"])),
            "job_summary": ""
            if pd.isna(job["job_summary"])
            else escape(str(job["job_summary"])),
            "company_summary": ""
            if pd.isna(job["company_summary"])
            else escape(str(job["company_summary"])),
            "salary": "" if pd.isna(job["salary"]) else escape(str(job["salary"])),
            "highlights_and_benefits": ""
            if pd.isna(job["highlights_and_benefits"])
            else escape(str(job["highlights_and_benefits"])),
            "application_decision_reason": ""
            if pd.isna(job["application_decision_reason"])
            else escape(str(job["application_decision_reason"])),
            "mismatch_summary": ""
            if pd.isna(job["mismatch_summary"])
            else escape(str(job["mismatch_summary"])),
            "recommended_action": ""
            if pd.isna(job["recommended_action"])
            else escape(str(job["recommended_action"])),
        }

        return f"""
        <article class="card">
          <div class="card-top">
            <div class="rank">#{rank}</div>
            <div>
              <h2><a href="{escaped["job_url"]}" target="_blank" rel="noopener noreferrer">{escaped["title"]}</a></h2>
              <div class="company">{escaped["company"]} · {escaped["job_type"]} · {escaped["location"]}</div>
            </div>
            <div class="decision">{escaped["application_decision"]}</div>
          </div>

          <p class="reason"><strong>Role:</strong> {escaped["job_summary"]}</p>
          <p class="reason"><strong>Company:</strong> {escaped["company_summary"]}</p>
          <p class="reason"><strong>Salary:</strong> {escaped["salary"]}</p>
          <p class="reason"><strong>Highlights & benefits:</strong> {escaped["highlights_and_benefits"]}</p>
          <p class="reason"><strong>Why {escaped["application_decision"]}:</strong> {escaped["application_decision_reason"]}</p>
          <p class="reason"><strong>Gaps:</strong> {escaped["mismatch_summary"]}</p>
          <p class="reason"><strong>Recommended action:</strong> {escaped["recommended_action"]}</p>

          <div class="skills">
            {self._render_skill_groups(job)}
          </div>
        </article>
        """

    def _render_skill_groups(self, job):
        skills_by_category = {}
        for skill in job["skills"]:
            skills_by_category.setdefault(skill["category"], []).append(skill)

        match_type_by_skill = {}
        for skill_name in job["matched_required_skills"]:
            match_type_by_skill[skill_name.lower()] = "full-match"
        for skill_name in job["partial_required_skills"]:
            match_type_by_skill[skill_name.lower()] = "partial-match"
        for skill_name in job["no_match_skills"]:
            match_type_by_skill[skill_name.lower()] = "no-match"

        skill_groups = []
        for category in SKILL_CATEGORIES:
            skills = skills_by_category.get(category)
            if not skills:
                continue

            chips = []
            for skill in skills:
                skill_name = skill["skill"]
                match_type = match_type_by_skill.get(skill_name.lower(), "no-match")
                escaped_skill_name = (
                    "" if pd.isna(skill_name) else escape(str(skill_name))
                )
                chips.append(
                    f'<span class="chip chip--{match_type}">{escaped_skill_name}</span>'
                )

            category_label = category.replace("-", " ") if category else "other"
            escaped_category_label = (
                "" if pd.isna(category_label) else escape(str(category_label))
            )
            skill_groups.append(
                f"""
                <div class="skill-group skill-group--{category}">
                  <div class="skill-category">{escaped_category_label}</div>
                  <div class="chips">{"".join(chips)}</div>
                </div>
                """
            )

        return "".join(skill_groups)
