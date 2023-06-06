import json

from . import settings


class SecretKeeper:
    class Bukvarix:
        def __init__(self, login: str, password: str) -> None:
            self.login = login
            self.password = password

    def __init__(self) -> None:
        with open(settings.BUKVARIX_SECRETS, 'r') as file:
            data = json.load(file)

        self.bukvarix = self.Bukvarix(data["login"], data["password"])
