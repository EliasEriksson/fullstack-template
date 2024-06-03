from __future__ import annotations
from typing import *
from abc import ABC, abstractmethod
import re
from itertools import chain
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
from api.headers import Headers


class AbstractAuthentication(AbstractAuthenticationMiddleware, ABC):
    @classmethod
    def not_authorized(cls, url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={
                Headers.www_authenticate: ", ".join(
                    challenge for challenge in cls.challenges(url)
                ),
                Headers.content_type: "application/json; charset=utf-8",
            },
        )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(Headers.authorization)
        if not authorization:
            raise self.not_authorized(connection.url)
        return await self.authenticate(connection, authorization)

    @classmethod
    @abstractmethod
    async def authenticate(
        cls,
        connection: ASGIConnection,
        authorization: str,
    ) -> AuthenticationResult: ...

    @staticmethod
    @abstractmethod
    def challenges(url: URL) -> Iterable[str]: ...


class PasswordAuthentication(AbstractAuthentication):
    pattern = re.compile(r"^Basic\s(.*)$")
    _credentialsPattern = re.compile(r"^([^:]+):?(.*)$")

    @classmethod
    async def authenticate(
        cls, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        if not (match := cls.pattern.match(authorization)):
            raise cls.not_authorized(connection.url)
        if not (encodedCredentials := match.group(1)):
            raise cls.not_authorized(connection.url)
        credentials = b64decode(encodedCredentials).decode("utf-8")
        if not (match := cls._credentialsPattern.match(credentials)):
            raise cls.not_authorized(connection.url)
        if not (email := match.group(1)) or not (password := match.group(2)):
            raise cls.not_authorized(connection.url)
        async with Database() as client:
            async with client.transaction():
                user = await client.users.fetch_by_email(email)
        if not user:
            raise cls.not_authorized(connection.url)
        for user_password in user.passwords:
            if user_password.verify(password):
                return AuthenticationResult(user=user, auth=None)
        raise cls.not_authorized(connection.url)

    @staticmethod
    def challenges(url: URL) -> Iterable[str]:
        return [f'Basic realm="{url.hostname}"']


class OtacTokenAuthentication(AbstractAuthentication):
    pattern = re.compile(
        rf"Bearer\s([\w\-+/=]{'{'}{math.ceil(models.Code.size * 4 / 3)}{'}'})", re.ASCII
    )

    @classmethod
    async def authenticate(
        cls, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        if not (match := cls.pattern.match(authorization)):
            raise cls.not_authorized(connection.url)
        if not (token := match.group(1)):
            raise cls.not_authorized(connection.url)
        async with Database() as client:
            async with client.transaction():
                code = await client.codes.fetch_by_token(token)
            if not code:
                raise cls.not_authorized(connection.url)
            async with client.transaction():
                code.email.verified = True
                await client.passwords.invalidate_by_email(code.email.address)
                await client.codes.delete_by_user_id(code.email.user.id)
        return AuthenticationResult(user=code.email.user, auth=code)

    @staticmethod
    def challenges(url: URL) -> Iterable[str]:
        return [f'Bearer realm="{url.hostname}"']


class JwtTokenAuthentication(AbstractAuthentication):
    pattern = re.compile(
        r"^Bearer\s((?:ey\w+\.){2}\w+)$",
    )

    @classmethod
    async def authenticate(
        cls, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        if not (match := cls.pattern.match(authorization)):
            raise cls.not_authorized(connection.url)
        if not (jwt := match.group(1)):
            raise cls.not_authorized(connection.url)
        try:
            token = schemas.token.Token.decode(jwt, connection.base_url)
        except schemas.token.exceptions.TokenDecodeException as error:
            raise cls.not_authorized(connection.url) from error
        async with Database() as client:
            async with client.transaction():
                session = await client.sessions.fetch_by_id(token.session)
        if not session:
            raise cls.not_authorized(connection.url)
        if session.expire < datetime.now():
            raise cls.not_authorized(connection.url)
        return AuthenticationResult(user=session.user, auth=token)

    @staticmethod
    def challenges(url: URL) -> Iterable[str]:
        return [f'Bearer realm="{url.hostname}"']


class AnyAuthentication(AbstractAuthentication):
    @classmethod
    async def authenticate(
        cls, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        strategies = [
            PasswordAuthentication,
            OtacTokenAuthentication,
            JwtTokenAuthentication,
        ]
        for strategy in strategies:
            try:
                return await strategy.authenticate(connection, authorization)
            except NotAuthorizedException:
                pass
        raise cls.not_authorized(connection.url)

    @staticmethod
    def challenges(url: URL) -> Iterable[str]:
        return chain(
            JwtTokenAuthentication.challenges(url),
            PasswordAuthentication.challenges(url),
            OtacTokenAuthentication.challenges(url),
        )
