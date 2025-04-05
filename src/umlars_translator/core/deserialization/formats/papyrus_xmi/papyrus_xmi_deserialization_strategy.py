from umlars_translator.core.configuration.config_namespace import  ConfigNamespace
from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_constants import (
    PapyrusXmiConfig,
)
from umlars_translator.core.deserialization.abstract.xml.xml_deserialization_strategy import (
    XmiDeserializationStrategy,
)
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.config import SupportedFormat
from umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_model_processing_pipeline import (
    UmlModelPipe,
    UmlClassPipe,
    UmlInterfacePipe,
    UmlAttributePipe,
    UmlOperationPipe,
    UmlOperationParameterPipe,
    UmlAssociationPipe,
    UmlAssociationOwnedEndPipe,
    UmlDataTypePipe,
    UmlEnumerationPipe,
)

from umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_format_detection_pipeline import (
    PapyrusXmiDetectionPipe,
)


@register_deserialization_strategy
class PapyrusXmiImportParsingStrategy(XmiDeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.UML_PAPYRUS
    CONFIG_NAMESPACE_CLASS = PapyrusXmiConfig

    def _build_format_detection_pipe(self) -> PapyrusXmiDetectionPipe:
        xmi_detection_pipe = PapyrusXmiDetectionPipe()
        return xmi_detection_pipe

    def _build_processing_pipe(self) -> UmlModelPipe:
        return self._build_uml_model_processing_pipe()

    def _build_uml_model_processing_pipe(self) -> UmlModelPipe:
        uml_model_pipe = UmlModelPipe()
        self._build_uml_class_processing_pipe(uml_model_pipe)
        self._build_uml_interface_processing_pipe(uml_model_pipe)
        self._build_association_processing_pipe(uml_model_pipe)
        self._build_uml_data_type_processing_pipe(uml_model_pipe)
        self._build_uml_enumeration_processing_pipe(uml_model_pipe)

        return uml_model_pipe

    def _build_uml_class_processing_pipe(
        self, package_pipe: UmlModelPipe
    ) -> UmlClassPipe:
        class_pipe = package_pipe.add_next(UmlClassPipe())
        self._build_classifier_processing_pipe(class_pipe)

        return class_pipe

    def _build_uml_interface_processing_pipe(
        self, package_pipe: UmlModelPipe
    ) -> UmlInterfacePipe:
        interface_pipe = package_pipe.add_next(UmlInterfacePipe())
        self._build_classifier_processing_pipe(interface_pipe)

        return interface_pipe

    def _build_uml_attribute_processing_pipe(
        self, parent_pipe: UmlClassPipe | UmlInterfacePipe
    ) -> UmlAttributePipe:
        attribute_pipe = parent_pipe.add_next(UmlAttributePipe())
        return attribute_pipe

    def _build_uml_operation_processing_pipe(
        self, parent_pipe: UmlClassPipe | UmlInterfacePipe
    ) -> UmlOperationPipe:
        operation_pipe = parent_pipe.add_next(UmlOperationPipe())
        parameter_pipe = operation_pipe.add_next(UmlOperationParameterPipe())
        return operation_pipe

    def _build_classifier_processing_pipe(
        self, parent_pipe: UmlClassPipe | UmlInterfacePipe
    ) -> UmlClassPipe | UmlInterfacePipe:
        self._build_uml_attribute_processing_pipe(parent_pipe)
        self._build_uml_operation_processing_pipe(parent_pipe)
        return parent_pipe
    
    def _build_uml_data_type_processing_pipe(
        self, parent_pipe: UmlModelPipe
    ) -> UmlDataTypePipe:
        data_type_pipe = parent_pipe.add_next(UmlDataTypePipe())
        return data_type_pipe
    
    def _build_uml_enumeration_processing_pipe(
        self, parent_pipe: UmlModelPipe
    ) -> UmlEnumerationPipe:
        enumeration_pipe = parent_pipe.add_next(UmlEnumerationPipe())
        return enumeration_pipe

    def _build_association_processing_pipe(
        self, parent_pipe: UmlModelPipe
    ) -> UmlAssociationPipe:
        association_pipe = parent_pipe.add_next(UmlAssociationPipe())
        owned_end_pipe = association_pipe.add_next(UmlAssociationOwnedEndPipe())
        return association_pipe
