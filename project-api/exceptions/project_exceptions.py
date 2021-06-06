class ProjectAlreadyExistsException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class ProjectNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
