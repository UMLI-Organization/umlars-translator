from typing import Any, NamedTuple, Iterator, Optional, Callable
from collections import deque
from enum import Enum

from umlars_translator.core.configuration.config_namespace import ConfigNamespace


class SupportedOperationType(Enum):
    GETATTR = "getattr"
    GETITEM = "getitem"


class DelayedOperation(NamedTuple):
    operation: SupportedOperationType
    args: Iterator[Any]


class OperationQueue:
    def __init__(self, operations: Optional[Iterator[Callable]] = None) -> None:
        self._operations = operations if operations is not None else deque()

    @property
    def operations(self) -> deque[Callable]:
        return self._operations

    def add_operation(self, operation: SupportedOperationType, *args: Any) -> None:
        if operation is SupportedOperationType.GETATTR:
            partial_operation = self._create_get_attr_operation(args[0])
            self._operations.append(partial_operation)
        elif operation is SupportedOperationType.GETITEM:
            partial_operation = self._create_get_item_operation(args[0])
            self._operations.append(partial_operation)

    def _create_get_attr_operation(self, name: str) -> Callable:
        return lambda instance: getattr(instance, name)

    def _create_get_item_operation(self, key: str) -> Callable:
        return lambda instance: instance[key]

    def __call__(self, instance: Any) -> Any:
        result = instance
        for operation in self._operations:
            result = operation(result)

        return result


# TODO: make config proxy just store dict of values to be parsed ->
# -> then function calls just take values from the dict (mutable) ->
# -> this way even if a key to the __get_item__ is taken from config it can be parsed ->
# -> if the received key to __getitem__ is ConfigProxy - it should be parsed

# TODO: also the best way it could be implemented is to evaluate the value represented by ConfigProxy
# whenever there is call to the check if some value is equal to it (__eq__  or  == ).
# The issue with this approach is that it would require acquiring the config used for evaluation from the current scope - it may not be always available.
class ConfigProxyMeta(type):
    def __getattr__(cls: type["OperationQueue"], name: str) -> "OperationQueue":
        if name.startswith("__"):
            return super().__getattr__(name)

        proxy_instance = cls()
        proxy_instance.add_operation(SupportedOperationType.GETATTR, name)
        return proxy_instance

    def __getitem__(cls: type["OperationQueue"], key: str) -> "OperationQueue":
        proxy_instance = cls()
        proxy_instance.add_operation(SupportedOperationType.GETITEM, key)
        return proxy_instance


class ConfigProxy(OperationQueue, metaclass=ConfigProxyMeta):
    def __getattr__(self, name: str) -> "ConfigProxy":
        if name.startswith("__"):
            """
            Python checks if class raises the AtributeError for particular dunder methods and based on the result determines its character.
            E.g. __isabstractmethod__ is a dunder method that is used to check if the class is an abstract class. If it didn't raise AttributeError, other classes having and instance of this class as static attribute were considered abstract.
            E.g. during debugging python looks for __iter__ method in _is_long_iter function to determine if the class is iterable.
            """
            return super().__getattr__(name)
        self.add_operation(SupportedOperationType.GETATTR, name)
        return self

    def __getitem__(self, key: str) -> "ConfigProxy":
        self.add_operation(SupportedOperationType.GETITEM, key)
        return self

    def __call__(self, instance: ConfigNamespace) -> Any:
        return super().__call__(instance)


class Config(ConfigProxy):
    """
    Proxy class for accessing configuration data.
    """


def get_configurable_value(value: Any | ConfigProxy, config: ConfigNamespace) -> Any:
    if isinstance(value, ConfigProxy):
        return value(config)
    return value
