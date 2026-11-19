
from intelligence.ml.feature_extractor import MLFeatureExtractor


def test_extract_locator_features():

    extractor = MLFeatureExtractor()

    candidate = {
        "similarity": 95,
        "locator_score": 100,
        "match_count": 1,
        "is_visible": True,
        "strategy": "id"
    }

    features = extractor.extract_features(candidate)

    print("\nExtracted ML Features:")
    print(features)

    assert features == [
        95,
        100,
        1,
        1,
        1,
        0,
        0,
        0
    ]

