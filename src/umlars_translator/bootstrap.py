import os
from logging import Logger

from kink import di

from umlars_translator.logger import create_logger
from umlars_translator import config


def bootstrap_di() -> None:
    main_logger_name = config.LOGGER_BASE_NAME
    main_logs_file = os.getenv("LOG_FILE", config.LOG_FILE)
    main_logger_level = os.getenv("LOG_LEVEL", config.LOG_LEVEL)
    logger = create_logger(main_logger_level, main_logger_name, main_logs_file)

    di[Logger] = logger
