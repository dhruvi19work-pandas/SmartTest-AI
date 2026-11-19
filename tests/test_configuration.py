
from config.settings import BASE_URL, BROWSER, HEADLESS


def test_application_url_is_configured():
    assert BASE_URL.startswith("https://")


def test_browser_configuration_is_valid():
    assert BROWSER in ["chromium", "firefox", "webkit"]


def test_headless_configuration_is_boolean():
    assert isinstance(HEADLESS, bool)
