import json
import os
from datetime import date
from html import escape
from pathlib import Path
from string import Template

import pandas as pd
import resend
from dotenv import load_dotenv
from jobspy import scrape_jobs
from openai import OpenAI

load_dotenv()

client = OpenAI()

SEND_EMAIL = os.getenv("SEND_EMAIL", "true").lower() in {"1", "true", "yes"}
OUTPUT_FILE = Path(__file__).with_name("digest.html")
REPORT_DATE = date.today()
CALENDAR_WEEK = REPORT_DATE.isocalendar().week

STUDENT_PROFILE = {
    "skills": [
        "python",
        "backend development",
        "rest apis",
        "sql",
        "testing",
        "pytest",
        "openai api",
        "llm apis",
        "prompt engineering",
        "structured outputs",
        "tool calling",
        "ai workflow automation",
        "pydantic",
        "caching",
        "logging",
        "evaluations",
        "llm as a judge",
        "observability",
        "langfuse",
        "docker",
        "aws",
        "agentic workflows",
    ],
    "languages": ["German", "English"],
    "minimum_salary": {
        "monthly_eur": 4000,
        "yearly_eur": 80000,
    },
    "work_preferences": {
        "remote": "Remote work is acceptable for companies in Europe.",
        "hybrid": "Hybrid work is acceptable for companies in and around Vienna.",
        "on_site": "Fully on-site roles are not preferred.",
    },
    "additional_preferences": (
        "I want to work for a company that has a positive impact for the world."
    ),
}


def normalize_skill(skill):
    return str(skill).strip().lower()


def get_skill_name(skill):
    if isinstance(skill, dict):
        return str(skill.get("skill", "")).strip()
    return str(skill).strip()


def get_skill_category(skill):
    if isinstance(skill, dict):
        return str(skill.get("category", "")).strip()
    return ""


def format_category(category):
    return category.replace("-", " ") if category else "uncategorized"


def format_skill_with_category(skill, categories_by_skill=None):
    skill_name = get_skill_name(skill)
    category = get_skill_category(skill)

    if not category and categories_by_skill:
        category = categories_by_skill.get(normalize_skill(skill_name), "")

    if category:
        return f"{skill_name} ({format_category(category)})"
    return skill_name


def render_skill_list_with_categories(skills, skill_items):
    categories_by_skill = {
        normalize_skill(get_skill_name(item)): get_skill_category(item)
        for item in skill_items
        if get_skill_name(item)
    }
    labels = [
        format_skill_with_category(skill, categories_by_skill)
        for skill in skills
        if get_skill_name(skill)
    ]
    return ", ".join(labels) if labels else "none"


def render_skill_chips(skills, matched_skills=None, partial_skills=None):
    matched = {normalize_skill(skill) for skill in (matched_skills or [])}
    partial = {normalize_skill(skill) for skill in (partial_skills or [])}

    grouped_skills = {}
    for skill in skills:
        skill_name = get_skill_name(skill)
        if not skill_name:
            continue
        category = get_skill_category(skill) or "other"
        grouped_skills.setdefault(category, []).append(skill)

    category_order = {
        category: index for index, category in enumerate(globals().get("skill_categories", []))
    }

    def match_rank(skill):
        normalized = normalize_skill(get_skill_name(skill))

        if normalized in matched:
            return 0
        if normalized in partial:
            return 1
        return 2

    def chip_style(skill):
        normalized = normalize_skill(get_skill_name(skill))

        if normalized in matched:
            return "#15803D", "#FFFFFF", "#166534"
        if normalized in partial:
            return "#ECFDF5", "#166534", "#A7F3D0"
        return "#FFFFFF", "#475569", "#CBD5E1"

    def render_chip(skill):
        colors = chip_style(skill)
        return (
            '<span style="display:inline-block;'
            f"background:{colors[0]};"
            f"color:{colors[1]};"
            f"border:1px solid {colors[2]};"
            "font-size:12px;font-weight:500;padding:5px 10px;border-radius:999px;margin:3px 5px 3px 0;"
            f'font-family:-apple-system,Segoe UI,sans-serif;">{safe_escape(get_skill_name(skill))}</span>'
        )

    rows = []
    for category, category_skills in sorted(
        grouped_skills.items(),
        key=lambda item: category_order.get(item[0], len(category_order)),
    ):
        rows.append(
            (
                '<tr>'
                '<td valign="top" style="width:150px;padding:7px 12px 5px 0;'
                'font-family:-apple-system,Segoe UI,sans-serif;font-size:12px;'
                'font-weight:700;text-transform:uppercase;letter-spacing:0.04em;'
                'color:#64748B;line-height:1.4;">'
                f"{safe_escape(format_category(category))}"
                "</td>"
                '<td valign="top" style="padding:2px 0 5px 0;">'
                f"{''.join(render_chip(skill) for skill in sorted(category_skills, key=match_rank))}"
                "</td>"
                "</tr>"
            )
        )

    if not rows:
        return ""

    return (
        '<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
        f"{''.join(rows)}"
        "</table>"
    )


