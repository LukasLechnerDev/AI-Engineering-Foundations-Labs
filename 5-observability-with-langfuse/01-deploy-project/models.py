from enum import StrEnum

from pydantic import BaseModel


class JobClassification(BaseModel):
    is_ai_engineering_role: bool
    reason: str


class JobType(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on-site"
    UNKNOWN = "unknown"


class SkillCategory(StrEnum):
    AI_ENGINEERING = "ai-engineering"
    MACHINE_LEARNING = "machine-learning"
    PROGRAMMING_LANGUAGES = "programming-languages"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASES = "databases"
    CLOUD = "cloud"
    DEV_OPS = "dev-ops"
    OTHER = "other"


class JobSkill(BaseModel):
    skill: str
    category: SkillCategory


class JobEnrichment(BaseModel):
    job_summary: str
    company_summary: str
    salary: str
    job_type: JobType
    location: str
    highlights_and_benefits: str
    skills: list[JobSkill]


class SkillMatch(BaseModel):
    matched_required_skills: list[str]
    partial_required_skills: list[str]
    no_match_skills: list[str]


class ApplicationDecision(StrEnum):
    APPLY_THIS_WEEK = "Apply this week"
    CONSIDER_APPLYING = "Consider applying"
    NOT_READY_YET = "Not ready yet"
    NO_FIT = "No fit"


class OverallJobMatch(BaseModel):
    overall_match_score: float
    application_decision: ApplicationDecision
    application_decision_reason: str
    mismatch_summary: str
    recommended_action: str
