from time import sleep

import requests

URL = 'http://192.168.88.131:9200/'


def make_request():
    status = requests.head(URL)
    return status


def check_es_status():
    while True:
        try:
            make_request()
            print("Elasticsearch Running")
            exit(0)
        except Exception as e:
            print(e.args[0].reason.args[0].split(':')[1].strip())
            print("Elasticsearch is not available. Sleep for 10 sec")
            sleep(10)
        else:
            exit(1)


if __name__ == '__main__':
    check_es_status()
