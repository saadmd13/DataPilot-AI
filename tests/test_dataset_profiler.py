import pandas as pd

from app.services.dataset_profiler import DatasetProfiler


def test_dataset_profile_basic_counts():
    dataframe = pd.DataFrame(
        {
            "customer_id": list(range(1, 101)),
            "name": [f"Customer {i}" for i in range(1, 101)],
            "age": [20 + (i % 30) for i in range(100)],
            "city": [
                [
                    "Hyderabad",
                    "Mumbai",
                    "Delhi",
                    "Bangalore",
                ][i % 4]
                for i in range(100)
            ],
            "active": [i % 2 == 0 for i in range(100)],
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(
        dataframe,
        filename="test_dataset.csv",
    )

    assert profile.row_count == 100
    assert profile.column_count == 5

    assert profile.numeric_column_count == 2
    assert profile.categorical_column_count == 1
    assert profile.text_column_count == 1
    assert profile.boolean_column_count == 1
    assert profile.datetime_column_count == 0


def test_duplicate_detection():
    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 2, 3],
            "name": ["A", "B", "B", "C"],
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(dataframe)

    assert profile.duplicate_row_count == 1
    assert profile.duplicate_percentage == 25.0


def test_missing_value_detection():
    dataframe = pd.DataFrame(
        {
            "age": [20, 30, None, 40],
            "city": ["Delhi", None, "Mumbai", "Delhi"],
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(dataframe)

    assert profile.missing_value_count == 2
    assert profile.missing_value_percentage == 25.0

def test_identifier_detection():
    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4, 5],
            "age": [20, 25, 30, 35, 40],
            "city": [
                "Delhi",
                "Mumbai",
                "Delhi",
                "Mumbai",
                "Delhi",
            ],
            "name": [
                "John",
                "Sarah",
                "Mike",
                "Aisha",
                "David",
            ],
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(dataframe)

    customer_id = next(
        column
        for column in profile.columns
        if column.name == "customer_id"
    )

    age = next(
        column
        for column in profile.columns
        if column.name == "age"
    )

    city = next(
        column
        for column in profile.columns
        if column.name == "city"
    )

    name = next(
        column
        for column in profile.columns
        if column.name == "name"
    )

    assert customer_id.is_identifier is True
    assert customer_id.identifier_confidence == 1.0

    assert age.is_identifier is False
    assert city.is_identifier is False
    assert name.is_identifier is False
def test_datetime_detection():
    dataframe = pd.DataFrame(
        {
            "signup_date": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
                "2026-01-04",
            ]
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(dataframe)

    column = profile.columns[0]

    assert column.semantic_type == "datetime"

    assert (
        column.datetime_parse_success_rate
        == 1.0
    )


def test_text_is_not_datetime():
    dataframe = pd.DataFrame(
        {
            "name": [
                "John",
                "Sarah",
                "Mike",
                "Aisha",
            ]
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(dataframe)

    column = profile.columns[0]

    assert column.semantic_type == "text"

    assert (
        column.datetime_parse_success_rate
        == 0.0
    )
def test_email_pattern_detection():
    dataframe = pd.DataFrame(
        {
            "email": [
                "saad@gmail.com",
                "john@yahoo.com",
                "aisha@example.com",
                "user@test.org",
            ]
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(
        dataframe
    )

    column = profile.columns[0]

    assert column.value_pattern == "email"

    assert (
        column.pattern_confidence
        == 1.0
    )

    assert (
        column.pattern_match_percentage
        == 100.0
    )


def test_url_pattern_detection():
    dataframe = pd.DataFrame(
        {
            "website": [
                "https://github.com",
                "https://google.com",
                "https://example.com",
                "https://openai.com",
            ]
        }
    )

    profiler = DatasetProfiler()

    profile = profiler.profile(
        dataframe
    )

    column = profile.columns[0]

    assert column.value_pattern == "url"

    assert (
        column.pattern_confidence
        == 1.0
    )