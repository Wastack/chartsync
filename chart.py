import logging
import os
import subprocess
import tempfile
from typing import Any, List, Optional

import yaml

from chartmuseum import sync_with_registry, ExportConfig, PackagedChart


def sync_charts(charts: List[Any], museum_url: str, overwrite_existing: bool):
    logging.debug("packaging charts")
    with tempfile.TemporaryDirectory() as tmp_folder:
        logging.debug("using tmp folder: %s", tmp_folder)
        tgz_files = []

        for chart in charts:
            chart_path = chart.get("path")
            if chart_path is None:
                logging.error('missing "path" key for chart')
                continue

            tgz = fetch_chart(chart_path, tmp_folder)
            if tgz is None:
                logging.error("failed to fetch chart from path: %s", chart_path)
                continue
            tgz_files.append(tgz)

        logging.debug("sync packaged charts with registry")
        sync_with_registry(ExportConfig(
            registry_url=museum_url,
            tgz_source_folder=tmp_folder,
            overwrite_charts=overwrite_existing,
            tgz_files=tgz_files,
        ))


def fetch_chart(path: str, tmp_folder: str) -> Optional[PackagedChart]:
    data = parse_yaml(os.path.join(path, "Chart.yaml"))
    if data is None:
        return None

    chart_name = data["name"]
    chart_version = data["version"]
    file_name = f"{chart_name}-{chart_version}.tgz"

    logging.info("packaging chart: %s", data.get("name"))
    try:
        subprocess.check_call(["helm", "package", "-d", tmp_folder, path])
    except subprocess.CalledProcessError as e:
        logging.error("failed to package helm chart with error code: %d, err: %s", e.returncode, e.stderr)
        return None
    return PackagedChart(chart_name=data["name"],
                         version=data["version"],
                         file_name=file_name)


def parse_yaml(path: str):
    try:
        with open(path) as f:
            content = f.read()
    except FileNotFoundError:
        logging.error("file is missing at path: %s", path)
        return None
    return yaml.safe_load(content)

