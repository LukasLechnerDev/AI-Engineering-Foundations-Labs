import json
import sys
from html import escape
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

sys.path.insert(0, str(Path(__file__).parents[1]))

from step_4_summarize import instructions, summarize

EVAL_FILE = Path(__file__).parents[1] / "evals/3-classified_jobs.jsonl"
SAMPLE_SIZE = 20
JUDGE_MODEL = "gpt-5.4-mini"


judge_instructions = f"""
You evaluate whether a 2-3 sentence summary of an AI engineering job posting is high quality.

The summarizer was given these instructions:
<summarizer instructions>
{instructions}
</summarizer instructions>

A good summary must satisfy all three criteria:
1. Concise: the summary is 2-3 sentences — no more, no less.
2. Accurate: every claim in the summary is supported by text in the job description.
3. No hallucinations: the summary does not introduce technologies or responsibilities not in the original.

Return passes=true only if all three criteria are met.
""".strip()

judge_schema = {
    "type": "object",
    "properties": {
        "passes": {"type": "boolean"},
        "feedback": {"type": "string"},
    },
    "required": ["passes", "feedback"],
    "additionalProperties": False,
}


def load_eval_jobs():
    return [json.loads(line) for line in EVAL_FILE.read_text().splitlines() if line]


def judge_summary(job: dict, client: OpenAI) -> dict:
    input_text = (
        f"Title: {job['title']}\n\n"
        f"Description:\n{job['description']}\n\n"
        f"Summary: {job['summary']}"
    )
    response = client.responses.create(
        model=JUDGE_MODEL,
        instructions=judge_instructions,
        input=input_text,
        text={
            "format": {
                "type": "json_schema",
                "name": "summary_judgment",
                "schema": judge_schema,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


REPORT_FILE = Path(__file__).parent / "llm-judge-summary-report.html"


def save_report(rows: list[dict], passes: int) -> None:
    total = len(rows)
    rate = passes / total

    cards = []
    for row in rows:
        status = "PASS" if row["passes"] else "FAIL"
        label_color = "#16a34a" if row["passes"] else "#dc2626"
        classification = (
            "AI engineering" if row["is_ai_engineering_role"] else "Not AI engineering"
        )
        cards.append(f"""
<div class="card">
  <div class="card-header">
    <a href="{escape(row["job_url"])}" target="_blank">{escape(row["title"])}</a>
    <span class="badge" style="background:{label_color}">{status}</span>
  </div>
  <p class="classification">Classification: <strong>{escape(classification)}</strong></p>
  <p class="label">LLM summary</p>
  <p class="reason">{escape(row["summary"])}</p>
  <p class="label">Judge feedback</p>
  <p class="reason">{escape(row["feedback"])}</p>
</div>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Eval Report</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'IBM Plex Sans', sans-serif; background: #FAFBFD; color: #0B1020; }}
    .hero {{ background: #0B1020; padding: 40px; }}
    .hero-inner {{ max-width: 800px; margin: 0 auto; }}
    .hero h1 {{ font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 600; color: #fff; }}
    .hero h1 span {{ color: #2F6BFF; }}
    .hero p {{ color: #8FB2FF; font-size: 0.875rem; margin-top: 6px; }}
    .content {{ max-width: 800px; margin: 36px auto; padding: 0 40px; }}
    .card {{ background: white; border-radius: 10px; padding: 20px 24px; margin-bottom: 12px; border: 1px solid #E7EDF7; }}
    .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 8px; }}
    .card-header a {{ font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 600; color: #0B1020; text-decoration: none; }}
    .card-header a:hover {{ color: #2F6BFF; }}
    .badge {{ font-size: 0.75rem; font-weight: 600; color: white; padding: 2px 10px; border-radius: 999px; white-space: nowrap; }}
    .classification {{ font-size: 0.825rem; color: #6B7280; margin-bottom: 12px; }}
    .label {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #6B7280; margin-bottom: 4px; margin-top: 12px; }}
    .reason {{ font-size: 0.875rem; color: #3D4660; line-height: 1.6; }}
  </style>
</head>
<body>
  <div class="hero">
    <div class="hero-inner">
      <h1>Eval Report: <span>Summary Quality</span></h1>
      <p>{passes}/{total} passed &nbsp;·&nbsp; {rate:.1%} pass rate</p>
    </div>
  </div>
  <div class="content">
    {"".join(cards)}
  </div>
</body>
</html>"""

    REPORT_FILE.write_text(html, encoding="utf-8")
    print(f"\n  Report saved to {REPORT_FILE}")


# Execute with: uv run pytest tests/test_summary_eval.py -s
def test_summary_quality():
    jobs = load_eval_jobs()[:SAMPLE_SIZE]
    df = pd.DataFrame(
        [
            {
                "title": j["title"],
                "job_url": j["job_url"],
                "description": j["description"],
                "is_ai_engineering_role": j["is_ai_engineering_role"],
            }
            for j in jobs
        ]
    )

    client = OpenAI()
    result_df = summarize(df, client)

    passes = 0
    report_rows = []
    for _, row in result_df.iterrows():
        judgment = judge_summary(row.to_dict(), client)

        status = "PASS" if judgment["passes"] else "FAIL"
        print(f"  [{status}] {row['title']}: {judgment['feedback']}")

        if judgment["passes"]:
            passes += 1

        report_rows.append({**row.to_dict(), **judgment})

    total = len(result_df)
    rate = passes / total
    print(f"\nSummary quality: {passes}/{total} ({rate:.1%})")

    save_report(report_rows, passes)

    assert rate >= 0.80, f"Summary quality {rate:.1%} is below the 80% threshold"
