from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.utils.file_utils import (
    get_file_extension,
    is_supported_extension,
)


@dataclass
class ValidationResult:
    """Result returned by the dataset file validator."""

    is_valid: bool
    message: str
    filename: str
    extension: str
    size_bytes: int


def validate_dataset_file(file_path: Path) -> ValidationResult:
    """
    Validate a dataset file before loading it.

    Checks:
    - file exists
    - extension is supported
    - file is not empty
    - file does not exceed the configured size limit
    """

    filename = file_path.name
    extension = get_file_extension(filename)

    if not file_path.exists():
        return ValidationResult(
            is_valid=False,
            message="File does not exist.",
            filename=filename,
            extension=extension,
            size_bytes=0,
        )

    if not file_path.is_file():
        return ValidationResult(
            is_valid=False,
            message="Path does not point to a file.",
            filename=filename,
            extension=extension,
            size_bytes=0,
        )

    size_bytes = file_path.stat().st_size

    if not is_supported_extension(filename):
        return ValidationResult(
            is_valid=False,
            message=f"Unsupported file type: {extension or 'none'}",
            filename=filename,
            extension=extension,
            size_bytes=size_bytes,
        )

    if size_bytes == 0:
        return ValidationResult(
            is_valid=False,
            message="File is empty.",
            filename=filename,
            extension=extension,
            size_bytes=size_bytes,
        )

    if size_bytes > settings.max_file_size_bytes:
        return ValidationResult(
            is_valid=False,
            message=(
                f"File exceeds the maximum allowed size of "
                f"{settings.max_file_size_mb} MB."
            ),
            filename=filename,
            extension=extension,
            size_bytes=size_bytes,
        )

    return ValidationResult(
        is_valid=True,
        message="File validation successful.",
        filename=filename,
        extension=extension,
        size_bytes=size_bytes,
    )