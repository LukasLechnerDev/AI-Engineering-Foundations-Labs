import json
import webbrowser
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from jobspy import scrape_jobs
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Your skill profile — rate each skill from 1 (beginner) to 10 (expert)
USER_SKILLS = {
    "Python": 8,
    "OpenAI API": 6,
    "LLMs": 7,
    "FastAPI": 5,
    "Docker": 4,
    "REST APIs": 7,
    "Git": 9,
}

# ── Step 1: Scrape ────────────────────────────────────────────────────────────

print("Step 1: Scraping jobs...")

jobs = scrape_jobs(
    site_name=["indeed", "linkedin"],
    linkedin_fetch_description=True,
    search_term='"AI Engineer"',
    location="USA",
    country_indeed="USA",
    job_type="fulltime",
    hours_old=24,
    results_wanted=2,
)

df = pd.DataFrame(jobs)
print(f"  Scraped: {len(df)} jobs")

# ── Step 2: Filter ────────────────────────────────────────────────────────────

print("\nStep 2: Filtering...")

mask = df["title"].str.contains("AI", case=False, na=False) & df["title"].str.contains(
    "Engineer", case=False, na=False
)
df = df[mask].copy()
print(f"  After title filter: {len(df)} jobs")

required_columns = ["title", "job_url", "description"]
has_required = (
    df[required_columns]
    .fillna("")
    .apply(lambda col: col.astype(str).str.strip() != "")
    .all(axis=1)
)
df = df[has_required].copy()
print(f"  After required-fields check: {len(df)} jobs")

df = df.drop_duplicates(subset=["title", "company"]).copy()
print(f"  After deduplication: {len(df)} jobs")

# ── Step 3: Classify ──────────────────────────────────────────────────────────

print("\nStep 3: Classifying with LLM...")

classification_instructions = """
You classify whether a job posting is truly an AI Engineering role.

An AI Engineering role means building applications on top of foundation models or LLMs.
It is NOT traditional ML engineering, data science, MLOps, or platform/infrastructure work.

Set is_ai_engineering_role to true only when the core responsibility is building
AI-powered product features using foundation models. If ambiguous, set it to false.
""".strip()

classification_schema = {
    "type": "object",
    "properties": {
        "is_ai_engineering_role": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": ["is_ai_engineering_role", "reason"],
    "additionalProperties": False,
}

classification_results = []

for i, (_, job) in enumerate(df.iterrows(), start=1):
    print(f"  Classifying {i}/{len(df)}: {job['title']}")
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=classification_instructions,
        input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
        text={
            "format": {
                "type": "json_schema",
                "name": "job_classification",
                "schema": classification_schema,
                "strict": True,
            }
        },
    )
    classification_results.append(json.loads(response.output_text))

classification_df = pd.DataFrame(classification_results)
df = pd.concat([df.reset_index(drop=True), classification_df], axis=1)
ai_jobs = df[df["is_ai_engineering_role"]].copy()

print(f"\n  AI engineering roles: {len(ai_jobs)} / {len(df)} screened")

# ── Step 4: Enrich ────────────────────────────────────────────────────────────

print("\nStep 4: Enriching jobs...")

enrichment_instructions = """
Extract structured information from a job posting.
- summary: 2 sentences describing the role and its main focus.
- highlights: up to 3 notable perks, benefits, or selling points.
- required_skills: specific technical skills mentioned as required or expected.
""".strip()

enrichment_schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "highlights": {"type": "array", "items": {"type": "string"}},
        "required_skills": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "highlights", "required_skills"],
    "additionalProperties": False,
}

enrichment_results = []

for i, (_, job) in enumerate(ai_jobs.iterrows(), start=1):
    print(f"  Enriching {i}/{len(ai_jobs)}: {job['title']}")
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=enrichment_instructions,
        input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
        text={
            "format": {
                "type": "json_schema",
                "name": "job_enrichment",
                "schema": enrichment_schema,
                "strict": True,
            }
        },
    )
    enrichment_results.append(json.loads(response.output_text))

