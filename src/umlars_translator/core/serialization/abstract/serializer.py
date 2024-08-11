from abc import abstractmethod

from src.umlars_translator.core.utils.visitor import IVisitor
from src.umlars_translator.core.model.abstract.uml_elements import IUmlElement, IUmlClass, IUmlAttribute, IUmlAssociation, IUmlAssociationEnd
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel


class UmlSerializer(IVisitor):
    @abstractmethod
    def visit_uml_element(self, uml_element: IUmlElement) -> str:
        ...

    @abstractmethod
    def visit_uml_model(self, model: IUmlModel) -> str:
        ...
    
    @abstractmethod
    def visit_class(self, class_: IUmlClass) -> str:
        ...
    
    @abstractmethod
    def visit_attribute(self, attribute: IUmlAttribute) -> str:
        ...
    
    @abstractmethod
    def visit_association(self, association: IUmlAssociation) -> str:
        ...
    
    @abstractmethod
    def visit_association_end(self, association_end: IUmlAssociationEnd) -> str:
        ...
