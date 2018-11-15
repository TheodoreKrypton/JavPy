def try_evaluate(lambda_expression, default=None):
    def evaluate(expression):
        try:
            return expression()
        except Exception:
            return default
    return evaluate(lambda_expression)
