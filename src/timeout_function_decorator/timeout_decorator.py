from functools import wraps


def timeout(
    _func=None,
    *,
    timeout_duration: float = None,
    exception_to_raise: Exception = TimeoutError
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
