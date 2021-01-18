# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class FieldTypeError(Error):
    """Raise when a field is not of the right type"""
    pass


class FieldTooShort(Error):
    """Raise when a field is too short"""
    pass