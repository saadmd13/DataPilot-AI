from pydantic import BaseModel, Field


class FeatureInsight(BaseModel):
    """Machine-learning insight about a dataset feature."""

    feature_name: str

    insight_type: str

    severity: str = "info"

    target_column: str | None = None

    message: str

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    score: float | None = Field(
        default=None,
        ge=-1.0,
        le=1.0,
    )

    metadata: dict = Field(
        default_factory=dict
    )