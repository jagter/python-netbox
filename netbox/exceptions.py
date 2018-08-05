class BaseExceptions(Exception):
    pass


class DeleteException(BaseException):
    """Raised when delete failed"""
    def __init__(self, resp_data):

        if isinstance(resp_data, dict):
            self.err = ''.join('Failed with reason {}'.format(val) for key, val in resp_data.items())
        else:
            self.err = 'Delete failed with an unknown reason'

    def __str__(self):
        return '{}'.format(self.err)


class NotFoundException(BaseException):
    """Raised when item is not found"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Unable to found {}'.format(self.msg)


class CreateException(BaseException):
    """Raised when creation failed"""
    def __init__(self, resp_data):

        if isinstance(resp_data, dict):
            self.err = ''.join('{} '.format(val[0]) for key, val in resp_data.items())
        else:
            self.err = 'Creation failed with unknown reason'

    def __str__(self):
        return '{}'.format(self.err)


class UpdateException(BaseException):
    """Raised when an object update fails"""
    def __init__(self, resp_data):
        if isinstance(resp_data, dict):
            self.err = ''.join('{} '.format(val[0]) for key, val in resp_data.items())
        else:
            self.err = 'Update failed with unknown reason'

    def __str__(self):
        return '{}'.format(self.err)


class AuthException(BaseException):
    """Raised when an API call method is not allowed"""
    pass
