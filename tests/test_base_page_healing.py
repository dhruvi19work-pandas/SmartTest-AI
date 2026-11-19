
from pages.login_page import LoginPage


def test_base_page_automatic_self_healing(page):

    login_page = LoginPage(page)

    # Open the login page normally.
    login_page.open()

    page.set_default_timeout(3000)

    # Original username element description.
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

    # Use the normal BasePage fill method.
    # Healing should happen internally.
    result = login_page.fill(
        locator="#user_name",
        value="tomsmith",
        original_element=original_element
    )

    assert result is True

    # Verify the replacement field received the value.
    assert page.locator("#username").input_value() == "tomsmith"

    print("\nBasePage self-healing integration successful!")
