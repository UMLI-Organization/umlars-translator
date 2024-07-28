from enum import Enum
import os


class SupportedFormat(Enum):
    """
    Each supported format is mapped to its string representation.
    """

    XMI_EA = "xmi-ea"
    XMI_PAPYRUS = "xmi-papyrus"
    MDJ = "mdj"
    UNKNOWN = "unknown"


"""
Base logger settings
"""
SYSTEM_NAME = "UMLARS"
LOGGER_BASE_NAME = SYSTEM_NAME

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE = os.getenv("LOG_FILE", "logs/umlars.log")
