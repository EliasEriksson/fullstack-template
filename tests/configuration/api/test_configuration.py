import os

from configuration import Configuration
from configuration.api.variables import Variables
from pathlib import Path
import re
from ..fixtures import environment

private_pattern = re.compile(
    r"^-----BEGIN PRIVATE KEY-----\n.*\n-----END PRIVATE KEY-----(\n|$)",
    re.DOTALL,
)
public_pattern = re.compile(
    r"^-----BEGIN PUBLIC KEY-----\n.*\n-----END PUBLIC KEY-----(\n|$)",
    re.DOTALL,
)


async def test_modified_defaults(environment: None) -> None:
    os.environ.clear()
    cli = {
        Variables.password_pepper: "pepper",
        Variables.jwt_private_key: __file__,
        Variables.jwt_public_key: __file__,
    }
    configuration = Configuration(
        cli=cli,
    )
    with Path(__file__) as file:
        contents = file.read_text()
    assert configuration.api.jwt_private_key == contents
    assert configuration.api.jwt_public_key == contents
    assert configuration.api.password_pepper == "pepper"


async def test_overwriting_defaults(environment: None) -> None:
    os.environ.clear()
    cli = {
        Variables.password_pepper: "",
        Variables.jwt_private_key: None,
        Variables.jwt_public_key: None,
    }
    configuration = Configuration(
        cli=cli,
    )
    assert configuration.mode == "test"
    assert configuration.api.password_pepper == ""
    assert private_pattern.search(configuration.api.jwt_private_key)
    assert public_pattern.search(configuration.api.jwt_public_key)


def test_defaults(environment: None) -> None:
    os.environ.clear()
    cli = {}
    configuration = Configuration(cli=cli)
    assert configuration.mode == "test"
    assert private_pattern.search(configuration.api.jwt_private_key)
    assert public_pattern.search(configuration.api.jwt_public_key)
    assert configuration.api.password_pepper == ""
    assert configuration.api.port == 8080