enrichment_df = pd.DataFrame(enrichment_results)
ai_jobs = pd.concat([ai_jobs.reset_index(drop=True), enrichment_df], axis=1)

# ── Step 5: Match ─────────────────────────────────────────────────────────────

print("\nStep 5: Matching against your skill profile...")


def score_skill_match(required_skills, user_skills):
    """Returns (score 0-100, matched skills list).

    user_skills is a dict of {skill_name: rating 1-10}.
    Uses substring matching to handle LLM skill name variations.
    Score is weighted by proficiency ratings.
    """
    if not required_skills:
        return 0, []
    matched = []
    for req in required_skills:
        req_lower = req.lower()
        for user_skill, rating in user_skills.items():
            if user_skill.lower() in req_lower or req_lower in user_skill.lower():
                matched.append((req, rating))
                break
    if not matched:
        return 0, []
    # Score = sum of matched ratings / (total required skills * max rating)
    score = round(sum(r for _, r in matched) / (len(required_skills) * 10) * 100)
    return score, [m[0] for m in matched]


matching_instructions = """
You explain how well a candidate fits a job based on a skill match analysis.
- fit_explanation: 2 sentences on why the candidate is or isn't a strong fit.
- skill_gaps: the most important skills the candidate is missing for this role.
""".strip()

matching_schema = {
    "type": "object",
    "properties": {
        "fit_explanation": {"type": "string"},
        "skill_gaps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["fit_explanation", "skill_gaps"],
    "additionalProperties": False,
}

match_results = []

for i, (_, job) in enumerate(ai_jobs.iterrows(), start=1):
    print(f"  Matching {i}/{len(ai_jobs)}: {job['title']}")

    required_skills = job.get("required_skills") or []
    score, matched_skills = score_skill_match(required_skills, USER_SKILLS)
    missing_skills = [s for s in required_skills if s not in matched_skills]

    user_skills_formatted = ", ".join(f"{s} ({r}/10)" for s, r in USER_SKILLS.items())

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=matching_instructions,
        input=f"""Job: {job["title"]}
Summary: {job["summary"]}
Required skills: {", ".join(required_skills)}
Candidate skills: {user_skills_formatted}
Match score: {score}%
Matched: {", ".join(matched_skills) or "none"}
Missing: {", ".join(missing_skills) or "none"}""",
        text={
            "format": {
                "type": "json_schema",
                "name": "skill_match",
                "schema": matching_schema,
                "strict": True,
            }
        },
    )

    result = json.loads(response.output_text)
    result["match_score"] = score
    result["matched_skills"] = matched_skills
    match_results.append(result)

match_df = pd.DataFrame(match_results)
ai_jobs = pd.concat([ai_jobs.reset_index(drop=True), match_df], axis=1)
ai_jobs = ai_jobs.sort_values("match_score", ascending=False).reset_index(drop=True)

# ── Step 6: Render HTML ───────────────────────────────────────────────────────

print("\nStep 6: Rendering HTML digest...")

cards = ""
for _, job in ai_jobs.iterrows():
    company = job.get("company") or ""
    summary = job.get("summary") or ""
    fit_explanation = job.get("fit_explanation") or ""
    score = job.get("match_score", 0)

    score_class = (
        "score-high" if score >= 60 else "score-mid" if score >= 30 else "score-low"
    )

    skill_tags = ""
    matched = set(s.lower() for s in (job.get("matched_skills") or []))
    for skill in job.get("required_skills") or []:
        is_match = skill.lower() in matched
        cls = "skill skill-match" if is_match else "skill"
        skill_tags += f'<span class="{cls}">{skill}</span>'

    highlight_items = "".join(f"<li>{h}</li>" for h in (job.get("highlights") or []))
    gap_items = "".join(
        f"<span class='skill skill-gap'>{g}</span>"
        for g in (job.get("skill_gaps") or [])
    )

    cards += f"""
    <div class="card">
      <div class="card-header">
        <div>
          <h2><a href="{job["job_url"]}" target="_blank">{job["title"]}</a></h2>
          <p class="company">{company}</p>
        </div>
        <div class="score {score_class}">{score}%</div>
      </div>
      <p class="summary">{summary}</p>
      <div class="skills">{skill_tags}</div>
      {"<ul class='highlights'>" + highlight_items + "</ul>" if highlight_items else ""}
      <p class="fit">{fit_explanation}</p>
      {"<div class='gaps-label'>Skill gaps</div><div class='skills'>" + gap_items + "</div>" if gap_items else ""}
    </div>
"""

