from pydantic import BaseModel, Field


class Transformation(BaseModel):
    """A planned data transformation."""

    transformation_type: str

    column_name: str | None = None

    method: str | None = None

    reason: str

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    parameters: dict = Field(
        default_factory=dict
    )