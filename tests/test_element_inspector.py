
from intelligence.element_inspector import ElementInspector


def test_inspect_login_page_elements(page):

    page.goto("https://the-internet.herokuapp.com/login")

    inspector = ElementInspector(page)

    elements = inspector.inspect_elements()

    assert len(elements) > 0

    for element in elements:
        print(element)

    # Confirm that the username field was discovered
    username_found = any(
        element["id"] == "username"
        for element in elements
    )

    assert username_found
