from litestar import Controller as LitestarController


class Controller(LitestarController):
    path = "/refresh"
