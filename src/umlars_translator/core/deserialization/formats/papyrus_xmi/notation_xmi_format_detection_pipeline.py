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
    ASSOCIATED_XML_TAG = Config.TAGS["root"]
    EXPECTED_XMI_BASE_VERSION: str = "2"

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

        self._check_if_namespaces_are_correct(data)

        if not aliases_to_values["xmi_version"].startswith(self.__class__.EXPECTED_XMI_BASE_VERSION):
            raise UnsupportedFormatException("Invalid XMI version.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)

    def _check_if_namespaces_are_correct(self, data: str) -> None:
        namespaces = retrieve_namespaces(data)
        if not namespaces:
            raise UnsupportedFormatException(
                "No namespaces found in the provided data. "
                "The data is not in the expected format."
            )
        
        if "eclipse" not in namespaces["uml"]:
            raise UnsupportedFormatException(
                "The data does not contain the expected namespace uri for uml. No 'eclipse' substring found."
            )
        
        if "xmi" not in namespaces:
            raise UnsupportedFormatException(
                "The data does not contain the expected namespace uri for xmi."
            )
        
        if "notation" not in namespaces:
            raise UnsupportedFormatException(
                "The data does not contain the expected namespace uri for notation."
            )