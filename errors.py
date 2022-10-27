class ApiError(Exception):
    @property
    def status(self):
        raise NotImplementedError


class Api404Error(ApiError):

    @property
    def status(self):
        return 404


class Api422Error(ApiError):
    
    @property
    def status(self):
        return 422