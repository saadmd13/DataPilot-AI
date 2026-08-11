from app.models.data_quality import DataQualityReport
from app.models.dataset_profile import (
    ColumnProfile,
    DatasetProfile,
)
from app.services.quality_score_engine import (
    QualityScoreEngine,
)


def make_profile(
    columns: list[ColumnProfile],
    rows: int = 100,
) -> DatasetProfile:

    return DatasetProfile(
        filename="test.csv",
        row_count=rows,
        column_count=len(columns),
        columns=columns,
    )


def test_perfect_dataset_gets_high_score():

    profile = make_profile(
        [
            ColumnProfile(
                name="customer_id",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=100,
                unique_percentage=100.0,
                cardinality_ratio=1.0,
                is_identifier=True,
            ),
            ColumnProfile(
                name="age",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=30,
                unique_percentage=30.0,
            ),
        ]
    )

    quality_report = DataQualityReport(
        total_cells=200,
        missing_cells=0,
        missing_percentage=0.0,
        duplicate_rows=0,
        duplicate_percentage=0.0,
        constant_columns=[],
    )

    engine = QualityScoreEngine()

    result = engine.calculate(
        profile,
        quality_report,
    )

    assert result.overall_score >= 90
    assert result.grade == "A"
    assert result.risk_level == "low"


def test_missing_values_reduce_completeness():

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

    quality_report = DataQualityReport(
        total_cells=100,
        missing_cells=20,
        missing_percentage=20.0,
        duplicate_rows=0,
        duplicate_percentage=0.0,
    )

    engine = QualityScoreEngine()

    result = engine.calculate(
        profile,
        quality_report,
    )

    assert result.completeness_score == 80.0
    assert result.overall_score < 100


def test_duplicate_rows_reduce_uniqueness():

    profile = make_profile(
        [
            ColumnProfile(
                name="age",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=50,
            )
        ]
    )

    quality_report = DataQualityReport(
        total_cells=100,
        missing_cells=0,
        missing_percentage=0.0,
        duplicate_rows=10,
        duplicate_percentage=10.0,
    )

    engine = QualityScoreEngine()

    result = engine.calculate(
        profile,
        quality_report,
    )

    assert result.uniqueness_score == 90.0
    assert result.warning_issues_count >= 1


def test_constant_columns_reduce_consistency():

    profile = make_profile(
        [
            ColumnProfile(
                name="country",
                pandas_dtype="str",
                semantic_type="categorical",
                unique_count=1,
            ),
            ColumnProfile(
                name="age",
                pandas_dtype="int64",
                semantic_type="numeric",
                unique_count=30,
            ),
        ]
    )

    quality_report = DataQualityReport(
        total_cells=200,
        missing_cells=0,
        missing_percentage=0.0,
        duplicate_rows=0,
        duplicate_percentage=0.0,
        constant_columns=["country"],
    )

    engine = QualityScoreEngine()

    result = engine.calculate(
        profile,
        quality_report,
    )

    assert result.consistency_score < 100
    assert result.warning_issues_count >= 1


def test_grade_and_risk_boundaries():

    engine = QualityScoreEngine()

    assert engine._calculate_grade(95) == "A"
    assert engine._calculate_grade(85) == "B"
    assert engine._calculate_grade(75) == "C"
    assert engine._calculate_grade(65) == "D"
    assert engine._calculate_grade(50) == "F"

    assert engine._calculate_risk_level(90) == "low"
    assert engine._calculate_risk_level(75) == "medium"
    assert engine._calculate_risk_level(60) == "high"
    assert engine._calculate_risk_level(40) == "critical"