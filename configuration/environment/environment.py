from __future__ import annotations
from typing import *
import os
from .types import TEnvironment, TVariables
from .exceptions import EnvironmentMissingVariableError
from .exceptions import EnvironmentValueTypeError


class Environment:
    _environment: TEnvironment

    def __init__(self, environment: TEnvironment | None = None) -> None:
        self._environment = os.environ.copy()
        if environment:
            self.write(environment)

    def __len__(self) -> int:
        return len(self._environment)

    def read(self, variables: TVariables) -> TEnvironment:
        return {variable: self._environment.get(variable) for variable in variables}

    def write(self, environment: TEnvironment) -> TEnvironment:
        for variable, value in environment.items():
            if value is not None:
                self._environment[variable] = value
                os.environ[variable] = str(value)
        return self._environment

    def write_missing(self, environment: TEnvironment) -> TEnvironment:
        cleaned = {
            variable: value
            for variable in environment
            if variable not in self._environment
            if (value := environment.get(variable)) is not None
        }
        return self.write(cleaned)

    def get_string(self, variable: str) -> str:
        result = self._environment.get(variable)
        if result is None:
            raise EnvironmentMissingVariableError(variable)
        return str(result)

    def set_string(self, variable: str, value: str) -> None:
        self.write({variable: value})

    def get_int(self, variable: str) -> int:
        result = self._environment.get(variable)
        if result is None:
            raise EnvironmentMissingVariableError(variable)
        try:
            return int(result)
        except ValueError:
            raise EnvironmentValueTypeError(variable, result, "int")

    def set_int(self, variable: str, value: int) -> None:
        self.write({variable: value})

    def get_float(self, variable: str) -> float:
        result = self._environment.get(variable)
        if result is None:
            raise EnvironmentMissingVariableError(variable)
        try:
            return float(result)
        except ValueError:
            raise EnvironmentValueTypeError(variable, result, "float")

    def set_float(self, variable: str, value: float) -> None:
        self.write({variable: value})

    @staticmethod
    def clean(environment: TEnvironment) -> TEnvironment:
        return {
            variable: value
            for variable in environment
            if (value := environment[variable]) is not None
        }
