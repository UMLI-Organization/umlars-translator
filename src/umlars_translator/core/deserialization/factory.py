from typing import Type, Optional, TYPE_CHECKING

from kink import inject

from umlars_translator.core.deserialization.config import SupportedFormat
from umlars_translator.core.deserialization.data_source import DataSource

if TYPE_CHECKING:
    from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
        DeserializationStrategy,
    )


class DeserializationStrategyFactory:
    """
    Factory used to create deserialization strategies.
    """

    def __init__(self) -> None:
        self._registered_strategies = {}

    def register_strategy(
        self, strategy_class: Type["DeserializationStrategy"]
    ) -> "DeserializationStrategy":
        """
        Decorator function used to register a strategy for a specific format name.
        """
        self._registered_strategies[
            strategy_class.get_supported_format()
        ] = strategy_class
        return strategy_class

    def get_strategy(
        self,
        *,
        format: Optional[SupportedFormat] = None,
        format_data_source: Optional[DataSource],
        **kwargs
    ) -> Optional["DeserializationStrategy"]:
        """
        Method used to retrieve a strategy for a specific format name.
        Using positional arguments is not allowed due to complexity of the method.
        """
        strategy_class = (
            self._registered_strategies.get(format) if format is not None else None
        )

        if strategy_class is None:
            registered_strategies = list(
                filter(
                    lambda strategy: strategy.can_deserialize_format(
                        format, format_data_source
                    ),
                    self._registered_strategies.values(),
                )
            )
            if len(registered_strategies) > 1:
                # TODO: add logging
                # TODO: add custom exception
                raise ValueError("Multiple strategies can deserialize the format data.")
            elif len(registered_strategies) == 0:
                raise ValueError("No strategy can deserialize the format data.")
            else:
                strategy_class = registered_strategies[0]

        return strategy_class(**kwargs)


@inject
def register_deserialization_strategy(
    strategy: type["DeserializationStrategy"], factory: DeserializationStrategyFactory
) -> type["DeserializationStrategy"]:
    factory.register_strategy(strategy)
    return strategy
