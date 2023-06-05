import logging
import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(f"{__file__}/.."))

# настройки парсера
# todo: нужен ли этот параметр
REQUEST_DOMAINS_AMOUNT = 30

# пути данных для парсинга
PARSER_DATA = "parser_data"
DOMAINS = os.path.normpath(f"{PARSER_DATA}/domains.xlsx")
TEST_DOMAINS = os.path.normpath(f"{PARSER_DATA}/test_domains.xlsx")

# пути секретов
SECRETS = "secrets"
BUKVARIX_SECRETS = os.path.normpath(f"{SECRETS}/bukvarix.json")
DATABASE_SECRETS = os.path.normpath(f"{SECRETS}/database.json")

# пути скачанных файлов
DOWNLOADS = os.path.normpath(f"{PROJECT_ROOT}/downloads")

# настройки логгера
LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
LOG_FOLDER = "logs"
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

# настройки pytest
PYTEST_ARGS = [
    # путь до тестов
    "-o", f"testpaths={PROJECT_ROOT}/parser",

    # игнорирование базовых тестов (родителей для наследования)
    "--ignore-glob=**/*base*",

    # соглашение об именовании тестов
    "-o", "python_files=*.py",
    "-o", "python_classes=*Parser",
    "-o", "python_functions=run*",

    # вывод логов в командную строку
    "-o", "log_cli=true",
    "-o", f"log_cli_format={LOG_FORMAT}",

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
