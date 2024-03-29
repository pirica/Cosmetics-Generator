class Error(Exception):
    pass


class NoDigit(Error):
    def __init__(self, message='[ERROR] No numbers provided') -> None:
        self.message = message
        super().__init__(self.message)
