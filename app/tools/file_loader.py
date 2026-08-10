from pathlib import Path

import pandas as pd

from app.utils.file_utils import get_file_extension
from app.utils.logger import get_logger
from app.utils.validators import validate_dataset_file


logger = get_logger(__name__)


class DatasetLoadError(Exception):
    """Raised when a dataset cannot be loaded."""


def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Validate and load a dataset into a pandas DataFrame.

    Supported formats:
    - CSV
    - XLSX
    - XLS
    - JSON
    """

    file_path = Path(file_path)

    validation = validate_dataset_file(file_path)

    if not validation.is_valid:
        logger.error(
            "Dataset validation failed: %s",
            validation.message,
        )

        raise DatasetLoadError(validation.message)

    extension = get_file_extension(file_path.name)

    logger.info(
        "Loading dataset: %s",
        file_path.name,
    )

    try:
        if extension == ".csv":
            dataframe = pd.read_csv(file_path)

        elif extension in {".xlsx", ".xls"}:
            dataframe = pd.read_excel(file_path)

        elif extension == ".json":
            dataframe = pd.read_json(file_path)

        else:
            raise DatasetLoadError(
                f"Unsupported file type: {extension}"
            )

    except DatasetLoadError:
        raise

    except Exception as exc:
        logger.exception(
            "Failed to load dataset: %s",
            file_path.name,
        )

        raise DatasetLoadError(
            f"Failed to load dataset: {exc}"
        ) from exc

    logger.info(
        "Dataset loaded successfully: %s rows, %s columns",
        len(dataframe),
        len(dataframe.columns),
    )

    return dataframe