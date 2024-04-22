import pytest
from api import schemas

from ...conftest import now
from datetime import datetime
from uuid import uuid4


@pytest.fixture()
async def audience() -> None:
    yield "http://localhost:8080/"


@pytest.fixture()
async def issuer() -> None:
    yield "http://localhost:8080/"


@pytest.fixture()
async def token(now: datetime, soon: datetime, audience: str, issuer: str) -> None:
    yield schemas.token.Token(
        audience=audience,
        issuer=issuer,
        subject=uuid4(),
        session=uuid4(),
        issued=now,
        expires=soon,
    )
