import json

from bukvarix_parser.settings import BukvarixSettings


class SecretKeeper:
    class Module:
        pass

    class Bukvarix(Module):
        login: str
        password: str

    bukvarix: Bukvarix

    def __init__(self) -> None:
        bukvarix_settings = BukvarixSettings()
        self.add_module("bukvarix", bukvarix_settings.BUKVARIX_SECRETS)

    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def add_module(self, name: str, settings_path: str):
        module = type(name, (self.Module,), self.read_json(settings_path))
        setattr(self, name, module)
