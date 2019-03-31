import datetime
from functools import wraps


def try_evaluate(lambda_expression, default=None):
    def evaluate(expression):
        try:
            return expression()
        except Exception:
            return default
    return evaluate(lambda_expression)


def cache(func):
    __cache = dict()

    @wraps(func)
    def _wrapped(*args, **kwargs):
        key = str(args) + "///" + str(kwargs)

        if key in __cache:
            if datetime.datetime.now() - __cache[key][0] < datetime.timedelta(hours=1):
                return __cache[key][1]

        res = func(*args, **kwargs)

        if res:
            __cache[key] = (datetime.datetime.now(), res)

        return res

    return _wrapped


def update_object(origin, new):
    assert type(origin) == type(new)
    for k in new.__dict__.keys():
        v = getattr(new, k)
        if v:
            setattr(origin, k, v)
