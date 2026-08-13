from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


client = TestClient(app)


def test_download_processed_dataset(
    tmp_path,
    monkeypatch,
):

    monkeypatch.setattr(
        settings,
        "processed_data_dir",
        str(tmp_path),
    )

    filename = "customers_processed_test.csv"

    processed_file = tmp_path / filename

    processed_file.write_text(
        "customer_id,age\n"
        "1,25\n"
        "2,30\n",
        encoding="utf-8",
    )

    response = client.get(
        f"/api/v1/datasets/{filename}"
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith("text/csv")

    assert response.content.decode(
        "utf-8"
    ).splitlines() == [
        "customer_id,age",
        "1,25",
        "2,30",
    ]


def test_download_missing_processed_dataset():

    response = client.get(
        "/api/v1/datasets/does_not_exist.csv"
    )

    assert response.status_code == 404


def test_download_rejects_invalid_filename():

    response = client.get(
        "/api/v1/datasets/../secret.csv"
    )

    assert response.status_code in {
        400,
        404,
    }


def test_download_rejects_non_csv():

    response = client.get(
        "/api/v1/datasets/test.txt"
    )

    assert response.status_code == 400