from app.models.data_quality import DataQualityReport
from app.models.dataset_profile import (
    ColumnProfile,
    DatasetProfile,
)
from app.models.quality_score import QualityScore
from app.services.recommendation_engine import (
    RecommendationEngine,
)


def make_profile(
    columns: list[ColumnProfile],
) -> DatasetProfile:

    return DatasetProfile(
        filename="test.csv",
        row_count=100,
        column_count=len(columns),
        columns=columns,
    )


def make_quality_report(
    missing_percentage: float = 0.0,
    duplicate_rows: int = 0,
    duplicate_percentage: float = 0.0,
    constant_columns: list[str] | None = None,
) -> DataQualityReport:

    return DataQualityReport(
        total_cells=100,
        missing_cells=int(
            missing_percentage
        ),
        missing_percentage=missing_percentage,
        duplicate_rows=duplicate_rows,
        duplicate_percentage=duplicate_percentage,
        constant_columns=(
            constant_columns or []
        ),
    )


def make_quality_score(
    overall_score: float = 90.0,
) -> QualityScore:

    return QualityScore(
        overall_score=overall_score,
        completeness_score=90.0,
        uniqueness_score=90.0,
        consistency_score=90.0,
        validity_score=90.0,
        grade="A",
        risk_level="low",
    )


def test_missing_numeric_column_recommendation():

    profile = make_profile(
        [
            ColumnProfile(
                name="age",
                pandas_dtype="float64",
                semantic_type="numeric",
                missing_count=20,
                missing_percentage=20.0,
            )
        ]
    )

    quality_report = make_quality_report(
        missing_percentage=20.0
    )

    score = make_quality_score()

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    recommendation = next(
        item
        for item in recommendations
        if item.recommendation_type
        == "missing_values"
    )

    assert recommendation.column_name == "age"
    assert recommendation.priority == "high"
    assert "median" in recommendation.action


def test_constant_column_recommendation():

    profile = make_profile(
        [
            ColumnProfile(
                name="country",
                pandas_dtype="str",
                semantic_type="categorical",
                unique_count=1,
            )
        ]
    )

    quality_report = make_quality_report(
        constant_columns=["country"]
    )

    score = make_quality_score()

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    assert any(
        item.recommendation_type
        == "constant_column"
        for item in recommendations
    )


def test_identifier_recommendation():

    profile = make_profile(
        [
            ColumnProfile(
                name="customer_id",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=100,
                cardinality_ratio=1.0,
                is_identifier=True,
                identifier_confidence=1.0,
            )
        ]
    )

    quality_report = make_quality_report()

    score = make_quality_score()

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    recommendation = next(
        item
        for item in recommendations
        if item.recommendation_type
        == "identifier"
    )

    assert recommendation.column_name == "customer_id"
    assert recommendation.confidence == 1.0


def test_email_pattern_recommendation():

    profile = make_profile(
        [
            ColumnProfile(
                name="email",
                pandas_dtype="str",
                semantic_type="text",
                value_pattern="email",
                pattern_confidence=1.0,
                pattern_match_percentage=100.0,
            )
        ]
    )

    quality_report = make_quality_report()

    score = make_quality_score()

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    recommendation = next(
        item
        for item in recommendations
        if item.recommendation_type
        == "value_pattern"
    )

    assert recommendation.column_name == "email"
    assert "structured contact" in (
        recommendation.action
    )


def test_duplicate_rows_recommendation():

    profile = make_profile(
        [
            ColumnProfile(
                name="age",
                pandas_dtype="int64",
                semantic_type="numeric",
            )
        ]
    )

    quality_report = make_quality_report(
        duplicate_rows=25,
        duplicate_percentage=25.0,
    )

    score = make_quality_score()

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    recommendation = next(
        item
        for item in recommendations
        if item.recommendation_type
        == "duplicate_rows"
    )

    assert recommendation.priority == "high"


def test_low_quality_dataset_recommendation():

    profile = make_profile(
        [
            ColumnProfile(
                name="age",
                pandas_dtype="float64",
            )
        ]
    )

    quality_report = make_quality_report()

    score = make_quality_score(
        overall_score=60.0
    )

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    assert any(
        item.recommendation_type
        == "overall_quality"
        for item in recommendations
    )


def test_recommendations_are_sorted_by_priority():

    profile = make_profile(
        [
            ColumnProfile(
                name="age",
                pandas_dtype="float64",
                semantic_type="numeric",
                missing_percentage=60.0,
                missing_count=60,
            ),
            ColumnProfile(
                name="customer_id",
                pandas_dtype="int64",
                semantic_type="numeric",
                is_identifier=True,
                identifier_confidence=1.0,
            ),
        ]
    )

    quality_report = make_quality_report(
        missing_percentage=60.0
    )

    score = make_quality_score(
        overall_score=60.0
    )

    engine = RecommendationEngine()

    recommendations = engine.generate(
        profile,
        quality_report,
        score,
    )

    priorities = [
        item.priority
        for item in recommendations
    ]

    priority_values = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    numeric_priorities = [
        priority_values[p]
        for p in priorities
    ]

    assert numeric_priorities == sorted(
        numeric_priorities
    )