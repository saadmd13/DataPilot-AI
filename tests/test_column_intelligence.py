from app.models.dataset_profile import ColumnProfile
from app.services.column_intelligence import ColumnIntelligence


def test_identifier_insight():

    column = ColumnProfile(
        name="customer_id",
        pandas_dtype="int64",
        semantic_type="numeric",
        unique_count=100,
        unique_percentage=100.0,
        cardinality_ratio=1.0,
        is_identifier=True,
        identifier_confidence=1.0,
    )

    service = ColumnIntelligence()

    insights = service.analyze(column)

    assert len(insights) == 1

    assert insights[0].insight_type == "identifier"


def test_missing_value_insight():

    column = ColumnProfile(
        name="age",
        pandas_dtype="float64",
        semantic_type="numeric",
        missing_count=50,
        missing_percentage=50.0,
    )

    service = ColumnIntelligence()

    insights = service.analyze(column)

    assert len(insights) == 1

    assert insights[0].insight_type == "missing_values"

    assert insights[0].severity == "critical"


def test_constant_column_insight():

    column = ColumnProfile(
        name="country",
        pandas_dtype="str",
        semantic_type="categorical",
        unique_count=1,
        unique_percentage=1.0,
        cardinality_ratio=0.01,
    )

    service = ColumnIntelligence()

    insights = service.analyze(column)

    assert any(
        insight.insight_type == "constant"
        for insight in insights
    )


def test_pattern_insight():

    column = ColumnProfile(
        name="email",
        pandas_dtype="str",
        semantic_type="text",
        value_pattern="email",
        pattern_confidence=1.0,
        pattern_match_percentage=100.0,
    )

    service = ColumnIntelligence()

    insights = service.analyze(column)

    assert any(
        insight.insight_type == "value_pattern"
        for insight in insights
    )


def test_high_cardinality_insight():

    column = ColumnProfile(
        name="name",
        pandas_dtype="str",
        semantic_type="text",
        unique_count=99,
        unique_percentage=99.0,
        cardinality_ratio=0.99,
        is_identifier=False,
    )

    service = ColumnIntelligence()

    insights = service.analyze(column)

    assert any(
        insight.insight_type == "high_cardinality"
        for insight in insights
    )