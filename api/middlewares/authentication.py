from __future__ import annotations
from typing import *
from abc import ABC, abstractmethod
import re
import math
from base64 import b64decode
from litestar.datastructures.url import URL
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AuthenticationResult
from litestar.middleware import AbstractAuthenticationMiddleware
from database import Database
from database import models
from api import schemas
from datetime import datetime
from datetime import timedelta


class AbstractAuthentication(AbstractAuthenticationMiddleware, ABC):
    header = "Authorization"

    @staticmethod
    @abstractmethod
    def _not_authorized(url: URL) -> NotAuthorizedException: ...

    @abstractmethod
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult: ...


class BasicAuthentication(AbstractAuthentication):
    _authorizationPattern = re.compile(r"^Basic\s(.*)$")
    _credentialsPattern = re.compile(r"^([^:]+):?(.*)$")

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
        async with Database() as client:
            async with client.transaction():
                user = await client.users.fetch_by_email(email)
        if not user:
            raise self._not_authorized(connection.url)
        for user_password in user.passwords:
            if user_password.verify(password):
                return AuthenticationResult(user=user, auth=None)
        raise self._not_authorized(connection.url)

    @staticmethod
    def _not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Basic realm="{url.hostname}"'},
        )


class OtacTokenAuthentication(AbstractAuthentication):
    _pattern = re.compile(
        rf"Bearer\s([\w\-+/=]{'{'}{math.ceil(models.Code.size * 4 / 3)}{'}'})", re.ASCII
    )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        print("Otac token authentication")
        authorization = connection.headers.get(self.header)
        if not authorization:
            raise self._not_authorized(connection.url)
        print("authorization", authorization)
        if not (match := self._pattern.match(authorization)):
            raise self._not_authorized(connection.url)
        print("match", match)
        if not (token := match.group(1)):
            raise self._not_authorized(connection.url)
        print("token", token)
        async with Database() as client:
            async with client.transaction():
                code = await client.codes.fetch_by_token(token)
        print("code", code)
        if not code:
            raise self._not_authorized(connection.url)
        return AuthenticationResult(user=code.email.user, auth=code)

    @staticmethod
    def _not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Bearer realm="{url.hostname}"'},
        )


class JwtTokenAuthentication(AbstractAuthentication):
    _pattern = re.compile(
        r"^Bearer\s((?:ey\w+\.){2}\w+)$",
    )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(self.header)
        if not authorization:
            raise self._not_authorized(connection.url)
        if not (match := self._pattern.match(authorization)):
            raise self._not_authorized(connection.url)
        if not (jwt := match.group(1)):
            raise self._not_authorized(connection.url)
        try:
            token = schemas.token.Token.decode(jwt, connection.base_url)
        except schemas.token.exceptions.TokenDecodeException as error:
            raise self._not_authorized(connection.url) from error
        async with Database() as client:
            async with client.transaction():
                session = await client.sessions.fetch_by_id(token.session)
        if not session:
            raise self._not_authorized(connection.url)
        if session.expire < datetime.now():
            raise self._not_authorized(connection.url)
        return session.user

    @staticmethod
    def _not_authorized(url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={f"WWW-Authenticate": f'Bearer realm="{url.hostname}"'},
        )
