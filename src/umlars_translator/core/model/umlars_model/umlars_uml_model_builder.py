from typing import Any, Optional
from logging import Logger

from kink import inject

from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from umlars_translator.core.model.umlars_model.umlars_uml_model import UmlarsUmlModel
from umlars_translator.core.utils.delayed_caller import (
    DelayedCaller,
    evaluate_elements_afterwards,
)


@inject
class UmlarsUmlModelBuilder(IUmlModelBuilder, DelayedCaller):
    def __init__(
        self, model: Optional[UmlarsUmlModel] = None, logger: Optional[Logger] = None
    ) -> None:
        self._logger = logger.getChild(self.__class__.__name__)
        # super(DelayedCaller, self).__init__(logger=self._logger)

        self._model = model if model is not None else UmlarsUmlModel()

    def build(self) -> UmlarsUmlModel:
        self._evaluate_elements()
        return self._model

    def clear(self) -> None:
        self._model = UmlarsUmlModel()

    # def __getattr__(self, name):
    #     def method(*args, **kwargs):
    #         print(f"Method called: {name}")
    #         print(f"Args: {args}")
    #         print(f"Kwargs: {kwargs}")
    #         self._logger.debug(f"Method called: {name}({args}, {kwargs})")
    #         return None

    #     return method


# #TODO: evaluate_elements_shouldnt_suppose_self - just be method of delayed caller and evaluate after pipe's process
