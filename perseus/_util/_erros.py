class APIError(Exception):
    pass

class APIReturnError(APIError):
    pass

class APIConnectionError(APIError):
    pass

class APIPathNotFoundError(APIError):
    pass