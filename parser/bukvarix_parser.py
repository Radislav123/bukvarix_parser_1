import glob
import os
import shutil

import openpyxl
import pandas
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages import DomainPage, LoginPage, SearchPage
from . import settings
from .secret_keeper import SecretKeeper


class BukvarixParser:
    """Отвечает за весь процесс парсинга."""

    driver: Chrome
    secrets: SecretKeeper
    _proxies: dict = None

    def setup_method(self) -> None:
        if os.path.exists(settings.DOWNLOADS):
            shutil.rmtree(settings.DOWNLOADS)
        self.secrets = SecretKeeper()

        options = ChromeOptions()
        # этот параметр тоже нужен, так как в режиме headless с некоторыми элементами нельзя взаимодействовать
        options.add_argument("--disable-blink-features=AutomationControlled")
        # todo: return headless mode
        # options.add_argument("--headless")
        # options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        prefs = {"download.default_directory": settings.DOWNLOADS}
        options.add_experimental_option("prefs", prefs)

        driver_manager = ChromeDriverManager(path = "").install()
        service = Service(executable_path = driver_manager)

        parameters = {
            "options": options,
            "service": service
        }
        self.driver = Chrome(**parameters)
        self.driver.maximize_window()

    def teardown_method(self) -> None:
        self.driver.quit()

    @staticmethod
    def get_domains() -> list[str]:
        # todo: заменить TEST_DOMAINS на DOMAINS
        book = openpyxl.load_workbook(settings.TEST_DOMAINS)
        sheet = book.active
        domains = []
        row = 1
        while sheet.cell(row, 1).value:
            domains.append(sheet.cell(row, 1).value)
            row += 1
        return domains

    @staticmethod
    def get_downloaded_data() -> pandas.DataFrame:
        files = glob.glob(f"{settings.DOWNLOADS}/*")
        dataframes = []
        for filename in files:
            dataframe = pandas.read_csv(filename, delimiter = ';')
            dataframes.append(dataframe)
        united_dataframe = pandas.concat(dataframes)
        return united_dataframe

    def old(self) -> None:
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(self.secrets.bukvarix.login, self.secrets.bukvarix.password)

        domains = self.get_domains()
        for start in range(0, len(domains), settings.REQUEST_DOMAINS_AMOUNT):
            search_page = SearchPage(self.driver)
            search_page.open()
            search_page.search(domains[start:start + settings.REQUEST_DOMAINS_AMOUNT])
            search_page.download_button.click()
            # todo: вернуть, если будут проблемы с антиспамом
            # time.sleep(random.randint(15, 45))

        dataframe = self.get_downloaded_data()
        # todo: реализовать пункт 6 из ТЗ

    def run(self) -> None:
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(self.secrets.bukvarix.login, self.secrets.bukvarix.password)

        # todo: return all domains
        for domain in self.get_domains()[:5]:
            # noinspection SpellCheckingInspection
            domain_page = DomainPage(self.driver, domain, "gmsk")
            domain_page.open()
            try:
                words = int(domain_page.report_header.text.split(':')[-1].strip())
                print(words)
            except TimeoutException:
                print(None)
