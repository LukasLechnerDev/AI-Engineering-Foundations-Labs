from dotenv import load_dotenv
from openai import OpenAI

from steps.step_1_scraping import ScrapingStep
from steps.step_2_classification import ClassificationStep
from steps.step_3_skill_extraction import SkillExtractionStep
from steps.step_4_rendering import HtmlRenderingStep


def main():
    load_dotenv(override=True)

    client = OpenAI()

    print("=== AI Engineer Job Agent ===")

    scraped_jobs = ScrapingStep().run()
    ai_engineering_jobs = ClassificationStep(client).run(scraped_jobs)
    jobs_with_skills = SkillExtractionStep(client).run(ai_engineering_jobs)
    HtmlRenderingStep().run(jobs_with_skills)

    print("\nDone!")


if __name__ == "__main__":
    main()
