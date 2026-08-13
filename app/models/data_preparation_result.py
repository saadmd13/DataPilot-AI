from pydantic import BaseModel, Field


class DataPreparationResult(BaseModel):
    """Result of an automated dataset preparation run."""

    original_row_count: int
    final_row_count: int

    original_column_count: int
    final_column_count: int

    original_missing_percentage: float = 0.0
    final_missing_percentage: float = 0.0

    transformations_applied: int = 0

    transformations: list[str] = Field(
        default_factory=list
    )

    success: bool = True

    message: str = ""