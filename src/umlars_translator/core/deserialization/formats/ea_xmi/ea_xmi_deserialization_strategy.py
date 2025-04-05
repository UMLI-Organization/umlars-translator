from umlars_translator.core.configuration.config_namespace import  ConfigNamespace
from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.deserialization.formats.ea_xmi.ea_constants import (
    EaXmiConfig,
)
from umlars_translator.core.deserialization.abstract.xml.xml_deserialization_strategy import (
    XmiDeserializationStrategy,
)
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.config import SupportedFormat
from umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_model_processing_pipeline import (
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
    UmlOperationPipe,
    UmlOperationParameterPipe,
    UmlAssociationPipe,
    UmlAssociationMemberEndPipe,
    UmlAssociationOwnedEndPipe,
    UmlDataTypePipe,
    UmlEnumerationPipe,
)

from umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_format_detection_pipeline import (
    EaXmiDetectionPipe,
    EaXmiDocumentationDetectionPipe,
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
        self._build_uml_interface_processing_pipe(package_pipe)
        self._build_association_processing_pipe(package_pipe)
        self._build_uml_data_type_processing_pipe(package_pipe)
        self._build_uml_enumeration_processing_pipe(package_pipe)

        return uml_model_pipe

    def _build_uml_class_processing_pipe(
        self, package_pipe: UmlPackagePipe
    ) -> UmlClassPipe:
        class_pipe = package_pipe.add_next(UmlClassPipe())
        self._build_classifier_processing_pipe(class_pipe)

        return class_pipe

    def _build_uml_interface_processing_pipe(
        self, package_pipe: UmlPackagePipe
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
        self, parent_pipe: UmlPackagePipe
    ) -> UmlDataTypePipe:
        data_type_pipe = parent_pipe.add_next(UmlDataTypePipe())
        return data_type_pipe
    
    def _build_uml_enumeration_processing_pipe(
        self, parent_pipe: UmlPackagePipe
    ) -> UmlEnumerationPipe:
        enumeration_pipe = parent_pipe.add_next(UmlEnumerationPipe())
        return enumeration_pipe
    

    def _build_association_processing_pipe(
        self, parent_pipe: UmlPackagePipe
    ) -> UmlAssociationPipe:
        association_pipe = parent_pipe.add_next(UmlAssociationPipe())
        member_end_pipe = association_pipe.add_next(UmlAssociationMemberEndPipe())
        owned_end_pipe = association_pipe.add_next(UmlAssociationOwnedEndPipe())
        return association_pipe

    def _build_extension_processing_pipe(self, root_pipe: RootPipe) -> ExtensionPipe:
        extension_pipe = root_pipe.add_next(ExtensionPipe())

        diagrams_pipe = extension_pipe.add_next(DiagramsPipe())
        diagram_pipe = diagrams_pipe.add_next(DiagramPipe())

        return extension_pipe
