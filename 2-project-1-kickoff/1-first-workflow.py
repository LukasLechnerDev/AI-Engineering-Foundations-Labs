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
    results_wanted=5,
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

icon_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" width="48" height="48" aria-hidden="true">
  <!-- Briefcase body -->
  <rect x="2" y="7" width="20" height="14" rx="2" stroke="#0B1020" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Handle -->
  <path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" stroke="#0B1020" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Horizontal divider -->
  <line x1="2" y1="13" x2="22" y2="13" stroke="#0B1020" stroke-width="2" stroke-linecap="round"/>
  <!-- Signal Blue clasp -->
  <rect x="10.5" y="11.5" width="3" height="3" rx="0.75" fill="#2F6BFF"/>
</svg>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Engineer Job Digest</title>
  <style>
    body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }}
    .header {{ display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }}
    h1 {{ color: #0B1020; margin: 0; }}
    .subtitle {{ color: #6B7280; margin-bottom: 32px; }}
    .card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .card h2 {{ margin: 0 0 6px; font-size: 1.1rem; }}
    .card a {{ color: #2F6BFF; text-decoration: none; }}
    .card a:hover {{ text-decoration: underline; }}
    .company {{ margin: 0 0 10px; color: #6B7280; font-weight: 600; font-size: 0.9rem; }}
    .reason {{ margin: 0; color: #444; font-size: 0.9rem; line-height: 1.5; }}
  </style>
</head>
<body>
  <div class="header">
    {icon_svg}
    <h1>AI Engineer Job Digest</h1>
  </div>
  <p class="subtitle">Found {len(ai_jobs)} verified AI engineering roles (from {len(df)} candidates)</p>
  {cards}
</body>
</html>"""

html_path = Path(__file__).parent / "digest.html"
html_path.write_text(html, encoding="utf-8")

# ── Step 5: Open in browser ───────────────────────────────────────────────────

print("\nStep 5: Opening digest in browser...")
print(f"  Saved to: {html_path.resolve()}")
webbrowser.open(str(html_path.resolve()))