icon_img = '<img src="../1-project-setup/digest-icon.png" width="32" height="32" alt="" style="filter: brightness(0) invert(1);">'

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Engineer Job Digest</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'IBM Plex Sans', sans-serif; background: #FAFBFD; color: #0B1020; }}

    .hero {{ background: #0B1020; padding: 40px; }}
    .hero-inner {{
      max-width: 860px; margin: 0 auto;
      display: flex; align-items: center; gap: 18px;
    }}
    .icon-wrap {{
      background: #1A2236; border-radius: 12px;
      width: 56px; height: 56px;
      display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }}
    .hero-text h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem; font-weight: 600; color: #fff; line-height: 1.2;
    }}
    .hero-text h1 span {{ color: #2F6BFF; }}
    .hero-text p {{ color: #8FB2FF; font-size: 0.875rem; margin-top: 6px; }}

    .content {{ max-width: 860px; margin: 36px auto; padding: 0 40px; }}

    .card {{
      background: white; border-radius: 10px;
      padding: 20px 24px; margin-bottom: 12px;
      border: 1px solid #8FB2FF;
    }}
    .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
    .card h2 {{ font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 600; margin-bottom: 3px; }}
    .card h2 a {{ color: #0B1020; text-decoration: none; }}
    .card h2 a:hover {{ color: #2F6BFF; }}
    .company {{ color: #6B7280; font-size: 0.825rem; font-weight: 500; }}

    .score {{
      font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; font-weight: 600;
      padding: 4px 10px; border-radius: 100px; white-space: nowrap; flex-shrink: 0;
    }}
    .score-high {{ background: #EEF3FF; color: #2F6BFF; }}
    .score-mid  {{ background: #F3F4F6; color: #6B7280; }}
    .score-low  {{ background: #F9FAFB; color: #9CA3AF; }}

    .summary {{ color: #3D4660; font-size: 0.875rem; line-height: 1.6; margin-bottom: 12px; }}

    .skills {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }}
    .skill {{
      font-size: 0.75rem; padding: 3px 9px; border-radius: 100px;
      background: #F3F4F6; color: #6B7280;
    }}
    .skill-match {{ background: #EEF3FF; color: #2F6BFF; }}
    .skill-gap   {{ background: #FFF7ED; color: #C2620A; }}

    .highlights {{ margin: 0 0 12px 16px; color: #3D4660; font-size: 0.85rem; line-height: 1.7; }}
    .fit {{ color: #3D4660; font-size: 0.875rem; line-height: 1.6; margin-bottom: 10px; }}
    .gaps-label {{ font-size: 0.75rem; font-weight: 600; color: #6B7280; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em; }}
  </style>
</head>
<body>
  <div class="hero">
    <div class="hero-inner">
      <div class="icon-wrap">{icon_img}</div>
      <div class="hero-text">
        <h1>AI Engineer <span>Job Digest</span></h1>
        <p>{len(ai_jobs)} verified roles &nbsp;·&nbsp; ranked by skill match &nbsp;·&nbsp; Last 24 hours</p>
      </div>
    </div>
  </div>
  <div class="content">
    {cards}
  </div>
</body>
</html>"""

html_path = Path(__file__).parent / "digest.html"
html_path.write_text(html, encoding="utf-8")

# ── Step 7: Open in browser ───────────────────────────────────────────────────

print("\nStep 7: Opening digest in browser...")
print(f"  Saved to: {html_path.resolve()}")
webbrowser.open(str(html_path.resolve()))
