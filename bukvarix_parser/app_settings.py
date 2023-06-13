import os

from core.app_settings import CoreSettings
from .apps import BukvarixParserConfig


class BukvarixSettings(CoreSettings):
    def __init__(self):
        super().__init__()
        self.APP_NAME = BukvarixParserConfig.name
        self.BUKVARIX_SECRETS = os.path.normpath(f"{self.SECRETS}/bukvarix.json")

        # настройки парсера
        self.REQUEST_DOMAINS_AMOUNT = 30
        self.DOMAIN_WORDS_AMOUNT = 50

