from typing import Any, NamedTuple, Iterator, Optional, Callable
from collections import deque
from enum import Enum

from umlars_translator.core.configuration.config_namespace import ConfigNamespace


class SupportedOperationType(Enum):
    GETATTR = 'getattr'
    GETITEM = 'getitem'


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
        while self._operations:
            operation = self._operations.popleft()
            result = operation(result)

        return result


class ConfigProxyMeta(type):
    def __getattr__(cls: type["OperationQueue"], name: str) -> "OperationQueue":
        proxy_instance = cls()
        proxy_instance.add_operation(SupportedOperationType.GETATTR, name)
        return proxy_instance

    def __getitem__(cls: type["OperationQueue"], key: str) -> "OperationQueue":
        proxy_instance = cls()
        proxy_instance.add_operation(SupportedOperationType.GETITEM, key)
        return proxy_instance


class ConfigProxy(OperationQueue, metaclass=ConfigProxyMeta):
    def __getattr__(self, name: str) -> "ConfigProxy":
        if name == "__isabstractmethod__":
            """
            This is required for Python not to recognize the class as an abstract class."""
            raise AttributeError("ConfigProxy class is not an abstract class.")
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
