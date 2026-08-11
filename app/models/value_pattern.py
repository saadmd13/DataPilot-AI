from pydantic import BaseModel, Field


class PatternDetection(BaseModel):
    """Detected value pattern for a dataset column."""

    pattern: str = "unknown"

    confidence: float = 0.0

    matched_count: int = 0

    total_count: int = 0

    match_percentage: float = 0.0

    examples: list[str] = Field(
        default_factory=list
    )