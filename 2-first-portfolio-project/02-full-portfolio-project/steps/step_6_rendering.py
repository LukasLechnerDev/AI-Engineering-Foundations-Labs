from datetime import date
from html import escape
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).parent.parent
REPORT_DIR = PROJECT_DIR / "report"
TEMPLATE_PATH = REPORT_DIR / "report-template.html"
OUTPUT_PATH = REPORT_DIR / "job-agent-report.html"
TOP_JOB_LIMIT = 10
FONT_STACK = "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"

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

CHIP_STYLES = {
    "full-match": {
        "background": "#15803D",
        "color": "#FFFFFF",
        "border": "#166534",
    },
    "partial-match": {
        "background": "#ECFDF5",
        "color": "#166534",
        "border": "#A7F3D0",
    },
    "no-match": {
        "background": "#F8FAFC",
        "color": "#475569",
        "border": "#E2E8F0",
    },
}


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
        return OUTPUT_PATH

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
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="background-color:#FFFFFF;border:1px solid #D8E3F8;border-radius:8px;border-collapse:separate;margin:0 0 16px 0;">
          <tr>
            <td style="padding:20px;font-family:{FONT_STACK};">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
                <tr>
                  <td valign="top">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
                      <tr>
                        <td valign="top" style="padding:0 12px 0 0;">
                          <span style="display:inline-block;background-color:#E7EDF7;color:#2F6BFF;border:1px solid #BFD1F2;border-radius:999px;font-family:{FONT_STACK};font-size:13px;font-weight:700;line-height:1;padding:8px 10px;">#{rank}</span>
                        </td>
                        <td valign="top">
                          <a href="{escaped["job_url"]}" target="_blank" rel="noopener noreferrer" style="color:#1D4ED8;font-family:{FONT_STACK};font-size:18px;font-weight:700;line-height:1.25;text-decoration:none;">{escaped["title"]}</a>
                          <div style="color:#6B7280;font-family:{FONT_STACK};font-size:14px;font-weight:500;line-height:1.4;margin-top:4px;">{escaped["company"]} &middot; {escaped["job_type"]} &middot; {escaped["location"]}</div>
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td width="180" valign="top" align="right" style="padding-left:12px;">
                    <span style="display:inline-block;background-color:#2F6BFF;color:#FFFFFF;border:1px solid #2457D6;border-radius:999px;font-family:{FONT_STACK};font-size:13px;font-weight:700;line-height:1.2;padding:7px 10px;white-space:nowrap;">{escaped["application_decision"]}</span>
                  </td>
                </tr>
              </table>

              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:18px;"><strong style="color:#0B1020;">Role:</strong> {escaped["job_summary"]}</div>
              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:12px;"><strong style="color:#0B1020;">Company:</strong> {escaped["company_summary"]}</div>
              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:12px;"><strong style="color:#0B1020;">Salary:</strong> {escaped["salary"]}</div>
              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:12px;"><strong style="color:#0B1020;">Highlights &amp; benefits:</strong> {escaped["highlights_and_benefits"]}</div>
              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:14px;"><strong style="color:#0B1020;">Why {escaped["application_decision"]}:</strong> {escaped["application_decision_reason"]}</div>
              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:12px;"><strong style="color:#0B1020;">Gaps:</strong> {escaped["mismatch_summary"]}</div>
              <div style="color:#3D4660;font-family:{FONT_STACK};font-size:14px;line-height:1.55;margin-top:12px;"><strong style="color:#0B1020;">Recommended action:</strong> {escaped["recommended_action"]}</div>

              <div style="color:#0B1020;font-family:{FONT_STACK};font-size:14px;line-height:1.5;margin-top:16px;"><strong>Skill match</strong></div>
              <div style="margin-top:6px;">{self._render_skill_groups(job)}</div>
            </td>
          </tr>
        </table>
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
                chips.append(self._render_skill_chip(skill_name, match_type))

            category_label = category.replace("-", " ") if category else "other"
            escaped_category_label = (
                "" if pd.isna(category_label) else escape(str(category_label))
            )
            skill_groups.append(
                f"""
                <tr>
                  <td valign="top" style="width:150px;padding:7px 12px 5px 0;font-family:{FONT_STACK};font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;color:#64748B;line-height:1.4;">
                    {escaped_category_label}
                  </td>
                  <td valign="top" style="padding:2px 0 5px 0;">
                    {"".join(chips)}
                  </td>
                </tr>
                """
            )

        if not skill_groups:
            return ""

        return f"""
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
          {"".join(skill_groups)}
        </table>
        """

    def _render_skill_chip(self, skill_name, match_type):
        style = CHIP_STYLES[match_type]
        escaped_skill_name = "" if pd.isna(skill_name) else escape(str(skill_name))
        return (
            '<span style="display:inline-block;'
            f"background-color:{style['background']};"
            f"color:{style['color']};"
            f"border:1px solid {style['border']};"
            f"font-family:{FONT_STACK};"
            "font-size:12px;font-weight:500;line-height:1.2;"
            "padding:5px 10px;border-radius:999px;margin:3px 5px 3px 0;"
            f'">{escaped_skill_name}</span>'
        )
