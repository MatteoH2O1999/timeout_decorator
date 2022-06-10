def timeout(
    func, timeout_duration: float = None, exception_to_raise: Exception = TimeoutError
):
    print("Test")
    return func
