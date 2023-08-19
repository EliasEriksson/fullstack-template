from .configuration import Configuration
from .configuration import ConfigurationValueError
from .configuration import ConfigurationMissingVariable


async def test_missing_variable():
    environment = {}
    try:
        Configuration(environment)
    except ConfigurationMissingVariable:
        pass
    environment = {
        "POSTGRES_USERNAME": "lite-star-u",
        "POSTGRES_PASSWORD": "lite-star-p",
        "POSTGRES_DATABASE": "lite-star-d",
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
    configuration = Configuration()

    assert configuration.port == 5432
    assert configuration.host == "localhost"
    assert configuration.username == "lite-star-u"
    assert configuration.password == "lite-star-p"
    assert configuration.database == "lite-star-d"
