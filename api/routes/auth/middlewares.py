from __future__ import annotations
from abc import ABC
from litestar.datastructures.url import URL
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware
from litestar.middleware import AuthenticationResult
from api.routes.auth.schemas.token import Token
from base64 import b64decode
import re
from .exceptions import TokenDecodeException
from database import Database
from database import models
from uuid import UUID


class AbstractAuthentication(AbstractAuthenticationMiddleware, ABC):
    authorization = "Authorization"
    user_agent = "User-Agent"


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
        authorization = connection.headers.get(self.authorization)
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
                user = await session.users.fetch_by_id(token.subject)
        if not user:
            raise self.not_authorized(connection.url)
        return AuthenticationResult(user=user, auth=token)


class BasicBase(AbstractAuthentication, ABC):
    _authorizationPattern = re.compile(r"^Basic\s(.*)$")
    _credentialsPattern = re.compile(r"^([^:]*):([^:]*)$")

    @staticmethod
    def not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Basic realm="{url.hostname}"'}
        )

    async def get_credentials(self, connection: ASGIConnection) -> tuple[str, str]:
        authorization = connection.headers.get(self.authorization)
        if not authorization:
            raise self.not_authorized(connection.url)
        if not (match := self._authorizationPattern.search(authorization)):
            raise self.not_authorized(connection.url)
        if not (encodedCredentials := match.group(1)):
            raise self.not_authorized(connection.url)
        credentials = b64decode(encodedCredentials).decode("utf-8")
        if not (match := self._credentialsPattern.search(credentials)):
            raise self.not_authorized(connection.url)
        if not (username := match.group(1)) or not (secret := match.group(2)):
            raise self.not_authorized(connection.url)
        return username, secret


class BasicUserRefreshTokenAuthentication(BasicBase):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        user_id, token = await self.get_credentials(connection)
        async with Database() as session:
            user_session = await session.sessions.fetch(
                connection.client.host, connection.headers.get(self.user_agent) or ""
            )
            if not user_session.verify(user_id, token):
                raise self.not_authorized(connection.url)
            user = await session.users.fetch_by_id(UUID(user_id))
        if not user:
            raise self.not_authorized(connection.url)
        return AuthenticationResult(user=user, auth=None)


class BasicUsernamePasswordAuthentication(BasicBase):
    async def authenticate_request(
        self,
        connection: ASGIConnection,
    ) -> AuthenticationResult:
        address, password = await self.get_credentials(connection)
        async with Database() as session:
            user = await session.users.fetch_by_email(address)
        if not user:
            raise self.not_authorized(connection.url)
        if not user.verify(password):
            raise self.not_authorized(connection.url)
        if not any(
            (
                email.address == address and email.verification.completed
                for email in user.emails
            )
        ):
            raise self.not_authorized(connection.url)
        return AuthenticationResult(user=user, auth=None)
