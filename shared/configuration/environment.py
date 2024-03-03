from __future__ import annotations
import os

TValue = str | int | float
TEnvironment = dict[str, TValue]
TVariables = TEnvironment


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


class Environment:
    _variables: TVariables
    _environment: TEnvironment

    def __init__(
        self,
        variables: TEnvironment,
        cli: TEnvironment | None = None,
        file: TEnvironment | None = None,
    ) -> None:
        self._variables = variables
        self._set_environment(
            {**os.environ.copy(), **(file or {}), **(cli or {})}, defaults=True
        )

    def _set_environment(self, environment: TEnvironment, defaults=False) -> None:
        self._environment = self._read_environment(environment)
        print("THE ENVIRONMENT", self._environment)
        for variable in self._variables:
            value = self._environment.get(variable) or (
                self._variables[variable] if defaults else None
            )
            if value:
                os.environ[variable] = str(value)

    def _get_environment(self) -> TEnvironment:
        return self._environment

    def _read_environment(self, environment: TEnvironment) -> TEnvironment:
        return {
            variable: value
            for variable in self._variables
            if (value := environment.get(variable))
        }

    def get_string(self, variable: str) -> str:
        result = self._environment.get(variable)
        if result is None:
            raise EnvironmentMissingVariableError(variable)
        return str(result)

    def set_string(self, variable: str, value: str) -> None:
        self._set_environment({variable: value})

    def get_int(self, variable: str) -> int:
        result = self._environment.get(variable)
        if result is None:
            raise EnvironmentMissingVariableError(variable)
        try:
            return int(result)
        except ValueError:
            raise EnvironmentValueTypeError(variable, result, "int")

    def set_int(self, variable: str, value: int) -> None:
        self._set_environment({variable: value})

    def get_float(self, variable: str) -> float:
        result = self._environment.get(variable)
        if result is None:
            raise EnvironmentMissingVariableError(variable)
        try:
            return float(result)
        except ValueError:
            raise EnvironmentValueTypeError(variable, result, "float")

    def set_float(self, variable: str, value: float) -> None:
        self._set_environment({variable: value})
