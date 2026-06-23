import pandas as pd


def filter_jobs(df: pd.DataFrame) -> pd.DataFrame:
    print("\nStep 2: Filtering...")

    # Title must contain both "AI" and "Engineer"
    mask = df["title"].str.contains("AI", case=False, na=False) & df[
        "title"
    ].str.contains("Engineer", case=False, na=False)
    df = df[mask].copy()
    print(f"  After title filter: {len(df)} jobs")

    # Keep only rows that have a title, job URL, and description
    required_columns = ["title", "job_url", "description"]
    has_required = (
        df[required_columns]
        .fillna("")
        .apply(lambda col: col.astype(str).str.strip() != "")
        .all(axis=1)
    )
    df = df[has_required].copy()
    print(f"  After required-fields check: {len(df)} jobs")

    # Remove duplicate title + company pairs
    df = df.drop_duplicates(subset=["title", "company"]).copy()
    print(f"  After deduplication: {len(df)} jobs")

    return df
