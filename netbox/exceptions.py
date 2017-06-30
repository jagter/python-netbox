class BaseExceptions(Exception):
    pass


class DeleteException(BaseException):
    """Raised when delete failed"""
    pass


class NotFoundException(BaseException):
    """Raised when item is not found"""

    def __init__(self, item):
        self.item = item

    def __str__(self):
        return 'Unable to found {}'.format(self.item)


class CreateException(BaseException):
    """Raised when creation failed"""
    pass


class AuthException(BaseException):
    """Raised when an API call method is not allowed"""
    pass
