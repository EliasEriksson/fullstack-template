from __future__ import annotations
from .. import password
from .. import base


class User(base.Base):
    email: str
    password: password.Password
