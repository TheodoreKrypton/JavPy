import datetime
import functools
import re

version = "0.3.6"


def try_evaluate(lambda_expression, default=None):
    def evaluate(expression):
        try:
            return expression(), None
        except Exception as ex:
            return default, ex

    return evaluate(lambda_expression)


def cache(f):
    """
    from https://gist.github.com/Morreski/c1d08a3afa4040815eafd3891e16b945
    """
    update_delta = datetime.timedelta(hours=1)
    next_update = datetime.datetime.now() - update_delta
    # Apply @lru_cache to f with no cache size limit
    f = functools.lru_cache(None)(f)

    @functools.wraps(f)
    def _wrapped(*args, **kwargs):
        nonlocal next_update
        now = datetime.datetime.now()
        if now >= next_update:
            f.cache_clear()
            next_update = now + update_delta
        return f(*args, **kwargs)
    return _wrapped


_class_name_pattern = re.compile(r"\.(.+?)\s")


def get_func_full_name(func):
    try:
        return func.__module__ + "." + func.__qualname__
    except AttributeError:
        try:
            return (
                func.__module__
                + re.search(_class_name_pattern, func.im_class).group(1)
                + "."
                + func.__name__
            )
        except AttributeError:
            return ""


def assign(origin, new):
    for k in new.__dict__.keys():
        v = getattr(new, k)
        if v:
            setattr(origin, k, v)
    return origin


def conclude(objects):
    if objects is None:
        return None
    objects = list(filter(lambda x: x, objects))
    if len(objects) == 0:
        return None
    if len(objects) == 1:
        return objects[0]
    return functools.reduce(assign, objects)


def urlencode(string, encoding):
    from urllib.parse import quote
    return quote(string.encode(encoding))


def urldecode(string, encoding):
    from urllib.parse import unquote
    return unquote(string, encoding)


def get_code_from_title(title):
    return re.search(r"\w+-?\d+", title).group(0)