def render_match_notes(match_decisions):
    notes = [
        item
        for item in match_decisions
        if item["match_type"] in {"equivalent", "closely_related", "partial"}
    ][:3]

    if not notes:
        return ""

    rows = "".join(
        '<span style="display:inline-block;'
        "font-size:12px;color:#6B7280;margin:0 8px 4px 0;"
        f'font-family:-apple-system,Segoe UI,sans-serif;">'
        f'{safe_escape(item["required_skill"])} -> {safe_escape(item["matched_profile_skill"])}</span>'
        for item in notes
    )
    return f'<div style="margin-top:8px;">{rows}</div>'


def safe_escape(value):
    if pd.isna(value):
        return ""
    return escape(str(value))


def render_inline_list(items):
    cleaned = [str(item).strip() for item in items if str(item).strip()]

    if not cleaned:
        return "None listed"

    return safe_escape(", ".join(cleaned[:4]))


def render_highlights_and_benefits(highlights, benefits):
    combined = []

    for item in list(highlights) + list(benefits):
        value = str(item).strip()
        if value and value not in combined:
            combined.append(value)

    return render_inline_list(combined)


APPLICATION_DECISIONS = [
    "Apply this week",
    "Consider applying",
    "Use as learning target",
    "Skip for now",
]

APPLICATION_DECISION_RANK = {
    decision: index for index, decision in enumerate(APPLICATION_DECISIONS)
}


def collect_salary_context(job):
    salary_columns = [
        "min_amount",
        "max_amount",
        "interval",
        "currency",
        "salary_source",
        "salary",
        "compensation",
    ]
    values = {}

    for column in salary_columns:
        if column in job and not pd.isna(job[column]):
            values[column] = str(job[column])

    if not values:
        return "No structured salary fields were provided by the scraper."

    return json.dumps(values, indent=2)


def format_location(job):
    location = job.get("location")
    title = str(job.get("title") or "")
    description = str(job.get("description") or "")
    location_text = "" if pd.isna(location) else str(location).strip()
    searchable_text = f"{title} {location_text} {description}".lower()

    if "remote" in searchable_text:
        return "Remote"
    if "hybrid" in searchable_text:
        return "Hybrid"
    if location_text:
        return location_text
    return ""


def calculate_match(match_decisions):
    weights = {
        "equivalent": 1.0,
        "closely_related": 1.0,
        "partial": 0.5,
        "none": 0.0,
    }

    if not match_decisions:
        return {
            "fit_score": 0,
            "matched_required_skills": [],
            "partial_required_skills": [],
            "missing_skills": [],
        }

    score = sum(weights[item["match_type"]] for item in match_decisions)
    fit_score = round((score / len(match_decisions)) * 100)

    matched = [
        item["required_skill"]
        for item in match_decisions
        if item["match_type"] in {"equivalent", "closely_related"}
    ]
    partial = [
        item["required_skill"]
        for item in match_decisions
        if item["match_type"] == "partial"
    ]
    missing = [
        item["required_skill"]
        for item in match_decisions
        if item["match_type"] in {"partial", "none"}
    ]

    return {
        "fit_score": fit_score,
        "matched_required_skills": matched,
        "partial_required_skills": partial,
        "missing_skills": missing[:5],
    }


