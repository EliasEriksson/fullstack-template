from .email import Email


class Local(Email):
    def __init__(self):
        ...

    @classmethod
    def name(cls) -> str:
        return "local"

    async def send_text(self, text: str) -> None:
        print(text)
