from datetime import datetime, timedelta
from api.schemas import token as schemas
from ..conftest import audience
import re
from uuid import uuid4, UUID

jwt_pattern = re.compile(r"^ey[^.]+\.ey[^.]+\.[^.]+$")


class Session:
    class User:
        class Password:
            digest: str

            def __init__(self, digest: str) -> None:
                self.digest = digest

        id: UUID
        passwords: list[Password]

        def __init__(self, passwords: list[str]) -> None:
            self.id = uuid4()
            self.passwords = [Session.User.Password(password) for password in passwords]

    id: UUID
    user: User

    def __init__(self, passwords: list[str]) -> None:
        self.id = uuid4()
        self.user = self.User(passwords)


class Token:
    audience: str
    issuer: str
    subject: UUID
    session: UUID
    secure: bool
    issued: datetime
    expires: datetime

    def __init__(
        self, audience: str, issuer: str, issued: datetime, expires: datetime
    ) -> None:
        self.audience = audience
        self.issuer = issuer
        self.subject = uuid4()
        self.session = uuid4()
        self.secure = True
        self.issued = issued
        self.expires = expires


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
    assert isinstance(
        schemas.Token.from_object(Token(audience, issuer, now, soon)), schemas.Token
    )


async def test_from_user(audience: str, issuer: str) -> None:
    assert isinstance(
        schemas.Token.create(Session(["asd"]), audience, issuer), schemas.Token
    )


async def test_refresh(
    audience: str, issuer: str, now: datetime, soon: datetime
) -> None:
    token = schemas.Token.create(Session(["qwe"]), audience, issuer)
    issued = token.issued
    expires = token.expires
    duration = timedelta(minutes=30)
    delta = timedelta(seconds=10)
    zero = issued + delta
    token.refresh(issued=zero, duration=duration)
    assert expires - issued == timedelta(minutes=20)
    assert token.expires - token.issued == duration
    assert issued != token.issued
    assert issued + delta == token.issued
