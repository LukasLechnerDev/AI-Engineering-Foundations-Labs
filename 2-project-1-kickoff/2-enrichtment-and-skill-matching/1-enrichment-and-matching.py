import json
from html import escape
from pathlib import Path
from string import Template

import pandas as pd
from dotenv import load_dotenv
from jobspy import scrape_jobs
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Your profile — edit this to match your own background.
# In a later lesson we'll extract this automatically from a CV PDF.
USER_PROFILE = """
Skills: Python, LLMs, OpenAI API, FastAPI, Docker, REST APIs, Git
Experience: 3 years as a backend developer, 1 year building LLM-powered features
Education: Bachelor's in Computer Science
"""

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

scraped_jobs_df = pd.DataFrame(jobs)
print(f"  Scraped: {len(scraped_jobs_df)} jobs")

# ── Step 2: Filter ────────────────────────────────────────────────────────────

print("\nStep 2: Filtering...")

# Title must contain both "AI" and "Engineer"
mask = scraped_jobs_df["title"].str.contains(
    "AI", case=False, na=False
) & scraped_jobs_df["title"].str.contains("Engineer", case=False, na=False)
scraped_jobs_df = scraped_jobs_df[mask].copy()
print(f"  After title filter: {len(scraped_jobs_df)} jobs")

# Keep only rows that have a title, job URL, and description
required_columns = ["title", "job_url", "description"]
has_required = (
    scraped_jobs_df[required_columns]
    .fillna("")
    .apply(lambda col: col.astype(str).str.strip() != "")
    .all(axis=1)
)
scraped_jobs_df = scraped_jobs_df[has_required].copy()
print(f"  After required-fields check: {len(scraped_jobs_df)} jobs")

# Remove duplicate title + company pairs
scraped_jobs_df = scraped_jobs_df.drop_duplicates(subset=["title", "company"]).copy()
print(f"  After deduplication: {len(scraped_jobs_df)} jobs")

# ── Step 3: Classify with LLM ─────────────────────────────────────────────────

print("\nStep 3: Classifying with LLM...")

instructions = """
You classify whether a job posting is truly for an AI Engineering role.

AI Engineering definition:
- AI engineering means building applications on top of foundation models or in other words integrating them into products.
- Traditional ML engineering focuses on building, training, or tuning models; AI engineering primarily leverages existing models.
- MLOps and platform engineering are not AI engineering, as they focus on infrastructure and tooling rather than building AI-powered features.

Decision rules:
- Set is_ai_engineering_role to true when the main responsibility is building product or application features on top of foundation models or LLMs.
- Set is_ai_engineering_role to false when the role is mainly traditional software engineering, data science, analytics, ML research, model training, classical ML engineering, MLOps or platform work, or something else where AI application work is not the core responsibility.
- If the posting is ambiguous or unclear, set is_ai_engineering_role to false.
""".strip()

schema = {
    "type": "object",
    "properties": {
        "is_ai_engineering_role": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": ["is_ai_engineering_role", "reason"],
    "additionalProperties": False,
}

results = []

for i, (_, job) in enumerate(scraped_jobs_df.iterrows(), start=1):
    print(f"  Classifying {i}/{len(scraped_jobs_df)}: {job['title']}")

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
        text={
            "format": {
                "type": "json_schema",
                "name": "job_classification",
                "schema": schema,
                "strict": True,
            }
        },
    )

    results.append(json.loads(response.output_text))

results_df = pd.DataFrame(results)

# Add the classification columns next to the original job data.
scraped_jobs_df = pd.concat(
    [scraped_jobs_df.reset_index(drop=True), results_df], axis=1
)

# Keep only the rows classified as AI engineering roles.
classified_jobs = scraped_jobs_df[scraped_jobs_df["is_ai_engineering_role"]].copy()

print(
    f"\n  AI engineering roles: {len(classified_jobs)} / {len(scraped_jobs_df)} screened"
)

# ── Step 4: Extract required skills ───────────────────────────────────────────

print("\nStep 4: Extracting required skills...")

skill_categories = [
    "ai-engineering",
    "ml",
    "data",
    "backend",
    "cloud",
    "ops",
    "languages",
    "frontend",
    "other",
]

category_text = "\n".join(f"- {category}" for category in skill_categories)

skill_instructions = """
You extract required skills from AI engineering job postings.

Return concise normalized skill names like 'python', 'rag', 'sql', 'aws', or 'docker'.
Only include skills that are clearly important for the role.
Assign each skill to one of the provided categories.
""".strip()

skill_schema = {
    "type": "object",
    "properties": {
        "skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "skill": {"type": "string"},
                    "category": {"type": "string", "enum": skill_categories},
                },
                "required": ["skill", "category"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["skills"],
    "additionalProperties": False,
}

extracted_skills_per_job = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Extracting skills {i}/{len(classified_jobs)}: {job['title']}")

    prompt = f"""
Extract the required skills for this AI engineering job posting.

Use only these categories:
{category_text}

Description:
{job["description"]}
""".strip()

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=skill_instructions,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "ai_engineering_skill_extraction",
                "schema": skill_schema,
                "strict": True,
            },
        },
    )

    result = json.loads(response.output_text)
    extracted_skills_per_job.append(
        [
            {"skill": item["skill"].strip().lower(), "category": item["category"]}
            for item in result["skills"]
        ]
    )

