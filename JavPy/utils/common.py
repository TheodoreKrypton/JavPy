import datetime
from functools import wraps, reduce


def try_evaluate(lambda_expression, default=None):
    def evaluate(expression):
        try:
            return expression(), None
        except Exception as ex:
            return default, ex
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
    for k in new.__dict__.keys():
        v = getattr(new, k)
        if v:
            setattr(origin, k, v)
    return origin


def sum_up(objects):
    if objects is None:
        return None
    objects = list(filter(lambda x: x, objects))
    if len(objects) == 0:
        return None
    if len(objects) == 1:
        return objects[0]
    return reduce(update_object, objects)


def urlencode(string, encoding):
    try:
        from urllib import quote as _urlencode
    except ImportError:
        from urllib.parse import quote as _urlencode

    return _urlencode(string.encode(encoding))
