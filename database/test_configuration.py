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
        "POSTGRES_USERNAME": "lite-star",
        "POSTGRES_PASSWORD": "lite-star",
        "POSTGRES_DATABASE": "lite-star",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "garbage",
    }
    try:
        Configuration(environment)
    except ConfigurationValueError:
        pass
    environment["POSTGRES_PORT"] = "5432"
    Configuration(environment)