classified_jobs = classified_jobs.reset_index(drop=True)
classified_jobs["extracted_skills"] = extracted_skills_per_job

# ── Step 5: Summary Enrichment ────────────────────────────────────────────────

print("\nStep 5: Generating summaries...")

summary_instructions = """
You write a 2-sentence summary of an AI engineering job posting.
Focus on the role's main responsibilities and the type of product or system being built.
""".strip()

summary_schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
    },
    "required": ["summary"],
    "additionalProperties": False,
}

summaries = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Summarizing {i}/{len(classified_jobs)}: {job['title']}")

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=summary_instructions,
        input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
        text={
            "format": {
                "type": "json_schema",
                "name": "job_summary",
                "schema": summary_schema,
                "strict": True,
            }
        },
    )

    summaries.append(json.loads(response.output_text)["summary"])

classified_jobs["summary"] = summaries

# ── Step 6: Highlights & Perks Enrichment ─────────────────────────────────────

print("\nStep 6: Extracting highlights and perks...")

highlights_instructions = """
You identify what makes a job posting stand out.
Return up to 3 short bullet points about perks, benefits, or unique selling points.
Focus on things that would excite a candidate: compensation, flexibility, mission, tech stack, growth, etc.
""".strip()

highlights_schema = {
    "type": "object",
    "properties": {
        "highlights": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["highlights"],
    "additionalProperties": False,
}

highlights_per_job = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Extracting highlights {i}/{len(classified_jobs)}: {job['title']}")

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=highlights_instructions,
        input=f"Title: {job['title']}\n\nDescription:\n{job['description']}",
        text={
            "format": {
                "type": "json_schema",
                "name": "job_highlights",
                "schema": highlights_schema,
                "strict": True,
            }
        },
    )

    highlights_per_job.append(json.loads(response.output_text)["highlights"])

classified_jobs["highlights"] = highlights_per_job

# ── Step 7: Skill Matching ────────────────────────────────────────────────────

print("\nStep 7: Matching skills against your profile...")

matching_instructions = """
You evaluate how well a candidate fits a job based on their profile and the required skills.

- matched_skills: the required skills the candidate has. Use semantic matching — treat equivalent
  terms as the same skill (e.g. "JS" and "JavaScript", "LLM" and "LLMs", "Postgres" and "PostgreSQL").
  Only return skills that appear in the required skills list.
- match_score: an integer from 0 to 100 reflecting overall fit, considering skills, experience level,
  and background — not just skill count.
- match_reasoning: 2–3 concise bullet points explaining why the candidate is or isn't a strong fit.
""".strip()

matching_schema = {
    "type": "object",
    "properties": {
        "matched_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "match_score": {"type": "integer"},
        "match_reasoning": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["matched_skills", "match_score", "match_reasoning"],
    "additionalProperties": False,
}

scores = []
matched_skills_per_job = []
match_reasoning_per_job = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Matching {i}/{len(classified_jobs)}: {job['title']}")

    required_skills = job["extracted_skills"] or []
    required_skill_names = [item["skill"] for item in required_skills]

    if not required_skill_names:
        scores.append(0)
        matched_skills_per_job.append(set())
        match_reasoning_per_job.append([])
        continue

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=matching_instructions,
        input=f"Candidate profile:\n{USER_PROFILE}\n\nRequired skills:\n{', '.join(required_skill_names)}",
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
    scores.append(result["match_score"])
    matched_skills_per_job.append(set(result["matched_skills"]))
    match_reasoning_per_job.append(result["match_reasoning"])

classified_jobs["match_score"] = scores
classified_jobs["matched_skills"] = matched_skills_per_job
classified_jobs["match_reasoning"] = match_reasoning_per_job

# Rank by score (highest first)
classified_jobs = classified_jobs.sort_values(
    "match_score", ascending=False
).reset_index(drop=True)

print(f"  Top score: {classified_jobs['match_score'].max()}")

# ── Step 8: Render HTML ───────────────────────────────────────────────────────

print("\nStep 8: Rendering HTML digest...")


def render_skill_groups(skills, matched_skills):
    grouped = {}
    for item in skills:
        grouped.setdefault(item["category"], []).append(item["skill"])

    groups_html = []
    for category in skill_categories:
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


cards = []
for _, job in classified_jobs.iterrows():
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
project_dir = Path(__file__).parent
html_template = Template(
    (project_dir / "digest-template.html").read_text(encoding="utf-8")
)
html = html_template.substitute(
    icon_img=icon_img,
    verified_role_count=len(classified_jobs),
    screened_job_count=len(scraped_jobs_df),
    cards="\n".join(cards),
)

# ── Step 9: Save HTML ─────────────────────────────────────────────────────────

print("\nStep 9: Saving digest...")

html_path = project_dir / "digest.html"
html_path.write_text(html, encoding="utf-8")
print(f"  Saved to: {html_path.resolve()}")
