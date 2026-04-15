from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from step_1_scrape import scrape
from step_2_filter import filter_jobs
from step_3_classify import classify
from step_4_summarize import summarize
from step_5_extract_skills import extract_skills
from step_6_render import render_html
from step_7_save import save_html

load_dotenv()
client = OpenAI()
project_dir = Path(__file__).parent
jobs_dir = project_dir / "jobs"
jobs_dir.mkdir(exist_ok=True)

scraped = scrape()
scraped.to_json(jobs_dir / "1-scraped_jobs.jsonl", orient="records", lines=True, force_ascii=False)

filtered = filter_jobs(scraped)
filtered.to_json(jobs_dir / "2-filtered_jobs.jsonl", orient="records", lines=True, force_ascii=False)
screened_count = len(filtered)

classified = classify(filtered, client)
classified.to_json(jobs_dir / "3-classified_jobs.jsonl", orient="records", lines=True, force_ascii=False)

summarized = summarize(classified, client)
summarized.to_json(jobs_dir / "4-summarized_jobs.jsonl", orient="records", lines=True, force_ascii=False)

with_skills = extract_skills(summarized, client)
with_skills.to_json(jobs_dir / "5-jobs_with_skills.jsonl", orient="records", lines=True, force_ascii=False)

html = render_html(with_skills, screened_count, project_dir)
save_html(html, project_dir / "digest.html")
