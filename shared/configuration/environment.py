from __future__ import annotations
from typing import *
import os

TValue = str | int | float | None
TEnvironment = dict[str, TValue]


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


class TVariables(Protocol):
    def __iter__(self) -> Iterable[str]: ...

    def __getitem__(self, item: str) -> TValue: ...


class Environment:
    _variables: TVariables
    _environment: TEnvironment
    _initial: TEnvironment | None = None

    def __init__(
        self,
        variables: TVariables,
        *,
        defaults: TEnvironment | None = None,
        cli: TEnvironment | None = None,
        file: TEnvironment | None = None,
    ) -> None:
        self._variables = variables
        self._reset()
        self._set_environment(
            {**(defaults or {}), **os.environ.copy(), **(file or {}), **(cli or {})},
        )

    def __len__(self) -> int:
        return len(self._environment)

    def _set_environment(self, environment: TEnvironment) -> None:
        self._environment = self._read_environment(environment)
        for variable, value in self._environment.items():
            if value:
                os.environ[variable] = str(value)
        if not self._initial:
            self._initial = os.environ.copy()

    def _get_environment(self) -> TEnvironment:
        return self._environment

    def _read_environment(self, environment: TEnvironment) -> TEnvironment:
        return {
            variable: value
            for name in self._variables
            if (value := environment.get((variable := self._variables[name])))
            is not None
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

    def _reset(self) -> None:
        if self._initial:
            os.environ.clear()
            os.environ.update(self._initial)
