from pathlib import Path
from alembic.config import Config as AlembicConfiguration
from shared.configuration import ConfigurationError
from shared.configuration import ConfigurationMissingVariable
from shared.configuration import Configuration
from shared.iterable import Iterable


class AlembicMigrationsNotFound(ConfigurationError):
    def __init__(self, path: Path) -> None:
        message = (
            f"Alembic migrations could not be found at location '{path.absolute()}'. "
            f"alembic.ini is either misconfigured or migrations directory is misplaced."
        )
        super().__init__(message)


class Variables(Iterable):
    username = "POSTGRES_USERNAME"
    password = "POSTGRES_PASSWORD"
    database = "POSTGRES_DATABASE"
    host = "POSTGRES_HOST"
    port = "POSTGRES_PORT"


class DatabaseConfiguration(Configuration):
    migrations: Path
    alembic: AlembicConfiguration

    variables = Variables()

    def __init__(
        self,
        environment: dict[str, str | int] | None = None,
        alembic: AlembicConfiguration | None = None,
    ) -> None:
        super().__init__(environment)
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
        self._write()

    @property
    def username(self) -> str:
        try:
            return self._string(self.variables.username)
        except ConfigurationMissingVariable:
            return "lite-star"

    @property
    def password(self) -> str:
        try:
            return self._string(self.variables.password)
        except ConfigurationMissingVariable:
            return "lite-star"

    @property
    def database(self) -> str:
        try:
            return self._string(self.variables.database)
        except ConfigurationMissingVariable:
            return "lite-star"

    @property
    def host(self) -> str:
        try:
            return self._string(self.variables.host)
        except ConfigurationMissingVariable:
            return "localhost"

    @property
    def port(self) -> int:
        try:
            return self._integer(self.variables.port)
        except ConfigurationMissingVariable:
            return 5432

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def _write(self) -> None:
        self._set(self.variables.username, self.username)
        self._set(self.variables.password, self.password)
        self._set(self.variables.database, self.database)
        self._set(self.variables.host, self.host)
        self._set(self.variables.port, self.port)
