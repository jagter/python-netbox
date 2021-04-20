class GeneralException(BaseException):
    def __init__(self, resp_data):
        if isinstance(resp_data, dict):
            if 'detail' in resp_data:
                self.err = resp_data['detail']
            else:
                self.err = ''.join('{} '.format(val[0]) for key, val in resp_data.items())
        else:
            self.err = 'Unknown Error, please check the Netbox logs'

    def __str__(self):
        return '{}'.format(self.err)


class DeleteException(GeneralException):
    """Raised when delete failed"""
    def __init__(self, resp_data):
        super().__init__(resp_data)


class NotFoundException(GeneralException):
    """Raised when item is not found"""
    def __init__(self, resp_data):
        super().__init__(resp_data)


class GetException(GeneralException):
    pass


class CreateException(GeneralException):
    """Raised when creation failed"""
    def __init__(self, resp_data):
        super().__init__(resp_data)


class UpdateException(BaseException):
    """Raised when an object update fails"""
    def __init__(self, resp_data):
        super().__init__(resp_data)


class AuthException(BaseException):
    """Raised when an API call method is not allowed"""
    pass


class AuthorizationException(GeneralException):
    """HTTP 403 status code"""
    def __init__(self, resp_data):
        super().__init__(resp_data)


class ClientException(GeneralException):
    """HTTP 400 status code"""
    def __init__(self, resp_data):
        super().__init__(resp_data)


class ServerException(GeneralException):
    """HTTP 5xx status code"""
    def __init__(self, resp_data):
        super().__init__(resp_data)
