from __future__ import annotations
from typing import *
from functools import cached_property
from .environment import EnvironmentError
from .environment import Environment
from .environment import TEnvironment
from .environment import TVariables
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
        variables: TVariables | None = None,
        *,
        cli: TEnvironment | None = None,
        file: TEnvironment | None = None,
        defaults: TEnvironment | None = None,
    ) -> None:
        self.environment = Environment(
            variables or Variables,
            cli=cli,
            file=file,
            defaults={Variables.mode: "dev", **(defaults or {})},
        )

    @cached_property
    def mode(self) -> Literal["prod", "dev"]:
        result = self.environment.get_string(Variables.mode)
        if result not in ["dev", "prod"]:
            raise ConfigurationValueError()
        return cast(Literal["dev", "prod"], result)
