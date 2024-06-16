from abc import ABC
from typing import Any, Optional
from logging import Logger

from kink import inject

from umlars_translator.core.model.uml_model import UmlModel
from umlars_translator.core.utils.delayed_caller import (
    DelayedCaller,
    evaluate_elements_afterwards,
)


@inject
class UmlModelBuilder(DelayedCaller):
    def __init__(
        self, model: Optional[UmlModel] = None, logger: Optional[Logger] = None
    ) -> None:
        self._model = None
        self._logger = logger.getChild(self.__class__.__name__)
        super(DelayedCaller, self).__init__()

    def add_class():
        ...

    def documentation(self, *args) -> None:
        print(args)
        # self._model.add_documentation(documentation)

    def model(self, *args) -> None:
        print(args)
        # self._model = model

    def xmi_version(self, *args) -> None:
        print(args)
        # self._model.set_xmi_version(xmi_version)

    def build(self) -> UmlModel:
        return self._model or UmlModel()

    def __getattr__(self, name):
        def method(*args, **kwargs):
            print(f"Method called: {name}")
            print(f"Args: {args}")
            print(f"Kwargs: {kwargs}")
            self._logger.debug(f"Method called: {name}")
            self._logger.debug(f"Args: {args}")
            self._logger.debug(f"Kwargs: {kwargs}")
            return None

        return method


# TODO: or factory?
# TODO: builder should be abstract, cause new subclasses will have different approach to the ID
# #TODO: evaluate_elements_shouldnt_suppose_self - just be method of delayed caller and evaluate after pipe's process