# ── Step 1: Scrape ────────────────────────────────────────────────────────────

print("Step 1: Scraping jobs...")

jobs = scrape_jobs(
    site_name=["indeed", "linkedin"],
    linkedin_fetch_description=True,
    search_term='"AI Engineer"',
    location="Austria",
    country_indeed="Austria",
    job_type="fulltime",
    hours_old=48,
    results_wanted=100,
)

scraped_jobs_df = pd.DataFrame(jobs)
print(f"  Scraped: {len(scraped_jobs_df)} jobs")

# ── Step 2: Filter ────────────────────────────────────────────────────────────

print("\nStep 2: Filtering...")

mask = scraped_jobs_df["title"].str.contains(
    "AI", case=False, na=False
) & scraped_jobs_df["title"].str.contains("Engineer", case=False, na=False)
scraped_jobs_df = scraped_jobs_df[mask].copy()
print(f"  After title filter: {len(scraped_jobs_df)} jobs")

required_columns = ["title", "job_url", "description"]
has_required = (
    scraped_jobs_df[required_columns]
    .fillna("")
    .apply(lambda col: col.astype(str).str.strip() != "")
    .all(axis=1)
)
scraped_jobs_df = scraped_jobs_df[has_required].copy()
print(f"  After required-fields check: {len(scraped_jobs_df)} jobs")

scraped_jobs_df = scraped_jobs_df.drop_duplicates(subset=["title", "company"]).copy()
print(f"  After deduplication: {len(scraped_jobs_df)} jobs")

# ── Step 3: Classify with LLM ─────────────────────────────────────────────────

print("\nStep 3: Classifying with LLM...")

classification_instructions = """
You classify whether a job posting is truly for an AI Engineering role.

AI Engineering definition:
- AI engineering means building applications on top of foundation models or integrating them into products.
- Traditional ML engineering focuses on building, training, or tuning models.
- MLOps and platform engineering focus on infrastructure and tooling, not AI-powered product features.

Decision rules:
- Set is_ai_engineering_role to true when the main responsibility is building product or application features on top of foundation models or LLMs.
- Set is_ai_engineering_role to false when the role is mainly traditional software engineering, data science, analytics, ML research, model training, classical ML engineering, MLOps, or platform work.
- If the posting is ambiguous or unclear, set is_ai_engineering_role to false.
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

for i, (_, job) in enumerate(scraped_jobs_df.iterrows(), start=1):
    print(f"  Classifying {i}/{len(scraped_jobs_df)}: {job['title']}")

    response = client.responses.create(
        model="gpt-5.4-mini",
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

results_df = pd.DataFrame(classification_results)
scraped_jobs_df = pd.concat(
    [scraped_jobs_df.reset_index(drop=True), results_df], axis=1
)
classified_jobs = scraped_jobs_df[scraped_jobs_df["is_ai_engineering_role"]].copy()

print(
    f"\n  AI engineering roles: {len(classified_jobs)} / {len(scraped_jobs_df)} screened"
)

# ── Step 4: Enrich jobs with LLM ──────────────────────────────────────────────

print("\nStep 4: Enriching jobs with LLM...")

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

app_categories = [
    "workflow-automation",
    "rag-knowledge-assistant",
    "document-processing",
    "decision-support",
    "customer-assistant",
    "content-generation",
    "agentic-system",
    "voice-or-multimodal",
    "other",
]

company_domains = [
    "finance",
    "healthcare",
    "ecommerce",
    "hr-recruiting",
    "legal",
    "education",
    "developer-tools",
    "enterprise-software",
    "cybersecurity",
    "manufacturing",
    "logistics",
    "media",
    "government",
    "consulting",
    "other",
    "unknown",
]

skill_category_list = "\n".join(f"- {category}" for category in skill_categories)
app_category_list = "\n".join(f"- {category}" for category in app_categories)
company_domain_list = "\n".join(f"- {domain}" for domain in company_domains)

enrichment_instructions = """
You enrich AI engineering job postings for a concise job digest.

