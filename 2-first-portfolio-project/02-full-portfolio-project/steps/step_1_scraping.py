import pandas as pd
from jobspy import scrape_jobs


class ScrapingStep:
    def run(self):
        print("\n--- Step 1: Scraping jobs ---")

        jobs = scrape_jobs(
            site_name=["indeed", "linkedin"],
            linkedin_fetch_description=True,
            search_term='"AI Engineer"',
            location="Austria",
            country_indeed="Austria",
            job_type="fulltime",
            hours_old=168,
            results_wanted=100,
        )

        jobs_df = pd.DataFrame(jobs)
        print(f"Scraped jobs: {len(jobs_df)}")

        if jobs_df.empty:
            return []

        required_columns = ["title", "job_url", "description"]
        missing_columns = [
            column for column in required_columns if column not in jobs_df.columns
        ]
        if missing_columns:
            print(f"Missing required columns: {', '.join(missing_columns)}")
            return []

        print("Filtering out jobs with missing title, URL, or description...")
        has_required_values = (
            jobs_df[required_columns]
            .fillna("")
            .apply(lambda column: column.astype(str).str.strip() != "")
            .all(axis=1)
        )
        jobs_df = jobs_df[has_required_values].copy()
        print(f"Jobs with required fields: {len(jobs_df)}")

        print("Keeping only jobs whose title contains both 'AI' and 'Engineer'...")
        title_contains_ai = jobs_df["title"].str.contains(
            r"\bai\b", case=False, na=False, regex=True
        )
        title_contains_engineer = jobs_df["title"].str.contains(
            "Engineer", case=False, na=False
        )
        jobs_df = jobs_df[title_contains_ai & title_contains_engineer].copy()
        print(f"Jobs after title filter: {len(jobs_df)}")

        print("Removing duplicate title/company pairs...")
        dedupe_columns = [
            column for column in ["title", "company"] if column in jobs_df.columns
        ]
        jobs_df = jobs_df.drop_duplicates(subset=dedupe_columns).copy()
        print(f"Jobs after deduplication: {len(jobs_df)}")

        return jobs_df.to_dict("records")
