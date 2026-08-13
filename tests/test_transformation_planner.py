import pandas as pd

from app.services.data_quality_analyzer import (
    DataQualityAnalyzer,
)
from app.services.dataset_profiler import (
    DatasetProfiler,
)
from app.services.transformation_planner import (
    TransformationPlanner,
)


def build_analysis(dataframe):

    profile = DatasetProfiler().profile(
        dataframe,
        filename="test.csv",
    )

    quality_report = (
        DataQualityAnalyzer().analyze(
            dataframe
        )
    )

    return profile, quality_report


def test_numeric_missing_values_use_median():

    dataframe = pd.DataFrame(
        {
            "age": [
                20,
                25,
                None,
                30,
                35,
            ]
        }
    )

    profile, quality_report = build_analysis(
        dataframe
    )

    transformations = (
        TransformationPlanner().plan(
            profile,
            quality_report,
        )
    )

    transformation = next(
        transformation
        for transformation in transformations
        if transformation.transformation_type
        == "missing_value_imputation"
    )

    assert transformation.column_name == "age"

    assert transformation.method == "median"

    assert (
        transformation.parameters["strategy"]
        == "median"
    )


def test_categorical_missing_values_use_mode():

    dataframe = pd.DataFrame(
        {
            "city": [
                "Delhi",
                "Mumbai",
                None,
                "Delhi",
                "Delhi",
            ]
        }
    )

    profile, quality_report = build_analysis(
        dataframe
    )

    transformations = (
        TransformationPlanner().plan(
            profile,
            quality_report,
        )
    )

    transformation = next(
        transformation
        for transformation in transformations
        if transformation.transformation_type
        == "missing_value_imputation"
    )

    assert transformation.column_name == "city"

    assert transformation.method == "mode"


def test_duplicate_rows_generate_transformation():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 2, 3],
            "value": [10, 20, 20, 30],
        }
    )

    profile, quality_report = build_analysis(
        dataframe
    )

    transformations = (
        TransformationPlanner().plan(
            profile,
            quality_report,
        )
    )

    duplicate_transformation = next(
        transformation
        for transformation in transformations
        if transformation.transformation_type
        == "duplicate_removal"
    )

    assert (
        duplicate_transformation.method
        == "drop_duplicates"
    )


def test_constant_column_generates_transformation():

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

    profile, quality_report = build_analysis(
        dataframe
    )

    transformations = (
        TransformationPlanner().plan(
            profile,
            quality_report,
        )
    )

    constant_transformation = next(
        transformation
        for transformation in transformations
        if transformation.transformation_type
        == "constant_column_removal"
    )

    assert (
        constant_transformation.column_name
        == "country"
    )

    assert constant_transformation.method == "drop"


def test_identifier_generates_exclusion():

    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "age": [20, 21, 22, 23],
        }
    )

    profile, quality_report = build_analysis(
        dataframe
    )

    transformations = (
        TransformationPlanner().plan(
            profile,
            quality_report,
        )
    )

    identifier_transformation = next(
        transformation
        for transformation in transformations
        if transformation.transformation_type
        == "identifier_exclusion"
    )

    assert (
        identifier_transformation.column_name
        == "customer_id"
    )

    assert (
        identifier_transformation.method
        == "exclude_from_features"
    )