import os

from dotenv import load_dotenv
from openai import OpenAI

from helper.argument_parser import parse_arguments
from steps.step_1_scraping import ScrapingStep
from steps.step_2_classification import ClassificationStep
from steps.step_3_enrichment import EnrichmentStep
from steps.step_4_skill_matching import SkillMatchingStep
from steps.step_5_overall_matching import OverallMatchingStep
from steps.step_6_rendering import RenderingStep
from steps.step_7_email import EmailStep


def main():
    load_dotenv(override=False)
    arguments = parse_arguments()

    client = OpenAI()

    print("=== AI Engineer Job Report ===")

    scraped_jobs = ScrapingStep().run(
        site_name=arguments.site_name,
        location=arguments.location,
        country_indeed=arguments.country_indeed,
        job_type=arguments.job_type,
        hours_old=arguments.hours_old,
        results_wanted=arguments.results_wanted,
    )
    classified_jobs = ClassificationStep(client).run(scraped_jobs)
    enriched_jobs = EnrichmentStep(client).run(classified_jobs)
    skill_matched_jobs = SkillMatchingStep(client).run(enriched_jobs)
    ranked_jobs = OverallMatchingStep(client).run(skill_matched_jobs)

    report_path = RenderingStep().run(ranked_jobs, arguments.location)
    send_email = os.environ.get("SEND_EMAIL", "false").lower() == "true"
    if send_email:
        EmailStep().run(report_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
