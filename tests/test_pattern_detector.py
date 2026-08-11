import pandas as pd

from app.services.pattern_detector import PatternDetector


def test_email_detection():
    series = pd.Series(
        [
            "saad@gmail.com",
            "john@yahoo.com",
            "aisha@example.com",
            "user@test.org",
        ]
    )

    detector = PatternDetector()

    result = detector.detect(series)

    assert result.pattern == "email"
    assert result.confidence == 1.0
    assert result.match_percentage == 100.0


def test_url_detection():
    series = pd.Series(
        [
            "https://github.com",
            "https://google.com",
            "https://example.com",
            "https://openai.com",
        ]
    )

    detector = PatternDetector()

    result = detector.detect(series)

    assert result.pattern == "url"
    assert result.confidence == 1.0


def test_uuid_detection():
    series = pd.Series(
        [
            "550e8400-e29b-41d4-a716-446655440000",
            "123e4567-e89b-12d3-a456-426614174000",
        ]
    )

    detector = PatternDetector()

    result = detector.detect(series)

    assert result.pattern == "uuid"
    assert result.confidence == 1.0


def test_ipv4_detection():
    series = pd.Series(
        [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "8.8.8.8",
        ]
    )

    detector = PatternDetector()

    result = detector.detect(series)

    assert result.pattern == "ipv4"
    assert result.confidence == 1.0


def test_unknown_pattern():
    series = pd.Series(
        [
            "John",
            "Sarah",
            "Mumbai",
            "Hyderabad",
        ]
    )

    detector = PatternDetector()

    result = detector.detect(series)

    assert result.pattern == "unknown"
    assert result.confidence == 0.0