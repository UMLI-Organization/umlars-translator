import importlib
from logging import Logger
from typing import Dict, Iterator, Optional, Any

from kink import inject


@inject
class ExtensionsManager:
    """
    Class used to manage extensions of the application. It allows to load plugins from directories and filter them by categories.
    Fasade for yapsy.PluginManager. 
    """
    def __init__(self, extensions_modules_groups_names: Optional[Iterator[str]]=None, logger: Optional[Logger] = None) -> None:
        self._logger = logger
        self._extensions_modules_groups_names = extensions_modules_groups_names
        self._extensions_modules = []

    def activate_extensions(self, extensions_modules_groups_names: Optional[Iterator[str]]=None) -> None:
        if extensions_modules_groups_names is None:
            if self._extensions_modules_groups_names is None:
                self._logger.error("No extensions modules groups names provided.")
                raise ValueError("No extensions modules groups names provided.")

            extensions_modules_groups_names = self._extensions_modules_groups_names

        entry_points = importlib.metadata.entry_points()

        for extension_module_group_name in extensions_modules_groups_names:
            if extension_module_group_name in entry_points:
                for entry_point in entry_points[extension_module_group_name]:
                    plugin_class = entry_point.load()
                    self._logger.info(f"Loaded plugin's dir: {dir(plugin_class)}")
                    
                    # plugin_class.load_module()

                    self._logger.info(f"Loaded plugin: {plugin_class.__name__}")