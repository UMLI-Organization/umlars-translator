from abc import ABC, abstractmethod
from typing import Type

from umlars_translator.core.deserializer.abstract.base.deserialization_strategy import ImportParsingStrategy
from umlars_translator.core.deserializer.abstract.xmi import XMIDeserializationFactory
from umlars_translator.core.deserializer.deserialization_factory_registry import DeserializationFactoryRegistry
from umlars_translator.core.deserializer.config import SupportedFormat


@DeserializationFactoryRegistry.register_factory
class EaXmiDeserializationFactory(XmiDeserializationFactory):
    SUPPORTED_FORMAT_NAME = SupportedFormat.XMI_EA

    def create_import_parsing_strategy(self) -> ImportParsingStrategy:
        pass