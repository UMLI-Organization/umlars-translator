from abc import ABC, abstractmethod
from typing import Any, Optional, Callable
from functools import wraps
from logging import Logger
import logging

from kink import inject

from src.umlars_translator.core.model.abstract.uml_model import IUmlModel


def log_calls_and_return_self(log_level: int = logging.DEBUG) -> Callable:
    def inner(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs) -> Any:
            self._logger.log(
                log_level, f"Method called: {method.__name__}({args}, {kwargs})"
            )
            return self

        return wrapper

    return inner


@inject
class IUmlModelBuilder(ABC):
    """
    Interface required by the final UmlBuilder implementation.
    Main requirement for a subclass is to provide methods `build` and `clear`.
    If other methods are not implemented, calling them won't disrupt the process and the call wll just be logged.
    """

    _logger: Logger
    _model: IUmlModel

    @property
    def model(self) -> IUmlModel:
        return self._model
    
    @model.setter
    def model(self, new_model: IUmlModel) -> None:
        self._model = new_model

    @abstractmethod
    def build(self) -> IUmlModel:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @log_calls_and_return_self()
    def bind_element_to_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_metadata(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_attribute(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_class(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_interface(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_model(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_package(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...
