from __future__ import annotations

import pandas as pd

from app.models.transformation import Transformation
from app.utils.logger import get_logger


logger = get_logger(__name__)


class TransformationExecutor:
    """Execute planned dataset transformations safely."""

    def execute(
        self,
        dataframe: pd.DataFrame,
        transformations: list[Transformation],
    ) -> pd.DataFrame:
        """
        Apply transformations to a copy of the input DataFrame.

        The original DataFrame is never modified.
        """

        result = dataframe.copy()

        for transformation in transformations:

            transformation_type = (
                transformation.transformation_type
            )

            logger.info(
                "Applying transformation: %s | column=%s",
                transformation_type,
                transformation.column_name,
            )

            # ========================================================
            # Missing value imputation
            # ========================================================

            if (
                transformation_type
                == "missing_value_imputation"
            ):
                self._impute_missing_values(
                    result,
                    transformation,
                )

            # ========================================================
            # Duplicate removal
            # ========================================================

            elif (
                transformation_type
                == "duplicate_removal"
            ):
                self._remove_duplicates(
                    result,
                    transformation,
                )

            # ========================================================
            # Constant column removal
            # ========================================================

            elif (
                transformation_type
                == "constant_column_removal"
            ):
                self._remove_column(
                    result,
                    transformation,
                )

            # ========================================================
            # Identifier exclusion
            # ========================================================
            #
            # IMPORTANT:
            # Identifier exclusion does NOT remove the column.
            #
            # The identifier remains available for record tracking,
            # while the transformation metadata indicates that it
            # should be excluded from future ML feature selection.
            # ========================================================

            elif (
                transformation_type
                == "identifier_exclusion"
            ):
                self._exclude_identifier(
                    result,
                    transformation,
                )

            # ========================================================
            # Unsupported transformation
            # ========================================================

            else:
                logger.warning(
                    "Unsupported transformation type: %s",
                    transformation_type,
                )

        logger.info(
            "Transformation execution completed: "
            "%s rows, %s columns",
            len(result),
            len(result.columns),
        )

        return result

    # ================================================================
    # Missing values
    # ================================================================

    def _impute_missing_values(
        self,
        dataframe: pd.DataFrame,
        transformation: Transformation,
    ) -> None:
        """Impute missing values using the planned strategy."""

        column_name = transformation.column_name

        if not column_name:
            raise ValueError(
                "Missing-value transformation requires "
                "a column name."
            )

        if column_name not in dataframe.columns:
            raise ValueError(
                f"Column '{column_name}' does not exist."
            )

        strategy = transformation.parameters.get(
            "strategy",
            transformation.method,
        )

        series = dataframe[column_name]

        # ------------------------------------------------------------
        # Median
        # ------------------------------------------------------------

        if strategy == "median":

            if not pd.api.types.is_numeric_dtype(
                series
            ):
                raise ValueError(
                    "Median imputation requires a numeric "
                    f"column: '{column_name}'."
                )

            value = series.median()

            dataframe[column_name] = (
                series.fillna(value)
            )

        # ------------------------------------------------------------
        # Mode
        # ------------------------------------------------------------

        elif strategy == "mode":

            modes = series.mode()

            if modes.empty:
                logger.warning(
                    "Unable to determine mode for column '%s'.",
                    column_name,
                )
                return

            value = modes.iloc[0]

            dataframe[column_name] = (
                series.fillna(value)
            )

        # ------------------------------------------------------------
        # Unsupported strategy
        # ------------------------------------------------------------

        else:
            raise ValueError(
                "Unsupported imputation strategy: "
                f"'{strategy}'."
            )

    # ================================================================
    # Duplicate rows
    # ================================================================

    def _remove_duplicates(
        self,
        dataframe: pd.DataFrame,
        transformation: Transformation,
    ) -> None:
        """Remove duplicate rows."""

        keep = transformation.parameters.get(
            "keep",
            "first",
        )

        dataframe.drop_duplicates(
            keep=keep,
            inplace=True,
        )

    # ================================================================
    # Column removal
    # ================================================================

    def _remove_column(
        self,
        dataframe: pd.DataFrame,
        transformation: Transformation,
    ) -> None:
        """Remove a column from the prepared dataset."""

        column_name = transformation.column_name

        if not column_name:
            raise ValueError(
                "Column removal requires a column name."
            )

        if column_name not in dataframe.columns:
            raise ValueError(
                f"Column '{column_name}' does not exist."
            )

        dataframe.drop(
            columns=[column_name],
            inplace=True,
        )

    # ================================================================
    # Identifier exclusion
    # ================================================================

    def _exclude_identifier(
        self,
        dataframe: pd.DataFrame,
        transformation: Transformation,
    ) -> None:
        """
        Preserve an identifier column in the prepared dataset.

        Identifier exclusion is a metadata/ML-feature decision,
        not a request to physically delete the column.
        """

        column_name = transformation.column_name

        if not column_name:
            raise ValueError(
                "Identifier exclusion requires "
                "a column name."
            )

        if column_name not in dataframe.columns:
            raise ValueError(
                f"Column '{column_name}' does not exist."
            )

        logger.info(
            "Preserving identifier column '%s' "
            "for record tracking; excluding it from "
            "future ML feature selection.",
            column_name,
        )