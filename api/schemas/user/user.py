from __future__ import annotations
from typing import *
from .. import password
from .. import base


class UserProtocol(base.BaseProtocol, Protocol):
    email: str
    password: password.PasswordProtocol


class User(base.Base):
    email: str
    password: password.PasswordProtocol
