from kink import di

from umlars_translator.core.deserialization.factory import DeserializationStrategyFactory
from umlars_translator.core.deserialization.deserializer import ModelDeserializer


def bootstrap_di() -> None:
    factory = DeserializationStrategyFactory()
    di[DeserializationStrategyFactory] = factory

    model_deserializer = ModelDeserializer()
    di[ModelDeserializer] = model_deserializer
