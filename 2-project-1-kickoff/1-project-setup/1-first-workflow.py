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

# ── Step 4: Render HTML ───────────────────────────────────────────────────────

print("\nStep 4: Rendering HTML digest...")

card_template = Template(
    """
<div class="card">
  <h2><a href="$job_url" target="_blank">$title</a></h2>
  <p class="company">$company</p>
  <p class="reason">$reason</p>
</div>
""".strip()
)

cards = []
for _, job in classified_jobs.iterrows():
    cards.append(
        card_template.substitute(
            job_url=escape(job.get("job_url") or ""),
            title=escape(job.get("title") or ""),
            company=escape(job.get("company") or ""),
            reason=escape(job.get("reason") or ""),
        )
    )

icon_img = '<img src="digest-icon.png" width="32" height="32" alt="" style="filter: brightness(0) invert(1);">'
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

# ── Step 5: Save HTML ─────────────────────────────────────────────────────────

print("\nStep 5: Saving digest...")

html_path = project_dir / "digest.html"
html_path.write_text(html, encoding="utf-8")
