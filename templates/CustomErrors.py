class Error(Exception):
    """Base class for other exceptions"""
    pass


class FStackWrongInputTypeError(Error):
    """Raised when the input obj is not callable"""
    pass


class StateAccessError(Error):
    """Raised when the object of active state has been accessed"""
    pass
