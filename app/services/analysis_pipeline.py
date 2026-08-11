from __future__ import annotations

import pandas as pd

from app.models.analysis_result import AnalysisResult
from app.models.dataset_profile import DatasetProfile
from app.services.data_quality_analyzer import DataQualityAnalyzer
from app.services.dataset_intelligence import DatasetIntelligence
from app.services.dataset_profiler import DatasetProfiler
from app.services.feature_intelligence import FeatureIntelligence
from app.services.ml_intelligence import MLIntelligence
from app.services.quality_score_engine import QualityScoreEngine
from app.services.recommendation_engine import RecommendationEngine
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DataPilotAnalyzer:
    """Run the complete DataPilot dataset analysis pipeline."""

    def __init__(self) -> None:

        self.profiler = DatasetProfiler()

        self.quality_analyzer = (
            DataQualityAnalyzer()
        )

        self.intelligence_engine = (
            DatasetIntelligence()
        )

        self.ml_intelligence = (
            MLIntelligence()
        )

        self.feature_intelligence = (
            FeatureIntelligence()
        )

        self.score_engine = (
            QualityScoreEngine()
        )

        self.recommendation_engine = (
            RecommendationEngine()
        )

    def analyze(
        self,
        dataframe: pd.DataFrame,
        filename: str | None = None,
    ) -> AnalysisResult:
        """Run complete DataPilot analysis."""

        resolved_filename = (
            filename or "unknown"
        )

        logger.info(
            "Starting complete DataPilot analysis: %s",
            resolved_filename,
        )

        # ============================================================
        # 1. Dataset profiling
        # ============================================================

        profile = self.profiler.profile(
            dataframe,
            filename=resolved_filename,
        )

        # ============================================================
        # 2. Data quality analysis
        # ============================================================

        quality_report = (
            self.quality_analyzer.analyze(
                dataframe
            )
        )

        # ============================================================
        # 3. Dataset intelligence
        # ============================================================

        insights = (
            self.intelligence_engine.analyze(
                profile
            )
        )

        # ============================================================
        # 4. ML intelligence
        # ============================================================

        ml_insights = (
            self.ml_intelligence.analyze(
                dataframe=dataframe,
                profile=profile,
            )
        )

        # ============================================================
        # 5. Determine target column
        # ============================================================

        target_column = (
            self._extract_target_column(
                ml_insights
            )
        )

        # ============================================================
        # 6. Feature intelligence
        # ============================================================

        feature_insights = (
            self.feature_intelligence.analyze(
                dataframe=dataframe,
                profile=profile,
                target_column=target_column,
            )
        )

        # ============================================================
        # 7. Quality scoring
        # ============================================================

        quality_score = (
            self.score_engine.calculate(
                profile=profile,
                quality_report=quality_report,
            )
        )

        # ============================================================
        # 8. Recommendations
        # ============================================================

        recommendations = (
            self.recommendation_engine.generate(
                profile=profile,
                quality_report=quality_report,
                quality_score=quality_score,
            )
        )

        # ============================================================
        # 9. Build unified result
        # ============================================================

        result = AnalysisResult(
            filename=resolved_filename,
            profile=profile,
            quality_report=quality_report,
            quality_score=quality_score,
            insights=insights,
            ml_insights=ml_insights,
            feature_insights=feature_insights,
            recommendations=recommendations,
        )

        logger.info(
            "Complete DataPilot analysis finished: "
            "%s rows, %s columns, score %.2f, "
            "%s ML insights, %s feature insights",
            profile.row_count,
            profile.column_count,
            quality_score.overall_score,
            len(ml_insights),
            len(feature_insights),
        )

        return result

    # ================================================================
    # Target extraction
    # ================================================================

    @staticmethod
    def _extract_target_column(
        ml_insights,
    ) -> str | None:
        """
        Extract the detected target column from ML insights.

        MLIntelligence produces a target_detection insight
        containing the detected column name.
        """

        for insight in ml_insights:

            if (
                insight.insight_type
                == "target_detection"
            ):
                return insight.column_name

        return None