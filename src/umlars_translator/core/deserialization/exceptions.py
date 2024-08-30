class InvalidFormatException(Exception):
    """
    Raised during parsing, when received format doesn't store the expected structure.
    """


class UnsupportedFormatException(Exception):
    """
    Raised when the format cannot be parsed in a chosen way, because it the expected format indicators couldn't be find or their values were invalid.
    """


class ImproperlyInstantiatedObjectError(Exception):
    """
    Raised when one tries to call particular method on not fully or properly instantiated object.
    """


class UnableToMapError(Exception):
    """
    Raised when value mapping fails.
    """


class UnsupportedSourceDataTypeError(Exception):
    """
    Raised when the data source type is not supported by any deserialization strategy.
    """