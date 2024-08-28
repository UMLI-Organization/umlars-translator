from typing import Any, Optional, TYPE_CHECKING
from logging import Logger

from kink import inject

from src.umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlElement
from src.umlars_translator.core.utils.delayed_caller import (
    DalayedIdToInstanceMapper,
    evaluate_elements_afterwards,
)
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlClass, UmlLifeline, UmlAssociationEnd, UmlAssociationBase, UmlVisibilityEnum, UmlInterface, UmlPackage, UmlPrimitiveType, UmlAttribute, UmlOperation, UmlLifeline, UmlAssociationEnd, UmlAssociationBase
from src.umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagram


@inject
class UmlModelBuilder(DalayedIdToInstanceMapper, IUmlModelBuilder):
    def __init__(
        self, model: Optional[UmlModel] = None, core_logger: Optional[Logger] = None
    ) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        super().__init__(core_logger=self._logger)

        self._model = model if model is not None else UmlModel(builder=self)

    def build(self) -> UmlModel:
        self._evaluate_queues()
        return self._model

    def clear(self) -> None:
        self._model = UmlModel(builder=self)

    def add_element(self, element: Any) -> 'IUmlModelBuilder':
        self.register_if_not_present(element)
        return self

    def construct_uml_model(self, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum | str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_model({args}, {kwargs})")
        self._model.name = name
        if visibility is not None:
            if isinstance(visibility, str):
                visibility = UmlVisibilityEnum(visibility)

        self._model.visibility = visibility
        return self

    def bind_element_to_diagram(self, element: Optional[UmlElement] = None, element_id: Optional[str] = None, diagram: Optional[UmlDiagram] = None, diagram_id: Optional[str] = None,  *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: bind_element_to_diagram({args}, {kwargs})")
        element = element if element is not None else self.get_instance_by_id(element_id)
        diagram = diagram if diagram is not None else self.get_instance_by_id(diagram_id)

        if element is None:
            self._bind_not_initialized_element_to_diagram(element_id, diagram, diagram_id)
        else:
            self._bind_initialized_element_to_diagram(element, diagram, diagram_id)

        return self

    # @log_calls_and_return_self()
    # def construct_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    def construct_metadata(self, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_metadata({args}, {kwargs})")
        self.model.metadata = kwargs
        return self

    # @log_calls_and_return_self()
    def construct_uml_class(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum | str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_class({args}, {kwargs})")
        uml_class = UmlClass(id=id, name=name, visibility=visibility, model=self._model, builder=self)
        self.add_class(uml_class)
        return self
    
    def add_class(self, uml_class: UmlClass) -> "IUmlModelBuilder":
        self.add_element(uml_class)
        self.model.elements.classes.append(uml_class)

    def construct_uml_attribute(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum | str] = None, type_id: Optional[str] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_read_only: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_attribute({args}, {kwargs})")
        type = self.get_instance_by_id(type_id)
        attribute = UmlAttribute(id=id, name=name, type=type, visibility=visibility, is_static=is_static, is_ordered=is_ordered, is_unique=is_unique, is_read_only=is_read_only, is_query=is_query, is_derived=is_derived, is_derived_union=is_derived_union, model=self._model, builder=self)
        self.add_attribute(attribute)

        if type is None:
            def _queued_assign_type(type: UmlElement) -> None:
                attribute.type = type
            
            self.register_dalayed_call_for_id(type_id, _queued_assign_type)

        return self
    
    def add_attribute(self, attribute: UmlAttribute) -> "IUmlModelBuilder":
        self.add_element(attribute)
        # TODO: add owners registration 
        # self.register_if_not_present(attribute.owner)

    # @log_calls_and_return_self()
    # def construct_uml_interface(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...


    def construct_uml_package(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum | str] = None,  
                              *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_package({args}, {kwargs})")
        package = UmlPackage(id=id, name=name, visibility=visibility, model=self._model, builder=self)
        self.add_package(package)
        return self
    
    def add_package(self, package: UmlPackage) -> "IUmlModelBuilder":
        self.add_element(package)
        self.model.packages.append(package)





    def _bind_not_initialized_element_to_diagram(self, element_id: str, diagram: Optional[UmlDiagram], diagram_id: Optional[str]) -> None:
        if diagram is not None:
            def _queued_assign_element_to_diagram(element: UmlElement) -> None:
                diagram.add_element(element)

            self.register_dalayed_call_for_id(element_id, _queued_assign_element_to_diagram)
        elif diagram_id is not None:
            def _queued_assign_element_to_diagram(element: UmlElement) -> None:
                self.bind_element_to_diagram(element=element, diagram_id=diagram_id)

            self.register_dalayed_call_for_id(element_id, _queued_assign_element_to_diagram)
        else:
            raise ValueError("Either diagram or diagram_id should be provided.")
         
    def _bind_initialized_element_to_diagram(self, element: UmlElement, diagram: Optional[UmlDiagram], diagram_id: Optional[str]) -> None:
        if diagram is not None:
            diagram.add_element(element)
        elif diagram_id is not None:
            def _queued_assign_element_to_diagram(diagram: UmlDiagram) -> None:
                diagram.add_element(element)
            
            self.register_dalayed_call_for_id(diagram_id, _queued_assign_element_to_diagram)
        else:
            raise ValueError("Either diagram or diagram_id should be provided.")


    # TODO: remove after final definition of the builder interface
    def __getattr__(self, name: str) -> "IUmlModelBuilder":
        def method(*args, **kwargs):
            self._logger.debug(f"Method called: {name}({args}, {kwargs})")
            return self

        return method


# #TODO: evaluate_elements_shouldnt_suppose_self - just be method of delayed caller and evaluate after pipe's process
