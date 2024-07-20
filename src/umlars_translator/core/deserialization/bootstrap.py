from kink import di

from src.umlars_translator.core.deserialization.factory import (
    DeserializationStrategyFactory,
)
from src.umlars_translator.core.deserialization.deserializer import ModelDeserializer
from src.umlars_translator.core.extensions_manager import ExtensionsManager


def bootstrap_di() -> None:
    factory = DeserializationStrategyFactory()
    di[DeserializationStrategyFactory] = factory

    deserialization_extensions_manager = ExtensionsManager()
    di[ExtensionsManager] = deserialization_extensions_manager

    model_deserializer = ModelDeserializer()
    di[ModelDeserializer] = model_deserializer
