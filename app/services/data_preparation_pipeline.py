from __future__ import annotations

import pandas as pd

from app.models.data_preparation_result import (
    DataPreparationResult,
)
from app.models.processed_dataset import (
    ProcessedDataset,
)
from app.services.data_quality_analyzer import (
    DataQualityAnalyzer,
)
from app.services.dataset_profiler import (
    DatasetProfiler,
)
from app.services.processed_dataset_writer import (
    ProcessedDatasetWriter,
)
from app.services.transformation_executor import (
    TransformationExecutor,
)
from app.services.transformation_planner import (
    TransformationPlanner,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DataPreparationPipeline:
    """Analyze, transform, validate, and save a dataset."""

    def __init__(self) -> None:

        self.profiler = DatasetProfiler()

        self.quality_analyzer = (
            DataQualityAnalyzer()
        )

        self.planner = TransformationPlanner()

        self.executor = TransformationExecutor()

        self.writer = ProcessedDatasetWriter()

    def prepare(
        self,
        dataframe: pd.DataFrame,
        filename: str | None = None,
        save_processed: bool = True,
    ) -> tuple[
        pd.DataFrame,
        DataPreparationResult,
        ProcessedDataset | None,
    ]:
        """
        Analyze and automatically prepare a dataset.

        The original DataFrame is never modified.

        Returns:
            prepared dataframe,
            preparation summary,
            processed dataset metadata.
        """

        if dataframe is None:
            raise ValueError(
                "Dataframe cannot be None."
            )

        if filename is None:
            filename = "dataset.csv"

        original = dataframe.copy()

        logger.info(
            "Starting data preparation: %s",
            filename,
        )

        # ============================================================
        # 1. Profile original dataset
        # ============================================================

        original_profile = (
            self.profiler.profile(
                original,
                filename=filename,
            )
        )

        # ============================================================
        # 2. Analyze original data quality
        # ============================================================

        original_quality = (
            self.quality_analyzer.analyze(
                original
            )
        )

        # ============================================================
        # 3. Generate transformation plan
        # ============================================================

        transformations = (
            self.planner.plan(
                profile=original_profile,
                quality_report=original_quality,
            )
        )

        logger.info(
            "Transformation plan contains %s actions.",
            len(transformations),
        )

        # ============================================================
        # 4. Execute transformations
        # ============================================================

        prepared = self.executor.execute(
            original,
            transformations,
        )

        # ============================================================
        # 5. Profile prepared dataset
        # ============================================================

        final_profile = (
            self.profiler.profile(
                prepared,
                filename=filename,
            )
        )

        # ============================================================
        # 6. Validate final dataset
        # ============================================================

        final_quality = (
            self.quality_analyzer.analyze(
                prepared
            )
        )

        if final_quality.missing_percentage > 0:
            logger.warning(
                "Prepared dataset still contains "
                "%.2f%% missing values.",
                final_quality.missing_percentage,
            )

        # ============================================================
        # 7. Build transformation descriptions
        # ============================================================

        transformation_descriptions: list[str] = []

        for transformation in transformations:

            description = (
                transformation.transformation_type
            )

            if transformation.column_name:
                description += (
                    f": {transformation.column_name}"
                )

            if transformation.method:
                description += (
                    f" ({transformation.method})"
                )

            transformation_descriptions.append(
                description
            )

        # ============================================================
        # 8. Build preparation result
        # ============================================================

        preparation_result = DataPreparationResult(
            original_row_count=(
                original_profile.row_count
            ),
            final_row_count=(
                final_profile.row_count
            ),
            original_column_count=(
                original_profile.column_count
            ),
            final_column_count=(
                final_profile.column_count
            ),
            original_missing_percentage=(
                original_profile.missing_value_percentage
            ),
            final_missing_percentage=(
                final_profile.missing_value_percentage
            ),
            transformations_applied=(
                len(transformations)
            ),
            transformations=(
                transformation_descriptions
            ),
            success=True,
            message=(
                "Dataset preparation completed successfully."
            ),
        )

        # ============================================================
        # 9. Save processed dataset
        # ============================================================

        processed_dataset = None

        if save_processed:

            processed_dataset = (
                self.writer.write(
                    prepared,
                    filename,
                )
            )

            logger.info(
                "Processed dataset created: %s",
                processed_dataset.path,
            )

        # ============================================================
        # 10. Final logging
        # ============================================================

        logger.info(
            "Data preparation completed: "
            "%s → %s rows, "
            "%s → %s columns, "
            "%s transformations.",
            preparation_result.original_row_count,
            preparation_result.final_row_count,
            preparation_result.original_column_count,
            preparation_result.final_column_count,
            preparation_result.transformations_applied,
        )

        return (
            prepared,
            preparation_result,
            processed_dataset,
        )