import argparse

from umlars_translator.core.deserializer.config import supported_formats


class CLIManager:
    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description="Tool for translating UML diagrams from external formats into other formats."
        )
        self._add_arguments()

    def _add_supported_formats_argumets(self):
        self._parser.add_argument(
            "--from-format",
            default=None,
            choices=supported_formats.keys(),
            help="Choose the format to translate the UML file from",
        )

    def _add_arguments(self):
        self._add_supported_formats_argumets()
        self._parser.add_argument(
            "--run-server", action="store_true", help="Run the REST API server"
        )

        self._parser.add_argument(
            "file_names", nargs="*", type=str, help="The UML file(s) to be translated"
        )

    def _parse_args(self):
        return self._parser.parse_args()

    def run(self):
        args = self._parse_args()
        if args.run_server:
            self._run_server()
        elif args.file_names:
            self._translate_files(args.file_names, args.from_format)
        else:
            self._parser.print_help()

    def _run_server(self):
        print("Running REST API server...")
        # TODO: Add logic to start the REST API server here

    def _translate_files(self, file_names, from_format):
        print(f"Translating files {file_names} to {from_format}...")
        # TODO: Add logic to translate the file here
