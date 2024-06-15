class InvalidFormatException(Exception):
    """
    Raised during parsing, when received format doesn't store the expected structure.
    """


class UnsupportedFormatException(Exception):
    """
    Raised when the format cannot be parsed in a chosen way, because it the expected format indicators couldn't be find or their values were invalid.
    """