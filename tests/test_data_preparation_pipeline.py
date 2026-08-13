import pandas as pd

from app.models.data_preparation_result import (
    DataPreparationResult,
)
from app.models.processed_dataset import (
    ProcessedDataset,
)
from app.services.data_preparation_pipeline import (
    DataPreparationPipeline,
)


def test_pipeline_returns_data_preparation_result():

    dataframe = pd.DataFrame(
        {
            "age": [
                20,
                None,
                40,
            ]
        }
    )

    prepared, result, processed_dataset = (
        DataPreparationPipeline().prepare(
            dataframe,
            filename="test.csv",
        )
    )

    assert isinstance(
        result,
        DataPreparationResult,
    )

    assert isinstance(
        processed_dataset,
        ProcessedDataset,
    )

    assert result.success is True

    assert result.original_row_count == 3

    assert result.final_row_count == 3

    assert result.original_column_count == 1

    assert result.final_column_count == 1

    assert (
        result.original_missing_percentage
        > 0
    )

    assert (
        result.final_missing_percentage
        == 0
    )

    assert processed_dataset.rows == 3

    assert processed_dataset.columns == 1

    assert processed_dataset.column_names == [
        "age"
    ]


def test_pipeline_removes_duplicates():

    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 2, 3],
            "age": [20, 30, 30, 40],
        }
    )

    prepared, result, processed_dataset = (
        DataPreparationPipeline().prepare(
            dataframe,
            filename="test.csv",
        )
    )

    assert len(prepared) == 3

    assert result.original_row_count == 4

    assert result.final_row_count == 3

    assert result.success is True

    assert result.transformations_applied >= 1

    assert processed_dataset is not None

    assert processed_dataset.rows == 3


def test_pipeline_imputes_missing_numeric_values():

    dataframe = pd.DataFrame(
        {
            "age": [
                20,
                30,
                None,
                40,
                50,
            ]
        }
    )

    prepared, result, processed_dataset = (
        DataPreparationPipeline().prepare(
            dataframe,
            filename="test.csv",
        )
    )

    assert prepared["age"].isna().sum() == 0

    assert (
        result.original_missing_percentage
        > 0
    )

    assert (
        result.final_missing_percentage
        == 0
    )

    assert processed_dataset is not None

    assert processed_dataset.rows == len(
        prepared
    )

    assert processed_dataset.columns == len(
        prepared.columns
    )


def test_pipeline_removes_constant_columns():

    dataframe = pd.DataFrame(
        {
            "country": [
                "India",
                "India",
                "India",
                "India",
            ],
            "age": [
                20,
                21,
                22,
                23,
            ],
        }
    )

    prepared, result, processed_dataset = (
        DataPreparationPipeline().prepare(
            dataframe,
            filename="test.csv",
        )
    )

    assert "country" not in prepared.columns

    assert "age" in prepared.columns

    assert (
        result.final_column_count
        < result.original_column_count
    )

    assert processed_dataset is not None

    assert processed_dataset.column_names == [
        "age"
    ]


def test_pipeline_does_not_modify_original():

    dataframe = pd.DataFrame(
        {
            "age": [
                20,
                None,
                40,
            ]
        }
    )

    original = dataframe.copy()

    prepared, result, processed_dataset = (
        DataPreparationPipeline().prepare(
            dataframe,
            filename="test.csv",
        )
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )

    assert prepared is not dataframe

    assert processed_dataset is not None


def test_pipeline_preserves_identifier():

    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "age": [20, 21, 22],
        }
    )

    prepared, result, processed_dataset = (
        DataPreparationPipeline().prepare(
            dataframe,
            filename="test.csv",
        )
    )

    assert result.success is True

    assert (
        result.transformations_applied >= 1
    )

    assert len(
        result.transformations
    ) >= 1

    assert any(
        "identifier_exclusion" in transformation
        for transformation
        in result.transformations
    )

    # Identifier must remain available
    # for record tracking.
    assert "customer_id" in prepared.columns

    assert "age" in prepared.columns

    assert processed_dataset is not None

    assert processed_dataset.column_names == [
        "customer_id",
        "age",
    ]

    assert processed_dataset.rows == 3

    assert processed_dataset.columns == 2