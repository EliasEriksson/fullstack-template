from __future__ import annotations
from typing import *
from functools import cached_property
from .environment import EnvironmentError
from .environment import Environment
from .environment import TEnvironment
from ..singleton import Singleton
from ..iterable import Iterable


class ConfigurationError(EnvironmentError):
    pass


class ConfigurationValueError(ConfigurationError):
    pass


class Variables(Iterable):
    mode = "MODE"


class Configuration(Singleton):
    environment: Environment

    def __init__(
        self,
        variables: TEnvironment | None = None,
        *,
        cli: TEnvironment | None = None,
        file: TEnvironment | None = None,
    ) -> None:
        self.environment = Environment(
            {Variables.mode: "dev", **(variables or {})}, cli=cli, file=file
        )

    @cached_property
    def mode(self) -> Literal["prod", "dev"]:
        result = self.environment.get_string(Variables.mode)
        if result not in ["dev", "prod"]:
            raise ConfigurationValueError()
        return cast(Literal["dev", "prod"], result)