Extract only information supported by the posting.
Use concise normalized skill names like 'python', 'rag', 'sql', 'aws', or 'docker'.
Return a short, faithful job summary and a separate company summary.
If the posting does not describe the company, set company_summary to "Not enough company information in the posting."
Extract notable highlights, uncommon perks, and benefits only when the posting clearly states them.
For salary, use the provided structured salary fields or explicit compensation text from the posting. If no salary is listed, return "Not listed".
""".strip()

enrichment_schema = {
    "type": "object",
    "properties": {
        "job_summary": {"type": "string"},
        "company_summary": {"type": "string"},
        "salary": {"type": "string"},
        "highlights": {
            "type": "array",
            "items": {"type": "string"},
        },
        "benefits": {
            "type": "array",
            "items": {"type": "string"},
        },
        "responsibilities": {
            "type": "array",
            "items": {"type": "string"},
        },
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
        },
        "app_category": {"type": "string", "enum": app_categories},
        "company_domain": {"type": "string", "enum": company_domains},
        "seniority": {
            "type": "string",
            "enum": ["junior", "mid-level", "senior", "staff", "unknown"],
        },
    },
    "required": [
        "job_summary",
        "company_summary",
        "salary",
        "highlights",
        "benefits",
        "responsibilities",
        "skills",
        "app_category",
        "company_domain",
        "seniority",
    ],
    "additionalProperties": False,
}

enrichments = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Enriching {i}/{len(classified_jobs)}: {job['title']}")

    prompt = f"""
Enrich this AI engineering job posting.

Use only these skill categories:
{skill_category_list}

Use only these AI app categories:
{app_category_list}

Use only these company domains:
{company_domain_list}

Title: {job["title"]}
Company: {job["company"]}

Structured salary fields from scraper:
{collect_salary_context(job)}

Description:
{job["description"]}
""".strip()

    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=enrichment_instructions,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "job_enrichment",
                "schema": enrichment_schema,
                "strict": True,
            },
        },
    )

    result = json.loads(response.output_text)
    result["skills"] = [
        {
            "skill": normalize_skill(item["skill"]),
            "category": item["category"],
        }
        for item in result["skills"]
    ]
    enrichments.append(result)

classified_jobs["job_summary"] = [item["job_summary"] for item in enrichments]
classified_jobs["company_summary"] = [item["company_summary"] for item in enrichments]
classified_jobs["salary"] = [item["salary"] for item in enrichments]
classified_jobs["highlights"] = [item["highlights"] for item in enrichments]
classified_jobs["benefits"] = [item["benefits"] for item in enrichments]
classified_jobs["responsibilities"] = [item["responsibilities"] for item in enrichments]
classified_jobs["extracted_skills"] = [item["skills"] for item in enrichments]
classified_jobs["app_category"] = [item["app_category"] for item in enrichments]
classified_jobs["company_domain"] = [item["company_domain"] for item in enrichments]
classified_jobs["seniority"] = [item["seniority"] for item in enrichments]

# ── Step 5: Match jobs against student profile ────────────────────────────────

print("\nStep 5: Matching jobs against student profile...")

skill_match_instructions = """
You semantically match required job skills to a student's profile skills.

