from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from JavPy.utils.common import noexcept
from functools import reduce

executor = ThreadPoolExecutor(max_workers=40)
PlaceHolder = object()


def submit(func, *args, **kwargs):
    return executor.submit(noexcept, lambda: func(*args, **kwargs))


def map_f(func, *fixed_args, **fixed_kwargs):
    args_place_holders = [i for i in range(len(fixed_args)) if fixed_args[i] is PlaceHolder]
    args = [fixed_args[i:j] for (i, j) in zip(map(lambda x: x+1, args_place_holders[:-1]), args_place_holders[1:])]
    if len(args) == 0:
        args = [None] * len(args_place_holders)
    else:
        if args_place_holders[0] != 0:
            args = list(fixed_args[0:args_place_holders[0]]) + args
        if args_place_holders[-1] != len(fixed_args) - 1:
            args = args + list(fixed_args[args_place_holders[-1]+1:])
        print(args)
        args = reduce(lambda args1, args2: args1 + [None] + args2, args)

    def processor(*x, **kwx):
        _args = args
        for i in args_place_holders:
            _args[i] = x[i]
        return noexcept(lambda: func(*_args, **fixed_kwargs, **kwx))

    return processor


def wait_until(fs, condition=lambda x: x is not None, timeout=60):
    for future in as_completed(fs, timeout=timeout):
        result = future.result()
        if result is None:
            continue
        if condition(result):
            return result
    return None


def wait_for_all(fs, timeout=60):
    wait(fs, timeout)
    return [f.result() for f in fs]


if __name__ == '__main__':
    import requests

    map_f(requests.get, PlaceHolder, verify=False)("https://indexav.com")
    map_f(requests.get, verify=False)(url="https://indexav.com")
