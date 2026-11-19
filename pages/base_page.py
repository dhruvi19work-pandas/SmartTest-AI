
from playwright.sync_api import Page
from core.logger import get_logger
from intelligence.self_healing_handler import SelfHealingHandler


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate(self, url: str):
        try:
            self.logger.info("Navigating to: %s", url)
            self.page.goto(url)
        except Exception:
            self.logger.exception("Navigation failed")
            raise

    def click(self, locator: str):
        try:
            self.logger.info("Clicking element: %s", locator)
            self.page.locator(locator).click()
        except Exception:
            self.logger.exception("Click failed: %s", locator)
            raise

    def fill(
        self,
        locator: str,
        value: str,
        original_element=None
    ):
        try:
            self.logger.info("Filling element: %s", locator)

            if original_element is not None:
                handler = SelfHealingHandler(self.page)

                return handler.fill_with_healing(
                    original_locator=locator,
                    original_element=original_element,
                    value=value
                )

            self.page.locator(locator).fill(value)
            return True

        except Exception:
            self.logger.exception("Fill failed: %s", locator)
            raise

    def get_text(self, locator: str):
        try:
            return self.page.locator(locator).inner_text()
        except Exception:
            self.logger.exception(
                "Could not retrieve text: %s", locator
            )
            raise

    def is_visible(self, locator: str):
        try:
            return self.page.locator(locator).is_visible()
        except Exception:
            self.logger.exception(
                "Visibility check failed: %s", locator
            )
            raise
