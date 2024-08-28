from kink import inject

from src.umlars_translator.core.serialization.abstract.serializer import UmlSerializer
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlElement, UmlClass, UmlAttribute, UmlAssociation, UmlAssociationEnd, UmlModelElements
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
import src.umlars_translator.app.dtos.uml_model as pydantic_uml


@inject(alias=UmlSerializer)
class UmlToPydanticSerializer(UmlSerializer):
    def serialize(self, model: UmlModel) -> str:
        return model.accept(self)

    def visit_uml_element(self, uml_element: UmlElement) -> str:
        return pydantic_uml.UmlModel(**uml_element.__dict__).model_dump_json()

    def visit_uml_model(self, model: UmlModel) -> str:
        return pydantic_uml.UmlModel(name=model.name, id=model.id, elements=pydantic_uml.UmlModelElements(), diagrams=pydantic_uml.UmlDiagrams()).model_dump_json() 
    
    def visit_class(self, class_: UmlClass) -> str:
        raise NotImplementedError
    
    def visit_attribute(self, attribute: UmlAttribute) -> str:
        raise NotImplementedError
    
    def visit_association(self, association: UmlAssociation) -> str:
        raise NotImplementedError
    
    def visit_association_end(self, association_end: UmlAssociationEnd) -> str:
        raise NotImplementedError
