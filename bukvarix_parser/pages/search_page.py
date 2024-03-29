from typing import List

from parsing_helper.web_elements import ExtendedWebElement, ExtendedWebElementCollection
from selenium.webdriver import Chrome

from .base_page import BasePage


# https://www.bukvarix.com/mcmp/
class SearchPage(BasePage):
    # noinspection SpellCheckingInspection
    path = "mcmp"

    class SearchOptionSelector(ExtendedWebElement):
        def __init__(self, page: "SearchPage", xpath: str):
            super().__init__(page, xpath)

            self.options = ExtendedWebElementCollection(self.page, '//ul[@class = "select-options"]')
            # noinspection SpellCheckingInspection
            self.moscow_google = ExtendedWebElement(self.page, f'{self.options.xpath}/li[@id = "gmsk"]')

        def choose_google_moscow(self) -> None:
            self.click()
            self.moscow_google.click()

    def __init__(self, driver: Chrome) -> None:
        super().__init__(driver)

        self.domains_input = ExtendedWebElement(self, '//textarea')
        self.search_options_selector = self.SearchOptionSelector(self, '//div[contains(@class, "select-styled")]')
        self.find_button = ExtendedWebElement(self, '//input')
        self.download_button = ExtendedWebElement(self, '//a[@class = "report-download-button"]')

    def search(self, domains: List[str]) -> None:
        self.search_options_selector.choose_google_moscow()
        for domain in domains:
            self.domains_input.send_keys(f"{domain}\n")
        self.find_button.click()
