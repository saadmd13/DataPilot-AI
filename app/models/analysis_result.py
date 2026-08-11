from pydantic import BaseModel, Field

from app.models.data_quality import DataQualityReport
from app.models.dataset_insight import DatasetInsight
from app.models.dataset_profile import DatasetProfile
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

    recommendations: list[Recommendation] = Field(
        default_factory=list
    )