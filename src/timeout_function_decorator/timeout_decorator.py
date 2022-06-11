"""
Module containing "timeout" decorator for sync and async callables.
"""

import asyncio

from inspect import iscoroutinefunction
from functools import partial, wraps
from threading import Thread
from typing import Type


def timeout(
    timeout_duration: float = None, exception_to_raise: Type[Exception] = TimeoutError
):
    """
    Wraps a function to raise the specified exception if execution time
    is greater than the specified timeout.

    Works with both synchronous and asynchronous callables, but with synchronous ones will introduce
    some overhead due to the backend use of threads and asyncio.

        :param float timeout_duration: Timeout duration in seconds. If none callable won't time out.
        :param Type[Exception] exception_to_raise: Exception to raise when the callable times out.
            Defaults to TimeoutError.
        :return: The decorated function.
        :rtype: callable
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            thread = _SyncWrapper(func, timeout_duration, *args, **kwargs)
            thread.start()
            thread.join()
            if thread.timed_out:
                raise exception_to_raise()
            return thread.result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                value = await asyncio.wait_for(
                    func(*args, **kwargs), timeout=timeout_duration
                )
                return value
            except asyncio.TimeoutError:
                raise exception_to_raise()

        if iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator


class _SyncWrapper(Thread):
    def __init__(self, func, timeout_duration, *args, **kwargs):
        super().__init__()
        self.result = None
        self.func = partial(func, *args, **kwargs)
        self.timeout_duration = timeout_duration
        self.timed_out = False

    def run(self) -> None:
        try:
            self.result = asyncio.new_event_loop().run_until_complete(
                asyncio.wait_for(self.run_func(), self.timeout_duration)
            )
        except asyncio.TimeoutError:
            self.timed_out = True

    async def run_func(self):
        value = await asyncio.get_event_loop().run_in_executor(None, self.func)
        return value
