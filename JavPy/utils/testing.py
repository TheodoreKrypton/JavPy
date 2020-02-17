def testing(*_, **parameters):
    nargs = len(parameters)
    keys = list(parameters.keys())
    if nargs > 1:
        for i in range(1, nargs):
            if len(parameters[keys[0]]) == len(parameters[keys[i]]):
                raise ValueError

    def decorator(func):
        def wrapper():
            print("==========Testing " + func.__name__)
            if not parameters:
                func()
                return
            for which, _ in enumerate(parameters[keys[0]]):
                parameter = dict(zip(keys, (parameters[key][which] for key in keys)))
                print(
                    "start to test @ %s"
                    % ", ".join(
                        (key + "=" + str(parameter[key]) for key in parameter.keys())
                    )
                )
                func(**parameter)

        return wrapper

    return decorator
