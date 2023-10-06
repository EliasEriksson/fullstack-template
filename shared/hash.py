from __future__ import annotations
from typing import *
from xxhash import xxh128


def hash(object: Any) -> str:
    return xxh128(str(object)).digest().hex()
