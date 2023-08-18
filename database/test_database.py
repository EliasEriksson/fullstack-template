import pytest
from . import create
from . import delete


@pytest.fixture
def setup():
    create()
    yield None
    delete()


async def test_user() -> None:
    assert 1 + 1 == 2
