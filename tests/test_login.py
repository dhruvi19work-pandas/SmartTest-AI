
import pytest

from pages.login_page import LoginPage


def test_successful_login(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("tomsmith", "SuperSecretPassword!")

    assert "You logged into a secure area!" in login_page.get_message()

    page.wait_for_timeout(2000)


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("wrong_user", "SuperSecretPassword!", "Your username is invalid!"),
        ("tomsmith", "wrong_password", "Your password is invalid!"),
        ("", "", "Your username is invalid!"),
    ]
)
def test_unsuccessful_login(page, username, password, expected_message):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(username, password)

    actual_message = login_page.get_message()

    assert expected_message in actual_message

    page.wait_for_timeout(1500)
