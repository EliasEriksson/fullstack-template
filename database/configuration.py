from __future__ import annotations
from pathlib import Path
from functools import cached_property
from alembic.config import Config as AlembicConfiguration
from shared.configuration import ConfigurationError
from shared.configuration.environment import EnvironmentMissingVariableError
from shared.configuration.environment import TEnvironment
from shared.configuration import Configuration as BaseConfiguration
from shared.configuration import Variables as BaseVariables


class AlembicMigrationsNotFound(ConfigurationError):
    def __init__(self, path: Path) -> None:
        message = (
            f"Alembic migrations could not be found at location '{path.absolute()}'. "
            f"alembic.ini is either misconfigured or migrations directory is misplaced."
        )
        super().__init__(message)


class Variables(BaseVariables):
    username = "POSTGRES_USERNAME"
    password = "POSTGRES_PASSWORD"
    database = "POSTGRES_DATABASE"
    host = "POSTGRES_HOST"
    port = "POSTGRES_PORT"


class DatabaseConfiguration(BaseConfiguration):
    migrations: Path
    alembic: AlembicConfiguration

    def __init__(
        self,
        *,
        cli: TEnvironment | None = None,
        file: TEnvironment | None = None,
        alembic: AlembicConfiguration | None = None,
    ) -> None:
        super().__init__(
            {
                Variables.mode: "dev",
                Variables.username: None,
                Variables.password: None,
                Variables.database: None,
                Variables.host: "localhost",
                Variables.port: 5432,
            },
            cli=cli,
            file=file,
        )
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

    @cached_property
    def username(self) -> str:
        try:
            return self.environment.get_string(Variables.username)
        except EnvironmentMissingVariableError as error:
            if self.mode == "prod":
                raise error
            return "lite-star"

    @cached_property
    def password(self) -> str:
        try:
            return self.environment.get_string(Variables.password)
        except EnvironmentMissingVariableError as error:
            if self.mode == "prod":
                raise error
            return "lite-star"

    @cached_property
    def database(self) -> str:
        try:
            return self.environment.get_string(Variables.database)
        except EnvironmentMissingVariableError as error:
            if self.mode == "prod":
                raise error
            return "lite-star"

    @cached_property
    def host(self) -> str:
        return self.environment.get_string(Variables.host)

    @cached_property
    def port(self) -> int:
        return self.environment.get_int(Variables.port)

    @cached_property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
