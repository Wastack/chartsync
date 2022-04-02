import logging
import yaml


def fetch_config(path: str):
    logging.info("Fetching configuration")
    with open(path) as f:
        return yaml.safe_load(f)

