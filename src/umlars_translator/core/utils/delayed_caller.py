from typing import Any, Callable, Optional, Type
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
        def inner(self: DalayedIdToInstanceMapper, *args, **kwargs) -> Any:
            returned_value = func(self, *args, **kwargs)
            self._evaluate_queues(blocking)
            return returned_value

        return inner

    return wrapper


@inject
class IdToInstanceMapper:
    _id_to_instance_mapping: dict[str, Any]
    _type_to_id_to_instance_mapping: dict[Type, dict[str, Any]]

    def __init__(self, core_logger: Optional[Logger] = None) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        self._id_to_instance_mapping = {}
        self._type_to_id_to_instance_mapping = defaultdict(dict) 

    def register_if_not_present(self, element: Any, old_id: Optional[str] = None, clear_old_id: bool = True, register_as_type: Optional[Type] = None) -> None:
        """
        Registers an element in the id-to-instance mapping if not already present.
        """
        self._logger.debug(f"Registering element {element} with id {getattr(element, 'id', 'attribute non-existent')}."
                           "" if old_id is None else f" Old ID: {old_id}."
                           "" if register_as_type is None else f" Registering as type: {register_as_type}.")
        try:
            element_id = element.id
        except AttributeError as ex:
            self._logger.debug(f"Element {element} has no ID, skipping registration. Error: {ex}")
            return

        type_of_element = register_as_type or type(element)        
        if element_id not in self._id_to_instance_mapping:
            self._id_to_instance_mapping[element_id] = element
            self._type_to_id_to_instance_mapping[type_of_element][element_id] = element

        if old_id is not None and clear_old_id and not old_id == element_id:
            self._id_to_instance_mapping.pop(old_id, None)
            self._type_to_id_to_instance_mapping[type_of_element].pop(old_id, None)

    def clear(self) -> None:
        """
        Clears the ID to instance mapping.
        """
        self._id_to_instance_mapping.clear()
        self._type_to_id_to_instance_mapping.clear()


class DalayedIdToInstanceMapper(IdToInstanceMapper, ABC):
    def __init__(self, core_logger: Optional[Logger] = None) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        self._id_to_evaluation_queue: dict[str, deque[Callable]] = defaultdict(deque)
        """
        Queue of functions to be called when Instance of the Object with given ID is available.
        The Instance has to be given as an argument to function call.
        """
        super().__init__(core_logger=core_logger)
    
    def _evaluate_queues(self, blocking: bool = False) -> None:
        """
        Function that evaluates all elements from the evaluation queue.
        :arg blocking - if set to True, it raises IdMismatchException when ID present as key in the evaluation
            queue is not present in the ID to instance mapping. Used for partial evaluation.
        """

        try:
            items_to_evaluate = self._id_to_evaluation_queue.items()
        except AttributeError:
            message = "No items to evaluate."
            self._logger.info(message)
            return

        for element_id, evaluation_queue in items_to_evaluate:
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

    def register_dalayed_call_for_id(self, element_id: str, function_to_call: Callable) -> None:
        """
        Registers a function to be called when an instance with given ID is available.
        """
        self._id_to_evaluation_queue[element_id].append(function_to_call)

    def get_instance_by_id(self, element_id: str) -> Any:
        """
        Returns an instance of an object with given ID.
        """
        return self._id_to_instance_mapping.get(element_id, None)
    
    def clear(self) -> None:
        """
        Clears the ID to instance mapping.
        """
        self._id_to_evaluation_queue.clear()
        super().clear()