from pydantic import BaseModel, Field

from app.models.data_preparation_result import (
    DataPreparationResult,
)
from app.models.data_quality import DataQualityReport
from app.models.dataset_insight import DatasetInsight
from app.models.dataset_profile import DatasetProfile
from app.models.feature_insight import FeatureInsight
from app.models.ml_insight import MLInsight
from app.models.processed_dataset import ProcessedDataset
from app.models.quality_score import QualityScore
from app.models.recommendation import Recommendation


class AnalysisResult(BaseModel):
    """Complete DataPilot analysis result for a dataset."""

    filename: str

    profile: DatasetProfile

    quality_report: DataQualityReport

    quality_score: QualityScore

    insights: list[DatasetInsight] = Field(
        default_factory=list
    )

    ml_insights: list[MLInsight] = Field(
        default_factory=list
    )

    feature_insights: list[FeatureInsight] = Field(
        default_factory=list
    )

    recommendations: list[Recommendation] = Field(
        default_factory=list
    )

    preparation: DataPreparationResult | None = None

    processed_dataset: ProcessedDataset | None = None