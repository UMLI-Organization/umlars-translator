from typing import Any
import io
from xml.etree import ElementTree as ET

from umlars_translator.core.deserialization.data_source import DataSource


def retrieve_namespaces(source: DataSource) -> dict[str, str]:
        namespaces = {}
        xml_file_like_data_reference = (
            source.file_path
            if source.file_path is not None
            else io.StringIO(source.retrieved_data)
        )

        for event, elem in ET.iterparse(
            xml_file_like_data_reference, events=("start-ns",)
        ):
            prefix, uri = elem
            namespaces[prefix] = uri
        return namespaces
