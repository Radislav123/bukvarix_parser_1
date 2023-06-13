from parsing_helper.web_elements import ExtendedWebElement
from selenium.webdriver import Chrome

from .base_page import BasePage


# https://www.bukvarix.com/login/
class LoginPage(BasePage):
    path = "login"

    def __init__(self, driver: Chrome) -> None:
        super().__init__(driver)

        self.authentication_switch = ExtendedWebElement(self, '//a[@href = "#login"]')
        self.login_input = ExtendedWebElement(self, '//input[@name = "signin_email"]')
        self.password_input = ExtendedWebElement(self, '//input[@name = "signin_password"]')
        self.enter_button = ExtendedWebElement(self, '//button[contains(text(), "Войти")]')

    def login(self, login: str, password: str) -> None:
        self.authentication_switch.click()
        self.login_input.send_keys(login)
        self.password_input.send_keys(password)
        self.enter_button.click()
