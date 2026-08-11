import pandas as pd

from app.services.analysis_pipeline import DataPilotAnalyzer


def create_test_dataframe() -> pd.DataFrame:
    """Create a representative test dataset."""

    return pd.DataFrame(
        {
            "customer_id": list(range(1, 101)),
            "name": [
                f"Customer {i}"
                for i in range(1, 101)
            ],
            "age": [
                20 + (i % 30)
                for i in range(100)
            ],
            "city": [
                [
                    "Hyderabad",
                    "Mumbai",
                    "Delhi",
                    "Bangalore",
                ][i % 4]
                for i in range(100)
            ],
            "active": [
                i % 2 == 0
                for i in range(100)
            ],
            "signup_date": [
                f"2026-01-{(i % 28) + 1:02d}"
                for i in range(100)
            ],
        }
    )


def test_complete_analysis_pipeline():

    dataframe = create_test_dataframe()

    analyzer = DataPilotAnalyzer()

    result = analyzer.analyze(
        dataframe,
        filename="test_dataset.csv",
    )

    assert result.filename == "test_dataset.csv"

    assert result.profile.row_count == 100

    assert result.profile.column_count == 6

    assert len(result.profile.columns) == 6

    assert result.quality_report.total_cells == 600

    assert result.quality_score.overall_score >= 0

    assert result.quality_score.overall_score <= 100

    assert result.quality_score.grade

    assert result.quality_score.risk_level

    assert isinstance(
        result.insights,
        list,
    )

    assert isinstance(
        result.recommendations,
        list,
    )


def test_pipeline_detects_identifier():

    dataframe = create_test_dataframe()

    analyzer = DataPilotAnalyzer()

    result = analyzer.analyze(
        dataframe,
        filename="test_dataset.csv",
    )

    customer_id = next(
        column
        for column in result.profile.columns
        if column.name == "customer_id"
    )

    assert customer_id.is_identifier is True

    assert (
        customer_id.identifier_confidence
        > 0
    )


def test_pipeline_detects_datetime():

    dataframe = create_test_dataframe()

    analyzer = DataPilotAnalyzer()

    result = analyzer.analyze(
        dataframe,
        filename="test_dataset.csv",
    )

    signup_date = next(
        column
        for column in result.profile.columns
        if column.name == "signup_date"
    )

    assert (
        signup_date.semantic_type
        == "datetime"
    )

    assert (
        signup_date.datetime_parse_success_rate
        > 0
    )


def test_pipeline_generates_recommendations():

    dataframe = create_test_dataframe()

    analyzer = DataPilotAnalyzer()

    result = analyzer.analyze(
        dataframe,
        filename="test_dataset.csv",
    )

    assert isinstance(
        result.recommendations,
        list,
    )

    assert any(
        recommendation.recommendation_type
        == "identifier"
        for recommendation
        in result.recommendations
    )


def test_pipeline_handles_missing_values():

    dataframe = create_test_dataframe()

    dataframe.loc[
        0:19,
        "age",
    ] = None

    analyzer = DataPilotAnalyzer()

    result = analyzer.analyze(
        dataframe,
        filename="missing_values.csv",
    )

    assert (
        result.quality_report.missing_cells
        > 0
    )

    assert any(
        recommendation.recommendation_type
        == "missing_values"
        for recommendation
        in result.recommendations
    )
def test_pipeline_includes_ml_insights():
    dataframe = pd.DataFrame(
        {
            "feature": range(10),
            "target": [
                0,
                1,
                0,
                1,
                0,
                1,
                0,
                1,
                0,
                1,
            ],
        }
    )

    analyzer = DataPilotAnalyzer()

    result = analyzer.analyze(
        dataframe,
        filename="ml_test.csv",
    )

    assert result.ml_insights

    problem_insights = [
        insight
        for insight in result.ml_insights
        if insight.insight_type == "problem_type"
    ]

    assert problem_insights

    assert (
        "classification"
        in problem_insights[0].message
    )
def test_pipeline_includes_ml_and_feature_insights():
    import pandas as pd

    from app.services.analysis_pipeline import (
        DataPilotAnalyzer,
    )

    dataframe = pd.DataFrame(
        {
            "feature": range(1, 11),
            "target": [
                2,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
            ],
        }
    )

    result = DataPilotAnalyzer().analyze(
        dataframe,
        filename="integration_test.csv",
    )

    assert result.ml_insights

    assert result.feature_insights

    assert any(
        insight.insight_type
        == "target_detection"
        for insight in result.ml_insights
    )

    assert any(
        insight.insight_type
        == "target_relationship"
        for insight in result.feature_insights
    )