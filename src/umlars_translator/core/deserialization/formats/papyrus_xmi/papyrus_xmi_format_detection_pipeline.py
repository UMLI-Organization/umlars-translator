from typing import Iterator

from src.umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlFormatDetectionPipe,
    DataBatch,
    AliasToXmlKey,
)
from src.umlars_translator.core.deserialization.exceptions import UnsupportedFormatException
from src.umlars_translator.core.configuration.config_proxy import Config
from src.umlars_translator.core.deserialization.abstract.xml.utils import retrieve_namespaces


# The following classes are used to detect the format of the data


class PapyrusXmiFormatDetectionPipe(XmlFormatDetectionPipe):
    ...


class PapyrusXmiDetectionPipe(PapyrusXmiFormatDetectionPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["model"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        data_root = self._get_root_element(data)
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                xmi_version=self.config.ATTRIBUTES["xmi_version"],
                uml_namespace=self.config.ATTRIBUTES["uml_namespace"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root,
            mandatory_attributes,
        )

        if "eclipse" not in aliases_to_values["uml_namespace"]:
            raise UnsupportedFormatException(
                "The data does not contain the expected namespace uri for uml. No 'eclipse' substring found."
            )

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)
