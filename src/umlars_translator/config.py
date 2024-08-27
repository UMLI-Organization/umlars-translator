from enum import Enum
import os


class SupportedFormat(Enum):
    """
    Each supported format is mapped to its string representation.
    """

    XMI_EA = "xmi-ea"
    UML_PAPYRUS = "uml-papyrus"
    NOTATION_PAPYRUS = "notation-papyrus"
    MDJ_STARTUML = "mdj_staruml"
    UNKNOWN = "unknown"


"""
Base logger settings
"""
SYSTEM_NAME = "UMLARS"
LOGGER_BASE_NAME = SYSTEM_NAME

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE = os.getenv("LOG_FILE", "logs/umlars.log")
