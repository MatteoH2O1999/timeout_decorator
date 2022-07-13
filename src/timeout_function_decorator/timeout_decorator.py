"""
Module containing "timeout" decorator for sync and async callables.
"""

import asyncio

from concurrent import futures
from inspect import iscoroutinefunction
from functools import wraps
from threading import Thread
from typing import Type
from sys import version_info as py_ver


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
            async def async_func():
                return func(*args, **kwargs)

            thread = _LoopWrapper()
            thread.start()
            future = asyncio.run_coroutine_threadsafe(async_func(), thread.loop)
            try:
                result = future.result(timeout=timeout_duration)
            except futures.TimeoutError:
                thread.stop_loop()
                raise exception_to_raise()
            thread.stop_loop()
            return result

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


class _LoopWrapper(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()

    def run(self) -> None:
        self.loop.run_forever()
        self.loop.call_soon_threadsafe(self.loop.close)

    def stop_loop(self):
        if py_ver.major == 3 and py_ver.minor >= 7:
            caller = asyncio
        else:
            caller = asyncio.Task
        for task in caller.all_tasks(self.loop):
            task.cancel()
        self.loop.call_soon_threadsafe(self.loop.stop)
