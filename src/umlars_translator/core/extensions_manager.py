import importlib.metadata
from logging import Logger
from typing import Iterator, Optional

from kink import inject


@inject
class ExtensionsManager:
    """
    Class used to manage extensions of the application. It allows to load plugins from directories and filter them by categories.
    """

    def __init__(
        self,
        extensions_modules_groups_names: Optional[Iterator[str]] = None,
        core_logger: Optional[Logger] = None,
    ) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        self._extensions_modules_groups_names = extensions_modules_groups_names

    def activate_extensions(
        self, extensions_modules_groups_names: Optional[Iterator[str]] = None
    ) -> None:
        if extensions_modules_groups_names is None:
            if self._extensions_modules_groups_names is None:
                self._logger.error("No extensions modules groups names provided.")
                raise ValueError("No extensions modules groups names provided.")

            extensions_modules_groups_names = self._extensions_modules_groups_names

        entry_points = importlib.metadata.entry_points()
        self._logger.info(f"Entry points: {len(entry_points)}")

        for extension_module_group_name in extensions_modules_groups_names:
            self._logger.info(f"Loading plugins for group: {extension_module_group_name}")

            if extension_module_group_name in entry_points:
                self._logger.info(f"Found plugins for group: {extension_module_group_name}")
                for entry_point in entry_points[extension_module_group_name]:
                    self._logger.info(f"Loading plugin: {entry_point.name}")
                    try:
                        plugin_class = entry_point.load()
                        self._logger.info(f"Loaded plugin: {plugin_class.__name__}")
                    except ModuleNotFoundError as ex:
                        error_message = (
                            f"Plugin {entry_point.name} could not be loaded."
                            f"Check pyproject.toml tool.poetry section for the plugin path. Set the plugin path to the correct value and run poetry install."
                            f"Error: : {ex}"
                        )
                        self._logger.error(error_message)
                        raise ModuleNotFoundError(error_message) from ex
