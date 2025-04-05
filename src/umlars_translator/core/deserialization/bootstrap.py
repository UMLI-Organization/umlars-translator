from kink import di

from umlars_translator.core.deserialization.factory import (
    DeserializationStrategyFactory,
)
from umlars_translator.core.deserialization.deserializer import ModelDeserializer
from umlars_translator.core.extensions_manager import ExtensionsManager


def bootstrap_di() -> None:
    factory = DeserializationStrategyFactory()
    di[DeserializationStrategyFactory] = factory

    deserialization_extensions_manager = ExtensionsManager()
    di[ExtensionsManager] = deserialization_extensions_manager

    model_deserializer = ModelDeserializer()
    di[ModelDeserializer] = model_deserializer
