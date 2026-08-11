import pandas as pd

from app.models.dataset_profile import (
    ColumnProfile,
    DatasetProfile,
)
from app.models.value_pattern import PatternDetection
from app.services.pattern_detector import PatternDetector
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DatasetProfiler:
    """Generate structured intelligence about a pandas DataFrame."""

    def profile(
        self,
        dataframe: pd.DataFrame,
        filename: str | None = None,
    ) -> DatasetProfile:
        """Generate a dataset profile."""

        logger.info(
            "Starting dataset profiling: %s",
            filename or "unknown",
        )

        row_count = len(dataframe)
        column_count = len(dataframe.columns)

        # ==========================================
        # Dataset-level statistics
        # ==========================================

        memory_usage = int(
            dataframe.memory_usage(
                index=True,
                deep=True,
            ).sum()
        )

        duplicate_count = int(
            dataframe.duplicated().sum()
        )

        duplicate_percentage = (
            (duplicate_count / row_count) * 100
            if row_count > 0
            else 0.0
        )

        missing_count = int(
            dataframe.isna().sum().sum()
        )

        total_cells = row_count * column_count

        missing_percentage = (
            (missing_count / total_cells) * 100
            if total_cells > 0
            else 0.0
        )

        # ==========================================
        # Semantic type counters
        # ==========================================

        numeric_count = 0
        categorical_count = 0
        datetime_count = 0
        text_count = 0
        boolean_count = 0

        columns = []

        # ==========================================
        # Pattern detector
        # ==========================================

        pattern_detector = PatternDetector()

        # ==========================================
        # Profile each column
        # ==========================================

        for column in dataframe.columns:

            series = dataframe[column]

            missing = int(
                series.isna().sum()
            )

            unique = int(
                series.nunique(
                    dropna=True
                )
            )

            cardinality_ratio = (
                unique / row_count
                if row_count > 0
                else 0.0
            )

            missing_pct = (
                (missing / row_count) * 100
                if row_count > 0
                else 0.0
            )

            unique_pct = (
                (unique / row_count) * 100
                if row_count > 0
                else 0.0
            )

            dtype = str(series.dtype)

            # ======================================
            # Semantic type detection
            # ======================================

            semantic_type = (
                self._detect_semantic_type(series)
            )

            # ======================================
            # Identifier detection
            # ======================================

            (
                is_identifier,
                identifier_confidence,
            ) = self._detect_identifier(
                series,
                str(column),
                cardinality_ratio,
            )

            # ======================================
            # Datetime detection
            # ======================================

            datetime_parse_success_rate = 0.0

            if semantic_type == "datetime":

                (
                    _,
                    datetime_parse_success_rate,
                ) = self._detect_datetime(series)

            # ======================================
            # Value pattern detection
            # ======================================

            if semantic_type in {
                "text",
                "categorical",
            }:

                pattern_detection = (
                    pattern_detector.detect(series)
                )

            else:

                pattern_detection = PatternDetection()

            value_pattern = (
                pattern_detection.pattern
            )

            pattern_confidence = (
                pattern_detection.confidence
            )

            pattern_match_percentage = (
                pattern_detection.match_percentage
            )

            pattern_examples = (
                pattern_detection.examples
            )

            # ======================================
            # Count semantic types
            # ======================================

            if semantic_type == "numeric":
                numeric_count += 1

            elif semantic_type == "categorical":
                categorical_count += 1

            elif semantic_type == "datetime":
                datetime_count += 1

            elif semantic_type == "text":
                text_count += 1

            elif semantic_type == "boolean":
                boolean_count += 1

            # ======================================
            # Initialize column statistics
            # ======================================

            min_value = None
            max_value = None
            mean_value = None
            median_value = None
            std_value = None

            top_values = []

            min_length = None
            max_length = None
            average_length = None

            # ======================================
            # Numeric statistics
            # ======================================

            if semantic_type == "numeric":

                numeric_series = series.dropna()

                if len(numeric_series) > 0:

                    min_value = float(
                        numeric_series.min()
                    )

                    max_value = float(
                        numeric_series.max()
                    )

                    mean_value = float(
                        numeric_series.mean()
                    )

                    median_value = float(
                        numeric_series.median()
                    )

                    std = numeric_series.std()

                    if pd.notna(std):
                        std_value = float(std)
                    else:
                        std_value = 0.0

            # ======================================
            # Categorical statistics
            # ======================================

            elif semantic_type == "categorical":

                value_counts = (
                    series
                    .dropna()
                    .value_counts()
                    .head(10)
                )

                top_values = [
                    {
                        "value": str(value),
                        "count": int(count),
                    }
                    for value, count
                    in value_counts.items()
                ]

            # ======================================
            # Text statistics
            # ======================================

            elif semantic_type == "text":

                text_series = (
                    series
                    .dropna()
                    .astype(str)
                )

                if len(text_series) > 0:

                    lengths = text_series.str.len()

                    min_length = int(
                        lengths.min()
                    )

                    max_length = int(
                        lengths.max()
                    )

                    average_length = float(
                        lengths.mean()
                    )

            # ======================================
            # Create column profile
            # ======================================

            columns.append(
                ColumnProfile(
                    name=str(column),

                    pandas_dtype=dtype,

                    semantic_type=semantic_type,

                    missing_count=missing,

                    missing_percentage=round(
                        missing_pct,
                        2,
                    ),

                    unique_count=unique,

                    unique_percentage=round(
                        unique_pct,
                        2,
                    ),

                    cardinality_ratio=round(
                        cardinality_ratio,
                        4,
                    ),

                    is_identifier=is_identifier,

                    identifier_confidence=round(
                        identifier_confidence,
                        2,
                    ),

                    datetime_parse_success_rate=round(
                        datetime_parse_success_rate,
                        4,
                    ),

                    value_pattern=value_pattern,

                    pattern_confidence=round(
                        pattern_confidence,
                        4,
                    ),

                    pattern_match_percentage=round(
                        pattern_match_percentage,
                        2,
                    ),

                    pattern_examples=pattern_examples,

                    min_value=min_value,

                    max_value=max_value,

                    mean_value=mean_value,

                    median_value=median_value,

                    std_value=std_value,

                    top_values=top_values,

                    min_length=min_length,

                    max_length=max_length,

                    average_length=(
                        round(
                            average_length,
                            2,
                        )
                        if average_length is not None
                        else None
                    ),
                )
            )

        # ==========================================
        # Create dataset profile
        # ==========================================

        profile = DatasetProfile(
            filename=filename or "unknown",

            row_count=row_count,

            column_count=column_count,

            memory_usage_bytes=memory_usage,

            duplicate_row_count=duplicate_count,

            duplicate_percentage=round(
                duplicate_percentage,
                2,
            ),

            missing_value_count=missing_count,

            missing_value_percentage=round(
                missing_percentage,
                2,
            ),

            numeric_column_count=numeric_count,

            categorical_column_count=(
                categorical_count
            ),

            datetime_column_count=(
                datetime_count
            ),

            text_column_count=text_count,

            boolean_column_count=boolean_count,

            columns=columns,
        )

        logger.info(
            "Dataset profiling completed: %s rows, %s columns",
            row_count,
            column_count,
        )

        return profile

    # ==============================================
    # Semantic type detection
    # ==============================================

    @staticmethod
    def _detect_semantic_type(
        series: pd.Series,
    ) -> str:
        """Determine a basic semantic type for a column."""

        # Boolean
        if pd.api.types.is_bool_dtype(series):
            return "boolean"

        # Already recognized datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"

        # Numeric
        if pd.api.types.is_numeric_dtype(series):
            return "numeric"

        # Strings / text / categorical / datetime
        if pd.api.types.is_string_dtype(series):

            non_null = series.dropna()

            if len(non_null) == 0:
                return "unknown"

            # Check datetime before classifying
            # the column as text or categorical.
            is_datetime, _ = (
                DatasetProfiler._detect_datetime(
                    series
                )
            )

            if is_datetime:
                return "datetime"

            unique_count = non_null.nunique()

            unique_ratio = (
                unique_count / len(non_null)
            )

            # Small-cardinality string columns
            # are generally categorical.
            if (
                unique_count <= 10
                and unique_ratio <= 0.5
            ):
                return "categorical"

            # For larger datasets, a low unique
            # ratio is a strong categorical signal.
            if (
                len(non_null) >= 20
                and unique_ratio <= 0.05
            ):
                return "categorical"

            return "text"

        return "unknown"

    # ==============================================
    # Identifier detection
    # ==============================================

    @staticmethod
    def _detect_identifier(
        series: pd.Series,
        column_name: str,
        cardinality_ratio: float,
    ) -> tuple[bool, float]:
        """Detect whether a column is likely an identifier."""

        name = column_name.lower().strip()

        normalized_name = (
            name.replace("-", "_")
            .replace(" ", "_")
        )

        exact_identifier_names = {
            "id",
            "uuid",
            "guid",
            "identifier",
        }

        identifier_suffixes = (
            "_id",
            "_uuid",
            "_guid",
        )

        name_signal = (
            normalized_name
            in exact_identifier_names
            or normalized_name.endswith(
                identifier_suffixes
            )
        )

        cardinality_signal = (
            cardinality_ratio >= 0.95
        )

        # Strong identifier signal:
        # explicit identifier naming + high cardinality.
        if name_signal and cardinality_signal:
            return True, 1.0

        # Moderate identifier signal:
        # explicit identifier naming even if
        # values are not completely unique.
        if name_signal:
            return True, 0.75

        # High cardinality alone is NOT enough.
        return False, 0.0

    # ==============================================
    # Datetime detection
    # ==============================================

    @staticmethod
    def _detect_datetime(
        series: pd.Series,
    ) -> tuple[bool, float]:
        """Detect whether a column contains datetime values."""

        non_null = series.dropna()

        if len(non_null) == 0:
            return False, 0.0

        # Already recognized by pandas.
        if pd.api.types.is_datetime64_any_dtype(series):
            return True, 1.0

        # Numeric columns should not automatically
        # be interpreted as dates.
        if not pd.api.types.is_string_dtype(series):
            return False, 0.0

        # Parse string values using mixed-format support.
        parsed = pd.to_datetime(
            non_null,
            errors="coerce",
            format="mixed",
        )

        success_rate = float(
            parsed.notna().mean()
        )

        is_datetime = (
            success_rate >= 0.90
        )

        return (
            is_datetime,
            success_rate,
        )