from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from step_1_scrape import scrape
from step_2_filter import filter_jobs
from step_3_classify import classify
from step_4_extract_skills import extract_skills
from step_5_summarize import summarize
from step_6_highlights import extract_highlights
from step_7_match import match_skills
from step_8_render import render_html
from step_9_save import save_html

load_dotenv()
client = OpenAI()
project_dir = Path(__file__).parent

scraped = scrape()
filtered = filter_jobs(scraped)
screened_count = len(filtered)

classified = classify(filtered, client)
with_skills = extract_skills(classified, client)
summarized = summarize(with_skills, client)
highlighted = extract_highlights(summarized, client)
matched = match_skills(highlighted, client)

html = render_html(matched, screened_count, project_dir)
save_html(html, project_dir / "digest.html")
