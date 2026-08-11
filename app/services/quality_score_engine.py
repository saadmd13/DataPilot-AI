from app.models.data_quality import DataQualityReport
from app.models.dataset_profile import DatasetProfile
from app.models.quality_score import QualityScore
from app.utils.logger import get_logger


logger = get_logger(__name__)


class QualityScoreEngine:
    """Calculate a structured quality score for a dataset."""

    def calculate(
        self,
        profile: DatasetProfile,
        quality_report: DataQualityReport,
    ) -> QualityScore:
        """Calculate quality dimensions and overall score."""

        completeness_score = self._calculate_completeness(
            quality_report
        )

        uniqueness_score = self._calculate_uniqueness(
            quality_report
        )

        consistency_score = self._calculate_consistency(
            profile,
            quality_report,
        )

        validity_score = self._calculate_validity(
            profile
        )

        # Weighted overall score.
        #
        # Completeness: 30%
        # Uniqueness:   25%
        # Consistency:  25%
        # Validity:     20%
        overall_score = (
            completeness_score * 0.30
            + uniqueness_score * 0.25
            + consistency_score * 0.25
            + validity_score * 0.20
        )

        overall_score = round(
            overall_score,
            2,
        )

        grade = self._calculate_grade(
            overall_score
        )

        risk_level = self._calculate_risk_level(
            overall_score
        )

        # ==========================================
        # Issue counts
        # ==========================================

        critical_issues_count = 0
        warning_issues_count = 0
        info_issues_count = 0

        # Missing values
        if quality_report.missing_percentage >= 50:
            critical_issues_count += 1

        elif quality_report.missing_percentage > 0:
            warning_issues_count += 1

        # Duplicate rows
        if quality_report.duplicate_percentage >= 20:
            critical_issues_count += 1

        elif quality_report.duplicate_rows > 0:
            warning_issues_count += 1

        # Constant columns
        warning_issues_count += len(
            quality_report.constant_columns
        )

        # Pattern information
        pattern_columns = [
            column
            for column in profile.columns
            if (
                column.value_pattern != "unknown"
                and column.pattern_confidence >= 0.8
            )
        ]

        info_issues_count = len(
            pattern_columns
        )

        issues_count = (
            critical_issues_count
            + warning_issues_count
            + info_issues_count
        )

        # ==========================================
        # Strengths
        # ==========================================

        strengths: list[str] = []

        if completeness_score >= 90:
            strengths.append(
                "Dataset has strong completeness."
            )

        if uniqueness_score >= 90:
            strengths.append(
                "Dataset has strong uniqueness."
            )

        if consistency_score >= 90:
            strengths.append(
                "Dataset has strong structural consistency."
            )

        if validity_score >= 90:
            strengths.append(
                "Dataset contains highly valid values."
            )

        if quality_report.missing_cells == 0:
            strengths.append(
                "No missing values detected."
            )

        if quality_report.duplicate_rows == 0:
            strengths.append(
                "No duplicate rows detected."
            )

        # ==========================================
        # Weaknesses
        # ==========================================

        weaknesses: list[str] = []

        if quality_report.missing_percentage > 0:
            weaknesses.append(
                f"{quality_report.missing_percentage:.2f}% "
                "of dataset cells are missing."
            )

        if quality_report.duplicate_rows > 0:
            weaknesses.append(
                f"{quality_report.duplicate_rows} "
                "duplicate rows detected."
            )

        if quality_report.constant_columns:
            weaknesses.append(
                "One or more columns contain only "
                "a single unique value."
            )

        if not weaknesses:
            weaknesses.append(
                "No major data quality weaknesses detected."
            )

        logger.info(
            "Calculated dataset quality score: %.2f (%s)",
            overall_score,
            grade,
        )

        return QualityScore(
            overall_score=overall_score,
            completeness_score=round(
                completeness_score,
                2,
            ),
            uniqueness_score=round(
                uniqueness_score,
                2,
            ),
            consistency_score=round(
                consistency_score,
                2,
            ),
            validity_score=round(
                validity_score,
                2,
            ),
            grade=grade,
            risk_level=risk_level,
            issues_count=issues_count,
            critical_issues_count=(
                critical_issues_count
            ),
            warning_issues_count=(
                warning_issues_count
            ),
            info_issues_count=(
                info_issues_count
            ),
            strengths=strengths,
            weaknesses=weaknesses,
        )

    # ==============================================
    # Completeness
    # ==============================================

    @staticmethod
    def _calculate_completeness(
        quality_report: DataQualityReport,
    ) -> float:
        """Calculate completeness from missing percentage."""

        score = (
            100.0
            - quality_report.missing_percentage
        )

        return max(
            0.0,
            min(100.0, score),
        )

    # ==============================================
    # Uniqueness
    # ==============================================

    @staticmethod
    def _calculate_uniqueness(
        quality_report: DataQualityReport,
    ) -> float:
        """Calculate uniqueness from duplicate percentage."""

        score = (
            100.0
            - quality_report.duplicate_percentage
        )

        return max(
            0.0,
            min(100.0, score),
        )

    # ==============================================
    # Consistency
    # ==============================================

    @staticmethod
    def _calculate_consistency(
        profile: DatasetProfile,
        quality_report: DataQualityReport,
    ) -> float:
        """Calculate structural consistency."""

        if profile.column_count == 0:
            return 0.0

        constant_count = len(
            quality_report.constant_columns
        )

        if constant_count == 0:
            return 100.0

        penalty = (
            constant_count
            / profile.column_count
            * 30.0
        )

        score = 100.0 - penalty

        return max(
            0.0,
            min(100.0, score),
        )

    # ==============================================
    # Validity
    # ==============================================

    @staticmethod
    def _calculate_validity(
        profile: DatasetProfile,
    ) -> float:
        """Calculate validity using detected patterns."""

        if profile.column_count == 0:
            return 0.0

        pattern_columns = sum(
            1
            for column in profile.columns
            if (
                column.value_pattern != "unknown"
                and column.pattern_confidence >= 0.8
            )
        )

        if pattern_columns == 0:
            return 100.0

        pattern_ratio = (
            pattern_columns
            / profile.column_count
        )

        score = (
            100.0
            + pattern_ratio * 5.0
        )

        return max(
            0.0,
            min(100.0, score),
        )

    # ==============================================
    # Grade
    # ==============================================

    @staticmethod
    def _calculate_grade(
        score: float,
    ) -> str:
        """Convert numerical score into a letter grade."""

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"

    # ==============================================
    # Risk level
    # ==============================================

    @staticmethod
    def _calculate_risk_level(
        score: float,
    ) -> str:
        """Determine overall dataset risk."""

        if score >= 85:
            return "low"

        if score >= 70:
            return "medium"

        if score >= 50:
            return "high"

        return "critical"