from abc import ABC, abstractmethod
from typing import Type, Optional

from umlars_translator.core.deserializer.config import SupportedFormat
from umlars_translator.core.deserializer.abstract.base.deserialization_strategy import DeserializationStrategy
from umlars_translator.core.deserializer.abstract.base.data_source import DataSource
    

class DeserializationStrategyFactory:
    """
    Factory used to create deserialization strategies. 
    TODO: make using dependency injection - for now it is just a static class with many class methods.
    """
    _registered_strategies = {}


    @classmethod
    def register_strategy(cls: Type["DeserializationStrategyFactory"], strategy_class: Type["DeserializationStrategy"]) -> "DeserializationStrategy":
        """
        Decorator function used to register a strategy for a specific format name.
        """
        cls._registered_strategies[strategy_class.get_supported_format()] = strategy_class
        return strategy_class


    @classmethod
    def get_strategy(cls: Type["DeserializationStrategyFactory"] , format: Optional[SupportedFormat] = None, format_data_source: Optional[DataSource]) -> Optional["DeserializationStrategy"]:
        """
        Method used to retrieve a strategy for a specific format name.
        """
        strategy_class = cls._registered_strategies.get(format) if format is not None else None
        
        if strategy_class is None:
            registered_strategies = list(filter(lambda strategy: strategy.can_deserialize_format(format, format_data_source), cls._registered_final_factories.values()))
            if len(registered_strategies) > 1:
                # TODO: add logging
                # TODO: add custom exception
                raise ValueError("Multiple factories can deserialize the format data.")
            elif len(registered_strategies) == 0:
                raise ValueError("No strategy can deserialize the format data.")
            else:
                return registered_strategies[0]()
        else:
            return strategy_class()


