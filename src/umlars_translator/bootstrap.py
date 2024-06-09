import os
from logging import Logger

from kink import di

from umlars_translator.logger import create_logger


def bootstrap_di() -> None:
    main_logger_name = os.getenv("MAIN_LOGGER_NAME", "umlars")
    main_logger_level = os.getenv("LOG_LEVEL", "INFO")
    logger = create_logger(main_logger_level, main_logger_name)

    di[Logger] = logger
