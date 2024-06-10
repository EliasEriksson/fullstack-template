from .email import Email


class Local(Email):
    @classmethod
    def name(cls) -> str:
        return "local"

    async def send_text(self, recipient: str, subject: str, text: str) -> None:
        print(f"Mail to: {recipient}\n{subject}\n{text}\n")
