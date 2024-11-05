from .types import TValue


class EnvironmentError(Exception):
    pass


class EnvironmentMissingVariableError(EnvironmentError):
    def __init__(self, variable: str) -> None:
        super().__init__(f"Variable: '{variable}' is missing from environment.")


class EnvironmentValueTypeError(EnvironmentError):
    def __init__(self, variable: str, value: TValue, expected: str) -> None:
        super().__init__(
            f"Unexpected type of variable: '{variable}'. "
            f"Received value: '{value}' of type: '{type(value)}', "
            f"expected type: '{expected}'."
        )
