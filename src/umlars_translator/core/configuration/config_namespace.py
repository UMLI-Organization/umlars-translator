from typing import Optional
from abc import ABC


class ConfigNamespace(ABC):
    """
    Abstract class, serving as a namespace for configuration data.
    """


class ParsedConfigNamespace(ConfigNamespace):
    def __init__(self, mapping_dict: Optional[dict[str, str]] = None) -> None:
        self._mapping_dict = mapping_dict if mapping_dict is not None else {}
        if self._mapping_dict:
            self._replace_placeholders()

    def parse(self, mapping_dict: Optional[dict[str, str]] = None) -> None:
        self._replace_placeholders(mapping_dict)

    def _replace_placeholders(
        self, namespace_patterns: Optional[dict[str, str]] = None
    ) -> None:
        if namespace_patterns is None:
            if self._mapping_dict:
                namespace_patterns = self._mapping_dict
            else:
                return None

        for attr_name in dir(self.__class__):
            attr_value = getattr(self.__class__, attr_name)
            if not attr_name.startswith("__") and not callable(attr_value):
                if isinstance(attr_value, dict):
                    formatted_dict = self.__class__._format_dict(
                        attr_value, namespace_patterns
                    )
                    setattr(self, attr_name, formatted_dict)

    @staticmethod
    def _format_dict(data: dict, namespace_patterns: dict) -> dict:
        formatted_data = {}
        for key, value in data.items():
            try:
                if isinstance(value, str):
                    value = value.format(**namespace_patterns)
                if isinstance(key, str):
                    key = key.format(**namespace_patterns)
            except KeyError:
                # If no namespace match is found, the value or key is left as is
                ...

            formatted_data[key] = value
        return formatted_data
