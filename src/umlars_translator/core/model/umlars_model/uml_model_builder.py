from typing import Any, Optional
from logging import Logger

from kink import inject

from src.umlars_translator.core.model.umlars_model.uml_elements import UmlClass, UmlLifeline, UmlAssociationEnd, UmlAssociationBase
from src.umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
from src.umlars_translator.core.utils.delayed_caller import (
    DalayedIdToInstanceMapper,
    evaluate_elements_afterwards,
)


@inject
class UmlModelBuilder(DalayedIdToInstanceMapper, IUmlModelBuilder):
    def __init__(
        self, model: Optional[UmlModel] = None, core_logger: Optional[Logger] = None
    ) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        super().__init__(core_logger=self._logger)

        self._model = model if model is not None else UmlModel()

    def build(self) -> UmlModel:
        self._evaluate_queues()
        return self._model

    def clear(self) -> None:
        self._model = UmlModel()


    def add_element(self, element: Any) -> None:
        self.register_if_not_present(element)



    # @log_calls_and_return_self()
    # def bind_element_to_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_metadata(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_uml_attribute(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_uml_class(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_uml_interface(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_uml_model(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...

    # @log_calls_and_return_self()
    # def construct_uml_package(self, *args, **kwargs) -> "IUmlModelBuilder":
    #     ...


    # TODO: remove after final definition of the builder interface
    def __getattr__(self, name: str) -> "IUmlModelBuilder":
        def method(*args, **kwargs):
            self._logger.debug(f"Method called: {name}({args}, {kwargs})")
            return self

        return method


# #TODO: evaluate_elements_shouldnt_suppose_self - just be method of delayed caller and evaluate after pipe's process
