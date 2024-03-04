from __future__ import annotations
from pathlib import Path
from functools import cached_property
from alembic.config import Config as AlembicConfiguration
from shared.configuration import ConfigurationError
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
        defaults: TEnvironment | None = None,
        alembic: AlembicConfiguration | None = None,
    ) -> None:
        print("DatabaseConfiguration:", defaults)
        super().__init__(
            Variables,
            cli=cli,
            file=file,
            defaults={
                Variables.username: "lite-star",
                Variables.password: "lite-star",
                Variables.database: "lite-star",
                Variables.host: "localhost",
                Variables.port: 5432,
                **(defaults or {}),
            },
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
        return self.environment.get_string(Variables.username)

    @cached_property
    def password(self) -> str:
        return self.environment.get_string(Variables.password)

    @cached_property
    def database(self) -> str:
        return self.environment.get_string(Variables.database)

    @cached_property
    def host(self) -> str:
        return self.environment.get_string(Variables.host)

    @cached_property
    def port(self) -> int:
        return self.environment.get_int(Variables.port)

    @cached_property
    def url(self) -> str:
        result = f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        print("url:", result)
        return result
