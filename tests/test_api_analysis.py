from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_dataset_endpoint():

    csv_content = (
        "customer_id,age,city,country,salary\n"
        "1,25,Delhi,India,30000\n"
        "2,,Mumbai,India,45000\n"
        "2,,Mumbai,India,45000\n"
        "3,35,,India,50000\n"
        "4,40,Delhi,India,\n"
    )

    response = client.post(
        "/api/v1/analyze",
        files={
            "file": (
                "api_test.csv",
                BytesIO(
                    csv_content.encode("utf-8")
                ),
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "api_test.csv"

    assert "profile" in data

    assert "quality_report" in data

    assert "quality_score" in data

    assert "ml_insights" in data

    assert "feature_insights" in data

    assert "recommendations" in data

    assert "preparation" in data

    assert data["preparation"]["success"] is True

    assert (
        data["preparation"][
            "transformations_applied"
        ]
        > 0
    )

    assert "processed_dataset" in data

    processed = data["processed_dataset"]

    assert processed is not None

    assert processed["rows"] == 4

    assert processed["columns"] == 4

    assert processed["filename"].endswith(
        ".csv"
    )

    assert processed["path"].endswith(
        processed["filename"]
    )