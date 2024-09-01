from abc import abstractmethod
from typing import Optional, Any
import json

from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline_deserialization_strategy import (
    PipelineDeserializationStrategy,
)
from src.umlars_translator.core.deserialization.data_source import DataSource
from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    FormatDetectionPipe,
)
from src.umlars_translator.core.deserialization.exceptions import InvalidFormatException
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_format_detection_pipeline import (
    StarumlMDJDetectionPipe,
)
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_model_processing_pipeline import (
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
    UmlPrimitiveTypePipe
)
from src.umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from src.umlars_translator.config import SupportedFormat
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_constants import (
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
