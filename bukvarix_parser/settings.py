import os

from parser_project.parser_settings import ParserSettings
from .apps import BukvarixParserConfig


class BukvarixSettings(ParserSettings):
    def __init__(self):
        super().__init__()
        self.BUKVARIX_SECRETS = os.path.normpath(f"{self.SECRETS}/bukvarix.json")

        # настройки парсера
        self.REQUEST_DOMAINS_AMOUNT = 30
        self.DOMAIN_WORDS_AMOUNT = 50
        self.PARSING_HISTORY_DEPTH = 10

    @property
    def APP_ROOT(self) -> str:
        return os.path.normpath(f"{self.PROJECT_ROOT}/{BukvarixParserConfig.name}")
