from litestar.exceptions import ClientException


class ForbiddenException(ClientException):
    status_code = 403


class PreconditionFailedException(ClientException):
    status_code = 412
