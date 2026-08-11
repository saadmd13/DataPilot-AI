import pandas as pd

from app.models.dataset_profile import DatasetProfile
from app.services.feature_intelligence import FeatureIntelligence


def build_profile(
    dataframe: pd.DataFrame,
) -> DatasetProfile:

    return DatasetProfile(
        filename="test.csv",
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
    )


def test_numeric_target_relationship():

    dataframe = pd.DataFrame(
        {
            "feature": range(1, 11),
            "target": [
                2,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
            ],
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    relationship = next(
        insight
        for insight in insights
        if insight.insight_type
        == "target_relationship"
    )

    assert relationship.feature_name == "feature"

    assert relationship.score is not None

    assert relationship.score > 0.95

    assert "strong" in relationship.message


def test_negative_numeric_relationship():

    dataframe = pd.DataFrame(
        {
            "feature": range(1, 11),
            "target": [
                20,
                18,
                16,
                14,
                12,
                10,
                8,
                6,
                4,
                2,
            ],
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    relationship = next(
        insight
        for insight in insights
        if insight.insight_type
        == "target_relationship"
    )

    assert relationship.score is not None

    assert relationship.score < -0.95

    assert "negative" in relationship.message


def test_weak_relationship_is_ignored():

    dataframe = pd.DataFrame(
        {
            "feature": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
            ],
            "target": [
                7,
                2,
                9,
                1,
                8,
                3,
                6,
                4,
                10,
                5,
            ],
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    relationships = [
        insight
        for insight in insights
        if insight.insight_type
        == "target_relationship"
    ]

    assert relationships == []


def test_highly_correlated_features_are_detected():

    dataframe = pd.DataFrame(
        {
            "feature_a": range(1, 11),
            "feature_b": [
                2,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
            ],
            "target": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
            ],
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    redundant = [
        insight
        for insight in insights
        if insight.insight_type
        == "redundant_feature"
    ]

    assert redundant

    assert (
        redundant[0].metadata[
            "related_feature"
        ]
        == "feature_b"
    )


def test_extreme_target_relationship_detects_leakage():

    dataframe = pd.DataFrame(
        {
            "feature": range(1, 11),
            "target": [
                2,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
            ],
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    leakage = [
        insight
        for insight in insights
        if insight.insight_type
        == "potential_leakage"
    ]

    assert leakage

    assert (
        leakage[0].feature_name
        == "feature"
    )


def test_target_column_is_not_analyzed_as_feature():

    dataframe = pd.DataFrame(
        {
            "feature": range(1, 11),
            "target": range(1, 11),
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    assert all(
        insight.feature_name
        != "target"
        for insight in insights
    )


def test_missing_values_are_handled():

    dataframe = pd.DataFrame(
        {
            "feature": [
                1,
                2,
                None,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
            ],
            "target": [
                2,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
            ],
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column="target",
    )

    relationships = [
        insight
        for insight in insights
        if insight.insight_type
        == "target_relationship"
    ]

    assert relationships


def test_no_target_returns_no_feature_insights():

    dataframe = pd.DataFrame(
        {
            "feature_a": range(10),
            "feature_b": range(10),
        }
    )

    profile = build_profile(
        dataframe
    )

    insights = FeatureIntelligence().analyze(
        dataframe,
        profile,
        target_column=None,
    )

    assert insights == []