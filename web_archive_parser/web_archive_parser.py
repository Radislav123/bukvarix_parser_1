import re

import requests

from core.base_parser import BaseParser
from . import models
from .app_settings import WebArchiveSettings


class WebArchiveParser(BaseParser):
    app_settings: WebArchiveSettings
    app_settings_class = WebArchiveSettings
    domains_model = models.DomainsParsingList

    @staticmethod
    def get_snapshot_url(site: str, timestamp: str) -> str:
        return f"https://web.archive.org/web/{timestamp}/https://{site}/"

    @staticmethod
    def retrieve_field(data: list[list[str]], field_name: str, snapshot_number: int = None) -> str:
        if snapshot_number is None:
            snapshot_number = 1
        return data[snapshot_number][data[0].index(field_name)]

    def run(self) -> None:
        # noinspection HttpUrlsUsage
        url = "http://web.archive.org/cdx/search/cdx"

        domains = self.get_domains()
        progress_capacity = len(domains) * 2
        self.parsing.capacity = progress_capacity
        self.parsing.save()

        for domain in domains:
            params = {
                "url": domain,
                "filter": "statuscode:200",
                "limit": 1,
                "output": "json"
            }

            timestamp_response = requests.get(url, params)
            data = timestamp_response.json()

            if len(data) > 0:
                timestamp = self.retrieve_field(data, "timestamp")
                snapshot_url = self.get_snapshot_url(params["url"], timestamp)
                self.update_progress(1)

                snapshot_response = requests.get(snapshot_url)
                title = re.search('<title>(.*)</title>', snapshot_response.text).group(1)
                snapshot = models.Snapshot(
                    parsing = self.parsing,
                    domain = domain,
                    title = title,
                    url = snapshot_url
                )
                self.update_progress(1)
                snapshot.save()
            else:
                self.update_progress(2)
