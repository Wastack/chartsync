import requests
import logging

from chartsync import sync_charts, fetch_config


def chartmuseum_url(config) -> str:
    url = config["chartMuseum"]["url"]

    r = requests.get(f"{url}/health")
    if not r.ok:
        logging.error("failed to reach chart_museum at: %s. Status code was: %d", url, r.status_code)
        raise RuntimeError()
    return url


def main():
    config = fetch_config("config.yaml")
    logger = logging.getLogger()
    logger.setLevel(config["logLevel"])
    sync_charts(config["charts"],
                chartmuseum_url(config),
                config["chartMuseum"]["overwriteExisting"])


if __name__ == '__main__':
    main()
