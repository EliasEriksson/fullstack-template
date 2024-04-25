from __future__ import annotations
from abc import ABC
import re
from base64 import b64decode
from litestar.datastructures.url import URL
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware
from litestar.middleware import AuthenticationResult
from database import Database


class AbstractAuthentication(ABC):
    header = "Authorization"


class BasicAuthenticationMiddleware(AbstractAuthentication):
    _authorizationPattern = re.compile(r"^Basic\s(.*)$")
    _credentialsPattern = re.compile(r"^([^:]+):?(.*)$")

    @staticmethod
    def _not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Basic realm="{url.hostname}"'}
        )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(self.header)
        if not authorization:
            raise self._not_authorized(connection.url)
        if not (match := self._authorizationPattern.search(authorization)):
            raise self._not_authorized(connection.url)
        if not (encodedCredentials := match.group(1)):
            raise self._not_authorized(connection.url)
        credentials = b64decode(encodedCredentials).decode("utf-8")
        if not (match := self._credentialsPattern.search(credentials)):
            raise self._not_authorized(connection.url)
        if not (email := match.group(1)) or not (password := match.group(2)):
            raise self._not_authorized(connection.url)
        async with Database() as session:
            async with session.transaction():
                pass
        #         users, _ = await session.users.list([email], size=1, page=0)
        # if not users or not (user := users[0]):
        #     raise self._not_authorized(connection.url)
        # if not user.verify(password):
        #     raise self._not_authorized(connection.url)
        # return AuthenticationResult(user=user, auth=None)
