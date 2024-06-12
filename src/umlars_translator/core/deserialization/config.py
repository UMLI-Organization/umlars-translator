from enum import Enum


class SupportedFormat(Enum):
    """
    Each supported format is mapped to its string representation.
    """
    XMI_EA = "xmi-ea"
    XMI_PAPYRUS = "xmi-papyrus"
    XMI_GENMYMODEL = "xmi-genmymodel"
    MDJ = "mdj"

"""
Extensions settings
"""
EXTENSIONS_BASE_DIRS = ["src/umlars_translator/core/deserialization/formats"]
