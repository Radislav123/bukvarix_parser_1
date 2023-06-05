import copy
import sys

import pytest

# noinspection PyUnresolvedReferences
import configure_django
from parser import settings


class Runner:
    # оригинал - https://git.miem.hse.ru/447/framework/-/blob/master/service/run.py
    def run(self):
        """Разбирает поступающую из командной строки команду и выполняет заданные операции."""

        # опции командной строки, которые будут переданы в pytest
        pytest_options = sys.argv[1:]
        self.before_pytest()
        self.pytest(pytest_options)
        self.after_pytest()

    @staticmethod
    def before_pytest():
        pass

    def after_pytest(self):
        pass

    @staticmethod
    def pytest(args):
        pytest_args = copy.deepcopy(settings.PYTEST_ARGS)
        pytest_args.extend(args)
        pytest.main(pytest_args)


if __name__ == "__main__":
    Runner().run()
