import argparse
from typing import Optional
from logging import Logger

from kink import inject

from src.umlars_translator.config import SupportedFormat
from src.umlars_translator.core.translator import ModelTranslator
from src.umlars_translator.core.utils.functions import get_enum_members_values
from src.umlars_translator.app.main import run_app


@inject
class CLIManager:
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self._parser = argparse.ArgumentParser(
            description="Tool for translating UML diagrams from external formats into other formats."
        )
        self._logger = logger.getChild(self.__class__.__name__)
        self._add_arguments()

    def _add_supported_formats_argumets(self) -> None:
        self._parser.add_argument(
            "--from-format",
            default=None,
            choices=get_enum_members_values(SupportedFormat),
            help="Choose the format to translate the UML file from",
        )

    def _add_arguments(self) -> None:
        self._add_supported_formats_argumets()
        self._parser.add_argument(
            "--run-server", action="store_true", help="Run the REST API server"
        )

        self._parser.add_argument(
            "file_names", nargs="*", type=str, help="The UML file(s) to be translated"
        )

    def _parse_args(self) -> argparse.Namespace:
        return self._parser.parse_args()

    def run(self) -> None:
        args = self._parse_args()
        if args.run_server:
            self._run_server()
        elif args.file_names:
            self._translate_files(args.file_names, args.from_format)
        else:
            self._parser.print_help()

    def _run_server(self) -> None:
        self._logger.info("Running REST API server...")
        run_app()
        # TODO: Add logic to start the REST API server here

    def _translate_files(self, file_names, from_format) -> None:
        self._logger.info(f"Translating files {file_names} from format {from_format}...")
        translator = ModelTranslator()
        translator.translate(file_paths=file_names, from_format=from_format)
