from __future__ import annotations
from typing import *
from functools import cached_property
import os
from shared.singleton import Singleton
from .variables import Variables
from .environment import Environment
from .environment.types import TEnvironment
from .exceptions import ConfigurationValueError
from . import api
from . import database


class Configuration(Singleton):
    _initial = os.environ.copy()
    _environment: Environment
    api: api.Configuration
    database: database.Configuration

    def __init__(
        self, *, cli: TEnvironment | None = None, file: TEnvironment | None = None
    ) -> None:
        self._reset()
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
        if self.mode != "test":
            self._initial = os.environ.copy()

    def _reset(self) -> None:
        os.environ.clear()
        os.environ.update(self._initial)

    @cached_property
    def mode(self) -> Literal["prod", "dev", "test"]:
        result = self._environment.get_string(Variables.mode)
        if result not in ["dev", "prod", "test"]:
            raise ConfigurationValueError()
        return cast(Literal["dev", "prod", "test"], result)
