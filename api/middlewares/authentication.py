from __future__ import annotations
from abc import ABC, abstractmethod
import re
import math
from datetime import datetime
from datetime import timezone
from base64 import b64decode
from litestar.datastructures.url import URL
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection
from litestar.middleware import AuthenticationResult
from litestar.middleware import AbstractAuthenticationMiddleware
from api.database import Database
from api.database import models
from api.exceptions import ForbiddenException
from api import schemas
from api.headers import Headers


class Strategy(ABC):
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    @abstractmethod
    def processable(cls, authorization: str) -> bool: ...

    @classmethod
    @abstractmethod
    def scheme(cls) -> str: ...

    @abstractmethod
    async def authenticate_request(
        self, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult: ...


class Authentication(AbstractAuthenticationMiddleware):
    strategies: list[Strategy]

    def __init__(self, *strategies: list[Strategy], **kwargs) -> None:
        self.strategies = strategies or []
        super().__init__(**kwargs)

    def not_authorized(self, url: URL) -> NotAuthorizedException:
        return NotAuthorizedException(
            headers={
                Headers.www_authenticate: "; ".join(
                    f"{scheme} realm={url}"
                    for scheme in {strategy.scheme() for strategy in self.strategies}
                )
                + "; charset=utf-8",
                Headers.content_type: "application/json; charset=utf-8",
            }
        )

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        authorization = connection.headers.get(Headers.authorization)
        for strategy in self.strategies:
            if strategy.processable(authorization):
                try:
                    return await strategy.authenticate_request(
                        connection, authorization
                    )
                except NotAuthorizedException as error:
                    raise self.not_authorized(connection.url) from error
        raise self.not_authorized(connection.url)


class JwtAuthentication(Strategy):
    authorization = re.compile(r"^Bearer\s((?:ey[\w+=/-]+\.){2}[\w+=/-]+)$")
    secure: bool

    def __init__(self, secure: bool = True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.secure = secure

    @classmethod
    def processable(cls, authorization: str) -> bool:
        return cls.authorization.match(authorization) is not None

    @classmethod
    def scheme(cls) -> str:
        return "Token"

    async def authenticate_request(
        self, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        if not (match := self.authorization.match(authorization)):
            raise NotAuthorizedException()
        if not (jwt := match.group(1)):
            raise NotAuthorizedException()
        try:
            token = schemas.token.Token.decode(jwt, connection.url.hostname)
        except schemas.token.exceptions.TokenDecodeException as error:
            raise NotAuthorizedException() from error
        if self.secure and not token.secure:
            raise ForbiddenException(
                f"Your user might not have a password yet. Create a password, reauthenticate and try again."
            )
        async with Database() as client:
            async with client.transaction():
                session = await client.sessions.fetch_by_id(token.session)
            if not session or session.expire < datetime.now(timezone.utc):
                raise NotAuthorizedException()
            agent = connection.headers.get(Headers.user_agent)
            if session.host != connection.client.host or session.agent != agent:
                raise NotAuthorizedException()
            async with client.transaction():
                session.refresh()
        return AuthenticationResult(user=session.user, auth=token)


class PasswordAuthentication(Strategy):
    authorization = re.compile(r"^Basic\s(.*)$")
    credentials = re.compile(r"^([^:]+):?(.*)$")

    @classmethod
    def processable(cls, authorization: str) -> bool:
        return cls.authorization.match(authorization) is not None

    @classmethod
    def scheme(cls) -> str:
        return "Basic"

    async def authenticate_request(
        self, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        if not (match := self.authorization.match(authorization)):
            raise NotAuthorizedException()
        if not (encodedCredentials := match.group(1)):
            raise NotAuthorizedException()
        credentials = b64decode(encodedCredentials).decode("utf-8")
        if not (match := self.credentials.match(credentials)):
            raise NotAuthorizedException()
        if not (email := match.group(1)) or not (password := match.group(2)):
            raise NotAuthorizedException()
        async with Database() as client:
            async with client.transaction():
                email = await client.emails.fetch_by_address(email)
            if not email:
                raise NotAuthorizedException()
            for password_model in email.user.passwords:
                if password_model.verify(password):
                    return AuthenticationResult(user=email.user, auth=email)
        raise NotAuthorizedException()


class OtacAuthentication(Strategy):
    authorization = re.compile(
        rf"Bearer\s([\w\-+/=]{'{'}{math.ceil(models.Code.size * 4 / 3)}{'}'})", re.ASCII
    )

    @classmethod
    def processable(cls, authorization: str) -> bool:
        return cls.authorization.match(authorization) is not None

    @classmethod
    def scheme(cls) -> str:
        return "Token"

    async def authenticate_request(
        self, connection: ASGIConnection, authorization: str
    ) -> AuthenticationResult:
        if not (match := self.authorization.match(authorization)):
            raise NotAuthorizedException()
        if not (token := match.group(1)):
            raise NotAuthorizedException()
        async with Database() as client:
            async with client.transaction():
                code = await client.codes.fetch_by_token(token)
            if not code:
                raise NotAuthorizedException()
            async with client.transaction():
                code.email.verified = True
                await client.passwords.invalidate_by_email(code.email.address)
                await client.codes.delete_by_user_id(code.email.user_id)
        return AuthenticationResult(user=code.email.user, auth=code)
