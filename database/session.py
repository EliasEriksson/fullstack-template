from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from .operations import Users
from .operations import Passwords
from .operations import Emails
from .operations import Sessions


class Session:
    _session: AsyncSession
    users: Users
    emails: Emails
    passwords: Passwords
    sessions: Sessions

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = Users(self._session)
        self.emails = Emails(self._session)
        self.passwords = Passwords(self._session)
        self.sessions = Sessions(self._session)

    def transaction(self) -> AsyncSessionTransaction:
        return self._session.begin()
