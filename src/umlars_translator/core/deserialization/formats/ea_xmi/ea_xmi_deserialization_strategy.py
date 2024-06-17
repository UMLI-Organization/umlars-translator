from umlars_translator.core.deserialization.formats.ea_xmi.ea_constants import EaXmiConfig
from umlars_translator.core.deserialization.abstract.xml.xml_deserialization_strategy import (
    XmiDeserializationStrategy,
)
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.core.deserialization.config import SupportedFormat
from umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_pipeline import (
    EaXmiDetectionPipe,
    EaXmiDocumentationDetectionPipe,
    RootPipe,
    DocumentationPipe,
    UmlModelPipe,
    UmlPackagePipe,
    UmlClassPipe,
    UmlInterfacePipe,
    ExtensionPipe,
    DiagramsPipe,
    DiagramPipe,
    UmlAttributePipe,
)


@register_deserialization_strategy
class EaXmiImportParsingStrategy(XmiDeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.XMI_EA
    CONFIG_NAMESPACE_CLASS = EaXmiConfig

    def _build_format_detection_pipe(self) -> EaXmiDetectionPipe:
        xmi_detection_pipe = EaXmiDetectionPipe()
        xmi_detection_pipe.add_next(EaXmiDocumentationDetectionPipe())
        return xmi_detection_pipe

    def _build_processing_pipe(self) -> RootPipe:
        root_pipe = RootPipe()
        documentation_pipe = root_pipe.add_next(DocumentationPipe())
        self._build_uml_model_processing_pipe(root_pipe)
        self._build_extension_processing_pipe(root_pipe)

        return root_pipe

    def _build_uml_model_processing_pipe(self, root_pipe: RootPipe) -> UmlModelPipe:
        uml_model_pipe = root_pipe.add_next(UmlModelPipe())
        package_pipe = uml_model_pipe.add_next(UmlPackagePipe())
        self._build_uml_class_processing_pipe(package_pipe)
        interface_pipe = package_pipe.add_next(UmlInterfacePipe())


        return uml_model_pipe
    
    def _build_uml_class_processing_pipe(self, package_pipe: RootPipe) -> UmlClassPipe:
        class_pipe = package_pipe.add_next(UmlClassPipe())
        attribute_pipe = class_pipe.add_next(UmlAttributePipe())


        return class_pipe

    def _build_extension_processing_pipe(self, root_pipe: RootPipe) -> ExtensionPipe:
        extension_pipe = root_pipe.add_next(ExtensionPipe())

        diagrams_pipe = extension_pipe.add_next(DiagramsPipe())
        diagram_pipe = diagrams_pipe.add_next(DiagramPipe())

        return extension_pipe
