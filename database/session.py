from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from sqlalchemy import Select
from sqlalchemy import Result
from .users import Users
from .emails import Emails
from .sessions import Sessions


class Session:
    _session: AsyncSession
    users: Users
    emails: Emails
    sessions: Sessions

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = Users(self._session)
        self.emails = Emails(self._session)
        self.sessions = Sessions(self._session)

    def transaction(self) -> AsyncSessionTransaction:
        return self._session.begin()

    async def commit(self) -> None:
        await self._session.commit()

    async def execute(self, query: Select) -> Result:
        return await self._session.execute(query)
