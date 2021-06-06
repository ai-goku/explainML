class TenantIDMissingException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class InvalidTenantIDException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

