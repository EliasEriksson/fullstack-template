from __future__ import annotations
from abc import ABC
from litestar.datastructures.url import URL
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware
from litestar.middleware import AuthenticationResult
from .schemas.token import Token
from base64 import b64decode
import re
from .exceptions import TokenDecodeException
from database import Database
from database import models
from uuid import UUID
from dataclasses import dataclass


class AbstractAuthentication(AbstractAuthenticationMiddleware, ABC):
    authorization = "Authorization"
    user_agent = "User-Agent"


class BearerBase(AbstractAuthentication, ABC):
    _authorizationPattern = re.compile(r"^Bearer\s(.*)$")

    @staticmethod
    def not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Bearer realm="{url.hostname}"'}
        )

    async def get_token(self, connection: ASGIConnection) -> str:
        authorization = connection.headers.get(self.authorization)
        if not authorization:
            raise self.not_authorized(connection.url)
        if not (match := self._authorizationPattern.search(authorization)):
            raise self.not_authorized(connection.url)
        if not (token := match.group(1)):
            raise self.not_authorized(connection.url)
        return token


class BearerJwtAuthentication(BearerBase):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        jwt = await self.get_token(connection)
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


class BasicUsernamePasswordAuthentication(BasicBase):
    @dataclass
    class Scope:
        @dataclass
        class State:
            refresh_token = "refresh_token"

        state = "state"

    async def authenticate_request(
        self,
        connection: ASGIConnection,
    ) -> AuthenticationResult:
        address, password = await self.get_credentials(connection)
        agent = connection.headers.get(self.user_agent)
        host = connection.client.host
        async with Database() as session:
            async with session.transaction():
                user = await session.users.fetch_by_email(address)
                if not user:
                    raise self.not_authorized(connection.url)
                if not user.verify(password):
                    raise self.not_authorized(connection.url)
                email: models.Email | None = next(
                    (email for email in user.emails if email.address == address), None
                )
                if email is None:
                    raise self.not_authorized(connection.url)
                if not email.verification.completed:
                    raise self.not_authorized(connection.url)
                user_session: models.Session | None = next(
                    (
                        session
                        for session in user.sessions
                        if session.agent == agent and session.host == host
                    ),
                    None,
                )
                if user_session is None:
                    _, refresh_token = await session.sessions.create(
                        host, agent, user=user
                    )
                else:
                    refresh_token = user_session.regenerate()
        connection.scope[self.Scope.state][
            self.Scope.State.refresh_token
        ] = refresh_token
        return AuthenticationResult(user=user, auth=email)


class BasicUsernamePasswordVerificationAuthentication(BasicBase):
    @dataclass
    class Scope:
        @dataclass
        class State:
            refresh_token = "refresh_token"

        state = "state"

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        address, password = await self.get_credentials(connection)
        agent = connection.headers.get(self.user_agent)
        if agent is None:
            raise self.not_authorized(connection.url)
        host = connection.client.host
        async with Database() as session:
            async with session.transaction():
                user = await session.users.fetch_by_email(address)
                if not user:
                    raise self.not_authorized(connection.url)
                if not user.verify(password):
                    raise self.not_authorized(connection.url)
                email: models.Email | None = next(
                    (email for email in user.emails if email.address == address), None
                )
                if email.verification.completed:
                    raise self.not_authorized(connection.url)
                email.verification.completed = True
                _, refresh_token = await session.sessions.create(host, agent, user=user)
        connection.scope[self.Scope.state][
            self.Scope.State.refresh_token
        ] = refresh_token
        return AuthenticationResult(user=user, auth=email)


class BasicRefreshTokenAuthentication(BasicBase):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        user_id, refresh_token = await self.get_credentials(connection)
        agent = connection.headers.get(self.user_agent)
        if agent is None:
            raise self.not_authorized(connection.url)
        host = connection.client.host
        async with Database() as session:
            async with session.transaction():
                user = await session.users.fetch_by_id(UUID(user_id))
        user_session: models.Session | None = next(
            (
                session
                for session in user.sessions
                if session.agent == agent and session.host == host
            ),
            None,
        )
        if not user_session.verify(user.id, refresh_token):
            raise self.not_authorized(connection.url)
        return AuthenticationResult(user=user, auth=user_id)
