from __future__ import annotations
from .. import base


class UserProtocol(base.BaseProtocol):
    email: str


class User(base.Base, UserProtocol):
    def __init__(self, user: UserProtocol) -> None:
        super().__init__(user)
        self.email = user.email
