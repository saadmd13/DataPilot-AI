from __future__ import annotations

import pandas as pd

from app.models.dataset_profile import DatasetProfile
from app.models.ml_insight import MLInsight
from app.utils.logger import get_logger


logger = get_logger(__name__)


class MLIntelligence:
    """Analyze a dataset from a machine-learning perspective."""

    TARGET_NAMES = {
        "target",
        "target_class",
        "label",
        "class",
        "y",
        "outcome",
        "response",
        "dependent_variable",
        "dependent",
    }

    def analyze(
        self,
        dataframe: pd.DataFrame,
        profile: DatasetProfile,
    ) -> list[MLInsight]:
        """Generate machine-learning insights."""

        insights: list[MLInsight] = []

        # ============================================================
        # Empty dataset
        # ============================================================

        if dataframe.empty:
            insights.append(
                MLInsight(
                    insight_type="empty_dataset",
                    severity="critical",
                    message=(
                        "The dataset contains no rows, so ML analysis "
                        "cannot be performed."
                    ),
                    confidence=1.0,
                )
            )

            return insights

        # ============================================================
        # Target detection
        # ============================================================

        target_column = self._detect_target(
            dataframe,
            profile,
        )

        if target_column is None:
            insights.append(
                MLInsight(
                    insight_type="target_detection",
                    severity="info",
                    message=(
                        "No likely target column was detected "
                        "automatically. Specify a target column before "
                        "supervised ML."
                    ),
                    confidence=0.7,
                )
            )

            logger.info(
                "No target column detected."
            )

            return insights

        target = dataframe[target_column]

        insights.append(
            MLInsight(
                insight_type="target_detection",
                severity="info",
                column_name=target_column,
                message=(
                    f"'{target_column}' appears to be the likely target "
                    "column for supervised machine learning."
                ),
                confidence=self._target_confidence(
                    target_column,
                    target,
                ),
            )
        )

        # ============================================================
        # Problem type
        # ============================================================

        problem_type = self._detect_problem_type(
            target
        )

        insights.append(
            MLInsight(
                insight_type="problem_type",
                severity="info",
                column_name=target_column,
                message=(
                    f"The likely machine-learning problem type is "
                    f"{problem_type}."
                ),
                confidence=0.95,
            )
        )

        # ============================================================
        # Classification intelligence
        # ============================================================

        if problem_type in {
            "binary_classification",
            "multiclass_classification",
        }:
            self._add_classification_insights(
                insights,
                target_column,
                target,
            )

        # ============================================================
        # Regression intelligence
        # ============================================================

        elif problem_type == "regression":
            self._add_regression_insight(
                insights,
                target_column,
                target,
            )

        # ============================================================
        # Feature intelligence
        # ============================================================

        self._add_feature_insights(
            insights,
            profile,
            target_column,
        )

        logger.info(
            "Generated %s ML insights for dataset.",
            len(insights),
        )

        return insights

    # ============================================================
    # Target detection
    # ============================================================

    def _detect_target(
        self,
        dataframe: pd.DataFrame,
        profile: DatasetProfile,
    ) -> str | None:
        """Detect the most likely target column."""

        columns = list(dataframe.columns)

        # ------------------------------------------------------------
        # Strong name-based detection
        # ------------------------------------------------------------

        for column in columns:
            normalized = (
                str(column)
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            if normalized in self.TARGET_NAMES:
                return str(column)

        # ------------------------------------------------------------
        # Low-cardinality categorical / boolean candidates
        # ------------------------------------------------------------

        candidates: list[tuple[str, float]] = []

        for column_profile in profile.columns:

            if column_profile.is_identifier:
                continue

            if column_profile.missing_percentage >= 50:
                continue

            if column_profile.semantic_type in {
                "categorical",
                "boolean",
            }:
                if 1 < column_profile.unique_count <= 20:

                    score = 0.7

                    if column_profile.unique_count == 2:
                        score = 0.85

                    candidates.append(
                        (
                            column_profile.name,
                            score,
                        )
                    )

        if candidates:
            candidates.sort(
                key=lambda item: item[1],
                reverse=True,
            )

            return candidates[0][0]

        # ------------------------------------------------------------
        # Small-cardinality numeric candidates
        # ------------------------------------------------------------

        numeric_candidates: list[
            tuple[str, float]
        ] = []

        for column_profile in profile.columns:

            if column_profile.is_identifier:
                continue

            if column_profile.semantic_type != "numeric":
                continue

            if column_profile.missing_percentage >= 50:
                continue

            if 2 <= column_profile.unique_count <= 10:
                numeric_candidates.append(
                    (
                        column_profile.name,
                        0.65,
                    )
                )

        if numeric_candidates:
            numeric_candidates.sort(
                key=lambda item: item[1],
                reverse=True,
            )

            return numeric_candidates[0][0]

        return None

    # ============================================================
    # Target confidence
    # ============================================================

    def _target_confidence(
        self,
        column_name: str,
        series: pd.Series,
    ) -> float:
        """Calculate confidence that a column is a target."""

        normalized = (
            str(column_name)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if normalized in self.TARGET_NAMES:
            return 1.0

        non_null = series.dropna()

        if len(non_null) == 0:
            return 0.0

        unique_count = non_null.nunique()

        if unique_count == 2:
            return 0.9

        if unique_count <= 10:
            return 0.75

        return 0.6

    # ============================================================
    # Problem type
    # ============================================================

    def _detect_problem_type(
        self,
        target: pd.Series,
    ) -> str:
        """
        Determine the likely supervised ML problem type.

        Rules:

        - Boolean -> binary classification
        - Exactly two values -> binary classification
        - Object/string/category -> multiclass classification
        - Low-cardinality integer target -> multiclass classification
        - Continuous numeric target -> regression
        """

        non_null = target.dropna()

        if len(non_null) == 0:
            return "unknown"

        unique_count = non_null.nunique()

        # ------------------------------------------------------------
        # Boolean target
        # ------------------------------------------------------------

        if pd.api.types.is_bool_dtype(target):
            return "binary_classification"

        # ------------------------------------------------------------
        # Exactly two unique values
        # ------------------------------------------------------------

        if unique_count == 2:
            return "binary_classification"

        # ------------------------------------------------------------
        # String / object / categorical target
        # ------------------------------------------------------------

        if (
            pd.api.types.is_object_dtype(target)
            or pd.api.types.is_string_dtype(target)
            or isinstance(
                target.dtype,
                pd.CategoricalDtype,
            )
        ):
            return "multiclass_classification"

        # ------------------------------------------------------------
        # Numeric target
        # ------------------------------------------------------------

        if pd.api.types.is_numeric_dtype(target):

            # Integer-like low-cardinality values commonly represent
            # encoded class labels.
            if (
                unique_count <= 10
                and pd.api.types.is_integer_dtype(target)
            ):
                return "multiclass_classification"

            # Continuous numeric targets are regression targets.
            return "regression"

        return "unknown"

    # ============================================================
    # Classification
    # ============================================================

    def _add_classification_insights(
        self,
        insights: list[MLInsight],
        target_column: str,
        target: pd.Series,
    ) -> None:
        """Add classification and class-balance insights."""

        distribution = (
            target
            .dropna()
            .value_counts()
        )

        total = int(
            distribution.sum()
        )

        if total == 0:
            return

        class_count = len(
            distribution
        )

        distribution_text = ", ".join(
            f"{value}: {(count / total) * 100:.2f}%"
            for value, count
            in distribution.items()
        )

        insights.append(
            MLInsight(
                insight_type="target_distribution",
                severity="info",
                column_name=target_column,
                message=(
                    f"Target '{target_column}' contains "
                    f"{class_count} classes. "
                    f"Distribution: "
                    f"{distribution_text}."
                ),
                confidence=1.0,
            )
        )

        if class_count < 2:
            return

        majority_count = int(
            distribution.iloc[0]
        )

        minority_count = int(
            distribution.iloc[-1]
        )

        minority_percentage = (
            minority_count / total
        ) * 100

        imbalance_ratio = (
            minority_count / majority_count
            if majority_count > 0
            else 0.0
        )

        if minority_percentage < 10:
            severity = "critical"

        elif minority_percentage < 20:
            severity = "warning"

        else:
            severity = "info"

        if minority_percentage < 20:

            majority_to_minority = (
                majority_count / minority_count
                if minority_count > 0
                else 0.0
            )

            insights.append(
                MLInsight(
                    insight_type="class_imbalance",
                    severity=severity,
                    column_name=target_column,
                    message=(
                        f"Target '{target_column}' is imbalanced. "
                        f"The minority class represents "
                        f"{minority_percentage:.2f}% of non-null "
                        f"target values, with a majority/minority "
                        f"ratio of approximately "
                        f"{majority_to_minority:.2f}:1."
                    ),
                    confidence=0.95,
                    metadata={
                        "minority_percentage": round(
                            minority_percentage,
                            2,
                        ),
                        "imbalance_ratio": round(
                            imbalance_ratio,
                            4,
                        ),
                    },
                )
            )

            insights.append(
                MLInsight(
                    insight_type="imbalance_recommendation",
                    severity="warning",
                    column_name=target_column,
                    message=(
                        "Use stratified train/test splitting and "
                        "evaluate precision, recall, F1-score and "
                        "PR-AUC. Consider class weighting or "
                        "resampling if appropriate."
                    ),
                    confidence=0.9,
                )
            )

    # ============================================================
    # Regression
    # ============================================================

    def _add_regression_insight(
        self,
        insights: list[MLInsight],
        target_column: str,
        target: pd.Series,
    ) -> None:
        """Add regression-specific insight."""

        non_null = target.dropna()

        if len(non_null) == 0:
            return

        insights.append(
            MLInsight(
                insight_type="regression_target",
                severity="info",
                column_name=target_column,
                message=(
                    f"'{target_column}' appears suitable as a "
                    "continuous regression target."
                ),
                confidence=0.9,
            )
        )

    # ============================================================
    # Feature intelligence
    # ============================================================

    def _add_feature_insights(
        self,
        insights: list[MLInsight],
        profile: DatasetProfile,
        target_column: str,
    ) -> None:
        """Identify potentially problematic ML features."""

        for column in profile.columns:

            if column.name == target_column:
                continue

            # --------------------------------------------------------
            # Identifier feature
            # --------------------------------------------------------

            if column.is_identifier:
                insights.append(
                    MLInsight(
                        insight_type="identifier_feature",
                        severity="warning",
                        column_name=column.name,
                        message=(
                            f"'{column.name}' appears to be an "
                            "identifier and should generally be "
                            "excluded from predictive features."
                        ),
                        confidence=column.identifier_confidence,
                    )
                )

            # --------------------------------------------------------
            # Missing-heavy feature
            # --------------------------------------------------------

            if column.missing_percentage >= 20:

                severity = (
                    "critical"
                    if column.missing_percentage >= 50
                    else "warning"
                )

                insights.append(
                    MLInsight(
                        insight_type="missing_feature",
                        severity=severity,
                        column_name=column.name,
                        message=(
                            f"Feature '{column.name}' contains "
                            f"{column.missing_percentage:.2f}% "
                            "missing values and may require "
                            "imputation or removal."
                        ),
                        confidence=1.0,
                    )
                )

            # --------------------------------------------------------
            # Constant feature
            # --------------------------------------------------------

            if (
                column.unique_count <= 1
                and column.missing_count == 0
            ):
                insights.append(
                    MLInsight(
                        insight_type="constant_feature",
                        severity="warning",
                        column_name=column.name,
                        message=(
                            f"Feature '{column.name}' is constant "
                            "and provides no useful variation for "
                            "most ML models."
                        ),
                        confidence=1.0,
                    )
                )

            # --------------------------------------------------------
            # High-cardinality feature
            #
            # IMPORTANT:
            # High cardinality is meaningful primarily for
            # categorical/text features. Continuous numeric features
            # naturally have many unique values and should NOT be
            # flagged merely because their cardinality ratio is high.
            # --------------------------------------------------------

            if (
                column.cardinality_ratio >= 0.95
                and column.semantic_type in {
                    "categorical",
                    "text",
                }
                and not column.is_identifier
            ):
                insights.append(
                    MLInsight(
                        insight_type="high_cardinality_feature",
                        severity="warning",
                        column_name=column.name,
                        message=(
                            f"Feature '{column.name}' has very high "
                            "cardinality and may require special "
                            "encoding or exclusion."
                        ),
                        confidence=column.cardinality_ratio,
                    )
                )