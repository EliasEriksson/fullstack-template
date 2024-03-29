from __future__ import annotations
import pytest
from datetime import datetime
from datetime import timedelta
from dataclasses import dataclass


@dataclass
class Times:
    now = datetime.now()
    soon = now + timedelta(minutes=20)


@pytest.fixture(autouse=True)
async def now():
    yield Times.now


@pytest.fixture(autouse=True)
async def soon():
    yield Times.soon
