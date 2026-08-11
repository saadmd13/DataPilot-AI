from pydantic import BaseModel


class ColumnInsight(BaseModel):
    """Human-readable intelligence about a dataset column."""

    column_name: str

    insight_type: str

    severity: str = "info"

    message: str

    confidence: float = 0.0