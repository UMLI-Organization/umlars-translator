import os
import importlib
from logging import Logger
from typing import Dict, List, Optional, Any

from kink import inject


@inject
class ExtensionsManager:
    """
    Class used to manage extensions of the application. It allows to load plugins from directories and filter them by categories.
    Fasade for yapsy.PluginManager. 
    """
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self._logger = logger
        self._extensions_modules = []

    def activate_extensions(self, directories_with_extensions: List[str]) -> None:
        for directory_path in directories_with_extensions:
            self._logger.info(f"Loading extensions from directory: {directory_path}")
            self.load_extensions_from_directory(directory_path)

    def load_extensions_from_directory(self, directory_path: str) -> None:
        """
        Method used to load extensions from a directory.
        """
        abs_directory_path = os.path.abspath(directory_path)
        for path, subdirs, file_names in os.walk(abs_directory_path):
            for file_name in file_names:
                if file_name.endswith(".py") and file_name != "__init__.py":
                    relative_path = os.path.relpath(path, abs_directory_path)
                    module_name = os.path.join(directory_path, relative_path, file_name[:-3]).replace(os.sep, ".")
                    self._logger.info(f"Loading module: {module_name}")

                    try:
                        module = importlib.import_module(module_name)
                        self._extensions_modules.append(module)
                    except Exception as e:
                        self._logger.error(f"Failed to load module {module_name}: {e}")

    # def load_plugins(self) -> List[Any]:
    #     plugins = []
    #     for entry_point in pkg_resources.iter_entry_points('my_app.plugins'):
    #         plugin_class = entry_point.load()
    #         plugins.append(plugin_class())
    #     return plugins
