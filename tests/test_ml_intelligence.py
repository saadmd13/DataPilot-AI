import pandas as pd

from app.models.dataset_profile import ColumnProfile, DatasetProfile
from app.services.ml_intelligence import MLIntelligence


def build_profile(dataframe: pd.DataFrame) -> DatasetProfile:
    """Build a minimal DatasetProfile for ML intelligence tests."""

    columns = []

    for column in dataframe.columns:
        series = dataframe[column]

        non_null = series.dropna()
        unique_count = int(non_null.nunique())
        row_count = len(dataframe)

        if pd.api.types.is_bool_dtype(series):
            semantic_type = "boolean"

        elif pd.api.types.is_numeric_dtype(series):
            semantic_type = "numeric"

        elif unique_count <= 10:
            semantic_type = "categorical"

        else:
            semantic_type = "text"

        columns.append(
            ColumnProfile(
                name=str(column),
                pandas_dtype=str(series.dtype),
                semantic_type=semantic_type,
                missing_count=int(series.isna().sum()),
                missing_percentage=(
                    float(series.isna().mean() * 100)
                    if row_count > 0
                    else 0.0
                ),
                unique_count=unique_count,
                unique_percentage=(
                    float(unique_count / row_count * 100)
                    if row_count > 0
                    else 0.0
                ),
                cardinality_ratio=(
                    float(unique_count / row_count)
                    if row_count > 0
                    else 0.0
                ),
                is_identifier=(
                    unique_count == row_count
                    and row_count > 0
                    and (
                        pd.api.types.is_numeric_dtype(series)
                        or "id" in str(column).lower()
                    )
                ),
                identifier_confidence=(
                    1.0
                    if (
                        unique_count == row_count
                        and row_count > 0
                        and (
                            pd.api.types.is_numeric_dtype(series)
                            or "id" in str(column).lower()
                        )
                    )
                    else 0.0
                ),
            )
        )

    return DatasetProfile(
        filename="test.csv",
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        columns=columns,
    )


def test_target_class_detection():
    dataframe = pd.DataFrame(
        {
            "feature_1": range(10),
            "feature_2": range(10, 20),
            "target_class": [0, 1] * 5,
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    target_insight = next(
        insight
        for insight in insights
        if insight.insight_type == "target_detection"
    )

    assert target_insight.column_name == "target_class"
    assert target_insight.confidence == 1.0


def test_binary_classification_detection():
    dataframe = pd.DataFrame(
        {
            "age": range(20, 30),
            "target_class": [0, 1] * 5,
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    problem_insight = next(
        insight
        for insight in insights
        if insight.insight_type == "problem_type"
    )

    assert problem_insight.column_name == "target_class"
    assert "binary_classification" in problem_insight.message


def test_multiclass_classification_detection():
    dataframe = pd.DataFrame(
        {
            "feature": range(12),
            "target": [
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
            ],
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    problem_insight = next(
        insight
        for insight in insights
        if insight.insight_type == "problem_type"
    )

    assert "multiclass_classification" in problem_insight.message


def test_regression_detection():
    dataframe = pd.DataFrame(
        {
            "feature": range(10),
            "target": [
                10.5,
                12.2,
                14.7,
                16.1,
                18.9,
                21.4,
                23.8,
                25.2,
                27.9,
                30.1,
            ],
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    problem_insight = next(
        insight
        for insight in insights
        if insight.insight_type == "problem_type"
    )

    assert "regression" in problem_insight.message


def test_class_imbalance_detection():
    dataframe = pd.DataFrame(
        {
            "feature": range(100),
            "target_class": (
                [0] * 91
                + [1] * 9
            ),
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    imbalance = next(
        insight
        for insight in insights
        if insight.insight_type == "class_imbalance"
    )

    assert imbalance.column_name == "target_class"
    assert imbalance.severity == "critical"
    assert imbalance.metadata["minority_percentage"] == 9.0


def test_identifier_feature_detection():
    dataframe = pd.DataFrame(
        {
            "customer_id": range(1, 11),
            "target_class": [0, 1] * 5,
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    identifier = next(
        insight
        for insight in insights
        if insight.insight_type == "identifier_feature"
    )

    assert identifier.column_name == "customer_id"


def test_missing_feature_detection():
    dataframe = pd.DataFrame(
        {
            "feature": [
                1,
                2,
                None,
                None,
                None,
                None,
                7,
                8,
                9,
                10,
            ],
            "target_class": [0, 1] * 5,
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    missing = next(
        insight
        for insight in insights
        if insight.insight_type == "missing_feature"
    )

    assert missing.column_name == "feature"
    assert missing.severity == "warning"


def test_no_target_detection():
    dataframe = pd.DataFrame(
        {
            "age": range(10),
            "income": range(100, 110),
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    target_insight = next(
        insight
        for insight in insights
        if insight.insight_type == "target_detection"
    )

    assert target_insight.column_name is None
    assert "No likely target" in target_insight.message

def test_numeric_high_cardinality_feature_is_not_flagged():
    dataframe = pd.DataFrame(
        {
            "continuous_feature": [
                float(i) + 0.123
                for i in range(100)
            ],
            "target": [
                0,
                1,
            ] * 50,
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    high_cardinality = [
        insight
        for insight in insights
        if insight.insight_type
        == "high_cardinality_feature"
    ]

    assert high_cardinality == []

def test_high_cardinality_categorical_feature_is_detected():
    dataframe = pd.DataFrame(
        {
            "email": [
                f"user{i}@example.com"
                for i in range(100)
            ],
            "target": [
                0,
                1,
            ] * 50,
        }
    )

    profile = build_profile(dataframe)

    insights = MLIntelligence().analyze(
        dataframe,
        profile,
    )

    high_cardinality = [
        insight
        for insight in insights
        if insight.insight_type
        == "high_cardinality_feature"
    ]

    assert high_cardinality

    assert high_cardinality[0].column_name == "email"