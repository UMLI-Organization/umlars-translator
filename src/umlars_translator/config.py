from enum import Enum
import os


class SupportedFormat(Enum):
    """
    Each supported format is mapped to its string representation.
    """

    XMI_EA = "xmi_ea"
    UML_PAPYRUS = "uml_papyrus"
    NOTATION_PAPYRUS = "notation_papyrus"
    MDJ_STARTUML = "mdj_staruml"
    UNKNOWN = "unknown"


"""
Base logger settings
"""
SYSTEM_NAME = "UMLARS"
LOGGER_BASE_NAME = SYSTEM_NAME

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")
LOG_FILE = os.getenv("LOG_FILE", "logs/umlars.log")