Rules:
- Return exactly one match decision for every required skill.
- Be conservative. Do not match skills just because they are both technical.
- Match provider-specific skills to broader profile skills when appropriate, for example OpenAI API to LLM APIs.
- Match cloud subservices to the broader cloud provider when appropriate, for example ECS Fargate or S3 to AWS.
- Match testing tools to testing when appropriate, for example pytest to testing.
- Do not match different concepts, for example RAG to LLM APIs, Docker to Kubernetes, or prompt engineering to fine-tuning.
""".strip()

match_types = ["equivalent", "closely_related", "partial", "none"]

skill_match_schema = {
    "type": "object",
    "properties": {
        "matches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "required_skill": {"type": "string"},
                    "matched_profile_skill": {
                        "type": ["string", "null"],
                    },
                    "match_type": {"type": "string", "enum": match_types},
                    "confidence": {"type": "number"},
                    "reason": {"type": "string"},
                },
                "required": [
                    "required_skill",
                    "matched_profile_skill",
                    "match_type",
                    "confidence",
                    "reason",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["matches"],
    "additionalProperties": False,
}

match_results = []
all_match_decisions = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Matching {i}/{len(classified_jobs)}: {job['title']}")

    required_skills = [item["skill"] for item in job["extracted_skills"]]

    prompt = f"""
Match these required job skills against the student profile skills.

Required job skills:
{json.dumps(required_skills, indent=2)}

Student profile skills:
{json.dumps(STUDENT_PROFILE["skills"], indent=2)}
""".strip()

    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=skill_match_instructions,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "semantic_skill_matching",
                "schema": skill_match_schema,
                "strict": True,
            },
        },
    )

    result = json.loads(response.output_text)
    decisions_by_skill = {
        normalize_skill(item["required_skill"]): item for item in result["matches"]
    }

    match_decisions = []
    for required_skill in required_skills:
        decision = decisions_by_skill.get(normalize_skill(required_skill))
        if decision is None:
            decision = {
                "required_skill": required_skill,
                "matched_profile_skill": None,
                "match_type": "none",
                "confidence": 0,
                "reason": "The model did not return a decision for this skill.",
            }
        else:
            decision["required_skill"] = required_skill

        match_decisions.append(decision)

    all_match_decisions.append(match_decisions)
    match_results.append(calculate_match(match_decisions))

classified_jobs["fit_score"] = [item["fit_score"] for item in match_results]
classified_jobs["matched_required_skills"] = [
    item["matched_required_skills"] for item in match_results
]
classified_jobs["partial_required_skills"] = [
    item["partial_required_skills"] for item in match_results
]
classified_jobs["missing_skills"] = [item["missing_skills"] for item in match_results]
classified_jobs["skill_match_decisions"] = all_match_decisions

# ── Step 6: Overall match with LLM ────────────────────────────────────────────

print("\nStep 6: Calculating overall match with LLM...")

overall_match_instructions = """
You evaluate how a student should prioritize an AI engineering job application.

Consider:
- required skills
- responsibilities
- seniority
- role type
- AI app category
- company domain
- student languages
- salary requirements
- remote, hybrid, and on-site work preferences
- additional free-form student preferences
- skill match results

Decision categories:
- Apply this week: strong role fit, enough matched skills, aligned with student requirements, worth near-term application effort.
- Consider applying: plausible fit with useful upside, but has notable gaps or uncertainty.
- Use as learning target: not a near-term application priority, but useful for identifying skills to build.
- Skip for now: weak fit, wrong role type, poor alignment, or too many critical gaps.

Rules:
- Return an overall match score from 0 to 100.
- Be conservative and grounded in the provided data.
- Do not invent facts about the student, company, or role.
- Do not mention numeric scores or percentages in the reasoning.
- Treat listed salaries below the student's minimum as a significant negative signal.
- If salary is not listed, do not reject the job for salary alone, but mention salary uncertainty when relevant.
- Treat language requirements outside the student's languages as a significant negative signal.
- Treat remote roles at European companies and hybrid roles around Vienna as location-compatible.
- Treat fully on-site roles as a negative signal unless the posting is otherwise unusually strong.
- Consider additional free-form student preferences when the posting provides enough evidence.
- Choose exactly one decision category.
- The reason must explain why that decision category was chosen.
- The mismatch summary must cover the most important profile/job mismatches, not just missing skills.
- The mismatch summary may mention skill gaps, seniority, salary, language, work mode, location, or additional preferences.
- If there is no important mismatch, set the mismatch summary to "No major mismatch."
- Keep the reason under 70 words.
- Keep the mismatch summary under 35 words.
- Keep the next step under 20 words.
""".strip()

overall_match_schema = {
    "type": "object",
    "properties": {
        "overall_match_score": {"type": "integer"},
        "application_decision": {
            "type": "string",
            "enum": APPLICATION_DECISIONS,
        },
        "application_decision_reason": {"type": "string"},
        "mismatch_summary": {"type": "string"},
        "next_step": {"type": "string"},
    },
    "required": [
        "overall_match_score",
        "application_decision",
        "application_decision_reason",
        "mismatch_summary",
        "next_step",
    ],
    "additionalProperties": False,
}

overall_matches = []

for i, (_, job) in enumerate(classified_jobs.iterrows(), start=1):
    print(f"  Overall matching {i}/{len(classified_jobs)}: {job['title']}")

    prompt = f"""
