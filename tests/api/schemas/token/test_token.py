import asyncio
from datetime import datetime, timedelta
from api.schemas import token as schemas
from ..conftest import audience
import re
from uuid import uuid4

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


async def test_from_object(
    audience: str, issuer: str, now: datetime, soon: datetime
) -> None:

    class Protocol:
        def __init__(self) -> None:
            self.audience = audience
            self.issuer = issuer
            self.subject = uuid4()
            self.issued = now
            self.expires = soon

    assert isinstance(schemas.Token.from_object(Protocol()), schemas.Token)


async def test_from_user(audience: str, issuer: str) -> None:
    class Protocol:
        def __init__(self) -> None:
            self.id = uuid4()

    assert isinstance(
        schemas.Token.from_user(Protocol(), audience, issuer), schemas.Token
    )


async def test_refresh(
    audience: str, issuer: str, now: datetime, soon: datetime
) -> None:
    class Protocol:
        def __init__(self) -> None:
            self.id = uuid4()

    token = schemas.Token.from_user(Protocol(), audience, issuer)
    issued = token.issued
    expires = token.expires
    duration = timedelta(minutes=30)
    delta = timedelta(seconds=10)
    token.refresh(issued=issued + delta, duration=duration)
    assert issued != token.issued
    assert issued + delta == token.issued
    # assert expires != token.expires
    # assert expires + delta == token.expires
    # TODO: test expires
