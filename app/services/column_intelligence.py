from app.models.column_insight import ColumnInsight
from app.models.dataset_profile import ColumnProfile
from app.utils.logger import get_logger


logger = get_logger(__name__)


class ColumnIntelligence:
    """Generate actionable intelligence from column profiles."""

    def analyze(
        self,
        column: ColumnProfile,
    ) -> list[ColumnInsight]:
        """Generate insights for a single column."""

        insights = []

        # Identifier insight
        if column.is_identifier:

            insights.append(
                ColumnInsight(
                    column_name=column.name,
                    insight_type="identifier",
                    severity="info",
                    message=(
                        f"'{column.name}' appears to be "
                        "an identifier column."
                    ),
                    confidence=column.identifier_confidence,
                )
            )

        # Missing value insight
        if column.missing_percentage > 0:

            severity = "warning"

            if column.missing_percentage >= 50:
                severity = "critical"

            insights.append(
                ColumnInsight(
                    column_name=column.name,
                    insight_type="missing_values",
                    severity=severity,
                    message=(
                        f"'{column.name}' contains "
                        f"{column.missing_percentage:.2f}% "
                        "missing values."
                    ),
                    confidence=1.0,
                )
            )

        # Constant column
        if (
            column.unique_count <= 1
            and column.missing_count == 0
        ):

            insights.append(
                ColumnInsight(
                    column_name=column.name,
                    insight_type="constant",
                    severity="warning",
                    message=(
                        f"'{column.name}' contains only "
                        "one unique value and may provide "
                        "little analytical value."
                    ),
                    confidence=1.0,
                )
            )

        # Pattern insight
        if (
            column.value_pattern != "unknown"
            and column.pattern_confidence >= 0.8
        ):

            insights.append(
                ColumnInsight(
                    column_name=column.name,
                    insight_type="value_pattern",
                    severity="info",
                    message=(
                        f"'{column.name}' appears to contain "
                        f"{column.value_pattern} values."
                    ),
                    confidence=column.pattern_confidence,
                )
            )

        # High cardinality insight
        if (
            column.cardinality_ratio >= 0.95
            and not column.is_identifier
        ):

            insights.append(
                ColumnInsight(
                    column_name=column.name,
                    insight_type="high_cardinality",
                    severity="warning",
                    message=(
                        f"'{column.name}' has very high "
                        "cardinality and may require "
                        "special handling during analysis."
                    ),
                    confidence=column.cardinality_ratio,
                )
            )

        logger.info(
            "Generated %s insights for column '%s'",
            len(insights),
            column.name,
        )

        return insights