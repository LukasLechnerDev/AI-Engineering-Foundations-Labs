from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from step_1_scrape import scrape
from step_2_filter import filter_jobs
from step_3_classify import classify
from step_4_extract_skills import extract_skills
from step_5_render import render_html
from step_6_save import save_html

load_dotenv()
client = OpenAI()
project_dir = Path(__file__).parent

scraped = scrape()
filtered = filter_jobs(scraped)
screened_count = len(filtered)
classified = classify(filtered, client)
with_skills = extract_skills(classified, client)
html = render_html(with_skills, screened_count, project_dir)
save_html(html, project_dir / "digest.html")
