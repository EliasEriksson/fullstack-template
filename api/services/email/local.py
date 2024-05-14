from .email import Email


class Local(Email):
    @classmethod
    def name(cls) -> str:
        return "local"

    def send_text(self, text: str) -> None:
        print(text)
