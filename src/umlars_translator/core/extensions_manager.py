import importlib.metadata
from logging import Logger
from typing import Iterator, Optional

from kink import inject


@inject
class ExtensionsManager:
    """
    Class used to manage extensions of the application. It allows to load plugins from directories and filter them by categories.
    Manages application extensions (plugins) via Python entry points.
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

        all_entry_points = importlib.metadata.entry_points()
        self._logger.info(f"Entry points loaded: {len(all_entry_points)}")

        for group in extensions_modules_groups_names:
            self._logger.info(f"Loading plugins for group: {group}")

            # Correct: filter entry points for the specific group
            matching_eps = all_entry_points.select(group=group)

            if not matching_eps:
                self._logger.warning(f"No plugins found for group: {group}")
                continue

            self._logger.info(f"Found {len(matching_eps)} plugins for group: {group}")

            for entry_point in matching_eps:
                self._logger.info(f"Loading plugin: {entry_point.name}")
                try:
                    plugin_class = entry_point.load()
                    self._logger.info(f"Loaded plugin: {plugin_class.__name__}")
                except ModuleNotFoundError as ex:
                    msg = (
                        f"Plugin '{entry_point.name}' could not be loaded. "
                        f"Check your [tool.poetry.plugins] section in pyproject.toml.\n"
                        f"Error: {ex}"
                    )
                    self._logger.error(msg)
                    raise ModuleNotFoundError(msg) from ex
