from shared.dependency.exceptions import DependencyNotFoundError
from api.services.email import Email
from api.services.email.local import Local


async def test_registry() -> None:
    assert len(Email._registry) == 1

    class EmailImplementation(Email):

        async def send_text(self, recipient: str, subject: str, text: str) -> None:
            return

        @classmethod
        def name(cls) -> str:
            return "test-implementation"

    assert len(Email._registry) == 2
    assert EmailImplementation._registry is Email._registry


async def test_instantiation() -> None:
    assert isinstance(Email("local"), Local)
    try:
        Email("does-not-exist")
    except DependencyNotFoundError:
        pass
