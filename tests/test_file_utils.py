from app.utils.file_utils import (
    generate_unique_filename,
    get_file_extension,
    is_supported_extension,
    sanitize_filename,
)


def test_get_file_extension():
    assert get_file_extension("CUSTOMERS.CSV") == ".csv"
    assert get_file_extension("data.XLSX") == ".xlsx"


def test_supported_extensions():
    assert is_supported_extension("data.csv")
    assert is_supported_extension("data.xlsx")
    assert is_supported_extension("data.xls")
    assert is_supported_extension("data.json")


def test_unsupported_extension():
    assert not is_supported_extension("data.txt")
    assert not is_supported_extension("data.pdf")


def test_sanitize_filename():
    assert sanitize_filename("../../secret.csv") == "secret.csv"


def test_generate_unique_filename():
    filename = generate_unique_filename("customers.csv")

    assert filename.startswith("customers_")
    assert filename.endswith(".csv")

    assert filename != "customers.csv"