import os


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

    def _get(self, variable: str) -> str:
        try:
            return self._environment[variable]
        except KeyError:
            raise ConfigurationMissingVariable(variable)


class DatabaseConfiguration(Configuration):
    def __init__(self, environment: dict[str, str] | None = None) -> None:
        super().__init__(environment)

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
