from typing import Type, Optional, Dict

from kink import inject

from umlars_translator.config import SupportedFormat
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.exceptions import UnsupportedSourceDataTypeError
from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder

from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)


class DeserializationStrategyFactory:
    """
    Factory used to create deserialization strategies.
    """

    def __init__(self) -> None:
        self._registered_strategies: Dict[SupportedFormat, DeserializationStrategy] = {}

    def register_strategy(
        self, strategy_class: Type["DeserializationStrategy"]
    ) -> Type["DeserializationStrategy"]:
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
        format_data_source: Optional[DataSource] = None,
        model_builder: Optional[IUmlModelBuilder] = None,
        **kwargs,
    ) -> Optional["DeserializationStrategy"]:
        """
        Method used to retrieve a strategy for a specific format name.
        Using positional arguments is not allowed due to complexity of the method.
        """

        def create_strategy(
            stategy_class: type["DeserializationStrategy"],
        ) -> DeserializationStrategy:
            return stategy_class(model_builder=model_builder, **kwargs)

        strategy_class = (
            self._registered_strategies.get(format_data_source.format) if format_data_source.format is not None else None
        )

        if strategy_class is not None:
            return create_strategy(strategy_class)

        strategies_instances_for_data = [
            strategy_instance
            for strategy_class in self._registered_strategies.values()
            if (
                strategy_instance := create_strategy(strategy_class)
            ).can_deserialize_format(format_data_source.format, format_data_source)
        ]

        if len(strategies_instances_for_data) > 1:
            # TODO: add logging
            # TODO: add custom exception
            raise ValueError(
                "Multiple strategies can deserialize the format data."
                f"Strategies: {strategies_instances_for_data}"
            )
        elif len(strategies_instances_for_data) == 0:
            raise UnsupportedSourceDataTypeError("No strategy can deserialize the format data.")
        else:
            strategy_instance = strategies_instances_for_data[0]

        return strategy_instance


@inject
def register_deserialization_strategy(
    strategy: type["DeserializationStrategy"], factory: DeserializationStrategyFactory
) -> type["DeserializationStrategy"]:
    factory.register_strategy(strategy)
    return strategy
