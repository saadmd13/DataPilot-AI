import pandas as pd

from app.services.data_quality_analyzer import (
    DataQualityAnalyzer,
)


def test_missing_value_analysis():

    dataframe = pd.DataFrame(
        {
            "name": [
                "John",
                "Sarah",
                None,
                "Mike",
            ],
            "age": [
                25,
                None,
                30,
                35,
            ],
        }
    )

    analyzer = DataQualityAnalyzer()

    report = analyzer.analyze(dataframe)

    assert report.total_cells == 8
    assert report.missing_cells == 2
    assert report.missing_percentage == 25.0


def test_duplicate_analysis():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 2, 3],
            "name": [
                "A",
                "B",
                "B",
                "C",
            ],
        }
    )

    analyzer = DataQualityAnalyzer()

    report = analyzer.analyze(dataframe)

    assert report.duplicate_rows == 1
    assert report.duplicate_percentage == 25.0


def test_constant_column_detection():

    dataframe = pd.DataFrame(
        {
            "name": [
                "John",
                "Sarah",
                "Mike",
            ],
            "country": [
                "India",
                "India",
                "India",
            ],
        }
    )

    analyzer = DataQualityAnalyzer()

    report = analyzer.analyze(dataframe)

    assert "country" in report.constant_columns

    country = next(
        column
        for column in report.columns
        if column.column_name == "country"
    )

    assert country.is_constant is True
    assert country.unique_count == 1