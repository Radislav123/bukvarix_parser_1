import abc
import logging
import os

from .apps import CoreConfig


# todo: copy to parsing_helper
class CoreSettings(abc.ABC):
    def __init__(self):
        self.PROJECT_ROOT = os.path.dirname(os.path.abspath(f"{__file__}/.."))
        self.APP_NAME = CoreConfig.name

        # настройки парсера
        self.PARSING_HISTORY_DEPTH = 10

        # настройки административной панели
        # noinspection SpellCheckingInspection
        self.DOWNLOAD_EXCEL_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        # пути секретов
        self.SECRETS = "secrets"

        # пути скачанных файлов
        self.DOWNLOADS = os.path.normpath(f"{self.APP_ROOT}/downloads")

        # настройки логгера
        self.LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(name)s - " \
                          "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        self.LOG_FOLDER = "logs"
        self.CONSOLE_LOG_LEVEL = logging.DEBUG
        self.FILE_LOG_LEVEL = logging.DEBUG

    # настройки pytest
    # noinspection PyPep8Naming
    @property
    def PYTEST_ARGS(self) -> list[str]:
        return [
            # путь до тестов
            # "-o", f"testpaths={self.APP_ROOT}",
            "-o", f"testpaths={self.APP_NAME}",

            # игнорирование базовых тестов (родителей для наследования)
            "--ignore-glob=**/*base*",

            # соглашение об именовании тестов
            "-o", "python_files=*parser.py",
            "-o", "python_classes=*Parser",
            "-o", "python_functions=run*",

            # вывод логов в командную строку
            "-o", "log_cli=true",
            "-o", f"log_cli_format={self.LOG_FORMAT}",

            # запрещает использование маркеров, если они не зарегистрированы
            # маркеры регистрируются в conftest.pytest_configure
            "--strict-markers",

            # https://docs.pytest.org/en/6.2.x/usage.html#detailed-summary-report
            "-rA",

            # указывает pytest, где находится файл настроек django
            # https://pytest-django.readthedocs.io/en/latest/tutorial.html#step-2-point-pytest-to-your-django-settings
            "-o", "DJANGO_SETTINGS_MODULE=parser_project.settings",

            # todo: check this parameter
            # запрещает создание и удаление БД, вместо этого использует существующую
            # https://pytest-django.readthedocs.io/en/latest/database.html#reuse-db-reuse-the-testing-database-between-test-runs
            # "--reuse-db",

            # убирает экранирование не ASCII символов
            "-o", "disable_test_id_escaping_and_forfeit_all_rights_to_community_support=True",

            # разрешает пользовательский ввод в командной строке
            "-s",
        ]

    # noinspection PyPep8Naming
    @property
    def APP_ROOT(self) -> str:
        return os.path.normpath(f"{self.PROJECT_ROOT}/{self.APP_NAME}")
