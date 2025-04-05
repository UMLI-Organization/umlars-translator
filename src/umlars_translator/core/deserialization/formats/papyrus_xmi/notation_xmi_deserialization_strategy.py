from umlars_translator.core.configuration.config_namespace import  ConfigNamespace
from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.deserialization.formats.papyrus_xmi.notation_constants import (
    NotationXmiConfig,
)
from umlars_translator.core.deserialization.abstract.xml.xml_deserialization_strategy import (
    XmiDeserializationStrategy,
)
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.config import SupportedFormat
from umlars_translator.core.deserialization.formats.papyrus_xmi.notation_xmi_model_processing_pipeline import (
    DiagramPipe, RootPipe
)

from umlars_translator.core.deserialization.formats.papyrus_xmi.notation_xmi_format_detection_pipeline import (
    NotationXmiDetectionPipe
)


@register_deserialization_strategy
class NotationXmiImportParsingStrategy(XmiDeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.NOTATION_PAPYRUS
    CONFIG_NAMESPACE_CLASS = NotationXmiConfig

    def _build_format_detection_pipe(self) -> NotationXmiDetectionPipe:
        xmi_detection_pipe = NotationXmiDetectionPipe()
        return xmi_detection_pipe

    def _build_processing_pipe(self) -> RootPipe:
        root_pipe = RootPipe()
        root_pipe.add_next(DiagramPipe())

        return root_pipe
