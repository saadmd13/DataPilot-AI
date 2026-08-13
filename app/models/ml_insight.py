from pydantic import BaseModel, Field


class MLInsight(BaseModel):
    """Machine-learning intelligence generated for a dataset."""

    insight_type: str

    severity: str = "info"

    column_name: str | None = None

    message: str

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict = Field(
        default_factory=dict
    )
    