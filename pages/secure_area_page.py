
from pages.base_page import BasePage


class SecureAreaPage(BasePage):

    LOGOUT_BUTTON = "a[href='/logout']"
    SUCCESS_MESSAGE = "#flash"

    def is_open(self):
        return "/secure" in self.page.url

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)
