import requests
from JavPy.utils.requester import executor, map_f, PlaceHolder
from JavPy.utils.config import proxy


def test(url):
    return requests.head(url, proxies=proxy).status_code == 200


def ping(url, n=5):
    latencies = list(map(lambda rsp: rsp.elapsed.microseconds, filter(
        lambda rsp: rsp and rsp.status_code == 200, executor.map(
            map_f(requests.head, PlaceHolder, proxies=proxy), (url for _ in range(n))
        )
    )))
    return 0 if not latencies else sum(latencies) / len(latencies)


if __name__ == "__main__":
    print(ping("https://playfinder.xyz/v/7j6mgsgxe601k3g#poster=https://findercdn.me/files/sksk-023.jpg"))
    print(ping("https://www.google.com"))
