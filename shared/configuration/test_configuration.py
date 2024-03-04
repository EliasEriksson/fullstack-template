from .configuration import Configuration
from .configuration import Variables
from .configuration import ConfigurationValueError
import os

original = os.environ.copy()


def reset_environ():
    os.environ.clear()
    os.environ.update(original)


async def test_acquisition():
    environment = {}
    assert Configuration(cli=environment) is Configuration()
    assert Configuration(cli=environment) is not Configuration(cli=environment)
    reset_environ()


async def test_defaults():
    configuration = Configuration()
    assert configuration.mode == "dev"
    assert len(configuration.environment) == 1
    reset_environ()


async def test_modified_defaults():
    defaults = {
        Variables.mode: "prod",
    }
    configuration = Configuration(
        defaults=defaults,
    )
    assert configuration.mode == "prod"
    reset_environ()


async def test_overwriting_defaults():
    defaults = {
        Variables.mode: "prod",
    }
    cli = {
        Variables.mode: "dev",
    }
    configuration = Configuration(
        cli=cli,
        defaults=defaults,
    )
    assert configuration.mode == "dev"
    reset_environ()


async def test_bad_values():
    cli = {
        Variables.mode: "ci",
    }
    configuration = Configuration(
        cli=cli,
    )
    try:
        assert configuration.mode == "ci"
        failed = False
    except ConfigurationValueError:
        failed = True
    assert failed is True
