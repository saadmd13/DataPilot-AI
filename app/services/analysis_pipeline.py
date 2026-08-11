import pandas as pd

from app.models.analysis_result import AnalysisResult
from app.services.data_quality_analyzer import DataQualityAnalyzer
from app.services.dataset_intelligence import DatasetIntelligence
from app.services.dataset_profiler import DatasetProfiler
from app.services.quality_score_engine import QualityScoreEngine
from app.services.recommendation_engine import RecommendationEngine
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DataPilotAnalyzer:
    """Run the complete DataPilot dataset analysis pipeline."""

    def __init__(self) -> None:

        self.profiler = DatasetProfiler()

        self.quality_analyzer = DataQualityAnalyzer()

        self.intelligence_engine = DatasetIntelligence()

        self.score_engine = QualityScoreEngine()

        self.recommendation_engine = (
            RecommendationEngine()
        )

    def analyze(
        self,
        dataframe: pd.DataFrame,
        filename: str | None = None,
    ) -> AnalysisResult:
        """Run complete dataset analysis."""

        resolved_filename = (
            filename or "unknown"
        )

        logger.info(
            "Starting complete DataPilot analysis: %s",
            resolved_filename,
        )

        # ------------------------------------------
        # 1. Dataset profiling
        # ------------------------------------------

        profile = self.profiler.profile(
            dataframe,
            filename=resolved_filename,
        )

        # ------------------------------------------
        # 2. Data quality analysis
        # ------------------------------------------

        quality_report = (
            self.quality_analyzer.analyze(
                dataframe
            )
        )

        # ------------------------------------------
        # 3. Dataset intelligence
        # ------------------------------------------

        insights = (
            self.intelligence_engine.analyze(
                profile
            )
        )

        # ------------------------------------------
        # 4. Quality scoring
        # ------------------------------------------

        quality_score = (
            self.score_engine.calculate(
                profile=profile,
                quality_report=quality_report,
            )
        )

        # ------------------------------------------
        # 5. Recommendations
        # ------------------------------------------

        recommendations = (
            self.recommendation_engine.generate(
                profile=profile,
                quality_report=quality_report,
                quality_score=quality_score,
            )
        )

        # ------------------------------------------
        # 6. Build unified result
        # ------------------------------------------

        result = AnalysisResult(
            filename=resolved_filename,
            profile=profile,
            quality_report=quality_report,
            quality_score=quality_score,
            insights=insights,
            recommendations=recommendations,
        )

        logger.info(
            "Complete DataPilot analysis finished: "
            "%s rows, %s columns, score %.2f",
            profile.row_count,
            profile.column_count,
            quality_score.overall_score,
        )

        return result