import pytest
import time

from timeout_function_decorator import timeout


@timeout()
def default_parameters():
    time.sleep(2)


def test_default_parameters():
    default_parameters()


@timeout(None)
def no_timeout():
    time.sleep(2)


def test_no_timeout():
    no_timeout()


@timeout(1)
def timeout_no_trigger():
    pass


def test_timeout_no_trigger():
    timeout_no_trigger()


@timeout(1)
def timeout_triggered():
    time.sleep(2)


def test_timeout_triggered():
    with pytest.raises(TimeoutError):
        timeout_triggered()


class CustomException(Exception):
    pass


@timeout(1, CustomException)
def timeout_triggered_custom_exception():
    time.sleep(2)


def test_timeout_triggered_custom_exception():
    with pytest.raises(CustomException):
        timeout_triggered_custom_exception()
