def try_evaluate(expression, default=None):
    def _try_evaluate(func):
        def evaluate():
            try:
                return func(0)
            except Exception:
                return default
        return evaluate
    return _try_evaluate(expression)()


