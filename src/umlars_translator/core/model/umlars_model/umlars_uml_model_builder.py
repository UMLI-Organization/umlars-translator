from typing import Any, Optional
from logging import Logger

from kink import inject

from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from umlars_translator.core.model.umlars_model.umlars_uml_model import UmlModel
from umlars_translator.core.utils.delayed_caller import (
    DelayedCaller,
    evaluate_elements_afterwards,
)


@inject
class UmlModelBuilder(DelayedCaller, IUmlModelBuilder):
    def __init__(
        self, model: Optional[UmlModel] = None, logger: Optional[Logger] = None
    ) -> None:
        self._logger = logger.getChild(self.__class__.__name__)
        super().__init__(logger=self._logger)

        self._model = model if model is not None else UmlModel()

    def build(self) -> UmlModel:
        self._evaluate_elements()
        return self._model

    def clear(self) -> None:
        self._model = UmlModel()

    # TODO: remove after final definition of the builder interface
    def __getattr__(self, name: str) -> "IUmlModelBuilder":
        def method(*args, **kwargs):
            self._logger.debug(f"Method called: {name}({args}, {kwargs})")
            return self

        return method


# #TODO: evaluate_elements_shouldnt_suppose_self - just be method of delayed caller and evaluate after pipe's process
