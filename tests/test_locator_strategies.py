
from intelligence.locator_strategies import LocatorStrategies


def test_multiple_locator_strategies(page):

    page.goto("https://the-internet.herokuapp.com/login")

    strategies = LocatorStrategies(page)

    results = strategies.find_username_candidates()

    print("\nLocator strategy results:")

    for result in results:
        print(result)

    # At least two strategies should find the username field
    usable_candidates = [
        result
        for result in results
        if result["usable"]
    ]

    assert len(usable_candidates) >= 2
