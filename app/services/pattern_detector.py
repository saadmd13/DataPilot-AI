import re

import pandas as pd

from app.models.value_pattern import PatternDetection
from app.utils.logger import get_logger


logger = get_logger(__name__)


class PatternDetector:
    """Detect common semantic patterns in column values."""

    PATTERNS = {
        "email": re.compile(
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}$"
        ),

        "url": re.compile(
            r"^https?://"
            r"(?:www\.)?"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
            r"(?:[/:?#].*)?$",
            re.IGNORECASE,
        ),

        "uuid": re.compile(
            r"^[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[1-5][0-9a-fA-F]{3}-"
            r"[89abAB][0-9a-fA-F]{3}-"
            r"[0-9a-fA-F]{12}$"
        ),

        "ipv4": re.compile(
            r"^(?:"
            r"(?:25[0-5]|2[0-4][0-9]|"
            r"1?[0-9]{1,2})\."
            r"){3}"
            r"(?:25[0-5]|2[0-4][0-9]|"
            r"1?[0-9]{1,2})$"
        ),

        "phone": re.compile(
            r"^\+?[0-9][0-9\s().-]{7,20}$"
        ),
    }

    def detect(
        self,
        series: pd.Series,
    ) -> PatternDetection:
        """Detect the dominant value pattern in a series."""

        non_null = (
            series
            .dropna()
            .astype(str)
            .str.strip()
        )

        total_count = len(non_null)

        if total_count == 0:
            return PatternDetection()

        best_pattern = "unknown"
        best_count = 0

        for pattern_name, pattern in self.PATTERNS.items():

            match_count = int(
                non_null.apply(
                    lambda value: bool(
                        pattern.fullmatch(value)
                    )
                ).sum()
            )

            if match_count > best_count:
                best_pattern = pattern_name
                best_count = match_count

        match_percentage = (
            (best_count / total_count) * 100
            if total_count > 0
            else 0.0
        )

        # Require at least 80% of values
        # to match before declaring a pattern.
        if match_percentage < 80.0:
            best_pattern = "unknown"
            best_count = 0
            match_percentage = 0.0

        confidence = (
            match_percentage / 100
            if best_pattern != "unknown"
            else 0.0
        )

        examples = []

        if best_pattern != "unknown":

            pattern = self.PATTERNS[
                best_pattern
            ]

            for value in non_null:

                if pattern.fullmatch(value):
                    examples.append(value)

                if len(examples) >= 5:
                    break

        logger.info(
            "Pattern detection completed: %s confidence=%.2f",
            best_pattern,
            confidence,
        )

        return PatternDetection(
            pattern=best_pattern,

            confidence=round(
                confidence,
                4,
            ),

            matched_count=best_count,

            total_count=total_count,

            match_percentage=round(
                match_percentage,
                2,
            ),

            examples=examples,
        )