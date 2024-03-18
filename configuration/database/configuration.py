from __future__ import annotations
from typing import *
from functools import cached_property
from pathlib import Path
from alembic.config import Config as AlembicConfiguration
from ..environment import Environment
from .exceptions import AlembicMigrationsNotFound
from .variables import Variables


if TYPE_CHECKING:
    from ..configuration import Configuration as Parent


class Configuration:
    _configuration: Parent
    _environment: Environment
    alembic: AlembicConfiguration

    def __init__(
        self,
        configuration: Parent,
        environment: Environment,
        alembic: AlembicConfiguration | None = None,
    ) -> None:
        self._configuration = configuration
        self._environment = environment
        self.alembic = (
            alembic if alembic is not None else AlembicConfiguration("./alembic.ini")
        )

        self.migrations = Path(
            self.alembic.get_main_option("script_location")
        ).joinpath("versions")
        try:
            self.migrations.mkdir(exist_ok=True)
        except FileNotFoundError:
            raise AlembicMigrationsNotFound(self.migrations)
        if self._configuration.mode != "prod":
            self._environment.write_missing(
                {
                    Variables.username: "lite-star",
                    Variables.password: "lite-star",
                    Variables.database: "lite-star",
                    Variables.test_database: "lite-star-test",
                    Variables.host: "localhost",
                    Variables.port: 5432,
                }
            )

    @cached_property
    def username(self) -> str:
        return self._environment.get_string(Variables.username)

    @cached_property
    def password(self) -> str:
        return self._environment.get_string(Variables.password)

    @cached_property
    def database(self) -> str:
        return self._environment.get_string(Variables.database)

    @cached_property
    def test_database(self) -> str:
        return self._environment.get_string(Variables.test_database)

    @cached_property
    def host(self) -> str:
        return self._environment.get_string(Variables.host)

    @cached_property
    def port(self) -> int:
        return self._environment.get_int(Variables.port)

    @cached_property
    def url(self) -> str:
        database = (
            self.test_database if self._configuration.mode == "test" else self.database
        )
        print(f"using database {database}")
        return f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{database}"
