from .configuration import DatabaseConfiguration
from .configuration import Variables
from shared.configuration.environment import EnvironmentValueTypeError
import os

original = os.environ.copy()


def reset_environ():
    os.environ.clear()
    os.environ.update(original)


async def test_defaults():
    configuration = DatabaseConfiguration()
    assert configuration.mode == "dev"
    assert configuration.username == "lite-star"
    assert configuration.password == "lite-star"
    assert configuration.database == "lite-star"
    assert configuration.host == "localhost"
    assert configuration.port == 5432
    assert len(configuration.environment) == 6
    reset_environ()


async def test_modified_defaults():
    defaults = {
        Variables.database: "lite-star-test",
    }
    configuration = DatabaseConfiguration(
        defaults=defaults,
    )
    assert configuration.mode == "dev"
    assert configuration.username == "lite-star"
    assert configuration.password == "lite-star"
    assert configuration.database == "lite-star-test"
    assert configuration.host == "localhost"
    assert configuration.port == 5432
    assert len(configuration.environment) == 6
    reset_environ()


async def test_overwriting_defaults():
    defaults = {
        Variables.mode: "prod",
        Variables.username: "garbage",
    }
    cli = {
        Variables.mode: "dev",
        Variables.username: "not-lite-star",
    }
    configuration = DatabaseConfiguration(
        cli=cli,
        defaults=defaults,
    )
    assert configuration.mode == "dev"
    assert configuration.username == "not-lite-star"
    assert len(configuration.environment) == 6
    reset_environ()


async def test_bad_values():
    cli = {
        Variables.port: "1234q",
    }
    configuration = DatabaseConfiguration(
        cli=cli,
    )
    try:
        assert configuration.port
        failed = True
    except EnvironmentValueTypeError:
        failed = True
    assert failed is True
    reset_environ()
