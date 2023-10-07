from litestar.exceptions import ClientException


class TokenException(Exception):
    pass


class TokenDecodeException(TokenException):
    pass


class TokenEncodeException(TokenException):
    pass


class ForbiddenException(ClientException):
    status_code = 403


class PreconditionFailedException(ClientException):
    status_code = 412
