from typing import TYPE_CHECKING, List, Union, Optional

from umlars_translator.core.model.abstract.uml_elements import IUmlElement
from umlars_translator.core.model.umlars_model.uml_elements import UmlElement, UmlLifeline, UmlClass, UmlAssociationEnd, UmlAssociationBase, UmlInterface, UmlPackage, UmlPrimitiveType, UmlAttribute, UmlOperation, UmlLifeline, UmlAssociationEnd, UmlAssociation, UmlAggregation, UmlComposition, UmlDependency, UmlRealization, UmlGeneralization, UmlMessage, UmlCombinedFragment, UmlDataType, UmlEnumeration, UmlPrimitiveType, UmlInteraction, UmlOccurrenceSpecification, UmlModelElements, UmlParameter, UmlOperand
from umlars_translator.core.model.abstract.uml_diagrams import IUmlDiagram, IUmlClassDiagram, IUmlSequenceDiagram, IUmlClassDiagramElements, IUmlSequenceDiagramElements, IUmlDiagrams
from umlars_translator.core.model.umlars_model.mixins import RegisteredInModelMixin
if TYPE_CHECKING:
    from umlars_translator.core.model.umlars_model.uml_model import UmlModel


class UmlDiagram(RegisteredInModelMixin, IUmlDiagram):
    def __init__(self, name: Optional[str] = None, description: str = None, model: Optional['UmlModel'] = None, id: str = None, **kwargs):
        super().__init__(id=id, model=model, **kwargs)
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, new_description: str):
        self._description = new_description


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

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlClass):
            self.classes.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.associations.append(element)
        elif isinstance(element, UmlInterface):
            self.interfaces.append(element)
        elif isinstance(element, UmlPrimitiveType):
            self.primitive_types.append(element)
        elif isinstance(element, UmlGeneralization):
            self.generalizations.append(element)
        elif isinstance(element, UmlDependency):
            self.dependencies.append(element)
        elif isinstance(element, UmlRealization):
            self.realizations.append(element)
        elif isinstance(element, UmlEnumeration):
            self.enumerations.append(element)
        elif isinstance(element, UmlDataType):
            self.data_types.append(element)
        elif isinstance(element, UmlAttribute):
            ...
        elif isinstance(element, UmlOperation):
            ...
        elif isinstance(element, UmlDiagram):
            ...
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlClassDiagram.")

    @property
    def classes(self) -> List[UmlClass]:
        return self._classes
    
    @classes.setter
    def classes(self, new_classes: List[UmlClass]):
        self._classes = new_classes
        if self._classes and self.builder:
            for class_element in self._classes:
                self.builder.add_class(class_element)

    @property
    def interfaces(self) -> List[UmlInterface]:
        return self._interfaces
    
    @interfaces.setter
    def interfaces(self, new_interfaces: List[UmlInterface]):
        self._interfaces = new_interfaces
        if self._interfaces and self.builder:
            for interface in self._interfaces:
                self.builder.add_class(interface)

    @property
    def data_types(self) -> List[UmlDataType]:
        return self._data_types
    
    @data_types.setter
    def data_types(self, new_data_types: List[UmlDataType]):
        self._data_types = new_data_types
        if self._data_types and self.builder:
            for data_type in self._data_types:
                self.builder.add_class(data_type)

    @property
    def enumerations(self) -> List[UmlEnumeration]:
        return self._enumerations
    
    @enumerations.setter
    def enumerations(self, new_enumerations: List[UmlEnumeration]):
        self._enumerations = new_enumerations
        if self._enumerations and self.builder:
            for enumeration in self._enumerations:
                self.builder.add_class(enumeration)

    @property
    def primitive_types(self) -> List[UmlPrimitiveType]:
        return self._primitive_types
    
    @primitive_types.setter
    def primitive_types(self, new_primitive_types: List[UmlPrimitiveType]):
        self._primitive_types = new_primitive_types
        if self._primitive_types and self.builder:
            for primitive_type in self._primitive_types:
                self.builder.add_class(primitive_type)

    @property
    def associations(self) -> List[Union[UmlAssociation, UmlAggregation, UmlComposition]]:
        return self._associations
    
    @associations.setter
    def associations(self, new_associations: List[Union[UmlAssociation, UmlAggregation, UmlComposition]]):
        self._associations = new_associations
        if self._associations and self.builder:
            for association in self._associations:
                self.builder.add_association(association)

    @property
    def generalizations(self) -> List[UmlGeneralization]:
        return self._generalizations
    
    @generalizations.setter
    def generalizations(self, new_generalizations: List[UmlGeneralization]):
        self._generalizations = new_generalizations
        if self._generalizations and self.builder:
            for generalization in self._generalizations:
                self.builder.add_generalization(generalization)

    @property
    def dependencies(self) -> List[UmlDependency]:
        return self._dependencies
    
    @dependencies.setter
    def dependencies(self, new_dependencies: List[UmlDependency]):
        self._dependencies = new_dependencies
        if self._dependencies and self.builder:
            for dependency in self._dependencies:
                self.builder.add_dependency(dependency)

    @property
    def realizations(self) -> List[UmlRealization]:
        return self._realizations
    
    @realizations.setter
    def realizations(self, new_realizations: List[UmlRealization]):
        self._realizations = new_realizations
        if self._realizations and self.builder:
            for realization in self._realizations:
                self.builder.add_realization(realization)

    @property
    def aggregations(self) -> List[UmlAggregation]:
        return self._aggregations
    
    @aggregations.setter
    def aggregations(self, new_aggregations: List[UmlAggregation]):
        self._aggregations = new_aggregations
        if self._aggregations and self.builder:
            for aggregation in self._aggregations:
                self.builder.add_aggregation(aggregation)

    @property
    def compositions(self) -> List[UmlComposition]:
        return self._compositions
    
    @compositions.setter
    def compositions(self, new_compositions: List[UmlComposition]):
        self._compositions = new_compositions
        if self._compositions and self.builder:
            for composition in self._compositions:
                self.builder.add_composition(composition)

    @property
    def attributes(self) -> List[UmlAttribute]:
        return self._attributes
    
    @attributes.setter
    def attributes(self, new_attributes: List[UmlAttribute]):
        self._attributes = new_attributes
        if self._attributes and self.builder:
            for attribute in self._attributes:
                self.builder.add_attribute(attribute)

    @property
    def operations(self) -> List[UmlOperation]:
        return self._operations
    
    @operations.setter
    def operations(self, new_operations: List[UmlOperation]):
        self._operations = new_operations
        if self._operations and self.builder:
            for operation in self._operations:
                self.builder.add_operation(operation)


