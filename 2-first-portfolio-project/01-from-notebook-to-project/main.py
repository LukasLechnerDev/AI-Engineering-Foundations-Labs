import json
from pathlib import Path
from textwrap import dedent

import pandas as pd
from dotenv import load_dotenv
from jobspy import scrape_jobs
from openai import OpenAI


def main():
    load_dotenv(override=True)
    client = OpenAI()

    print("=== AI Engineer Job Agent ===")

    # === Step 1: Scrape AI Engineer jobs ===

    print("\n--- Step 1: Scraping jobs ---")
    jobs = scrape_jobs(
        site_name=["linkedin", "indeed"],
        linkedin_fetch_description=True,
        search_term='"AI Engineer"',
        location="USA",
        country_indeed="USA",
        job_type="fulltime",
        hours_old=72,
        results_wanted=5,
    )

    jobs_df = pd.DataFrame(jobs)
    print(f"Total jobs scraped: {len(jobs_df)}")

    # Keep only jobs that have title, job URL, and description.
    print("Filtering out jobs with missing title, URL, or description...")
    required_columns = ["title", "job_url", "description"]
    has_required_values = (
        jobs_df[required_columns]
        .fillna("")
        .apply(lambda column: column.astype(str).str.strip() != "")
        .all(axis=1)
    )
    jobs_df = jobs_df[has_required_values].copy()
    print(f"Jobs with required fields: {len(jobs_df)}")

    # Title must contain both "AI" and "Engineer".
    print("Keeping only jobs whose title contains both 'AI' and 'Engineer'...")
    title_contains_ai = jobs_df["title"].str.contains("AI", case=False, na=False)
    title_contains_engineer = jobs_df["title"].str.contains(
        "Engineer", case=False, na=False
    )
    jobs_df = jobs_df[title_contains_ai & title_contains_engineer].copy()
    print(f"Jobs after title filter: {len(jobs_df)}")

    # Drop duplicate title/company pairs.
    print("Removing duplicate title/company pairs...")
    jobs_df = jobs_df.drop_duplicates(subset=["title", "company"]).copy()
    print(f"Jobs after deduplication: {len(jobs_df)}")

    # === Step 2: Classify whether each job is an AI Engineer role ===

    print("\n--- Step 2: Classifying jobs ---")

    classify_instructions = dedent("""
        You classify whether a job posting is truly for an AI Engineering role.

        AI Engineering definition:
        - AI engineering means building applications on top of foundation models or in other words integrating them into products.
        - Traditional ML engineering focuses on building, training, or tuning models; AI engineering primarily leverages existing models.
        - MLOps and platform engineering are not AI engineering, as they focus on infrastructure and tooling rather than building AI-powered features.

        Decision rules:
        - Set is_ai_engineering_role to true when the main responsibility is building product or application features on top of foundation models or LLMs.
        - Set is_ai_engineering_role to false when the role is mainly traditional software engineering, data science, analytics, ML research, model training, classical ML engineering, MLOps or platform work, or something else where AI application work is not the core responsibility.
        - If the posting is ambiguous or unclear, set is_ai_engineering_role to false.
        - In reason, briefly explain the main evidence for the decision in one sentence.
    """)

    classify_schema = {
        "type": "object",
        "properties": {
            "is_ai_engineering_role": {"type": "boolean"},
            "reason": {"type": "string"},
        },
        "required": ["is_ai_engineering_role", "reason"],
        "additionalProperties": False,
    }

    ai_engineering_jobs = []
    for i, (_, job) in enumerate(jobs_df.iterrows(), start=1):
        title = job["title"]
        description = job["description"]
        job_url = job["job_url"]

        print(f"Classifying job {i}/{len(jobs_df)}: {title}")

        classify_response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=classify_instructions,
            input=f"Classify this job posting.\n\nTitle: {title}\n\nDescription:\n{description}",
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ai_engineering_job_screening",
                    "schema": classify_schema,
                    "strict": True,
                },
                "verbosity": "low",
            },
        )
        classification = json.loads(classify_response.output_text)

        if classification["is_ai_engineering_role"]:
            print(f"  -> Kept (AI Engineer): {classification['reason']}")
            ai_engineering_jobs.append(
                {"title": title, "job_url": job_url, "description": description}
            )
        else:
            print(f"  -> Skipped (not AI Engineer): {classification['reason']}")

    print(
        f"\n{len(ai_engineering_jobs)}/{len(jobs_df)} jobs classified as AI engineering roles"
    )

    # === Step 3: Extract required skills for the remaining jobs ===

    print("\n--- Step 3: Extracting required skills ---")

    skill_categories = [
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

    skills_instructions = dedent(f"""
        You extract required skills from AI engineering job postings.

        Return concise normalized skill names like 'python', 'rag', 'langchain', 'aws', or 'docker'.
        Return all skill names in lowercase.

        Only include skills that are clearly important for the role.

        Assign each skill to one of these categories:
        {", ".join(skill_categories)}
    """)

    skills_schema = {
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

    results = []
    for i, job in enumerate(ai_engineering_jobs, start=1):
        print(
            f"Extracting skills for job {i}/{len(ai_engineering_jobs)}: {job['title']}"
        )

        skills_response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=skills_instructions,
            input=job["description"],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ai_engineering_skill_extraction",
                    "schema": skills_schema,
                    "strict": True,
                },
                "verbosity": "low",
            },
        )
        skills = json.loads(skills_response.output_text)["skills"]
        print(f"  -> Extracted {len(skills)} skills")

        results.append(
            {"title": job["title"], "job_url": job["job_url"], "skills": skills}
        )

    # === Step 4: Render results as a simple HTML file ===

    print("\n--- Step 4: Rendering HTML report ---")
    cards = []
    for job in results:
        # Group skills by category.
        skills_by_category = {}
        for skill in job["skills"]:
            skills_by_category.setdefault(skill["category"], []).append(skill["skill"])

        category_blocks = []
        for category in skill_categories:
            if category not in skills_by_category:
                continue
            skill_chips = "".join(
                f'<span class="chip">{name}</span>'
                for name in skills_by_category[category]
            )
            category_blocks.append(
                f'<div class="category"><h3>{category}</h3>'
                f'<div class="chips">{skill_chips}</div></div>'
            )

        cards.append(
            f"""
            <article class="card">
                <h2><a href="{job["job_url"]}" target="_blank">{job["title"]}</a></h2>
                {"".join(category_blocks)}
            </article>
            """
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Engineer Job Agent Report</title>
<style>
  :root {{
    --paper: #FAFBFD;
    --mist: #E7EDF7;
    --ink: #0B1020;
    --slate: #6B7280;
    --signal: #2F6BFF;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 2.5rem 1.5rem;
    background: var(--paper);
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.5;
  }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  header {{ margin-bottom: 2rem; }}
  header h1 {{ margin: 0 0 0.25rem; font-size: 2rem; }}
  header p {{ margin: 0; color: var(--slate); }}
  .grid {{
    display: grid;
    gap: 1.25rem;
    grid-template-columns: 1fr;
  }}
  .card {{
    background: white;
    border: 1px solid var(--mist);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 2px rgba(11, 16, 32, 0.04);
  }}
  .card h2 {{ margin: 0 0 1rem; font-size: 1.15rem; line-height: 1.35; }}
  .card h2 a {{ color: var(--ink); text-decoration: none; }}
  .card h2 a:hover {{ color: var(--signal); }}
  .category {{ margin-top: 0.75rem; }}
  .category h3 {{
    margin: 0 0 0.4rem;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--slate);
  }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}
  .chip {{
    background: var(--mist);
    color: var(--ink);
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.8rem;
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>AI Engineer Job Agent Report</h1>
    <p>{len(results)} matching job{"s" if len(results) != 1 else ""}</p>
  </header>
  <div class="grid">
    {"".join(cards)}
  </div>
</div>
</body>
</html>
"""

    output_path = Path(__file__).parent / "job-agent-report.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Saved report with {len(results)} jobs to {output_path}")
    print("\nDone!")


if __name__ == "__main__":
    main()
