from .singleton import Singleton


async def test_init_once() -> None:
    class Implementation(metaclass=Singleton):
        counter = 0

        def __init__(self) -> None:
            Implementation.counter += 1

    implementation = Implementation()
    implementations = [
        Implementation(),
        Implementation(),
    ]
    assert all((instance is implementation for instance in implementations)) is True
    assert Implementation.counter == 1
