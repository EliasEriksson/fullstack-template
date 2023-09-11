class Meta(type):
    def __iter__(cls):
        return (getattr(cls, key) for key in cls.__dict__ if not key.startswith("_"))


class Iterable(metaclass=Meta):
    def __iter__(self):
        return (getattr(self, key) for key in self.__dir__() if not key.startswith("_"))