Evaluate the overall match between this job and the student profile.

Job:
- title: {job["title"]}
- company: {job["company"]}
- location: {format_location(job)}
- raw_location: {job.get("location")}
- company_domain: {job["company_domain"]}
- seniority: {job["seniority"]}
- app_category: {job["app_category"]}
- salary: {job["salary"]}
- job_summary: {job["job_summary"]}
- company_summary: {job["company_summary"]}
- responsibilities: {json.dumps(job["responsibilities"], indent=2)}
- highlights: {json.dumps(job["highlights"], indent=2)}
- benefits: {json.dumps(job["benefits"], indent=2)}
- required_skills: {json.dumps([item["skill"] for item in job["extracted_skills"]], indent=2)}
- posting_description: {job["description"]}

Student profile:
{json.dumps(STUDENT_PROFILE, indent=2)}

Skill match result:
- skill_match_score_internal: {job["fit_score"]}
- matched_required_skills: {job["matched_required_skills"]}
- partial_required_skills: {job["partial_required_skills"]}
- missing_skills: {job["missing_skills"]}
- skill_match_decisions: {json.dumps(job["skill_match_decisions"], indent=2)}
""".strip()

    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=overall_match_instructions,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "overall_job_match",
                "schema": overall_match_schema,
                "strict": True,
            },
        },
    )

    overall_matches.append(json.loads(response.output_text))

classified_jobs["overall_match_score"] = [
    max(0, min(100, int(item["overall_match_score"]))) for item in overall_matches
]
classified_jobs["application_decision"] = [
    item["application_decision"]
    if item["application_decision"] in APPLICATION_DECISIONS
    else "Skip for now"
    for item in overall_matches
]
classified_jobs["application_decision_reason"] = [
    item["application_decision_reason"] for item in overall_matches
]
classified_jobs["mismatch_summary"] = [
    item["mismatch_summary"] for item in overall_matches
]
classified_jobs["next_step"] = [item["next_step"] for item in overall_matches]
classified_jobs["application_decision_rank"] = [
    APPLICATION_DECISION_RANK[decision]
    for decision in classified_jobs["application_decision"]
]

classified_jobs = classified_jobs.sort_values(
    by=["application_decision_rank", "overall_match_score", "fit_score"],
    ascending=[True, False, False],
).reset_index(drop=True)

# ── Step 7: Render email HTML ─────────────────────────────────────────────────

print("\nStep 7: Rendering email HTML...")

card_template = Template(
    """
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="margin-bottom:16px;background-color:#FFFFFF;border:1px solid #e5e7eb;border-radius:8px;">
  <tr>
    <td valign="top" style="padding:20px;font-family:-apple-system,Segoe UI,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td valign="top">
            <table cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td valign="top" style="padding-right:12px;">
                  <span style="display:inline-block;background-color:#1D4ED8;color:#FFFFFF;border:1px solid #1E40AF;font-size:13px;font-weight:700;line-height:1;padding:8px 10px;border-radius:999px;">#$rank</span>
                </td>
                <td valign="top">
                  <a href="$job_url" style="font-size:18px;font-weight:600;color:#1D4ED8;text-decoration:none;">$title</a>
                  <div style="color:#6B7280;font-size:14px;margin-top:4px;">$company · $location</div>
                </td>
              </tr>
            </table>
          </td>
          <td width="190" valign="top" align="right">
            <span style="display:inline-block;background-color:#1D4ED8;color:#FFFFFF;border:1px solid #1E40AF;font-size:13px;font-weight:700;padding:7px 10px;border-radius:999px;white-space:nowrap;">$application_decision</span>
          </td>
        </tr>
      </table>
      <div style="margin-top:18px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>Role:</strong> $job_summary</div>
      <div style="margin-top:12px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>Company:</strong> $company_summary</div>
      <div style="margin-top:12px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>Salary:</strong> $salary</div>
      <div style="margin-top:12px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>Highlights & benefits:</strong> $highlights_and_benefits</div>
      <div style="margin-top:14px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>Why $application_decision:</strong> $application_decision_reason</div>
      <div style="margin-top:12px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>What doesn't fit:</strong> $mismatch_summary</div>
      <div style="margin-top:16px;color:#0B1020;font-size:14px;line-height:1.5;"><strong>Skill match</strong></div>
      <div style="margin-top:6px;">$matched_skill_chips</div>
    </td>
  </tr>
