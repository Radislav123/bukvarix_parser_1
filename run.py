import copy
import sys

import pytest

from bukvarix_parser.app_settings import BukvarixSettings
from core.app_settings import CoreSettings
from web_archive_parser.app_settings import WebArchiveSettings


class InvalidParserName(Exception):
    pass


# todo: copy to parsing_helper
class Runner:
    # оригинал - https://git.miem.hse.ru/447/framework/-/blob/master/service/run.py
    def run_from_cli(self):
        """Разбирает поступающую из командной строки команду и выполняет заданные операции."""

        # опции командной строки, которые будут переданы в pytest
        pytest_options = sys.argv[2:]
        parser = sys.argv[1]
        if parser == "bukvarix":
            settings = BukvarixSettings()
        elif parser == "web_archive":
            settings = WebArchiveSettings()
        else:
            raise InvalidParserName()
        self.run_from_code(settings, pytest_options)

    def run_from_code(self, app_settings: CoreSettings, args: list = None):
        if args is None:
            args = []
        self.pytest(app_settings, args)

    @staticmethod
    def pytest(app_settings: CoreSettings, args):
        pytest_args = copy.deepcopy(app_settings.PYTEST_ARGS)
        pytest_args.extend(args)
        pytest.main(pytest_args)


if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    import configure_django

    Runner().run_from_cli()
