import json
import webbrowser
from pathlib import Path

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
    results_wanted=10,
)

df = pd.DataFrame(jobs)
print(f"  Scraped: {len(df)} jobs")

# ── Step 2: Filter ────────────────────────────────────────────────────────────

print("\nStep 2: Filtering...")

# Title must contain both "AI" and "Engineer"
mask = df["title"].str.contains("AI", case=False, na=False) & df["title"].str.contains(
    "Engineer", case=False, na=False
)
df = df[mask].copy()
print(f"  After title filter: {len(df)} jobs")

# Keep only rows that have a title, job URL, and description
required_columns = ["title", "job_url", "description"]
has_required = (
    df[required_columns]
    .fillna("")
    .apply(lambda col: col.astype(str).str.strip() != "")
    .all(axis=1)
)
df = df[has_required].copy()
print(f"  After required-fields check: {len(df)} jobs")

# Remove duplicate title + company pairs
df = df.drop_duplicates(subset=["title", "company"]).copy()
print(f"  After deduplication: {len(df)} jobs")

# ── Step 3: Classify with LLM ─────────────────────────────────────────────────

print("\nStep 3: Classifying with LLM...")

instructions = """
You classify whether a job posting is truly an AI Engineering role.

An AI Engineering role means building applications on top of foundation models or LLMs.
It is NOT traditional ML engineering, data science, MLOps, or platform/infrastructure work.

Set is_ai_engineering_role to true only when the core responsibility is building
AI-powered product features using foundation models. If ambiguous, set it to false.
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

for i, (_, job) in enumerate(df.iterrows(), start=1):
    print(f"  Classifying {i}/{len(df)}: {job['title']}")

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
df = pd.concat([df.reset_index(drop=True), results_df], axis=1)
ai_jobs = df[df["is_ai_engineering_role"]].copy()

print(f"\n  AI engineering roles: {len(ai_jobs)} / {len(df)} screened")

# ── Step 4: Render HTML ───────────────────────────────────────────────────────

print("\nStep 4: Rendering HTML digest...")

cards = ""
for _, job in ai_jobs.iterrows():
    company = job.get("company") or ""
    reason = job.get("reason") or ""
    cards += f"""
    <div class="card">
      <h2><a href="{job["job_url"]}" target="_blank">{job["title"]}</a></h2>
      <p class="company">{company}</p>
      <p class="reason">{reason}</p>
    </div>
"""

icon_img = '<img src="digest-icon.png" width="32" height="32" alt="" style="filter: brightness(0) invert(1);">'

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

    .hero {{
      background: #0B1020;
      padding: 40px;
    }}
    .hero-inner {{
      max-width: 800px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 18px;
    }}
    .icon-wrap {{
      background: #1A2236;
      border-radius: 12px;
      width: 56px;
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .hero-text h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem;
      font-weight: 600;
      color: #FFFFFF;
      line-height: 1.2;
    }}
    .hero-text h1 span {{
      color: #2F6BFF;
    }}
    .hero-text p {{
      color: #8FB2FF;
      font-size: 0.875rem;
      margin-top: 6px;
    }}
    .content {{
      max-width: 800px;
      margin: 36px auto;
      padding: 0 40px;
    }}

    .card {{
      background: white;
      border-radius: 10px;
      padding: 20px 24px;
      margin-bottom: 12px;
      border: 1px solid #8FB2FF;
    }}
    .card h2 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 4px;
    }}
    .card h2 a {{ color: #0B1020; text-decoration: none; }}
    .card h2 a:hover {{ color: #2F6BFF; }}
    .company {{ color: #6B7280; font-size: 0.825rem; font-weight: 500; margin-bottom: 10px; }}
    .reason {{ color: #3D4660; font-size: 0.875rem; line-height: 1.6; }}
  </style>
</head>
<body>
  <div class="hero">
    <div class="hero-inner">
      <div class="icon-wrap">{icon_img}</div>
      <div class="hero-text">
        <h1>AI Engineer <span>Job Digest</span></h1>
        <p>{len(ai_jobs)} verified roles &nbsp;·&nbsp; from {len(df)} candidates &nbsp;·&nbsp; Last 24 hours</p>
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

# ── Step 5: Open in browser ───────────────────────────────────────────────────

print("\nStep 5: Opening digest in browser...")
print(f"  Saved to: {html_path.resolve()}")
webbrowser.open(str(html_path.resolve()))
