from configuration import Configuration


class Services:
    _configuration: Configuration

    def __init__(self) -> None:
        self._configuration = Configuration()
