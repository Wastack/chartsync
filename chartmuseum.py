import logging
import os
from typing import Iterable

import requests
from dataclasses import dataclass


@dataclass
class ExportConfig:
    """DTO for export configuration"""
    registry_url: str
    tgz_source_folder: str
    overwrite_charts: bool
    tgz_files: Iterable['PackagedChart']


@dataclass
class PackagedChart:
    """DTO holding information of packaged charts"""
    file_name: str
    version: str
    chart_name: str


def sync_with_registry(export_config: 'ExportConfig'):
    url = export_config.registry_url

    for tgz in export_config.tgz_files:
        if export_config.overwrite_charts:
            # Before exporting, delete previous version
            r = requests.delete(f"{url}/api/charts/{tgz.chart_name}/{tgz.version}")
            if r.ok:
                logging.debug("deleted previous chart with name: %s, version: %s", tgz.chart_name, tgz.version)

        with open(os.path.join(
                export_config.tgz_source_folder,
                os.path.join(export_config.tgz_source_folder, tgz.file_name)),
                "rb") as f:
            dat = f.read()

        logging.debug("exporting helm chart: %s, version: %s", tgz.chart_name, tgz.version)
        resp = requests.post(f"{export_config.registry_url}/api/charts", data=dat)
        logging.info("Posted helm chart, status code: %d", resp.status_code)
        if not resp.ok:
            logging.info("posting helm chart failed: %s", resp.content)

