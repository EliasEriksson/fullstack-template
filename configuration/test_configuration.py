from configuration import Configuration


async def test_acquisition():
    environment = {}
    assert Configuration(cli=environment) is Configuration()
    assert Configuration(cli=environment) is not Configuration(cli=environment)


async def test_defaults():
    configuration = Configuration()
    assert configuration.mode == "test"
