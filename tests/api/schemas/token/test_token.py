import pytest
from api.schemas import token as schemas
from datetime import datetime
from datetime import timedelta
from uuid import uuid4

# from ..fixtures import audience
import re

jwt_pattern = re.compile(r"^ey[^.]+\.[^.]+\.[^.]+$")


async def test_constants() -> None:
    assert schemas.Algorithms.RS512 == "RS512"
    assert schemas.Claims.audience == "aud"
    assert schemas.Claims.subject == "sub"
    assert schemas.Claims.expires == "exp"
    assert schemas.Claims.issued == "iat"
    assert schemas.Claims.issuer == "iss"


@pytest.mark.usefixtures("token", "issuer", "now", "soon")
async def test_encode_decode(
    token: schemas.Token,
    audience: str,
    # now: datetime,
    # soon: datetime,
    # issuer: str,
) -> None:
    jwt = token.encode()
    assert isinstance(jwt, str)
    assert jwt_pattern.match(jwt)
    result = schemas.Token.decode(jwt, audience)
    assert result == token
