from typing import Optional

from umlars_translator.core.deserializer.abstract.base.factory import DeserializationStrategyFactory
from umlars_translator.core.deserializer.abstract.base.deserialization_strategy import DeserializationStrategy
from umlars_translator.core.deserializer.abstract.base.data_source import DataSource
from umlars_translator.core.deserializer.config import SupportedFormat


class ModelDeserializer:
    def __init__(self):
        self._factory = DeserializationStrategyFactory

    def deserialize(self, format: Optional[SupportedFormat], source: DataSource) -> UMLModel:
        import_parsing_strategy = self.get_strategy_for_source(format, source)
        return import_parsing_strategy.retrieve_model(source)
    
    def get_strategy_for_source(self, format: Optional[SupportedFormat], source: DataSource) -> DeserializationStrategy:
        return self._factory.get_strategy(format_data_source=source)