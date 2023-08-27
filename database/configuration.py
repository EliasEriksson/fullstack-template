import os
from pathlib import Path
from alembic.config import Config as AlembicConfiguration


class Meta(type):
    """
    Configuration metaclass

    works similar to a singleton but the instance is overwritten if args/kwargs are given
    is this a good idea? probably not but it makes it easy to test for now
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances or args or kwargs:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigurationError(Exception):
    pass


class ConfigurationMissingVariable(ConfigurationError):
    def __init__(self, variable: str) -> None:
        super().__init__(f"Variable: '{variable}' is missing from environment.")


class ConfigurationValueError(ConfigurationError):
    def __init__(self, variable: str, value: str, expected: str) -> None:
        super().__init__(
            f"Unexpected type of environment variable: '{variable}', "
            f"received value: {value}, expected type: {expected}."
        )


class AlembicMigrationsNotFound(ConfigurationError):
    def __init__(self, path: Path) -> None:
        message = (
            f"Alembic migrations could not be found at location '{path.absolute()}'. "
            f"alembic.ini is either misconfigured or migrations directory is misplaced."
        )
        super().__init__(message)


class Configuration(metaclass=Meta):
    _environment: dict[str, str]

    def __init__(self, environment: dict[str, str] | None = None) -> None:
        environment = environment if environment is not None else {}
        self._environment = {
            **environment,
            **os.environ,
        }

    def _string(self, variable: str) -> str:
        return self._get(variable)

    def _integer(self, variable: str) -> int:
        value = self._get(variable)
        try:
            return int(value)
        except ValueError:
            raise ConfigurationValueError(variable, value, "int")
        except TypeError:
            raise ConfigurationMissingVariable(variable)

    def _get(self, variable: str) -> str:
        try:
            value = self._environment[variable]
            if value is None:
                raise KeyError
            return value
        except KeyError:
            raise ConfigurationMissingVariable(variable)


class DatabaseConfiguration(Configuration):
    migrations: Path
    alembic: AlembicConfiguration

    def __init__(
        self,
        environment: dict[str, str] | None = None,
        alembic: AlembicConfiguration | None = None,
    ) -> None:
        super().__init__(environment)
        self.alembic = (
            alembic if alembic is not None else AlembicConfiguration("./alembic.ini")
        )
        self.migrations = Path(
            self.alembic.get_main_option("script_location")
        ).joinpath("versions")
        if not self.migrations.is_dir():
            raise AlembicMigrationsNotFound(self.migrations)

    @property
    def username(self) -> str:
        try:
            return self._string("POSTGRES_USERNAME")
        except ConfigurationMissingVariable:
            return "lite-star"

    @property
    def password(self) -> str:
        try:
            return self._string("POSTGRES_PASSWORD")
        except ConfigurationMissingVariable:
            return "lite-star"

    @property
    def database(self):
        try:
            return self._string("POSTGRES_DATABASE")
        except ConfigurationMissingVariable:
            return "lite-star"

    @property
    def host(self):
        try:
            return self._string("POSTGRES_HOST")
        except ConfigurationMissingVariable:
            return "localhost"

    @property
    def port(self):
        try:
            return self._integer("POSTGRES_PORT")
        except ConfigurationMissingVariable:
            return "5432"

    @property
    def url(self):
        return f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
