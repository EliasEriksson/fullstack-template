from __future__ import annotations
from typing import *
from functools import cached_property
from shared.singleton import Singleton
from .variables import Variables
from .environment import Environment
from .environment.types import TEnvironment
from .exceptions import ConfigurationValueError
from . import api
from . import database


class Configuration(Singleton):
    _environment: Environment
    api: api.Configuration
    database: database.Configuration

    def __init__(
        self, *, cli: TEnvironment | None = None, file: TEnvironment | None = None
    ) -> None:
        print("initiating new instance")
        environment = Environment(
            {**Environment.clean(file or {}), **Environment.clean(cli or {})}
        )
        self._environment = environment
        self._environment.write_missing(
            {
                Variables.mode: "test",
            }
        )
        self.api = api.Configuration(self, environment)
        self.database = database.Configuration(self, environment)

    @cached_property
    def mode(self) -> Literal["prod", "dev", "test"]:
        result = self._environment.get_string(Variables.mode)
        if result not in ["dev", "prod", "test"]:
            raise ConfigurationValueError()
        return cast(Literal["dev", "prod", "test"], result)
