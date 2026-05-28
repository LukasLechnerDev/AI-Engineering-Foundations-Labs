from datetime import date
from pathlib import Path

from steps.helpers import (
    format_category,
    safe_escape,
)

PROJECT_DIR = Path(__file__).parent.parent
REPORT_DIR = PROJECT_DIR / "report"
TEMPLATE_PATH = REPORT_DIR / "report-template.html"
OUTPUT_PATH = REPORT_DIR / "report.html"
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
            template
            .replace("{{ report_date }}", report_date.strftime("%B %d, %Y"))
            .replace("{{ calendar_week }}", str(report_date.isocalendar().week))
            .replace("{{ report_title }}", report_title)
            .replace("{{ cards }}", "".join(cards))
        )

        OUTPUT_PATH.write_text(html, encoding="utf-8")
        print(f"Saved report with {len(visible_jobs)} jobs to {OUTPUT_PATH}")

    def _render_job_card(self, rank, job):
        return f"""
        <article class="card">
          <div class="card-top">
            <div class="rank">#{rank}</div>
            <div>
              <h2><a href="{safe_escape(job["job_url"])}" target="_blank" rel="noopener noreferrer">{safe_escape(job["title"])}</a></h2>
              <div class="company">{safe_escape(job.get("company", ""))} · {safe_escape(job["job_type"])} · {safe_escape(job["location"])}</div>
            </div>
            <div class="decision">{safe_escape(job["application_decision"])}</div>
          </div>

          <p class="reason"><strong>Role:</strong> {safe_escape(job["job_summary"])}</p>
          <p class="reason"><strong>Company:</strong> {safe_escape(job["company_summary"])}</p>
          <p class="reason"><strong>Salary:</strong> {safe_escape(job["salary"])}</p>
          <p class="reason"><strong>Highlights & benefits:</strong> {safe_escape(job["highlights_and_benefits"])}</p>
          <p class="reason"><strong>Why {safe_escape(job["application_decision"])}:</strong> {safe_escape(job["application_decision_reason"])}</p>
          <p class="reason"><strong>Gaps:</strong> {safe_escape(job["mismatch_summary"])}</p>
          <p class="reason"><strong>Recommended action:</strong> {safe_escape(job["recommended_action"])}</p>

          <div class="skills">
            {self._render_skill_groups(job)}
          </div>
        </article>
        """

    def _render_skill_groups(self, job):
        skills_by_category = {}
        for skill in job["skills"]:
            skills_by_category.setdefault(skill["category"], []).append(skill)

        decisions_by_skill = {
            decision["required_skill"].lower(): decision["match_type"]
            for decision in job["skill_match_decisions"]
        }

        skill_groups = []
        for category in SKILL_CATEGORIES:
            skills = skills_by_category.get(category)
            if not skills:
                continue

            chips = []
            for skill in skills:
                skill_name = skill["skill"]
                match_type = decisions_by_skill.get(skill_name.lower(), "no-match")
                chips.append(
                    f'<span class="chip chip--{match_type}">{safe_escape(skill_name)}</span>'
                )

            skill_groups.append(
                f"""
                <div class="skill-group skill-group--{category}">
                  <div class="skill-category">{safe_escape(format_category(category))}</div>
                  <div class="chips">{"".join(chips)}</div>
                </div>
                """
            )

        return "".join(skill_groups)
