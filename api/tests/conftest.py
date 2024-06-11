from __future__ import annotations
import pytest
from datetime import datetime
from datetime import timedelta
from dataclasses import dataclass


@dataclass
class Times:
    now = datetime.now().replace(microsecond=0)
    soon = now + timedelta(minutes=20)


@pytest.fixture()
async def now():
    yield Times.now


@pytest.fixture()
async def soon():
    yield Times.soon
