from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from .users import Users


class Session:
    _session: AsyncSession
    users: Users

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = Users(self._session)

    def transaction(self) -> AsyncSessionTransaction:
        return self._session.begin()
