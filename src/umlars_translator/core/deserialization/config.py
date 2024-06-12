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
DESERIALIZATION_EXTENSIONS_GROUP_NAME = [
    "umlars_translator.core.deserialization.abstract.base.deserialization_strategy"
]
