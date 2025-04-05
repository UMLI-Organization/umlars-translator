from abc import abstractmethod
from typing import Optional, Any
import json

from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline_deserialization_strategy import (
    PipelineDeserializationStrategy,
)
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    FormatDetectionPipe,
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException
from umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_format_detection_pipeline import (
    StarumlMDJDetectionPipe,
)
from umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_model_processing_pipeline import (
    RootPipe,
    UmlModelPipe,
    UmlClassPipe,
    UmlInterfacePipe,
    UmlAttributePipe,
    UmlOperationPipe,
    UmlOperationParameterPipe,
    UmlDataTypePipe,
    UmlEnumerationPipe,
    UmlAssociationPipe,
    UmlAssociationEndPipe,
    UmlGeneralizationPipe,
    UmlInterfaceRealizationPipe,
    UmlPrimitiveTypePipe, 
    UmlClassDiagramPipe,
    UmlCollaborationPipe,
    UmlAnyViewPipe,
    UmlInteractionPipe,
    UmlSequenceDiagramPipe,
    UmlLifelinePipe,
    UmlMessagePipe,
    UmlInteractionUsePipe,
    UmlCombinedFragmentPipe,
    UmlInteractionOperandPipe,
)
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.config import SupportedFormat
from umlars_translator.core.deserialization.formats.staruml_mdj.staruml_constants import (
    StarumlMDJConfig,
)


class JSONDeserializationStrategy(PipelineDeserializationStrategy):
    def __init__(
        self,
        pipe: Optional[ModelProcessingPipe] = None,
        format_detection_pipe: Optional[ModelProcessingPipe] = None,
        **kwargs,
    ) -> None:
        self._pipe = pipe
        self._format_detection_pipe = format_detection_pipe
        self._parsed_data = None
        super().__init__(**kwargs)

    def _parse_format_data(self, data_source: DataSource) -> Any:
        try:
            return json.loads(data_source.retrieved_data)
        except json.JSONDecodeError as ex:
            error_message = f"Error parsing JSON data from {data_source}: {ex}"
            self._logger.error(error_message)
            raise InvalidFormatException(error_message)


@register_deserialization_strategy
class StarumlMDJDeserializationStrategy(JSONDeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.MDJ_STARTUML
    CONFIG_NAMESPACE_CLASS = StarumlMDJConfig

    def _build_processing_pipe(self) -> ModelProcessingPipe:
        # Start with the root pipe
        root_pipe = RootPipe()

        # Build the UML model pipe chain
        uml_model_pipe = root_pipe.add_next(UmlModelPipe())

        # Add class processing pipe
        uml_class_pipe = uml_model_pipe.add_next(UmlClassPipe())
        self._build_classifier_processing_pipe(uml_class_pipe)

        # Add interface processing pipe
        uml_interface_pipe = uml_model_pipe.add_next(UmlInterfacePipe())
        self._build_classifier_processing_pipe(uml_interface_pipe)

        # Add data type processing pipe
        uml_data_type_pipe = uml_model_pipe.add_next(UmlDataTypePipe())

        # Add enumeration processing pipe
        uml_enumeration_pipe = uml_model_pipe.add_next(UmlEnumerationPipe())

        # Add primitive type processing pipe
        uml_primitive_type_pipe = uml_model_pipe.add_next(UmlPrimitiveTypePipe())
        
        # Add class diagram processing pipe
        uml_class_diagram_pipe = uml_model_pipe.add_next(UmlClassDiagramPipe())

        # Add view processing pipe
        uml_any_view_pipe_for_class = uml_class_diagram_pipe.add_next(UmlAnyViewPipe())
        # Provide recursive view processing to add all elements to the model
        uml_any_view_pipe_for_class.add_next(uml_any_view_pipe_for_class)

        # Add collaboration processing pipe
        uml_collaboration_pipe = uml_model_pipe.add_next(UmlCollaborationPipe())

        # Add interaction processing pipe
        uml_interaction_pipe = uml_collaboration_pipe.add_next(UmlInteractionPipe())

        # Add sequence diagram processing pipe
        uml_sequence_diagram_pipe = uml_interaction_pipe.add_next(UmlSequenceDiagramPipe())

        uml_message_pipe = uml_interaction_pipe.add_next(UmlMessagePipe())
        uml_life_line_pipe = uml_interaction_pipe.add_next(UmlLifelinePipe())

        uml_interaction_use_pipe = uml_interaction_pipe.add_next(UmlInteractionUsePipe())
        uml_combined_fragment_pipe = uml_interaction_pipe.add_next(UmlCombinedFragmentPipe())
        uml_interaction_operand_pipe = uml_combined_fragment_pipe.add_next(UmlInteractionOperandPipe())

        return root_pipe

    def _build_classifier_processing_pipe(
        self, parent_pipe: UmlClassPipe | UmlInterfacePipe
    ) -> UmlClassPipe | UmlInterfacePipe:
        # Add attribute processing pipe
        attribute_pipe = parent_pipe.add_next(UmlAttributePipe())

        # Add operation processing pipe
        operation_pipe = parent_pipe.add_next(UmlOperationPipe())
        operation_pipe.add_next(UmlOperationParameterPipe())

        uml_association_pipe = parent_pipe.add_next(UmlAssociationPipe())
        uml_association_pipe.add_next(UmlAssociationEndPipe())

        uml_generalization_pipe = parent_pipe.add_next(UmlGeneralizationPipe())
        uml_interface_realization_pipe = parent_pipe.add_next(UmlInterfaceRealizationPipe())

        return parent_pipe

    def _build_format_detection_pipe(self) -> FormatDetectionPipe:
        return StarumlMDJDetectionPipe()
