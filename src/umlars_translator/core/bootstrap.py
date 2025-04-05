import os
import logging

from kink import di

from umlars_translator.core import config
from umlars_translator.logger import add_file_handler


def bootstrap_di() -> None:
    main_logger_name = config.LOGGER_BASE_NAME
    main_logs_file = config.LOG_FILE
    main_logger_level = config.LOG_LEVEL

    core_logger = di[logging.Logger].getChild(main_logger_name)
    core_logger.setLevel(main_logger_level)
    add_file_handler(core_logger, main_logs_file, config.LOG_LEVEL)

    di["core_logger"] = core_logger
