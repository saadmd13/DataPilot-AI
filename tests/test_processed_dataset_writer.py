import pandas as pd

from app.services.processed_dataset_writer import (
    ProcessedDatasetWriter,
)


def test_processed_dataset_writer(
    tmp_path,
    monkeypatch,
):

    from app.config import settings

    monkeypatch.setattr(
        settings,
        "processed_data_dir",
        str(tmp_path),
    )

    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "age": [20, 30, 40],
        }
    )

    result = ProcessedDatasetWriter().write(
        dataframe,
        "customers.csv",
    )

    assert result.rows == 3
    assert result.columns == 2

    assert result.column_names == [
        "customer_id",
        "age",
    ]

    assert result.filename.startswith(
        "customers_processed_"
    )

    assert result.filename.endswith(
        ".csv"
    )

    assert result.path

    assert result.path.endswith(
        result.filename
    )