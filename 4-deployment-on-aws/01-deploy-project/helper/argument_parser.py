import argparse
import os

DEFAULT_SITE_NAME = "linkedin,indeed"
DEFAULT_LOCATION = "USA"
DEFAULT_COUNTRY_INDEED = "USA"
DEFAULT_JOB_TYPE = "fulltime"
DEFAULT_HOURS_OLD = 72
DEFAULT_RESULTS_WANTED = 10


def parse_site_names(value):
    return [site.strip() for site in value.split(",") if site.strip()]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate an AI Engineer job report.")
    parser.add_argument(
        "--site-name",
        "--site_name",
        nargs="+",
        default=parse_site_names(os.environ.get("SITE_NAME", DEFAULT_SITE_NAME)),
    )
    parser.add_argument(
        "--location",
        default=os.environ.get("LOCATION", DEFAULT_LOCATION),
    )
    parser.add_argument(
        "--country-indeed",
        "--country_indeed",
        default=os.environ.get("COUNTRY_INDEED", DEFAULT_COUNTRY_INDEED),
    )
    parser.add_argument(
        "--job-type",
        "--job_type",
        default=os.environ.get("JOB_TYPE", DEFAULT_JOB_TYPE),
    )
    parser.add_argument(
        "--hours-old",
        "--hours_old",
        type=int,
        default=os.environ.get("HOURS_OLD", DEFAULT_HOURS_OLD),
    )
    parser.add_argument(
        "--results-wanted",
        "--results_wanted",
        type=int,
        default=os.environ.get("RESULTS_WANTED", DEFAULT_RESULTS_WANTED),
    )
    arguments = parser.parse_args()
    arguments.site_name = parse_site_names(",".join(arguments.site_name))

    return arguments
