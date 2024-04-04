import pytest
from api.schemas import token as schemas
from ..conftest import audience
import re

jwt_pattern = re.compile(r"^ey[^.]+\.ey[^.]+\.[^.]+$")


async def test_constants() -> None:
    assert schemas.Algorithms.RS512 == "RS512"
    assert schemas.Claims.audience == "aud"
    assert schemas.Claims.subject == "sub"
    assert schemas.Claims.expires == "exp"
    assert schemas.Claims.issued == "iat"
    assert schemas.Claims.issuer == "iss"


async def test_encode_decode(
    token: schemas.Token,
    audience: str,
) -> None:
    jwt = token.encode()
    assert isinstance(jwt, str)
    assert jwt_pattern.match(jwt)
    result = schemas.Token.decode(jwt, audience)
    assert result.audience == token.audience
    assert result.issuer == token.issuer
    assert result.issued == token.issued
    assert result.subject == token.subject
    assert result.expires == token.expires
