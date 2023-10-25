from __future__ import annotations
from api.schemas import Base
from database import models
from msgspec import Struct
from msgspec import field
from shared import hash
from datetime import datetime


class Creatable(Struct):
    host: str
    agent: str

    @staticmethod
    def create():
        pass
