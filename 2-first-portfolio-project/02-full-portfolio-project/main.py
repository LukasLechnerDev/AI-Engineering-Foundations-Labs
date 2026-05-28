from dotenv import load_dotenv
from openai import OpenAI

from steps.step_1_scraping import ScrapingStep
from steps.step_2_classification import ClassificationStep
from steps.step_3_enrichment import EnrichmentStep
from steps.step_4_skill_matching import SkillMatchingStep
from steps.step_5_overall_matching import OverallMatchingStep
from steps.step_6_rendering import RenderingStep


def main():
    load_dotenv(override=True)

    client = OpenAI()

    print("=== AI Engineer Job Report ===")

    scraped_jobs = ScrapingStep().run()
    classified_jobs = ClassificationStep(client).run(scraped_jobs)
    enriched_jobs = EnrichmentStep(client).run(classified_jobs)
    skill_matched_jobs = SkillMatchingStep(client).run(enriched_jobs)
    ranked_jobs = OverallMatchingStep(client).run(skill_matched_jobs)

    RenderingStep().run(ranked_jobs)

    print("\nDone!")


if __name__ == "__main__":
    main()
