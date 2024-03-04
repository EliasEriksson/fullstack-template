from __future__ import annotations


class AbstractSingletonInstanceError(Exception):
    pass


class Meta(type):
    """
    configuration metaclass

    works similar to a singleton but the instance is overwritten if args/kwargs are given
    is this a good idea? probably not but it makes it easy to test for now
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances or args or kwargs:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=Meta):
    pass
