from configuration import Configuration
from ..fixtures import environment


async def test_defaults(environment: None) -> None:
    configuration = Configuration()
    assert configuration.mode == "test"
    username = configuration.database.username
    assert username == "fullstack"
    password = configuration.database.password
    assert password == "fullstack"
    name = configuration.database.name
    assert name == "fullstack"
    test = configuration.database.test
    assert test == "fullstack_test"
    host = configuration.database.host
    assert host == "localhost"
    port = configuration.database.port
    assert port == "5432"
    url = configuration.database.url
    assert url == f"postgresql+psycopg://{username}:{password}@{host}:{port}/{name}"
