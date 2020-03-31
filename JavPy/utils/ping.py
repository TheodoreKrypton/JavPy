import requests
from JavPy.utils.requester import executor
from JavPy.utils.config import proxy
from JavPy.utils.common import noexcept


def ping(url, n=1):
    latencies = list(map(lambda rsp: rsp.elapsed.microseconds, filter(
        lambda rsp: rsp and rsp.status_code == 200, executor.map(
            lambda x: noexcept(lambda: requests.head(x, proxies=proxy)), (url for _ in range(n))
        )
    )))
    return 0 if not latencies else sum(latencies) / len(latencies)


if __name__ == "__main__":
    print(ping("https://playfinder.xyz/v/7j6mgsgxe601k3g#poster=https://findercdn.me/files/sksk-023.jpg", 5))
