import pandas as pd
import pytest

from app.tools.file_loader import (
    DatasetLoadError,
    load_dataset,
)


def test_load_csv(tmp_path):
    file_path = tmp_path / "customers.csv"

    file_path.write_text(
        "id,name,age\n"
        "1,John,25\n"
        "2,Sarah,31\n"
        "3,Mike,28\n",
        encoding="utf-8",
    )

    dataframe = load_dataset(file_path)

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape == (3, 3)
    assert list(dataframe.columns) == [
        "id",
        "name",
        "age",
    ]


def test_invalid_file():
    file_path = "does_not_exist.csv"

    with pytest.raises(DatasetLoadError):
        load_dataset(file_path)


def test_unsupported_file(tmp_path):
    file_path = tmp_path / "data.txt"

    file_path.write_text(
        "hello",
        encoding="utf-8",
    )

    with pytest.raises(DatasetLoadError):
        load_dataset(file_path)