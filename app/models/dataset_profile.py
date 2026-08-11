from pydantic import BaseModel, Field


class ColumnProfile(BaseModel):
    """Profile information for a single dataset column."""

    name: str
    pandas_dtype: str

    semantic_type: str = "unknown"

    missing_count: int = 0
    missing_percentage: float = 0.0

    unique_count: int = 0
    unique_percentage: float = 0.0

    cardinality_ratio: float = 0.0

    is_identifier: bool = False
    identifier_confidence: float = 0.0

    datetime_parse_success_rate: float = 0.0

    # Numeric statistics
    min_value: float | None = None
    max_value: float | None = None
    mean_value: float | None = None
    median_value: float | None = None
    std_value: float | None = None

    # Categorical statistics
    top_values: list[dict] = Field(
        default_factory=list
    )

    # Text statistics
    min_length: int | None = None
    max_length: int | None = None
    average_length: float | None = None


class DatasetProfile(BaseModel):
    """Structured intelligence summary for a dataset."""

    filename: str

    row_count: int
    column_count: int

    memory_usage_bytes: int = 0

    duplicate_row_count: int = 0
    duplicate_percentage: float = 0.0

    missing_value_count: int = 0
    missing_value_percentage: float = 0.0

    numeric_column_count: int = 0
    categorical_column_count: int = 0
    datetime_column_count: int = 0
    text_column_count: int = 0
    boolean_column_count: int = 0

    columns: list[ColumnProfile] = Field(
        default_factory=list
    )