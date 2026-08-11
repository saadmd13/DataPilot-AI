import pandas as pd

from app.models.dataset_profile import (
    ColumnProfile,
    DatasetProfile,
)
from app.services.dataset_intelligence import (
    DatasetIntelligence,
)


def test_constant_column_detection():

    profile = DatasetProfile(
        filename="test.csv",
        row_count=100,
        column_count=2,
        columns=[
            ColumnProfile(
                name="country",
                pandas_dtype="str",
                semantic_type="categorical",
                unique_count=1,
                missing_count=0,
            ),
            ColumnProfile(
                name="age",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=30,
            ),
        ],
    )

    service = DatasetIntelligence()

    insights = service.analyze(profile)

    assert any(
        insight.insight_type
        == "constant_columns"
        for insight in insights
    )


def test_identifier_detection():

    profile = DatasetProfile(
        filename="test.csv",
        row_count=100,
        column_count=1,
        columns=[
            ColumnProfile(
                name="customer_id",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=100,
                cardinality_ratio=1.0,
                is_identifier=True,
            )
        ],
    )

    service = DatasetIntelligence()

    insights = service.analyze(profile)

    assert any(
        insight.insight_type
        == "identifier_columns"
        for insight in insights
    )


def test_pattern_detection():

    profile = DatasetProfile(
        filename="test.csv",
        row_count=100,
        column_count=1,
        columns=[
            ColumnProfile(
                name="email",
                pandas_dtype="str",
                semantic_type="text",
                value_pattern="email",
                pattern_confidence=1.0,
                pattern_match_percentage=100.0,
            )
        ],
    )

    service = DatasetIntelligence()

    insights = service.analyze(profile)

    assert any(
        insight.insight_type
        == "detected_patterns"
        for insight in insights
    )


def test_missing_value_detection():

    profile = DatasetProfile(
        filename="test.csv",
        row_count=100,
        column_count=1,
        missing_value_count=50,
        missing_value_percentage=50.0,
        columns=[
            ColumnProfile(
                name="age",
                pandas_dtype="float64",
                semantic_type="numeric",
                missing_count=50,
                missing_percentage=50.0,
            )
        ],
    )

    service = DatasetIntelligence()

    insights = service.analyze(profile)

    missing_insight = next(
        insight
        for insight in insights
        if insight.insight_type
        == "missing_values"
    )

    assert missing_insight.severity == "critical"


def test_empty_dataset():

    profile = DatasetProfile(
        filename="empty.csv",
        row_count=0,
        column_count=0,
    )

    service = DatasetIntelligence()

    insights = service.analyze(profile)

    assert len(insights) == 1

    assert (
        insights[0].insight_type
        == "empty_dataset"
    )

    assert (
        insights[0].severity
        == "critical"
    )