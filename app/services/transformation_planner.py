from __future__ import annotations

from app.models.data_quality import DataQualityReport
from app.models.dataset_profile import DatasetProfile
from app.models.quality_score import QualityScore
from app.models.transformation import Transformation
from app.utils.logger import get_logger


logger = get_logger(__name__)


class TransformationPlanner:
    """Generate safe transformation plans from dataset intelligence."""

    def plan(
        self,
        profile: DatasetProfile,
        quality_report: DataQualityReport,
        quality_score: QualityScore | None = None,
    ) -> list[Transformation]:
        """Generate a list of recommended transformations."""

        transformations: list[Transformation] = []

        # ============================================================
        # Missing values
        # ============================================================

        for column in profile.columns:

            if column.missing_count <= 0:
                continue

            # --------------------------------------------------------
            # Numeric → median
            # --------------------------------------------------------

            if column.semantic_type == "numeric":

                transformations.append(
                    Transformation(
                        transformation_type=(
                            "missing_value_imputation"
                        ),
                        column_name=column.name,
                        method="median",
                        reason=(
                            f"Numeric column '{column.name}' "
                            f"contains "
                            f"{column.missing_percentage:.2f}% "
                            "missing values."
                        ),
                        confidence=0.90,
                        parameters={
                            "strategy": "median",
                        },
                    )
                )

            # --------------------------------------------------------
            # Categorical → mode
            # --------------------------------------------------------

            elif column.semantic_type == "categorical":

                transformations.append(
                    Transformation(
                        transformation_type=(
                            "missing_value_imputation"
                        ),
                        column_name=column.name,
                        method="mode",
                        reason=(
                            f"Categorical column "
                            f"'{column.name}' contains "
                            f"{column.missing_percentage:.2f}% "
                            "missing values."
                        ),
                        confidence=0.90,
                        parameters={
                            "strategy": "mode",
                        },
                    )
                )

            # --------------------------------------------------------
            # Boolean → mode
            # --------------------------------------------------------

            elif column.semantic_type == "boolean":

                transformations.append(
                    Transformation(
                        transformation_type=(
                            "missing_value_imputation"
                        ),
                        column_name=column.name,
                        method="mode",
                        reason=(
                            f"Boolean column '{column.name}' "
                            f"contains "
                            f"{column.missing_percentage:.2f}% "
                            "missing values."
                        ),
                        confidence=0.90,
                        parameters={
                            "strategy": "mode",
                        },
                    )
                )

            # --------------------------------------------------------
            # Text → mode
            # --------------------------------------------------------

            elif column.semantic_type == "text":

                transformations.append(
                    Transformation(
                        transformation_type=(
                            "missing_value_imputation"
                        ),
                        column_name=column.name,
                        method="mode",
                        reason=(
                            f"Text column '{column.name}' "
                            f"contains "
                            f"{column.missing_percentage:.2f}% "
                            "missing values."
                        ),
                        confidence=0.85,
                        parameters={
                            "strategy": "mode",
                        },
                    )
                )

            # --------------------------------------------------------
            # Datetime → no automatic imputation
            # --------------------------------------------------------

            elif column.semantic_type == "datetime":

                logger.info(
                    "Skipping automatic datetime imputation "
                    "for column '%s'.",
                    column.name,
                )

        # ============================================================
        # Duplicate rows
        # ============================================================

        if quality_report.duplicate_rows > 0:

            transformations.append(
                Transformation(
                    transformation_type="duplicate_removal",
                    method="drop_duplicates",
                    reason=(
                        f"Dataset contains "
                        f"{quality_report.duplicate_rows} "
                        "duplicate rows."
                    ),
                    confidence=0.98,
                    parameters={
                        "keep": "first",
                    },
                )
            )

        # ============================================================
        # Constant columns
        # ============================================================

        for column_name in quality_report.constant_columns:

            transformations.append(
                Transformation(
                    transformation_type=(
                        "constant_column_removal"
                    ),
                    column_name=column_name,
                    method="drop",
                    reason=(
                        f"Column '{column_name}' "
                        "contains only one unique value "
                        "and provides no useful variance."
                    ),
                    confidence=0.95,
                )
            )

        # ============================================================
        # Identifier columns
        # ============================================================
        #
        # IMPORTANT:
        # Identifier exclusion does NOT mean deleting the column.
        #
        # The transformation executor preserves the identifier
        # in the cleaned dataset while marking it as excluded
        # from future ML feature selection.
        # ============================================================

        for column in profile.columns:

            if not column.is_identifier:
                continue

            transformations.append(
                Transformation(
                    transformation_type=(
                        "identifier_exclusion"
                    ),
                    column_name=column.name,
                    method="exclude_from_features",
                    reason=(
                        f"Column '{column.name}' appears to "
                        "uniquely identify records and should "
                        "generally not be used as a predictive "
                        "feature."
                    ),
                    confidence=column.identifier_confidence,
                    parameters={
                        "preserve_column": True,
                        "exclude_from_ml_features": True,
                    },
                )
            )

        # ============================================================
        # Logging
        # ============================================================

        logger.info(
            "Generated %s transformation plans.",
            len(transformations),
        )

        return transformations