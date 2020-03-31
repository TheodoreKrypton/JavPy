from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from JavPy.utils.common import noexcept

executor = ThreadPoolExecutor(max_workers=20)


def wait_until(fs, condition=lambda x: x is not None):
    for future in as_completed(fs):
        result = noexcept(lambda: future.result())
        if result is None:
            continue
        if condition(result):
            return result
    return None


def wait_for_all(fs):
    done, _ = wait(fs)
    return [d.result() for d in done]
