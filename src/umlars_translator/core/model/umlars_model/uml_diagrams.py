from typing import TYPE_CHECKING, List, Union

from src.umlars_translator.core.model.umlars_model.uml_elements import UmlElement, UmlLifeline, UmlClass, UmlAssociationEnd, UmlAssociationBase, UmlInterface, UmlPackage, UmlPrimitiveType, UmlAttribute, UmlOperation, UmlLifeline, UmlAssociationEnd, UmlAssociation, UmlAggregation, UmlComposition, UmlDependency, UmlRealization, UmlGeneralization, UmlMessage, UmlCombinedFragment, UmlDataType, UmlEnumeration, UmlPrimitiveType, UmlInteraction, UmlOccurrenceSpecification, UmlModelElements, UmlParameter, UmlOperand
from src.umlars_translator.core.model.abstract.uml_diagrams import IUmlDiagram, IUmlClassDiagram, IUmlSequenceDiagram, IUmlClassDiagramElements, IUmlSequenceDiagramElements, IUmlDiagrams
from src.umlars_translator.core.model.umlars_model.mixins import RegisteredInModelMixin
if TYPE_CHECKING:
    from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel


class UmlDiagram(RegisteredInModelMixin, IUmlDiagram):
    def __init__(self, name: str, model: 'UmlModel', id: str = None, **kwargs):
        super().__init__(id=id, model=model, **kwargs)
        self.name = name

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlClass):
            self.classes.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.associations.append(element)
        elif isinstance(element, UmlInterface):
            self.interfaces.append(element)
        elif isinstance(element, UmlPackage):
            self.packages.append(element)
        elif isinstance(element, UmlPrimitiveType):
            self.primitive_types.append(element)
        elif isinstance(element, UmlAttribute):
            self.attributes.append(element)
        elif isinstance(element, UmlOperation):
            self.operations.append(element)
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlClassDiagram.")


class UmlClassDiagramElements(IUmlClassDiagramElements):
    def __init__(self, classes: List[UmlClass] = None, interfaces: List[UmlInterface] = None, data_types: List[UmlDataType] = None, enumerations: List[UmlEnumeration] = None, primitive_types: List[UmlPrimitiveType] = None, associations: List[Union[UmlAssociation, UmlAggregation, UmlComposition]] = None, generalizations: List[UmlGeneralization] = None, dependencies: List[UmlDependency] = None, realizations: List[UmlRealization] = None, aggregations: List[UmlAggregation] = None, compositions: List[UmlComposition] = None, attributes: List[UmlAttribute] = None, operations: List[UmlOperation] = None, **kwargs):
        self.classes = classes or []
        self.interfaces = interfaces or []
        self.data_types = data_types or []
        self.enumerations = enumerations or []
        self.primitive_types = primitive_types or []
        self.associations = associations or []
        self.generalizations = generalizations or []
        self.dependencies = dependencies or []
        self.realizations = realizations or []
        self.aggregations = aggregations or []
        self.compositions = compositions or []
        self.attributes = attributes or []
        self.operations = operations or []
        super().__init__(**kwargs)

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlClass):
            self.classes.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.associations.append(element)
        elif isinstance(element, UmlInterface):
            self.interfaces.append(element)
        elif isinstance(element, UmlPackage):
            self.packages.append(element)
        elif isinstance(element, UmlPrimitiveType):
            self.primitive_types.append(element)
        elif isinstance(element, UmlAttribute):
            self.attributes.append(element)
        elif isinstance(element, UmlOperation):
            self.operations.append(element)
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlClassDiagram.")


class UmlSequenceDiagramElements(IUmlSequenceDiagramElements):
    def __init__(self, interactions: List[UmlInteraction] = None, **kwargs):
        self.interactions = interactions or []
        super().__init__(**kwargs)

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlInteraction):
            self.interactions.append(element)
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlSequenceDiagram.")


class UmlClassDiagram(UmlDiagram, IUmlClassDiagram):
    def __init__(self, name: str, model: 'UmlModel', id: str = None, **kwargs):
        super().__init__(name=name, model=model, id=id, **kwargs)
        self.elements = UmlClassDiagramElements(**kwargs)


class UmlSequenceDiagram(UmlDiagram, IUmlSequenceDiagram):
    def __init__(self, name: str, model: 'UmlModel', id: str = None, **kwargs):
        super().__init__(name=name, model=model, id=id, **kwargs)
        self.elements = UmlSequenceDiagramElements(**kwargs)


class UmlDiagrams(IUmlDiagrams):
    def __init__(self, class_diagrams: List[UmlClassDiagram] = None, sequence_diagrams: List[UmlSequenceDiagram] = None, **kwargs):
        self.class_diagrams = class_diagrams or []
        self.sequence_diagrams = sequence_diagrams or []
        super().__init__(**kwargs)

    def add_element(self, element: UmlElement) -> 'UmlDiagrams':
        if isinstance(element, UmlClassDiagram):
            self.class_diagrams.append(element)
        elif isinstance(element, UmlSequenceDiagram):
            self.sequence_diagrams.append(element)
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlDiagrams.")
        
        return self
    
    @property
    def class_diagrams(self) -> List[UmlClassDiagram]:
        return self._class_diagrams
    
    @class_diagrams.setter
    def class_diagrams(self, new_class_diagrams: List[UmlClassDiagram]):
        self._class_diagrams = new_class_diagrams
        if self._class_diagrams and self.builder:
            for class_diagram in self._class_diagrams:
                self.builder.add_diagram(class_diagram)

    @property
    def sequence_diagrams(self) -> List[UmlSequenceDiagram]:
        return self._sequence_diagrams
    
    @sequence_diagrams.setter
    def sequence_diagrams(self, new_sequence_diagrams: List[UmlSequenceDiagram]):
        self._sequence_diagrams = new_sequence_diagrams
        if self._sequence_diagrams and self.builder:
            for sequence_diagram in self._sequence_diagrams:
                self.builder.add_diagram(sequence_diagram)
                