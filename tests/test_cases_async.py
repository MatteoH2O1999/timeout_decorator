import asyncio
import pytest

from timeout_function_decorator import timeout


@timeout()
async def default_parameters():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_default_parameters():
    await default_parameters()


@timeout(None)
async def no_timeout():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_no_timeout():
    await no_timeout()


@timeout(1)
async def timeout_no_trigger():
    pass


@pytest.mark.asyncio
async def test_timeout_no_trigger():
    await timeout_no_trigger()


@timeout(1)
async def timeout_triggered():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_timeout_triggered():
    with pytest.raises(TimeoutError):
        await timeout_triggered()


class CustomException(Exception):
    pass


@timeout(1, CustomException)
async def timeout_triggered_custom_exception():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_timeout_triggered_custom_exception():
    with pytest.raises(CustomException):
        await timeout_triggered_custom_exception()


@timeout()
async def timeout_return_value(value):
    await asyncio.sleep(2)
    return value


@pytest.mark.asyncio
async def test_timeout_return_value():
    value = await timeout_return_value(2)
    assert value == 2


@timeout(1)
async def timeout_triggered_return_value(value):
    await asyncio.sleep(2)
    return value


@pytest.mark.asyncio
async def test_timeout_triggered_return_value():
    value = None
    with pytest.raises(TimeoutError):
        value = await timeout_triggered_return_value(2)
    assert value is None


@timeout(1)
async def timeout_triggered_infinite_function(value):
    while True:
        await asyncio.sleep(1)
    return value


@pytest.mark.asyncio
async def test_timeout_triggered_infinite_function():
    value = None
    with pytest.raises(TimeoutError):
        value = await timeout_triggered_infinite_function(2)
    assert value is None
