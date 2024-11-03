from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from .operations import Users
from .operations import Password
from .operations import Emails
from .operations import Sessions
from .operations import Codes


class Client:
    _session: AsyncSession
    users: Users
    emails: Emails
    passwords: Password
    sessions: Sessions
    codes: Codes

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = Users(session)
        self.emails = Emails(session)
        self.passwords = Password(session)
        self.sessions = Sessions(session)
        self.codes = Codes(session)

    def transaction(self) -> AsyncSessionTransaction:
        return self._session.begin()
