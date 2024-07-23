import os
import logging

from kink import di

from src.umlars_translator.core import config
from src.umlars_translator.logger import add_file_handler


def bootstrap_di() -> None:
    main_logger_name = config.LOGGER_BASE_NAME
    main_logs_file = os.getenv("CORE_LOG_FILE", config.LOG_FILE)
    main_logger_level = os.getenv("CORE_LOG_LEVEL", config.LOG_LEVEL)

    core_logger = di[logging.Logger].getChild(main_logger_name)
    core_logger.setLevel(main_logger_level)
    add_file_handler(core_logger, main_logs_file, config.LOG_LEVEL)

    di["core_logger"] = core_logger
