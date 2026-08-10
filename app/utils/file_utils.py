from pathlib import Path
from uuid import uuid4


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
}


def get_file_extension(filename: str) -> str:
    """Return a normalized file extension."""

    return Path(filename).suffix.lower()


def is_supported_extension(filename: str) -> bool:
    """Check whether the filename has a supported dataset extension."""

    return get_file_extension(filename) in SUPPORTED_EXTENSIONS


def sanitize_filename(filename: str) -> str:
    """
    Return a safe filename containing only the final path component.

    This prevents user-provided filenames from being interpreted
    as filesystem paths.
    """

    return Path(filename).name


def generate_unique_filename(filename: str) -> str:
    """
    Generate a unique filename while preserving the original extension.

    Example:
        customers.csv
        →
        customers_a13f8c2d.csv
    """

    safe_name = sanitize_filename(filename)

    path = Path(safe_name)

    unique_id = uuid4().hex[:8]

    return f"{path.stem}_{unique_id}{path.suffix.lower()}"


def ensure_directory(directory: Path) -> Path:
    """Create a directory if it doesn't exist and return it."""

    directory.mkdir(parents=True, exist_ok=True)

    return directory