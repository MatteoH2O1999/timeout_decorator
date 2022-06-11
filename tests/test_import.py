from timeout_function_decorator import timeout as short_import
from timeout_function_decorator.timeout_decorator import timeout as long_import


def test_import():
    assert short_import is long_import
