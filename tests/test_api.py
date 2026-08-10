from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "DataPilot AI"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_csv():
    csv_content = (
        "id,name,age\n"
        "1,John,25\n"
        "2,Sarah,31\n"
        "3,Mike,28\n"
    )

    response = client.post(
        "/dataset/upload",
        files={
            "file": (
                "test.csv",
                BytesIO(csv_content.encode("utf-8")),
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    dataset = data["dataset"]

    assert dataset["rows"] == 3
    assert dataset["columns"] == 3
    assert dataset["original_filename"] == "test.csv"


def test_upload_unsupported_file():
    response = client.post(
        "/dataset/upload",
        files={
            "file": (
                "test.txt",
                BytesIO(b"hello"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert "Unsupported file type" in data["detail"]