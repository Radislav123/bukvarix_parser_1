from parsing_helper.web_elements import ExtendedWebElement
from selenium.webdriver import Chrome

from .bukvarix_base_page import BukvarixBasePage


# https://www.bukvarix.com/mcmp/
class DomainPage(BukvarixBasePage):
    # noinspection SpellCheckingInspection
    path = "site"

    def __init__(self, driver: Chrome, domain: str, region: str) -> None:
        super().__init__(driver)
        self.parameters = {"q": domain, "region": region}

        self.report_header = ExtendedWebElement(self, '//div[@class = "report-header"]/h2')
        self.download_button = ExtendedWebElement(self, '//a[@class = "report-download-button"]')
