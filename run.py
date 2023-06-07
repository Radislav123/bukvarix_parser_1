import copy
import sys

import pytest

from parser_app import settings


class Runner:
    # оригинал - https://git.miem.hse.ru/447/framework/-/blob/master/service/run.py
    def run(self):
        """Разбирает поступающую из командной строки команду и выполняет заданные операции."""

        # опции командной строки, которые будут переданы в pytest
        pytest_options = sys.argv[1:]
        self.run_from_code(pytest_options)

    def run_from_code(self, args: list = None):
        if args is None:
            args = []
        self.before_pytest()
        self.pytest(args)
        self.after_pytest()

    def before_pytest(self):
        pass

    def after_pytest(self):
        pass

    @staticmethod
    def pytest(args):
        pytest_args = copy.deepcopy(settings.PYTEST_ARGS)
        pytest_args.extend(args)
        pytest.main(pytest_args)


if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    import configure_django

    Runner().run()
