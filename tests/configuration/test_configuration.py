from configuration import Configuration
from .fixtures import environment


async def test_acquisition(environment: None):
    environment = {}
    assert Configuration(cli=environment) is Configuration()
    assert Configuration(cli=environment) is not Configuration(cli=environment)


async def test_defaults(environment: None):
    configuration = Configuration()
    assert configuration.mode == "test"
