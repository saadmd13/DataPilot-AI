from app.models.data_quality import DataQualityReport
from app.models.dataset_profile import DatasetProfile
from app.models.quality_score import QualityScore
from app.models.recommendation import Recommendation
from app.utils.logger import get_logger


logger = get_logger(__name__)


class RecommendationEngine:
    """Generate actionable recommendations from dataset intelligence."""

    def generate(
        self,
        profile: DatasetProfile,
        quality_report: DataQualityReport,
        quality_score: QualityScore,
    ) -> list[Recommendation]:
        """Generate recommendations for a dataset."""

        recommendations: list[Recommendation] = []

        # ==========================================
        # Column-level recommendations
        # ==========================================

        for column in profile.columns:

            # --------------------------------------
            # Missing values
            # --------------------------------------

            if column.missing_percentage > 0:

                if column.semantic_type == "numeric":

                    action = (
                        "Consider median imputation "
                        "for missing numeric values."
                    )

                elif column.semantic_type == "categorical":

                    action = (
                        "Consider replacing missing "
                        "categorical values with the "
                        "most frequent category or "
                        "an explicit 'Unknown' category."
                    )

                elif column.semantic_type == "datetime":

                    action = (
                        "Review the source data before "
                        "imputing missing datetime values."
                    )

                else:

                    action = (
                        "Review the missing values and "
                        "determine whether they should "
                        "be imputed, removed, or retained."
                    )

                priority = self._missing_priority(
                    column.missing_percentage
                )

                recommendations.append(
                    Recommendation(
                        recommendation_type="missing_values",
                        priority=priority,
                        column_name=column.name,
                        title=(
                            f"Handle missing values "
                            f"in '{column.name}'"
                        ),
                        description=(
                            f"'{column.name}' contains "
                            f"{column.missing_percentage:.2f}% "
                            "missing values."
                        ),
                        action=action,
                        confidence=0.95,
                    )
                )

            # --------------------------------------
            # Constant columns
            # --------------------------------------

            if (
                column.unique_count <= 1
                and column.missing_count == 0
            ):

                recommendations.append(
                    Recommendation(
                        recommendation_type="constant_column",
                        priority="medium",
                        column_name=column.name,
                        title=(
                            f"Review constant column "
                            f"'{column.name}'"
                        ),
                        description=(
                            f"'{column.name}' contains "
                            "only one unique value."
                        ),
                        action=(
                            "Consider removing this column "
                            "if it provides no business "
                            "or analytical value."
                        ),
                        confidence=1.0,
                    )
                )

            # --------------------------------------
            # Identifier columns
            # --------------------------------------

            if column.is_identifier:

                recommendations.append(
                    Recommendation(
                        recommendation_type="identifier",
                        priority="low",
                        column_name=column.name,
                        title=(
                            f"Treat '{column.name}' "
                            "as an identifier"
                        ),
                        description=(
                            f"'{column.name}' appears to "
                            "uniquely identify records."
                        ),
                        action=(
                            "Use this column as a record "
                            "identifier rather than as a "
                            "predictive feature unless "
                            "there is a specific reason "
                            "to use it."
                        ),
                        confidence=(
                            column.identifier_confidence
                        ),
                    )
                )

            # --------------------------------------
            # High-cardinality text
            # --------------------------------------

            if (
                column.semantic_type == "text"
                and column.cardinality_ratio >= 0.95
                and not column.is_identifier
            ):

                recommendations.append(
                    Recommendation(
                        recommendation_type="high_cardinality",
                        priority="medium",
                        column_name=column.name,
                        title=(
                            f"Review high-cardinality "
                            f"column '{column.name}'"
                        ),
                        description=(
                            f"'{column.name}' has a "
                            f"cardinality ratio of "
                            f"{column.cardinality_ratio:.2f}."
                        ),
                        action=(
                            "Review whether this column "
                            "should be transformed, "
                            "excluded, or handled using "
                            "special encoding techniques."
                        ),
                        confidence=0.9,
                    )
                )

            # --------------------------------------
            # Structured value patterns
            # --------------------------------------

            if (
                column.value_pattern != "unknown"
                and column.pattern_confidence >= 0.8
            ):

                if column.value_pattern == "email":

                    action = (
                        "Treat this as structured contact "
                        "data and avoid using the raw email "
                        "value directly as a numerical feature."
                    )

                elif column.value_pattern == "phone":

                    action = (
                        "Treat this as structured contact "
                        "data and consider standardizing "
                        "the phone number format."
                    )

                elif column.value_pattern == "url":

                    action = (
                        "Consider extracting useful URL "
                        "components such as domain, path, "
                        "or protocol instead of using the "
                        "raw URL."
                    )

                else:

                    action = (
                        "Review the detected value pattern "
                        "and standardize the values if "
                        "necessary."
                    )

                recommendations.append(
                    Recommendation(
                        recommendation_type="value_pattern",
                        priority="low",
                        column_name=column.name,
                        title=(
                            f"Structured pattern detected "
                            f"in '{column.name}'"
                        ),
                        description=(
                            f"Values in '{column.name}' "
                            f"appear to follow the "
                            f"'{column.value_pattern}' "
                            "pattern."
                        ),
                        action=action,
                        confidence=(
                            column.pattern_confidence
                        ),
                    )
                )

        # ==========================================
        # Dataset-level recommendations
        # ==========================================

        if quality_score.overall_score < 70:

            recommendations.append(
                Recommendation(
                    recommendation_type="overall_quality",
                    priority="high",
                    title="Improve overall dataset quality",
                    description=(
                        f"The dataset has an overall "
                        f"quality score of "
                        f"{quality_score.overall_score:.2f}/100."
                    ),
                    action=(
                        "Address the highest-priority "
                        "missing-value, duplicate, "
                        "constant-column, and validity "
                        "issues before downstream analysis."
                    ),
                    confidence=1.0,
                )
            )

        if quality_report.duplicate_rows > 0:

            recommendations.append(
                Recommendation(
                    recommendation_type="duplicate_rows",
                    priority=(
                        "high"
                        if quality_report.duplicate_percentage
                        >= 20
                        else "medium"
                    ),
                    title="Review duplicate rows",
                    description=(
                        f"The dataset contains "
                        f"{quality_report.duplicate_rows} "
                        "duplicate rows."
                    ),
                    action=(
                        "Investigate duplicate records and "
                        "remove them if they represent "
                        "unintended duplication."
                    ),
                    confidence=1.0,
                )
            )

        # ==========================================
        # Sort recommendations
        # ==========================================

        priority_order = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
        }

        recommendations.sort(
            key=lambda item: priority_order.get(
                item.priority,
                99,
            )
        )

        logger.info(
            "Generated %s recommendations",
            len(recommendations),
        )

        return recommendations

    # ==============================================
    # Missing-value priority
    # ==============================================

    @staticmethod
    def _missing_priority(
        percentage: float,
    ) -> str:
        """Determine recommendation priority."""

        if percentage >= 50:
            return "critical"

        if percentage >= 20:
            return "high"

        if percentage > 0:
            return "medium"

        return "low"