from typing import Optional

from umlars_translator.core.deserialization.abstract.xml.xml_deserialization_strategy import XmiDeserializationStrategy
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.core.deserialization.config import SupportedFormat
from umlars_translator.core.deserialization.formats.ea_xmi.pipeline import (
    RootPipe, DocumentationPipe, ModelPipe, EaXmiDetectionPipe, EaXmiDocumentationDetectionPipe
)



@register_deserialization_strategy
class EaXmiImportParsingStrategy(XmiDeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.XMI_EA


    def _build_processing_pipe(self) -> RootPipe:
        root_pipe = RootPipe()
        documentation_pipe = root_pipe.add_next(DocumentationPipe())
        model_pipe = documentation_pipe.add_next(ModelPipe())

        return root_pipe
    
    
    def _build_format_detection_pipe(self) -> EaXmiDetectionPipe:
        xmi_detection_pipe = EaXmiDetectionPipe()
        xmi_detection_pipe.add_next(EaXmiDocumentationDetectionPipe())
        return xmi_detection_pipe



    # def _build_processing_pipe(self) -> RootPipe:
    #     with ModelProcessingPipe() as root_pipe:
    #         with root_pipe.add_next(ModelProcessingPipe()) as model_pipe:
    #             with model_pipe.add_next(ModelProcessingPipe()) as package_pipe:
    #                 class_pipe = self._create_class_pipe(package_pipe)
    #                 interaction_pipe = self._create_interaction_pipe(package_pipe)
                    
    # def _create_class_pipe(self, parent_pipe: ModelProcessingPipe) -> ModelProcessingPipe:
    #     with parent_pipe.add_next(ModelProcessingPipe()) as class_pipe:
    #         self._create_attribute_pipe(class_pipe)
    #         self._create_operation_pipe(class_pipe)
    #     return class_pipe
    
    # def _create_interaction_pipe(self, parent_pipe: ModelProcessingPipe) -> ModelProcessingPipe:
    #     return parent_pipe.add_next(ModelProcessingPipe())
    
    # def _create_attribute_pipe(self, parent_pipe: ModelProcessingPipe) -> ModelProcessingPipe:
    #     return parent_pipe.add_next(ModelProcessingPipe())
    
    # def _create_operation_pipe(self, parent_pipe: ModelProcessingPipe) -> ModelProcessingPipe:
    #     return parent_pipe.add_next(ModelProcessingPipe())