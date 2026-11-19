import pytest
from config.settings import BROWSER, BROWSER_CHANNEL, HEADLESS
from core.browser_manager import BrowserManager

@pytest.fixture
def browser():
    manager=BrowserManager(browser_name=BROWSER,headless=HEADLESS,browser_channel=BROWSER_CHANNEL)
    instance=manager.start_browser()
    yield instance
    manager.stop_browser()

@pytest.fixture
def page(browser):
    instance=browser.new_page()
    yield instance
    instance.close()
