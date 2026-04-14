import pandas as pd
from jobspy import scrape_jobs


def scrape() -> pd.DataFrame:
    print("Step 1: Scraping jobs...")

    jobs = scrape_jobs(
        site_name=["indeed", "linkedin"],
        linkedin_fetch_description=True,
        search_term='"AI Engineer"',
        location="USA",
        country_indeed="USA",
        job_type="fulltime",
        hours_old=24,
        results_wanted=3,
    )

    df = pd.DataFrame(jobs)
    print(f"  Scraped: {len(df)} jobs")
    return df
