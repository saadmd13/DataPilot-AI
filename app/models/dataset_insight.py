from pydantic import BaseModel


class DatasetInsight(BaseModel):
    """Human-readable intelligence about a dataset."""

    insight_type: str

    severity: str = "info"

    message: str

    confidence: float = 0.0