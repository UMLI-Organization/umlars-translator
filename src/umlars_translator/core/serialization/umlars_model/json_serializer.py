import json

from src.umlars_translator.core.serialization.abstract.serializer import UmlSerializer
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlElement, UmlClass, UmlAttribute, UmlAssociation, UmlAssociationEnd
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel

from dataclass_wizard import asdict



class JSONUmlSerializer(UmlSerializer):
    INDENT = 4

    def serialize(self, model: UmlModel) -> str:
        return model.accept(self)

    def visit_uml_element(self, uml_element: UmlElement) -> str:
        return json.dumps(asdict(uml_element), indent=self.__class__.INDENT)

    def visit_uml_model(self, model: UmlModel) -> str:
        return model.to_dict(indent=self.__class__.INDENT, exclude=['builder'])
        return model.to_json(indent=self.__class__.INDENT, exclude=['builder'])
    
    def visit_class(self, class_: UmlClass) -> str:
        raise NotImplementedError
    
    def visit_attribute(self, attribute: UmlAttribute) -> str:
        raise NotImplementedError
    
    def visit_association(self, association: UmlAssociation) -> str:
        raise NotImplementedError
    
    def visit_association_end(self, association_end: UmlAssociationEnd) -> str:
        raise NotImplementedError