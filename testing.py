class IterableMeta(type):
    def __iter__(cls):
        return (getattr(cls, key) for key in cls.__dict__ if not key.startswith("_"))


class Iterable(metaclass=IterableMeta):
    def __iter__(self):
        return (getattr(self, key) for key in self.__dir__() if not key.startswith("_"))


class Variables(Iterable):
    username = "POSTGRES_USERNAME"
    password = "POSTGRES_PASSWORD"
    database = "POSTGRES_DATABASE"
    host = "POSTGRES_HOST"
    port = "POSTGRES_PORT"


if __name__ == "__main__":
    for v in Variables:
        print(v)
    variables = Variables()
    for v in variables:
        print(v)
