from typing import Any, Callable, Optional
from collections import deque, defaultdict
from functools import wraps
from logging import Logger
from abc import ABC

from kink import inject

from umlars_translator.core.utils.exceptions import IdMismatchException


def evaluate_elements_afterwards(blocking: bool = False) -> Callable:
    """
    Decorator that evaluates all elements from the evaluation queue.

    Args:
        blocking (bool, optional): if set to True, it raises IdMismatchException when ID present as a key in evaluation queue is not present in the ID to instance mapping.
    """

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(self: DelayedCaller, *args, **kwargs) -> Any:
            returned_value = func(self, *args, **kwargs)
            self._evaluate_elements(blocking)
            return returned_value

        return inner

    return wrapper


@inject
class DelayedCaller(ABC):
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self._logger = logger.getChild(self.__class__.__name__)
        self._id_to_instance_mapping: dict[str, Any] = dict()
        self._id_to_evaluation_queue: dict[str, deque[Callable]] = defaultdict(deque)
        """
        Queue of functions to be called when Instance of the Object with given ID is available.
        The Instance has to be given as an argument to function call.
        """

    def _evaluate_elements(self, blocking: bool = False) -> None:
        """
        Function that evaluates all elements from the evaluation queue.
        :arg blocking - if set to True, it raises IdMismatchException when ID present as key in the evaluation
            queue is not present in the ID to instance mapping. Used for partial evaluation.
        """
        for element_id, evaluation_queue in self._id_to_evaluation_queue.items():
            try:
                element_instance = self._id_to_instance_mapping[element_id]
            except KeyError as ex:
                message = f"Couldn't associate given referred object id: {element_id} with any known instance."
                if blocking:
                    raise IdMismatchException(message) from ex
                else:
                    self._logger.info(message)
                    continue

            while evaluation_queue:
                function_to_call = evaluation_queue.popleft()
                function_to_call(element_instance)

