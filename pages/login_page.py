
from config.settings import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    MESSAGE = "#flash"

    def open(self):
        self.navigate(f"{BASE_URL}/login")

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_message(self):
        return self.get_text(self.MESSAGE)

    def is_message_visible(self):
        return self.is_visible(self.MESSAGE)
