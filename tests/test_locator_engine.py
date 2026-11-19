
from intelligence.locator_engine import LocatorEngine


def test_locator_engine_finds_username(page):

    page.goto("https://the-internet.herokuapp.com/login")

    # Original username element information
    original_element = {
        "tag": "input",
        "id": "username",
        "name": "username",
        "type": "text",
        "placeholder": "",
        "aria_label": "",
        "role": "",
        "text": "",
        "href": ""
    }

    engine = LocatorEngine(page)

    results = engine.find_best_locator(original_element)

    print("\nIntelligence Pipeline Results:")

    for result in results:
        print(result)

    best_locator = engine.get_best_locator(original_element)

    assert best_locator is not None
    assert best_locator["recommended"] is True
    assert best_locator["confidence"] >= 85

    print("\nBest locator:", best_locator["locator"])
    print("Confidence:", best_locator["confidence"])
