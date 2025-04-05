import argparse
from typing import Optional
from logging import Logger
import os

from kink import inject

from umlars_translator.config import SupportedFormat
from umlars_translator.core.translator import ModelTranslator
from umlars_translator.core.utils.functions import get_enum_members_values
from umlars_translator.app.main import run_app


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

        self._parser.add_argument(
            "--join", action="store_true", help="Join all files data into one model"
        )

    def _parse_args(self) -> argparse.Namespace:
        return self._parser.parse_args()

    def run(self) -> None:
        args = self._parse_args()
        if args.run_server:
            self._run_server()
        elif args.file_names:
            self._translate_files(args.file_names, args.from_format, args.join)
        else:
            self._parser.print_help()

    def _run_server(self) -> None:
        self._logger.info("Running REST API server...")
        run_app()

    def _translate_files(self, file_names, from_format, join_into_one_model) -> None:
        self._logger.info(f"Translating files {file_names} from format {from_format}...")
        translator = ModelTranslator()
        current_working_directory = os.getcwd()
        output_directory = os.path.join(current_working_directory, "output")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self._logger.info(f"Output directory: {output_directory}")

        if join_into_one_model:
            for file_name in file_names:
                file_base_name = os.path.basename(file_name)
                self._logger.info(f"Translating file {file_base_name}...")
                translated_data = translator.translate(file_name=file_name, from_format=from_format, clear_model_afterwards=False)
            
            output_file_name = f"{file_base_name}_merged_translated.umj"
            output_location = os.path.join(output_directory, output_file_name)
            self._logger.info(f"Files translated to {output_location}")
            with open(output_location, "w") as output_file:
                output_file.write(translated_data)
        
        else:        
            for file_name in file_names:
                file_base_name = os.path.basename(file_name)
                self._logger.info(f"Translating file {file_base_name}...")
                
                output_file_name = f"{file_base_name}_translated.umj"
                output_location = os.path.join(output_directory, output_file_name)
                translated_data = translator.translate(file_name=file_name, from_format=from_format, clear_model_afterwards=True)
                with open(output_location, "w") as output_file:
                    output_file.write(translated_data)

                self._logger.info(f"File {file_name} translated to {output_location}")

            
