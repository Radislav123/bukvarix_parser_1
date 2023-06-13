from core.app_settings import CoreSettings
from .apps import WebArchiveParserConfig


class WebArchiveSettings(CoreSettings):
    def __init__(self):
        super().__init__()
        self.APP_NAME = WebArchiveParserConfig.name