</table>
""".strip()
)

cards = []
TOP_JOB_LIMIT = 10
visible_job_count = min(TOP_JOB_LIMIT, len(classified_jobs))
job_label = "Job" if visible_job_count == 1 else "Jobs"
EMAIL_SUBJECT = f"Your Top {visible_job_count} AI Engineering {job_label} of the Week"

for rank, (_, job) in enumerate(classified_jobs.head(TOP_JOB_LIMIT).iterrows(), start=1):
    required_skill_items = job["extracted_skills"]

    cards.append(
        card_template.substitute(
            rank=rank,
            job_url=safe_escape(job["job_url"]),
            title=safe_escape(job["title"]),
            company=safe_escape(job["company"]),
            location=safe_escape(format_location(job)),
            salary=safe_escape(job["salary"]),
            job_summary=safe_escape(job["job_summary"]),
            company_summary=safe_escape(job["company_summary"]),
            highlights_and_benefits=render_highlights_and_benefits(
                job["highlights"], job["benefits"]
            ),
            application_decision=safe_escape(job["application_decision"]),
            application_decision_reason=safe_escape(job["application_decision_reason"]),
            mismatch_summary=safe_escape(job["mismatch_summary"]),
            matched_skill_chips=render_skill_chips(
                required_skill_items,
                matched_skills=job["matched_required_skills"],
                partial_skills=job["partial_required_skills"],
            ),
        )
    )

html = f"""
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:32px 0;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
      <tr><td style="font-family:-apple-system,Segoe UI,sans-serif;color:#0B1020;">
        <p style="color:#64748B;font-size:18px;font-weight:500;margin:0 0 18px 0;">
          {REPORT_DATE.strftime("%B %d, %Y")} · Calendar week {CALENDAR_WEEK}
        </p>
        <h1 style="font-size:36px;line-height:1.1;margin:0 0 28px 0;color:#0B1020;">
          {EMAIL_SUBJECT}
        </h1>
        {"".join(cards)}
      </td></tr>
    </table>
  </td></tr>
</table>
"""

# ── Step 9: Send email or write local HTML ────────────────────────────────────

if SEND_EMAIL:
    print("\nStep 9: Sending email...")

    resend.api_key = os.environ["RESEND_API_KEY"]

    params: resend.Emails.SendParams = {
        "from": os.getenv("EMAIL_FROM", "Acme <onboarding@resend.dev>"),
        "to": [os.getenv("EMAIL_TO", "office@lukaslechner.com")],
        "subject": EMAIL_SUBJECT,
        "html": html,
    }

    email = resend.Emails.send(params)
    print(email)
else:
    print("\nStep 9: Writing local HTML...")
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"  Wrote {OUTPUT_FILE.resolve()}")
