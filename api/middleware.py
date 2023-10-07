from __future__ import annotations
from abc import ABC
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware
from litestar.middleware import AuthenticationResult
from database import Database
from .schemas import Token
from .exceptions import TokenDecodeException
from base64 import b64decode
import re


class AbstractAuthentication(AbstractAuthenticationMiddleware, ABC):
    header = "Authorization"


class BearerAuthentication(AbstractAuthentication):
    _authorizationPattern = re.compile(r"^Bearer\s(.*)$")

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(self.header)
        if not authorization:
            raise NotAuthorizedException()
        if not (match := self._authorizationPattern.search(authorization)):
            raise NotAuthorizedException()
        if not (jwt := match.group(1)):
            raise NotAuthorizedException()
        try:
            token = Token.decode(jwt)
        except TokenDecodeException:
            raise NotAuthorizedException()
        async with Database() as session:
            async with session.transaction():
                user = await session.users.fetch(token.sub)
        if not user:
            raise NotAuthorizedException()
        return AuthenticationResult(user=user, auth=token)


class BasicAuthentication(AbstractAuthentication):
    _authorizationPattern = re.compile(r"^Basic\s(.*)$")
    _credentialsPattern = re.compile(r"^([^:]*):([^:]*)$")

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(self.header)
        if not authorization:
            # add www-authenticate header to response. Is this done in route handler? security kwarg?
            raise NotAuthorizedException()
        if not (match := self._authorizationPattern.search(authorization)):
            raise NotAuthorizedException()
        if not (encodedCredentials := match.group(1)):
            raise NotAuthorizedException()
        credentials = b64decode(encodedCredentials).decode("utf-8")
        if not (match := self._credentialsPattern.search(credentials)):
            raise NotAuthorizedException()
        if not (email := match.group(1)) or not (password := match.group(2)):
            raise NotAuthorizedException()
        async with Database() as session:
            async with session.transaction():
                users, _ = await session.users.list([email], size=1, page=0)
        if not users or not (user := users[0]):
            raise NotAuthorizedException()
        if not user.verify(password):
            raise NotAuthorizedException()
        return AuthenticationResult(user=user, auth=None)
