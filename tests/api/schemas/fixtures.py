import pytest
from api import schemas
from ...fixtures import now
from datetime import datetime
from uuid import uuid4


@pytest.fixture(autouse=True)
async def audience() -> None:
    yield "http://localhost:8080/"


@pytest.fixture(autouse=True)
async def issuer() -> None:
    yield "http://localhost:8080/"


@pytest.fixture
async def token(now: datetime, soon: datetime, audience: str, issuer: str) -> None:
    yield schemas.token.Token(
        audience=audience,
        issuer=issuer,
        subject=uuid4(),
        issued=now,
        expires=soon,
    )
