
from pages.login_page import LoginPage
from pages.secure_area_page import SecureAreaPage


def test_login_and_logout_workflow(page):

    login_page = LoginPage(page)

    # Open login page
    login_page.open()

    # Perform login
    login_page.login("tomsmith", "SuperSecretPassword!")

    # Create secure area page object
    secure_page = SecureAreaPage(page)

    # Verify successful login
    assert secure_page.is_open()

    assert "You logged into a secure area!" in (
        secure_page.get_success_message()
    )

    page.wait_for_timeout(1500)

    # Logout
    secure_page.logout()

    # Verify user returned to login page
    assert "/login" in page.url

    assert "You logged out of the secure area!" in (
        login_page.get_message()
    )
