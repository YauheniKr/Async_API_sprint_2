import logging
from time import sleep

import requests

URL = 'http://elasticsearch:9200/'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def make_request():
    status = requests.head(URL)
    return status


def check_es_status():
    while True:
        try:
            make_request()
            logger.info("Elasticsearch Running")
            exit(0)
        except Exception as e:
            logger.error(e.args[0].reason.args[0].split(':')[1].strip())
            logger.error("Elasticsearch is not available. Sleep for 10 sec")
            sleep(10)
        else:
            exit(1)


if __name__ == '__main__':
    check_es_status()
