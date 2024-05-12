from abc import ABC
from shared import dependency


async def test_registry() -> None:
    class Email(dependency.Dependency, ABC):
        pass

    class EmailImplementation(Email):
        @classmethod
        def name(cls) -> str:
            return "email-implementation"

    class GoogleImplementation(Email):
        @classmethod
        def name(cls) -> str:
            return "google-implementation"

    class Phone(dependency.Dependency, ABC):
        pass

    class PhoneImplementation(Phone):
        @classmethod
        def name(cls) -> str:
            return "phone-implementation"

    assert len(Email._registry) == 2
    assert len(Phone._registry) == 1
    assert len(EmailImplementation._registry) == 2
    assert len(PhoneImplementation._registry) == 1


async def test_instantiation() -> None:
    class Email(dependency.Dependency, ABC):
        pass

    class Local(Email):
        @classmethod
        def name(cls) -> str:
            return "local"

    assert isinstance(Email.create("local"), Local)
    try:
        Email.create("does-not-exist")
    except dependency.exceptions.DependencyNotFoundError:
        pass
