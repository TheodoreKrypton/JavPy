import requests
from JavPy.utils.requester import Task, spawn_many


def ping(url, n=1):
    latencies = list(map(lambda rsp: rsp.elapsed.microseconds, filter(
        lambda rsp: rsp.status_code == 200, spawn_many(
            (Task(requests.head, url) for _ in range(n))).wait_for_all_finished()
    )))
    return 0 if not latencies else sum(latencies) / len(latencies)


if __name__ == "__main__":
    print(ping("http://www.google.com", 5))
