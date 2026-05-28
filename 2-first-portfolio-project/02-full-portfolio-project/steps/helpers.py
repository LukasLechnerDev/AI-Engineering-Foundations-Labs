from html import escape

import pandas as pd


def safe_escape(value):
    if value is None or pd.isna(value):
        return ""
    return escape(str(value))


def format_category(category):
    return category.replace("-", " ") if category else "other"


def calculate_match(match_decisions):
    weights = {
        "full-match": 1.0,
        "partial-match": 0.5,
        "no-match": 0.0,
    }

    if not match_decisions:
        return {
            "fit_score": 0,
            "matched_required_skills": [],
            "partial_required_skills": [],
            "missing_skills": [],
        }

    score = sum(weights[item["match_type"]] for item in match_decisions)
    fit_score = round((score / len(match_decisions)) * 100)

    matched = [
        item["required_skill"]
        for item in match_decisions
        if item["match_type"] == "full-match"
    ]
    partial = [
        item["required_skill"]
        for item in match_decisions
        if item["match_type"] == "partial-match"
    ]
    missing = [
        item["required_skill"]
        for item in match_decisions
        if item["match_type"] in {"partial-match", "no-match"}
    ]

    return {
        "fit_score": fit_score,
        "matched_required_skills": matched,
        "partial_required_skills": partial,
        "missing_skills": missing[:5],
    }
