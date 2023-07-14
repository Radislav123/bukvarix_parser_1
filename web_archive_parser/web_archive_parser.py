import datetime
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
    def get_snapshot_url(site: str, timestamp_str: str, exists_in_archive: bool) -> str:
        if exists_in_archive:
            url = f"https://web.archive.org/web/{timestamp_str}/https://{site}/"
        else:
            url = f"https://web.archive.org/web/{timestamp_str}/{site}/"
        return url

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
                "limit": -1,
                "output": "json"
            }

            timestamp_response = requests.get(url, params)
            data = timestamp_response.json()
            exists_in_archive = len(data) > 0

            if exists_in_archive:
                timestamp_str = self.retrieve_field(data, "timestamp")
                snapshot_url = self.get_snapshot_url(params["url"], timestamp_str, exists_in_archive)
                self.update_progress(1)

                snapshot_response = requests.get(snapshot_url)
                if snapshot_response.headers["x-archive-guessed-charset"] != "latin1":
                    snapshot_response.encoding = snapshot_response.headers["x-archive-guessed-charset"]
                try:
                    title = re.search('<title>(.*)</title>', snapshot_response.text).group(1)
                except AttributeError:
                    title = None
                snapshot = models.Snapshot(
                    parsing = self.parsing,
                    domain = domain,
                    title = title,
                    url = snapshot_url,
                    exists_in_archive = exists_in_archive
                )
            else:
                timestamp_str = f"{datetime.date.today().year}0000000000*"
                snapshot = models.Snapshot(
                    parsing = self.parsing,
                    domain = domain,
                    title = None,
                    url = self.get_snapshot_url(params["url"], timestamp_str, exists_in_archive),
                    exists_in_archive = exists_in_archive
                )
                self.update_progress(1)

            snapshot.save()
            self.update_progress(1)
