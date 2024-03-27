from configuration import Configuration
import os
import pytest


@pytest.fixture
async def environment():
    original = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original)
    Configuration(cli=original)
