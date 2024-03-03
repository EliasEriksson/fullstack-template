from shared.configuration import Configuration
from shared.configuration import ConfigurationValueError
from shared.configuration.environment import EnvironmentMissingVariableError


async def test_missing_variable():
    environment = {}
    try:
        Configuration(environment)
    except EnvironmentMissingVariableError:
        pass
    environment = {
        "POSTGRES_USERNAME": "lite-star",
        "POSTGRES_PASSWORD": "lite-star",
        "POSTGRES_DATABASE": "lite-star-test",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "garbage",
    }
    try:
        Configuration(environment)
    except ConfigurationValueError:
        pass
    environment["POSTGRES_PORT"] = "5432"
    assert Configuration(environment) is Configuration()
    assert Configuration(environment) is not Configuration(environment)
