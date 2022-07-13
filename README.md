<h1 align="center">Timeout function decorator</h1>

<p align="center">
<a href="https://github.com/MatteoH2O1999/timeout_decorator/actions/workflows/test.yml"><img src="https://github.com/MatteoH2O1999/timeout_decorator/actions/workflows/test.yml/badge.svg" alt="Test package"></a>
<a href="https://github.com/MatteoH2O1999/timeout_decorator/actions/workflows/release.yml"><img src="https://github.com/MatteoH2O1999/timeout_decorator/actions/workflows/release.yml/badge.svg" alt="Release package"></a>
<a href="https://github.com/MatteoH2O1999/timeout_decorator/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/timeout-function-decorator" alt="PyPI - License"></a>
<a href="https://codecov.io/gh/MatteoH2O1999/timeout_decorator"><img src="https://codecov.io/gh/MatteoH2O1999/timeout_decorator/branch/main/graph/badge.svg?token=MV9PYET185" alt="codecov"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
<a href="https://badge.fury.io/py/timeout-function-decorator"><img src="https://badge.fury.io/py/timeout-function-decorator.svg" alt="PyPI version"></a>
<a href="https://badge.fury.io/py/timeout-function-decorator"><img src="https://img.shields.io/pypi/pyversions/timeout-function-decorator" alt="PyPI - Python Version"></a>
<a href="https://pepy.tech/project/timeout-function-decorator"><img src="https://pepy.tech/badge/timeout-function-decorator" alt="Downloads"></a>
</p>

Timeout decorator for synchronous and asynchronous functions.

## Dependencies

Written in pure `Python` and has no dependencies other than the base libraries.

## Installation

From source code:

```commandline
pip install .
```

From `PyPI`:

```commandline
pip install timeout-function-decorator
```

## Import

There are three ways to import the decorator:
1. Import directly from the package
```python
from timeout_function_decorator import timeout
```
2. Import directly from the module
```python
from timeout_function_decorator.timeout_decorator import timeout
```
3. Import the module
```python
from timeout_function_decorator import timeout_decorator
```

This last case is useful if a `timeout` function is already present in your namespace.

## Usage

Using the decorator is as simple as:
```python
import time
from timeout_function_decorator import timeout


@timeout()
def i_will_never_time_out(value):
    while True:
        time.sleep(1)

        
@timeout(None)
def i_will_never_time_out(value):
    while True:
        time.sleep(1)
        

@timeout(1)
def i_will_not_time_out(value):
    return value


@timeout(1)
def i_will_time_out(value):
    time.sleep(2)
    return value


@timeout(1, RuntimeError)
def i_will_raise_runtime_error(value):
    time.sleep(2)
    return value
```

As you may have noticed, the decorator requires the brackets even when no parameters are passed.

The same result could be obtained for asynchronous functions:
```python
import asyncio
from timeout_function_decorator import timeout


@timeout()
async def i_will_never_time_out(value):
    while True:
        await asyncio.sleep(1)

        
@timeout(None)
async def i_will_never_time_out(value):
    while True:
        await asyncio.sleep(1)
        

@timeout(1)
async def i_will_not_time_out(value):
    return value


@timeout(1)
async def i_will_time_out(value):
    await asyncio.sleep(2)
    return value


@timeout(1, RuntimeError)
async def i_will_raise_runtime_error(value):
    await asyncio.sleep(2)
    return value
```

If you already have a `timeout` function in your namespace, you could as easily use the decorator with the module namespace:
```python
import time
from timeout_function_decorator import timeout_decorator


@timeout_decorator.timeout(1)
def i_still_time_out(value):
    time.sleep(2)
    return value
```

> :warning: **Warning:** When a function times out, an exception is raised but cancellation is not guaranteed. This decorator only notifies the user when enough time has passed since a function call. Handling of the situation and ensuring cancellation is up to the user.

## Signature

In general, the decorator accepts two parameters:

- `timeout_duration`: a `float` specifying the timeout time in seconds. If `None`, the function will not time out. Defaults to `None`
- `exception_to_raise`: the `Exception` type to be raised. Defaults to `TimeoutError`.

They can be passed as positional or keyword arguments.

## Intended use cases

The wrapper uses asyncio and threads to keep track of timeouts.
This adds a non-trivial overhead on the wrapped functions, in particular on the synchronous ones as they need a thread to be
created.

As such, common use cases would include test suites where control on what happens when they time out is important, as with
packages like `pytest-timeout` you can not have tests fail with a specified exception.

Use cases in production code, on the other hand, would be limited to long functions with a low call rate as the overhead is
linear with the number of calls but independent of the size of the function or its execution time.

A notebook outlining the impact of the overhead on sync and async functions can be found [here](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/notebooks/overhead.ipynb).

Plots from the notebook are presented below for a quick performance evaluation.

## Performance evaluation

### General performance

![general_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/general.png?raw=true)

### Sync performance

![sync_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/sync.png?raw=true)

#### Quick function performance

![quick_sync_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/sync_quick.png?raw=true)

#### Medium function performance

![medium_sync_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/sync_medium.png?raw=true)

#### Long function performance

![long_sync_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/sync_long.png?raw=true)

#### Huge function performance

![huge_sync_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/sync_huge.png?raw=true)

### Async performance

![async_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/async.png?raw=true)

#### Quick function performance

![quick_async_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/async_quick.png?raw=true)

#### Medium function performance

![medium_async_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/async_medium.png?raw=true)

#### Long function performance

![long_async_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/async_long.png?raw=true)

#### Huge function performance

![huge_async_performance](https://github.com/MatteoH2O1999/timeout_decorator/blob/main/performance/async_huge.png?raw=true)