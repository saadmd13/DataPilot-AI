import pandas as pd
import pytest

from app.models.transformation import Transformation
from app.services.transformation_executor import (
    TransformationExecutor,
)


def test_median_imputation():

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

    transformations = [
        Transformation(
            transformation_type=(
                "missing_value_imputation"
            ),
            column_name="age",
            method="median",
            reason="Missing numeric values.",
            confidence=0.9,
            parameters={
                "strategy": "median",
            },
        )
    ]

    result = TransformationExecutor().execute(
        dataframe,
        transformations,
    )

    assert result["age"].isna().sum() == 0
    assert result["age"].iloc[2] == 35


def test_mode_imputation():

    dataframe = pd.DataFrame(
        {
            "city": [
                "Delhi",
                "Mumbai",
                "Delhi",
                None,
                "Delhi",
            ]
        }
    )

    transformations = [
        Transformation(
            transformation_type=(
                "missing_value_imputation"
            ),
            column_name="city",
            method="mode",
            reason="Missing categorical values.",
            confidence=0.9,
            parameters={
                "strategy": "mode",
            },
        )
    ]

    result = TransformationExecutor().execute(
        dataframe,
        transformations,
    )

    assert result["city"].isna().sum() == 0
    assert result["city"].iloc[3] == "Delhi"


def test_duplicate_removal():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 2, 3],
            "value": [10, 20, 20, 30],
        }
    )

    transformations = [
        Transformation(
            transformation_type="duplicate_removal",
            method="drop_duplicates",
            reason="Duplicate rows detected.",
            confidence=0.98,
            parameters={
                "keep": "first",
            },
        )
    ]

    result = TransformationExecutor().execute(
        dataframe,
        transformations,
    )

    assert len(result) == 3
    assert result["id"].tolist() == [1, 2, 3]


def test_constant_column_removal():

    dataframe = pd.DataFrame(
        {
            "country": [
                "India",
                "India",
                "India",
            ],
            "age": [
                20,
                21,
                22,
            ],
        }
    )

    transformations = [
        Transformation(
            transformation_type=(
                "constant_column_removal"
            ),
            column_name="country",
            method="drop",
            reason="Constant column.",
            confidence=0.95,
        )
    ]

    result = TransformationExecutor().execute(
        dataframe,
        transformations,
    )

    assert "country" not in result.columns
    assert "age" in result.columns

def test_identifier_exclusion_preserves_column():

    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "age": [20, 21, 22],
        }
    )

    transformations = [
        Transformation(
            transformation_type=(
                "identifier_exclusion"
            ),
            column_name="customer_id",
            method="exclude_from_features",
            reason="Identifier column.",
            confidence=1.0,
        )
    ]

    result = TransformationExecutor().execute(
        dataframe,
        transformations,
    )

    assert "customer_id" in result.columns
    assert "age" in result.columns

    assert result["customer_id"].tolist() == [
        1,
        2,
        3,
    ]

def test_original_dataframe_is_not_modified():

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

    transformations = [
        Transformation(
            transformation_type=(
                "missing_value_imputation"
            ),
            column_name="age",
            method="median",
            reason="Missing values.",
            confidence=0.9,
            parameters={
                "strategy": "median",
            },
        )
    ]

    TransformationExecutor().execute(
        dataframe,
        transformations,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_missing_column_raises_error():

    dataframe = pd.DataFrame(
        {
            "age": [20, 30, 40]
        }
    )

    transformations = [
        Transformation(
            transformation_type=(
                "missing_value_imputation"
            ),
            column_name="salary",
            method="median",
            reason="Missing values.",
            confidence=0.9,
            parameters={
                "strategy": "median",
            },
        )
    ]

    with pytest.raises(ValueError):
        TransformationExecutor().execute(
            dataframe,
            transformations,
        )


def test_invalid_median_column_raises_error():

    dataframe = pd.DataFrame(
        {
            "city": [
                "Delhi",
                None,
                "Mumbai",
            ]
        }
    )

    transformations = [
        Transformation(
            transformation_type=(
                "missing_value_imputation"
            ),
            column_name="city",
            method="median",
            reason="Invalid median operation.",
            confidence=0.9,
            parameters={
                "strategy": "median",
            },
        )
    ]

    with pytest.raises(ValueError):
        TransformationExecutor().execute(
            dataframe,
            transformations,
        )