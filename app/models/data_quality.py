from pydantic import BaseModel, Field


class ColumnQuality(BaseModel):
    """Quality information for a single column."""

    column_name: str

    missing_count: int = 0
    missing_percentage: float = 0.0

    unique_count: int = 0
    unique_percentage: float = 0.0

    is_constant: bool = False


class DataQualityReport(BaseModel):
    """Structured data quality report."""

    total_cells: int = 0

    missing_cells: int = 0
    missing_percentage: float = 0.0

    duplicate_rows: int = 0
    duplicate_percentage: float = 0.0

    constant_columns: list[str] = Field(
        default_factory=list
    )

    columns: list[ColumnQuality] = Field(
        default_factory=list
    )