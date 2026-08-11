from app.models.dataset_insight import DatasetInsight
from app.models.dataset_profile import DatasetProfile
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DatasetIntelligence:
    """Generate dataset-level intelligence."""

    def analyze(
        self,
        profile: DatasetProfile,
    ) -> list[DatasetInsight]:
        """Analyze a complete dataset profile."""

        insights = []

        # ==========================================
        # Empty dataset
        # ==========================================

        if profile.row_count == 0:

            insights.append(
                DatasetInsight(
                    insight_type="empty_dataset",
                    severity="critical",
                    message=(
                        "The dataset contains no rows."
                    ),
                    confidence=1.0,
                )
            )

            return insights

        # ==========================================
        # Missing values
        # ==========================================

        if profile.missing_value_percentage > 0:

            severity = "warning"

            if (
                profile.missing_value_percentage
                >= 50
            ):
                severity = "critical"

            insights.append(
                DatasetInsight(
                    insight_type="missing_values",
                    severity=severity,
                    message=(
                        f"The dataset contains "
                        f"{profile.missing_value_percentage:.2f}% "
                        "missing values."
                    ),
                    confidence=1.0,
                )
            )

        # ==========================================
        # Duplicate rows
        # ==========================================

        if profile.duplicate_row_count > 0:

            severity = "warning"

            if (
                profile.duplicate_percentage
                >= 20
            ):
                severity = "critical"

            insights.append(
                DatasetInsight(
                    insight_type="duplicate_rows",
                    severity=severity,
                    message=(
                        f"The dataset contains "
                        f"{profile.duplicate_row_count} "
                        f"duplicate rows "
                        f"({profile.duplicate_percentage:.2f}%)."
                    ),
                    confidence=1.0,
                )
            )

        # ==========================================
        # Constant columns
        # ==========================================

        constant_columns = [
            column.name
            for column in profile.columns
            if (
                column.unique_count <= 1
                and column.missing_count == 0
            )
        ]

        if constant_columns:

            insights.append(
                DatasetInsight(
                    insight_type="constant_columns",
                    severity="warning",
                    message=(
                        "The following columns contain "
                        "only one unique value: "
                        + ", ".join(
                            constant_columns
                        )
                    ),
                    confidence=1.0,
                )
            )

        # ==========================================
        # Identifier columns
        # ==========================================

        identifiers = [
            column.name
            for column in profile.columns
            if column.is_identifier
        ]

        if identifiers:

            insights.append(
                DatasetInsight(
                    insight_type="identifier_columns",
                    severity="info",
                    message=(
                        "Potential identifier columns: "
                        + ", ".join(
                            identifiers
                        )
                    ),
                    confidence=1.0,
                )
            )

        # ==========================================
        # Pattern columns
        # ==========================================

        pattern_columns = [
            (
                column.name,
                column.value_pattern,
            )
            for column in profile.columns
            if (
                column.value_pattern
                != "unknown"
                and column.pattern_confidence
                >= 0.8
            )
        ]

        if pattern_columns:

            descriptions = [
                f"{name} ({pattern})"
                for name, pattern
                in pattern_columns
            ]

            insights.append(
                DatasetInsight(
                    insight_type="detected_patterns",
                    severity="info",
                    message=(
                        "Detected value patterns: "
                        + ", ".join(
                            descriptions
                        )
                    ),
                    confidence=0.8,
                )
            )

        # ==========================================
        # Dataset composition
        # ==========================================

        insights.append(
            DatasetInsight(
                insight_type="dataset_composition",
                severity="info",
                message=(
                    f"The dataset contains "
                    f"{profile.row_count} rows and "
                    f"{profile.column_count} columns: "
                    f"{profile.numeric_column_count} numeric, "
                    f"{profile.categorical_column_count} categorical, "
                    f"{profile.text_column_count} text, "
                    f"{profile.datetime_column_count} datetime, "
                    f"and "
                    f"{profile.boolean_column_count} boolean."
                ),
                confidence=1.0,
            )
        )

        logger.info(
            "Generated %s dataset-level insights",
            len(insights),
        )

        return insights