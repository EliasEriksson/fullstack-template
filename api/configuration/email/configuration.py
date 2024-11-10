from __future__ import annotations
from typing import *
from functools import cached_property
from ..environment import Environment
from .variables import Variables

if TYPE_CHECKING:
    from ..configuration import Configuration as Parent


# TODO add support for sending DKIM signed emails using local SMTP server
class Configuration:
    _configuration: Parent
    _environment: Environment

    def __init__(self, configuration: Parent, environment: Environment) -> None:
        self._configuration = configuration
        self._environment = environment
        if self._configuration.mode != "prod":
            self._environment.write_missing(
                {
                    Variables.provider: "local",
                }
            )

    @cached_property
    def provider(self) -> str:
        return self._environment.get_string(Variables.provider)
