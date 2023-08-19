import os
from .singleton import Singleton


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


class Configuration(metaclass=Singleton):
    environment: dict[str, str]
    username: str
    password: str
    database: str
    host: str
    port: int

    def __init__(self, environment: dict[str, str] = os.environ) -> None:
        self.environment = environment
        self.username = self.string("POSTGRES_USERNAME")
        self.password = self.string("POSTGRES_PASSWORD")
        self.database = self.string("POSTGRES_DATABASE")
        self.host = self.string("POSTGRES_HOST")
        self.port = self.integer("POSTGRES_PORT")

    def string(self, variable: str) -> str:
        return self.get(variable)

    def integer(self, variable: str) -> int:
        value = self.get(variable)
        try:
            return int(value)
        except ValueError:
            raise ConfigurationValueError(variable, value, "int")

    def get(self, variable: str) -> str:
        try:
            return self.environment[variable]
        except KeyError:
            raise ConfigurationMissingVariable(variable)
