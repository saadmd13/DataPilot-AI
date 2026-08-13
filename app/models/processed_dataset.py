from pydantic import BaseModel


class ProcessedDataset(BaseModel):
    """Metadata describing a processed dataset."""

    filename: str
    path: str
    rows: int
    columns: int
    column_names: list[str]