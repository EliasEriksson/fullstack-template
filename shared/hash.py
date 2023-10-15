from __future__ import annotations
from xxhash import xxh128
from bcrypt import hashpw
from bcrypt import gensalt
from datetime import datetime


def etag(time: datetime) -> str:
    return xxh128(time.timestamp().hex()).digest().hex()


def password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt())
