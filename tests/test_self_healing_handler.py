
from intelligence.self_healing_handler import SelfHealingHandler


def test_automatic_fill_retry_after_locator_failure(page):

    # First, open the website with enough navigation time.
    page.goto(
        "https://the-internet.herokuapp.com/login",
        wait_until="domcontentloaded",
        timeout=20000
    )

    # Apply a shorter timeout for the broken locator test.
    page.set_default_timeout(3000)

    handler = SelfHealingHandler(page)

    # Original element description with an outdated ID.
    original_element = {
        "tag": "input",
        "id": "user_name",
        "name": "username",
        "type": "text",
        "placeholder": "",
        "aria_label": "",
        "text": "",
        "href": ""
    }

    # This locator intentionally does not exist.
    original_locator = "#user_name"

    result = handler.fill_with_healing(
        original_locator=original_locator,
        original_element=original_element,
        value="tomsmith"
    )

    assert result is True

    # Verify that the replacement field received the value.
    username_field = page.locator("#username")

    assert username_field.input_value() == "tomsmith"

    print("\nAutomatic self-healing retry successful!")
    print("Original locator:", original_locator)
    print("Replacement locator: #username")
    print("Entered value:", username_field.input_value())



def test_rejects_healing_when_no_replacement_exists(page):

    # Create a page with no interactive elements.
    page.set_content("""
        <html>
            <body>
                <h1>No login form available</h1>
                <p>This page has no input fields or buttons.</p>
            </body>
        </html>
    """)

    handler = SelfHealingHandler(page)

    original_element = {
        "tag": "input",
        "id": "username",
        "name": "username",
        "type": "text",
        "placeholder": "",
        "aria_label": "",
        "text": "",
        "href": ""
    }

    healed_locator = handler.heal_locator(
        original_element
    )

    # No replacement should be returned.
    assert healed_locator is None

    print("\nUnsafe healing correctly rejected!")
