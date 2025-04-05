from xml.etree import ElementTree as ET
from typing import Iterator, Any

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlModelProcessingPipe,
    XmlAttributeCondition,
    DataBatch,
    AliasToXmlKey,
)
from umlars_translator.core.deserialization.exceptions import UnableToMapError
from umlars_translator.core.configuration.config_proxy import Config, get_configurable_value
from umlars_translator.core.model.constants import UmlDiagramType


class NotationXmiModelProcessingPipe(XmlModelProcessingPipe):
    ...


class RootPipe(NotationXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["root"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data_root = self._get_root_element(data_batch.data)

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class DiagramPipe(NotationXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["diagram"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                name=self.config.ATTRIBUTES["name"],
                type=self.config.PAPYRUS_EXTENDED_ATTRIBUTES["type"],
            )
            aliases_to_values = self._get_attributes_values_for_aliases(
                data, mandatory_attributes
            )

            self._construct_diagram(aliases_to_values)

            diagram_elements = data.iter(self.config.PAPYRUS_EXTENDED_TAGS["element"])

            self._construct_diagram_elements(diagram_elements, aliases_to_values["id"])
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)

    def _construct_diagram_elements(
        self, diagram_elements: Iterator[ET.Element], diagram_id: str
    ) -> None:
        self._logger.debug(f"Constructing diagram elements for diagram: {diagram_id}")
        for element in diagram_elements:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                element_href=self.config.ATTRIBUTES["href"],
            )
            aliases_to_values = self._get_attributes_values_for_aliases(
                element, mandatory_attributes
            )
            element_id = aliases_to_values["element_href"].split(".uml#")[-1]

            self.model_builder.bind_element_to_diagram(
                element_id=element_id, diagram_id=diagram_id
            )

    def _construct_diagram(self, aliases_to_values: dict[str, Any]) -> None:
            diagram_type_name = aliases_to_values.pop("type")
            diagram_type_config = Config.PAPYRUS_DIAGRAMS_TYPES_MAPPING[diagram_type_name]
            diagram_type_parsed = get_configurable_value(diagram_type_config, self.config)

            self._logger.debug(f"Constructing diagram of type: {diagram_type_parsed}")

            match (diagram_type_parsed):
                case UmlDiagramType.CLASS:
                    self.model_builder.construct_class_diagram(**aliases_to_values)
                case UmlDiagramType.SEQUENCE:
                    self.model_builder.construct_sequence_diagram(**aliases_to_values)
                case _:
                    self._logger.warning(f"Diagram type: {diagram_type_parsed} is not supported.")
