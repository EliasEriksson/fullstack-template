from __future__ import annotations
from typing import *
from xxhash import xxh128
from bcrypt import hashpw
from bcrypt import gensalt


def etag(object: Any) -> str:
    return xxh128(str(object)).digest().hex()


def password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt())
