
from intelligence.confidence_scorer import ConfidenceScorer


def test_high_confidence_locator():

    scorer = ConfidenceScorer()

    result = scorer.calculate_confidence(
        similarity_score=95,
        locator_score=100,
        match_count=1,
        is_visible=True
    )

    print("\nHigh confidence result:", result)

    assert result["level"] == "HIGH"
    assert result["recommended"] is True


def test_low_confidence_for_multiple_matches():

    scorer = ConfidenceScorer()

    result = scorer.calculate_confidence(
        similarity_score=95,
        locator_score=100,
        match_count=3,
        is_visible=True
    )

    print("\nMultiple match result:", result)

    assert result["confidence"] == 0
    assert result["recommended"] is False


def test_low_confidence_for_invisible_element():

    scorer = ConfidenceScorer()

    result = scorer.calculate_confidence(
        similarity_score=95,
        locator_score=100,
        match_count=1,
        is_visible=False
    )

    assert result["recommended"] is False
