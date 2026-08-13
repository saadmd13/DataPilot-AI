from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.config import settings
from app.models.processed_dataset import ProcessedDataset
from app.utils.file_utils import (
    ensure_directory,
    generate_unique_filename,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


class ProcessedDatasetWriter:
    """Save prepared datasets to processed storage."""

    def write(
        self,
        dataframe: pd.DataFrame,
        original_filename: str,
    ) -> ProcessedDataset:
        """
        Save a prepared DataFrame as a CSV file.

        The input DataFrame is never modified.
        """

        if dataframe is None:
            raise ValueError(
                "Dataframe cannot be None."
            )

        if not original_filename:
            raise ValueError(
                "Original filename is required."
            )

        output_directory = ensure_directory(
            settings.project_root
            / settings.processed_data_dir
        )

        base_filename = Path(
            original_filename
        ).stem

        output_filename = generate_unique_filename(
            f"{base_filename}_processed.csv"
        )

        destination = (
            output_directory
            / output_filename
        )

        logger.info(
            "Saving processed dataset: %s",
            destination,
        )

        dataframe.to_csv(
            destination,
            index=False,
        )

        result = ProcessedDataset(
            filename=output_filename,
            path=str(destination),
            rows=len(dataframe),
            columns=len(dataframe.columns),
            column_names=dataframe.columns.tolist(),
        )

        logger.info(
            "Processed dataset saved successfully: "
            "%s rows, %s columns",
            result.rows,
            result.columns,
        )

        return result