from __future__ import annotations

import pandas as pd

from app.models.dataset_profile import DatasetProfile
from app.models.feature_insight import FeatureInsight
from app.utils.logger import get_logger


logger = get_logger(__name__)


class FeatureIntelligence:
    """Analyze relationships between dataset features and the target."""

    def analyze(
        self,
        dataframe: pd.DataFrame,
        profile: DatasetProfile,
        target_column: str | None = None,
    ) -> list[FeatureInsight]:
        """Generate feature-level machine-learning insights."""

        insights: list[FeatureInsight] = []

        if dataframe.empty:
            return insights

        if not target_column:
            logger.info(
                "No target column supplied for feature intelligence."
            )
            return insights

        if target_column not in dataframe.columns:
            logger.warning(
                "Target column '%s' not found in dataframe.",
                target_column,
            )
            return insights

        target = dataframe[target_column]

        # Feature-level numeric relationships
        insights.extend(
            self._analyze_numeric_relationships(
                dataframe=dataframe,
                target=target,
                target_column=target_column,
            )
        )

        # Highly correlated numeric feature pairs
        insights.extend(
            self._analyze_feature_redundancy(
                dataframe=dataframe,
                target_column=target_column,
            )
        )

        logger.info(
            "Generated %s feature intelligence insights.",
            len(insights),
        )

        return insights

    # ============================================================
    # Numeric feature / target relationships
    # ============================================================

    def _analyze_numeric_relationships(
        self,
        dataframe: pd.DataFrame,
        target: pd.Series,
        target_column: str,
    ) -> list[FeatureInsight]:
        """Analyze numeric feature relationships with the target."""

        insights: list[FeatureInsight] = []

        if not pd.api.types.is_numeric_dtype(target):
            return insights

        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns

        for feature_name in numeric_columns:

            if feature_name == target_column:
                continue

            feature = dataframe[feature_name]

            if feature.nunique(
                dropna=True
            ) <= 1:
                continue

            paired = pd.concat(
                [
                    feature.rename("feature"),
                    target.rename("target"),
                ],
                axis=1,
            ).dropna()

            if len(paired) < 3:
                continue

            correlation = paired[
                "feature"
            ].corr(
                paired["target"]
            )

            if pd.isna(correlation):
                continue

            correlation = float(correlation)

            absolute_correlation = abs(
                correlation
            )

            relationship = (
                self._relationship_strength(
                    absolute_correlation
                )
            )

            # Only surface meaningful relationships.
            if absolute_correlation < 0.20:
                continue

            if absolute_correlation >= 0.70:
                severity = "info"
                confidence = min(
                    1.0,
                    absolute_correlation + 0.10,
                )

            elif absolute_correlation >= 0.40:
                severity = "info"
                confidence = absolute_correlation

            else:
                severity = "info"
                confidence = absolute_correlation

            direction = (
                "positive"
                if correlation > 0
                else "negative"
            )

            message = (
                f"Feature '{feature_name}' has a "
                f"{relationship} {direction} relationship "
                f"with target '{target_column}' "
                f"(correlation={correlation:.3f})."
            )

            insights.append(
                FeatureInsight(
                    feature_name=feature_name,
                    insight_type="target_relationship",
                    severity=severity,
                    target_column=target_column,
                    message=message,
                    confidence=round(
                        confidence,
                        4,
                    ),
                    score=round(
                        correlation,
                        4,
                    ),
                    metadata={
                        "correlation": round(
                            correlation,
                            4,
                        ),
                        "absolute_correlation": round(
                            absolute_correlation,
                            4,
                        ),
                        "relationship_strength": relationship,
                        "sample_count": len(paired),
                    },
                )
            )

            # Potential leakage warning
            if absolute_correlation >= 0.95:
                insights.append(
                    FeatureInsight(
                        feature_name=feature_name,
                        insight_type="potential_leakage",
                        severity="warning",
                        target_column=target_column,
                        message=(
                            f"Feature '{feature_name}' has an "
                            f"extremely strong relationship with "
                            f"target '{target_column}' "
                            f"(correlation={correlation:.3f}). "
                            "Investigate whether this feature "
                            "contains target leakage."
                        ),
                        confidence=0.9,
                        score=round(
                            correlation,
                            4,
                        ),
                        metadata={
                            "correlation": round(
                                correlation,
                                4,
                            ),
                            "reason": (
                                "extremely_high_target_correlation"
                            ),
                        },
                    )
                )

        return insights

    # ============================================================
    # Feature redundancy
    # ============================================================

    def _analyze_feature_redundancy(
        self,
        dataframe: pd.DataFrame,
        target_column: str,
    ) -> list[FeatureInsight]:
        """Detect highly correlated numeric feature pairs."""

        insights: list[FeatureInsight] = []

        numeric_dataframe = dataframe.select_dtypes(
            include="number"
        ).drop(
            columns=[target_column],
            errors="ignore",
        )

        if numeric_dataframe.shape[1] < 2:
            return insights

        correlation_matrix = (
            numeric_dataframe.corr()
        )

        columns = list(
            correlation_matrix.columns
        )

        for index, first_column in enumerate(
            columns
        ):

            for second_column in columns[
                index + 1:
            ]:

                correlation = correlation_matrix.loc[
                    first_column,
                    second_column,
                ]

                if pd.isna(correlation):
                    continue

                correlation = float(
                    correlation
                )

                absolute_correlation = abs(
                    correlation
                )

                if absolute_correlation < 0.90:
                    continue

                insights.append(
                    FeatureInsight(
                        feature_name=first_column,
                        insight_type="redundant_feature",
                        severity="warning",
                        message=(
                            f"Feature '{first_column}' is highly "
                            f"correlated with '{second_column}' "
                            f"(correlation={correlation:.3f}) "
                            "and may contain redundant information."
                        ),
                        confidence=min(
                            1.0,
                            absolute_correlation,
                        ),
                        score=round(
                            correlation,
                            4,
                        ),
                        metadata={
                            "related_feature": second_column,
                            "correlation": round(
                                correlation,
                                4,
                            ),
                        },
                    )
                )

        return insights

    # ============================================================
    # Relationship classification
    # ============================================================

    @staticmethod
    def _relationship_strength(
        absolute_correlation: float,
    ) -> str:
        """Classify correlation strength."""

        if absolute_correlation >= 0.70:
            return "strong"

        if absolute_correlation >= 0.40:
            return "moderate"

        if absolute_correlation >= 0.20:
            return "weak"

        return "minimal"