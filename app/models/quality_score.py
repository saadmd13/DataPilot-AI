from pydantic import BaseModel, Field


class QualityScore(BaseModel):
    """Overall data quality assessment for a dataset."""

    overall_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    completeness_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    uniqueness_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    consistency_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    validity_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    grade: str = "F"

    risk_level: str = "high"

    issues_count: int = 0

    critical_issues_count: int = 0

    warning_issues_count: int = 0

    info_issues_count: int = 0

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )
    