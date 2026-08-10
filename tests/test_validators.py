from pathlib import Path

from app.utils.validators import validate_dataset_file


def test_valid_dataset(tmp_path):
    file_path = tmp_path / "customers.csv"

    file_path.write_text(
        "id,name\n1,John\n2,Sarah\n",
        encoding="utf-8",
    )

    result = validate_dataset_file(file_path)

    assert result.is_valid
    assert result.extension == ".csv"
    assert result.size_bytes > 0


def test_missing_file(tmp_path):
    file_path = tmp_path / "missing.csv"

    result = validate_dataset_file(file_path)

    assert not result.is_valid
    assert result.message == "File does not exist."


def test_unsupported_file(tmp_path):
    file_path = tmp_path / "document.txt"

    file_path.write_text(
        "hello",
        encoding="utf-8",
    )

    result = validate_dataset_file(file_path)

    assert not result.is_valid
    assert "Unsupported file type" in result.message


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"

    file_path.touch()

    result = validate_dataset_file(file_path)

    assert not result.is_valid
    assert result.message == "File is empty."