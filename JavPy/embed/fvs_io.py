import requests
from JavPy.utils.ping import ping
from JavPy.utils.config import proxy
from JavPy.utils.requester import executor
from itertools import repeat


class fvs_io:
    @staticmethod
    def test_latency(url):
        rsp = requests.get(url, allow_redirects=False, proxies=proxy)
        if rsp:
            return ping(rsp.headers["Location"]), rsp.headers["Location"]
        else:
            return None

    @staticmethod
    def decode(fvs_url):
        retry = 4

        return min(
            filter(lambda x: x, executor.map(fvs_io.test_latency, repeat(fvs_url, retry))),
            key=lambda latency_location: latency_location[0],
        )[1]


if __name__ == "__main__":
    print(
        fvs_io.decode(
            "https://fvs.io/redirector?token=dlNQbFlJVXhjNmt3bWM3V2tXSE9KSm5lU1ErZTdQeXRRTG93czRacm8zdG4reDdQbG9Sc2pGV0ZYMUZ6NzJVbm9OcmRHYWVSOHBoZTZkd0gzVGFNUzE5QU11SzZXbElHOS81N2pxYzQvOGtaV1BGUTJrSjVUbVo5dW1ETnVOQU1nWDM2R3RyOWlNWnNKRjYzT1VuLzJEdUJIcDJRUWFyd0h1ND06dDR2ejE1RkVzb29oS21vbm9kVDRkZz09"
        )
    )
