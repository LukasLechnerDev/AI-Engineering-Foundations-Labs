from html import escape
from pathlib import Path
from string import Template

import pandas as pd

from step_5_extract_skills import SKILL_CATEGORIES

card_template = Template(
    """
<div class="card">
  <h2><a href="$job_url" target="_blank">$title</a></h2>
  <p class="company">$company</p>
  <p class="classification">Classification: <strong>$classification</strong></p>
  <p class="summary">$summary</p>
  <p class="reason">$reason</p>
  <div class="skills">$skill_groups</div>
</div>
""".strip()
)


def render_skill_groups(skills: list) -> str:
    grouped = {}
    for item in skills:
        grouped.setdefault(item["category"], []).append(item["skill"])

    groups_html = []
    for category in SKILL_CATEGORIES:
        if category not in grouped:
            continue
        chips = "".join(
            f'<span class="chip">{escape(skill)}</span>' for skill in grouped[category]
        )
        groups_html.append(
            f'<div class="skill-group skill-group--{category}">'
            f'<span class="skill-category">{escape(category)}</span>'
            f'<div class="chips">{chips}</div>'
            f"</div>"
        )
    return "\n".join(groups_html)


def render_html(
    classified_jobs: pd.DataFrame, screened_count: int, project_dir: Path
) -> str:
    print("\nStep 6: Rendering HTML digest...")

    cards = []
    for _, job in classified_jobs.iterrows():
        cards.append(
            card_template.substitute(
                job_url=escape(job["job_url"]),
                title=escape(job["title"]),
                company=escape(job["company"]),
                classification="AI engineering"
                if job["is_ai_engineering_role"]
                else "Not AI engineering",
                summary=escape(job["summary"]),
                reason=escape(job["reason"]),
                skill_groups=render_skill_groups(job["extracted_skills"]),
            )
        )

    icon_img = '<img src="digest-icon.png" width="32" height="32" alt="" style="filter: brightness(0) invert(1);">'
    html_template = Template(
        (project_dir / "digest-template.html").read_text(encoding="utf-8")
    )
    return html_template.substitute(
        icon_img=icon_img,
        verified_role_count=len(classified_jobs),
        screened_job_count=screened_count,
        cards="\n".join(cards),
    )
