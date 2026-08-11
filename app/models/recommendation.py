from pydantic import BaseModel


class Recommendation(BaseModel):
    """Actionable recommendation for improving or analyzing a dataset."""

    recommendation_type: str

    priority: str = "medium"

    column_name: str | None = None

    title: str

    description: str

    action: str

    confidence: float = 0.0