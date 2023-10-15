from __future__ import annotations
from abc import ABC
from litestar.datastructures.url import URL
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware
from litestar.middleware import AuthenticationResult
from database import Database
from api.routes.auth.schemas.token import Token
from .exceptions import TokenDecodeException
from base64 import b64decode
import re


class AbstractAuthentication(AbstractAuthenticationMiddleware, ABC):
    header = "Authorization"


class BearerAuthentication(AbstractAuthentication):
    _authorizationPattern = re.compile(r"^Bearer\s(.*)$")

    @staticmethod
    def not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Bearer realm="{url.hostname}"'}
        )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(self.header)
        if not authorization:
            raise self.not_authorized(connection.url)
        if not (match := self._authorizationPattern.search(authorization)):
            raise self.not_authorized(connection.url)
        if not (jwt := match.group(1)):
            raise self.not_authorized(connection.url)
        try:
            token = Token.decode(jwt, connection.base_url)
        except TokenDecodeException:
            raise self.not_authorized(connection.url)
        async with Database() as session:
            async with session.transaction():
                user = await session.users.fetch(token.subject)
        if not user:
            raise self.not_authorized(connection.url)
        return AuthenticationResult(user=user, auth=token)


class BasicAuthentication(AbstractAuthentication):
    _authorizationPattern = re.compile(r"^Basic\s(.*)$")
    _credentialsPattern = re.compile(r"^([^:]*):([^:]*)$")

    @staticmethod
    def not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Basic realm="{url.hostname}"'}
        )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(self.header)
        if not authorization:
            raise self.not_authorized(connection.url)
        if not (match := self._authorizationPattern.search(authorization)):
            raise self.not_authorized(connection.url)
        if not (encodedCredentials := match.group(1)):
            raise self.not_authorized(connection.url)
        credentials = b64decode(encodedCredentials).decode("utf-8")
        if not (match := self._credentialsPattern.search(credentials)):
            raise self.not_authorized(connection.url)
        if not (email := match.group(1)) or not (password := match.group(2)):
            raise self.not_authorized(connection.url)
        async with Database() as session:
            async with session.transaction():
                users, _ = await session.users.list([email], size=1, page=0)
        if not users or not (user := users[0]):
            raise self.not_authorized(connection.url)
        if not user.verify(password):
            raise self.not_authorized(connection.url)
        return AuthenticationResult(user=user, auth=None)
