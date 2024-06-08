from typing import NamedTuple, Optional
from abc import ABC, abstractmethod


class FormatElementType(NamedTuple):
    """
    Named tuple is used so that the iteration step element type can be used as a key in a dictionary. 
    """
    element_type_name: str
    element_context: Optional["FormatElementType"] = None



class FormatElement(ABC):
    def __init__(self, element_data: dict, type: int):
        self.element_data: dict = element_data
        self.type: str = type


example_config = {

}


supported_elements = [ 
    FormatElementType("uml::Class", element_context=FormatElementType("uml::Package")),
]