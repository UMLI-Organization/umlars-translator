from typing import Iterator

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlFormatDetectionPipe,
    DataBatch,
    AliasToXmlKey,
)
from umlars_translator.core.deserialization.exceptions import UnsupportedFormatException
from umlars_translator.core.configuration.config_proxy import Config, get_configurable_value


# The following classes are used to detect the format of the data


class NotationXmiFormatDetectionPipe(XmlFormatDetectionPipe):
    ...


class NotationXmiDetectionPipe(NotationXmiFormatDetectionPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["root"]
    EXPECTED_XMI_BASE_VERSION: str = "2"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        data_root = self._get_root_element(data)
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                xmi_version=self.config.ATTRIBUTES["xmi_version"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root,
            mandatory_attributes,
        )

        if not aliases_to_values["xmi_version"].startswith(self.__class__.EXPECTED_XMI_BASE_VERSION):
            raise UnsupportedFormatException("Invalid XMI version.")

        diagram_tag_name_config = Config.TAGS["diagram"]
        diagram_tag_name = get_configurable_value(diagram_tag_name_config, self.config)

        if data_root.find(diagram_tag_name) is None:
            raise UnsupportedFormatException("No diagram found in the data.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)
