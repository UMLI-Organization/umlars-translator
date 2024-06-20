from typing import Iterator

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlFormatDetectionPipe,
    DataBatch,
    AliasToXmlKey,
)
from umlars_translator.core.deserialization.exceptions import UnsupportedFormatException
from umlars_translator.core.configuration.config_proxy import Config


# The following classes are used to detect the format of the data


class EaXmiFormatDetectionPipe(XmlFormatDetectionPipe):
    ...


class EaXmiDetectionPipe(EaXmiFormatDetectionPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["root"]
    EXPECTED_XMI_VERSION: str = "2.1"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        data_root = self._get_root_element(data)
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                xmi_version=self.config.ATTRIBUTES["xmi_version"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root,
            mandatory_attributes,
        )

        if aliases_to_values["xmi_version"] != self.__class__.EXPECTED_XMI_VERSION:
            raise UnsupportedFormatException("Invalid XMI version.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class EaXmiDocumentationDetectionPipe(EaXmiFormatDetectionPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["documentation"]
    # TODO: take from config
    EXPECTED_EXPORTER: str = "Enterprise Architect"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                exporter=self.config.ATTRIBUTES["exporter"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data,
            mandatory_attributes,
        )

        if aliases_to_values["exporter"] != self.__class__.EXPECTED_EXPORTER:
            raise UnsupportedFormatException("Invalid exporter.")

        yield from self._create_data_batches(data)