class UmlSequenceDiagramElements(IUmlSequenceDiagramElements):
    def __init__(self, interactions: List[UmlInteraction] = None, **kwargs):
        self.interactions = interactions or []
        super().__init__()

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlInteraction):
            self.interactions.append(element)
        elif isinstance(element, UmlDiagram):
            ...
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlSequenceDiagram.")

    @property
    def interactions(self) -> List[UmlInteraction]:
        return self._interactions
    
    @interactions.setter
    def interactions(self, new_interactions: List[UmlInteraction]):
        self._interactions = new_interactions
        if self._interactions and self.builder:
            for interaction in self._interactions:
                self.builder.add_interaction(interaction)


class UmlClassDiagram(UmlDiagram, IUmlClassDiagram):
    def __init__(self, name: str, model: 'UmlModel', id: str = None, **kwargs):
        super().__init__(name=name, model=model, id=id, **kwargs)
        self.elements = UmlClassDiagramElements(**kwargs)

    def add_element(self, element: IUmlElement) -> None:
        return self.elements.add_element(element)

    @property
    def elements(self) -> IUmlClassDiagramElements:
        return self._elements

    @elements.setter
    def elements(self, new_elements: IUmlClassDiagramElements):
        self._elements = new_elements
        if self._elements and self.builder:
            for class_element in self._elements.classes:
                self.builder.add_class(class_element)
            for association in self._elements.associations:
                self.builder.add_association(association)
            for interface in self._elements.interfaces:
                self.builder.add_class(interface)


class UmlSequenceDiagram(UmlDiagram, IUmlSequenceDiagram):
    def __init__(self, name: str, model: 'UmlModel', id: str = None, **kwargs):
        super().__init__(name=name, model=model, id=id, **kwargs)
        self.elements = UmlSequenceDiagramElements(**kwargs)

    def add_element(self, element: IUmlElement) -> None:
        return self.elements.add_element(element)

    @property
    def elements(self) -> IUmlSequenceDiagramElements:
        return self._elements

    @elements.setter
    def elements(self, new_elements: IUmlSequenceDiagramElements):
        self._elements = new_elements
        if self._elements and self.builder:
            for interaction in self._elements.interactions:
                self.builder.add_class(interaction)


class UmlDiagrams(IUmlDiagrams):
    def __init__(self, class_diagrams: List[UmlClassDiagram] = None, sequence_diagrams: List[UmlSequenceDiagram] = None, **kwargs):
        self.class_diagrams = class_diagrams or []
        self.sequence_diagrams = sequence_diagrams or []
        super().__init__()

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
                