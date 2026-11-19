
from intelligence.locator_ranker import LocatorRanker


def test_locator_ranking():

    element = {
        "tag": "input",
        "id": "username",
        "name": "username",
        "type": "text",
        "placeholder": "Enter username",
        "aria_label": "Username",
        "text": ""
    }

    ranker = LocatorRanker()

    candidates = ranker.rank_element(element)

    # Ensure candidates were generated
    assert len(candidates) > 0

    # Ensure highest score comes first
    assert candidates[0]["score"] == 100

    # Ensure ID is ranked first
    assert candidates[0]["strategy"] == "id"

    # Ensure scores are sorted
    scores = [candidate["score"] for candidate in candidates]

    assert scores == sorted(scores, reverse=True)

    print("\nRanked locator candidates:")

    for candidate in candidates:
        print(candidate)
