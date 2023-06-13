from secret_keeper import SecretKeeper
from . import models
from .app_settings import CoreSettings


class BaseParser:
    parsing: models.Parsing
    secrets: SecretKeeper
    app_settings: CoreSettings
    app_settings_class = CoreSettings
    domains_model: models.DomainsParsingListModel

    @property
    def parser_name(self) -> str:
        return self.__class__.__name__

    def setup_method(self) -> None:
        self.app_settings = self.app_settings_class()
        self.secrets = SecretKeeper()

        self.parsing = models.Parsing(capacity = 0, parser_name = self.parser_name)
        self.parsing.save()

    def teardown_method(self) -> None:
        pass

    def update_progress(self, addition: int) -> None:
        self.parsing.current += addition
        self.parsing.save()

    def keep_parsing_history_depth(self):
        instances_to_delete = models.Parsing.objects.filter(parser_name = self.parser_name) \
                                  .order_by("-start_time")[self.app_settings.PARSING_HISTORY_DEPTH:]
        models.Parsing.objects.filter(id__in = [x.id for x in instances_to_delete]).delete()

    def get_domains(self) -> list[str]:
        instances = self.domains_model.objects.all()
        if len(instances) > 0:
            instance = instances[0]
            domains = [x.strip() for x in instance.domains.split()]
            domains = [x for x in domains if x]
        else:
            domains = []
        return domains
