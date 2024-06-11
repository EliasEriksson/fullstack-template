import os
from api.configuration import Configuration
from api.configuration.variables import Variables
from .conftest import environment


async def test_acquisition(environment: None):
    os.environ.clear()
    cli = {Variables.mode: "test"}
    assert Configuration(cli=cli) is Configuration()
    assert Configuration(cli=cli) is not Configuration(cli=cli)


async def test_defaults_dev(environment: None):
    os.environ.clear()
    cli = {Variables.mode: "dev"}
    configuration = Configuration(cli=cli)
    assert configuration.mode == "dev"


async def test_defaults_test(environment: None):
    os.environ.clear()
    cli = {Variables.mode: "test"}
    configuration = Configuration(cli=cli)
    assert configuration.mode == "test"
