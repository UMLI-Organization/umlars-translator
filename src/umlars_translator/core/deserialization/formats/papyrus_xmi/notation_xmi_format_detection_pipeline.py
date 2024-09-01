from typing import Iterator

from src.umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlFormatDetectionPipe,
    DataBatch,
    AliasToXmlKey,
)
from src.umlars_translator.core.deserialization.exceptions import UnsupportedFormatException
from src.umlars_translator.core.configuration.config_proxy import Config


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
                notation_namespace=self.config.ATTRIBUTES["notation_namespace"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root,
            mandatory_attributes,
        )

        self._check_if_namespaces_are_correct()

        if not aliases_to_values["xmi_version"].startswith(self.__class__.EXPECTED_XMI_BASE_VERSION):
            raise UnsupportedFormatException("Invalid XMI version.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)
