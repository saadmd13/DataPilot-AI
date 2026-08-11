import pandas as pd

from app.models.data_quality import (
    ColumnQuality,
    DataQualityReport,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DataQualityAnalyzer:
    """Analyze common data-quality issues."""

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> DataQualityReport:
        """Generate a data-quality report."""

        logger.info(
            "Starting data quality analysis."
        )

        row_count = len(dataframe)
        column_count = len(dataframe.columns)

        total_cells = row_count * column_count

        missing_cells = int(
            dataframe.isna().sum().sum()
        )

        missing_percentage = (
            (missing_cells / total_cells) * 100
            if total_cells > 0
            else 0.0
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        duplicate_percentage = (
            (duplicate_rows / row_count) * 100
            if row_count > 0
            else 0.0
        )

        constant_columns = []

        columns = []

        for column in dataframe.columns:

            series = dataframe[column]

            missing_count = int(
                series.isna().sum()
            )

            missing_pct = (
                (missing_count / row_count) * 100
                if row_count > 0
                else 0.0
            )

            unique_count = int(
                series.nunique(
                    dropna=True
                )
            )

            unique_pct = (
                (unique_count / row_count) * 100
                if row_count > 0
                else 0.0
            )

            is_constant = unique_count <= 1

            if is_constant:
                constant_columns.append(
                    str(column)
                )

            columns.append(
                ColumnQuality(
                    column_name=str(column),
                    missing_count=missing_count,
                    missing_percentage=round(
                        missing_pct,
                        2,
                    ),
                    unique_count=unique_count,
                    unique_percentage=round(
                        unique_pct,
                        2,
                    ),
                    is_constant=is_constant,
                )
            )

        report = DataQualityReport(
            total_cells=total_cells,
            missing_cells=missing_cells,
            missing_percentage=round(
                missing_percentage,
                2,
            ),
            duplicate_rows=duplicate_rows,
            duplicate_percentage=round(
                duplicate_percentage,
                2,
            ),
            constant_columns=constant_columns,
            columns=columns,
        )

        logger.info(
            "Data quality analysis completed."
        )

        return report