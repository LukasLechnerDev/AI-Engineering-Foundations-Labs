from html import escape
from pathlib import Path
from string import Template

import pandas as pd

from step_4_extract_skills import SKILL_CATEGORIES


def render_skill_groups(skills, matched_skills):
    grouped = {}
    for item in skills:
        grouped.setdefault(item["category"], []).append(item["skill"])

    groups_html = []
    for category in SKILL_CATEGORIES:
        if category not in grouped:
            continue
        chips = ""
        for skill in grouped[category]:
            match_class = " chip-match" if skill in matched_skills else ""
            chips += f'<span class="chip{match_class}">{escape(skill)}</span>'
        groups_html.append(
            f'<div class="skill-group skill-group--{category}">'
            f'<span class="skill-category">{escape(category)}</span>'
            f'<div class="chips">{chips}</div>'
            f"</div>"
        )
    return "\n".join(groups_html)


def render_html(df: pd.DataFrame, screened_count: int, project_dir: Path) -> str:
    print("\nStep 8: Rendering HTML digest...")

    cards = []
    for _, job in df.iterrows():
        score = job["match_score"]
        score_class = (
            "score-high" if score >= 60 else "score-mid" if score >= 30 else "score-low"
        )

        highlights = job.get("highlights") or []
        highlights_html = (
            "<ul class='highlights'>"
            + "".join(f"<li>{escape(h)}</li>" for h in highlights)
            + "</ul>"
            if highlights
            else ""
        )

        reasoning = job.get("match_reasoning") or []
        reasoning_html = (
            "<ul class='reasoning'>"
            + "".join(f"<li>{escape(r)}</li>" for r in reasoning)
            + "</ul>"
            if reasoning
            else ""
        )

        skill_groups = render_skill_groups(
            job.get("extracted_skills") or [], job.get("matched_skills") or set()
        )

        cards.append(
            f"""
<div class="card">
  <div class="card-header">
    <div>
      <h2><a href="{escape(job.get("job_url") or "")}" target="_blank">{escape(job.get("title") or "")}</a></h2>
      <p class="company">{escape(job.get("company") or "")}</p>
    </div>
    <div class="score {score_class}">Matching {score}%</div>
  </div>
  <p class="section-label">Description</p>
  <p class="summary">{escape(job.get("summary") or "")}</p>
  {"<p class='section-label'>Highlights</p>" if highlights_html else ""}{highlights_html}
  {"<p class='section-label'>Match Analysis</p>" if reasoning_html else ""}{reasoning_html}
  <p class="section-label">Required Skills</p>
  <div class="skills">{skill_groups}</div>
</div>""".strip()
        )

    icon_img = '<img src="../1-project-setup/digest-icon.png" width="32" height="32" alt="" style="filter: brightness(0) invert(1);">'
    html_template = Template(
        (project_dir / "digest-template.html").read_text(encoding="utf-8")
    )
    return html_template.substitute(
        icon_img=icon_img,
        verified_role_count=len(df),
        screened_job_count=screened_count,
        cards="\n".join(cards),
    )
