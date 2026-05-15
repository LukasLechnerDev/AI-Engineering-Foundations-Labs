import json
import os
from html import escape
from string import Template

import pandas as pd
import resend
from dotenv import load_dotenv
from jobspy import scrape_jobs
from openai import OpenAI

load_dotenv()
client = OpenAI()
resend.api_key = os.environ["RESEND_API_KEY"]

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
    results_wanted=3,
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
        model="gpt-5.4-mini",
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
{"\n".join(f"- {category}" for category in skill_categories)}

Description:
{job["description"]}
""".strip()

    response = client.responses.create(
        model="gpt-5.4-mini",
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

classified_jobs["extracted_skills"] = extracted_skills_per_job

# ── Step 5: Render email HTML ─────────────────────────────────────────────────

print("\nStep 5: Rendering email HTML...")

card_template = Template(
    """
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:16px;background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;">
  <tr><td style="padding:20px;font-family:-apple-system,Segoe UI,sans-serif;">
    <a href="$job_url" style="font-size:18px;font-weight:600;color:#2F6BFF;text-decoration:none;">$title</a>
    <div style="color:#6B7280;font-size:14px;margin-top:4px;">$company</div>
    <p style="color:#0B1020;font-size:14px;line-height:1.5;margin:12px 0;">$reason</p>
    <div>$skill_chips</div>
  </td></tr>
</table>
""".strip()
)


def render_skill_chips(skills):
    return "".join(
        '<span style="display:inline-block;background:#E7EDF7;color:#0B1020;'
        "font-size:12px;padding:4px 10px;border-radius:12px;margin:2px 4px 2px 0;"
        f'font-family:-apple-system,Segoe UI,sans-serif;">{escape(item["skill"])}</span>'
        for item in skills
    )


cards = []
for _, job in classified_jobs.iterrows():
    cards.append(
        card_template.substitute(
            job_url=escape(job["job_url"]),
            title=escape(job["title"]),
            company=escape(job["company"]),
            reason=escape(job["reason"]),
            skill_chips=render_skill_chips(job["extracted_skills"]),
        )
    )

html = f"""
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FAFBFD;padding:32px 0;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" border="0">
      <tr><td style="font-family:-apple-system,Segoe UI,sans-serif;color:#0B1020;">
        <h1 style="font-size:24px;margin:0 0 8px 0;">AI Engineer Job Digest</h1>
        <p style="color:#6B7280;margin:0 0 24px 0;">{len(classified_jobs)} roles found today</p>
        {"".join(cards)}
      </td></tr>
    </table>
  </td></tr>
</table>
"""

# ── Step 6: Send email ────────────────────────────────────────────────────────

print("\nStep 6: Sending email...")

params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["office@lukaslechner.com"],
    "subject": "AI Engineer job digest",
    "html": html,
}

email = resend.Emails.send(params)
print(email)
