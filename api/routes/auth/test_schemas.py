from . import schemas
from database import models
from .schemas import Token
from .schemas import Claims
from .schemas import Algorithms
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
import re

now = datetime.fromtimestamp(round(datetime.now().timestamp()))
soon = now + timedelta(minutes=20)
jwt_pattern = re.compile(r"^ey[^.]+\.[^.]+\.[^.]+$")


def create() -> schemas.Token:
    return schemas.Token(subject=uuid4(), expires=soon, issued=now)


async def test_constants():
    assert Algorithms.RS512 == "RS512"
    assert Claims.subject == "sub"
    assert Claims.expires == "exp"
    assert Claims.issued == "iss"


async def test__init__() -> None:
    token = create()
    assert isinstance(token, schemas.Token)


async def test_to_jose_dict() -> None:
    token = create()
    assert token._to_jose_dict() == {
        Claims.subject: str(token.subject),
        Claims.expires: round(token.expires.timestamp()),
        Claims.issued: round(token.issued.timestamp()),
    }


async def test_from_jose_dict() -> None:
    token = create()
    processed = token._to_jose_dict()
    assert schemas.Token._from_jose_dict(processed) == token


async def test_encode() -> None:
    token = create()
    encoded = token.encode()
    assert isinstance(encoded, str)
    assert jwt_pattern.match(encoded)


async def test_decode() -> None:
    token = create()
    encoded = token.encode()
    decoded = Token.decode(encoded)
    assert token == decoded


async def test_from_model() -> None:
    user = models.User(id=uuid4())
    encoded = Token.encode_model(user)
    assert jwt_pattern.match(encoded)
    token = Token.decode(encoded)
    assert token.subject == user.id
