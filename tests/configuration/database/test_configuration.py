import os
from api.configuration import Configuration
from api.configuration.variables import Variables as ConfigurationVariables
from api.configuration.database.variables import Variables
from ..conftest import environment


async def test_defaults_dev(environment: None) -> None:
    os.environ.clear()
    cli = {ConfigurationVariables.mode: "dev"}
    configuration = Configuration(cli=cli)
    assert configuration.mode == "dev"
    username = configuration.database.username
    assert username == "fullstack"
    password = configuration.database.password
    assert password == "fullstack"
    name = configuration.database.name
    assert name == "fullstack"
    test = configuration.database.test
    assert test == "fullstack-test"
    host = configuration.database.host
    assert host == "localhost"
    port = configuration.database.port
    assert port == 5432
    url = configuration.database.url
    assert url == f"postgresql+psycopg://{username}:{password}@{host}:{port}/{name}"


async def test_default_test(environment: None) -> None:
    os.environ.clear()
    cli = {ConfigurationVariables.mode: "test"}
    configuration = Configuration(cli=cli)
    username = configuration.database.username
    password = configuration.database.password
    test = configuration.database.test
    host = configuration.database.host
    port = configuration.database.port
    url = configuration.database.url
    assert url == f"postgresql+psycopg://{username}:{password}@{host}:{port}/{test}"


async def test_modified_defaults(environment: None) -> None:
    os.environ.clear()
    cli = {
        ConfigurationVariables.mode: "dev",
        Variables.username: "not-fullstack",
        Variables.password: "password-of-fullstack",
        Variables.host: "192.168.1.20",
        Variables.port: 2345,
        Variables.name: "database-of-fullstack",
    }
    configuration = Configuration(cli=cli)
    username = configuration.database.username
    assert username == "not-fullstack"
    password = configuration.database.password
    assert password == "password-of-fullstack"
    name = configuration.database.name
    assert name == "database-of-fullstack"
    host = configuration.database.host
    assert host == "192.168.1.20"
    port = configuration.database.port
    assert port == 2345
    url = configuration.database.url
    assert url == f"postgresql+psycopg://{username}:{password}@{host}:{port}/{name}"


async def test_from_environment(environment: None) -> None:
    os.environ.clear()
    os.environ.update(
        {
            ConfigurationVariables.mode: "dev",
            Variables.username: "fullstack-not",
            Variables.password: "the-password",
            Variables.host: "192.168.1.20",
            Variables.port: "2345",
            Variables.name: "the-database-name",
        }
    )
    cli = {
        Variables.port: 3245,
    }
    configuration = Configuration(cli=cli)
    username = configuration.database.username
    assert username == "fullstack-not"
    password = configuration.database.password
    assert password == "the-password"
    name = configuration.database.name
    assert name == "the-database-name"
    host = configuration.database.host
    assert host == "192.168.1.20"
    port = configuration.database.port
    assert port == 3245
    url = configuration.database.url
    assert url == f"postgresql+psycopg://{username}:{password}@{host}:{port}/{name}"
