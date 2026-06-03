import pandas as pd
from jobspy import scrape_jobs


def scrape() -> pd.DataFrame:
    print("Step 1: Scraping jobs...")

    jobs = scrape_jobs(
        site_name=["indeed", "linkedin"],
        linkedin_fetch_description=True,
        search_term='"AI Engineer"',
        location="Austria",
        country_indeed="Austria",
        job_type="fulltime",
        hours_old=240,
        results_wanted=20,
    )

    df = pd.DataFrame(jobs)
    print(f"  Scraped: {len(df)} jobs")
    return df
