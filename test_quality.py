import pandas as pd

from app.services.data_quality_analyzer import (
    DataQualityAnalyzer,
)


dataframe = pd.DataFrame(
    {
        "customer_id": [1, 2, 3, 4, 4],
        "name": [
            "John",
            "Sarah",
            None,
            "Mike",
            "Mike",
        ],
        "age": [
            25,
            31,
            28,
            None,
            None,
        ],
        "country": [
            "India",
            "India",
            "India",
            "India",
            "India",
        ],
    }
)


analyzer = DataQualityAnalyzer()

report = analyzer.analyze(dataframe)

print(
    report.model_dump_json(
        indent=2
    )
)