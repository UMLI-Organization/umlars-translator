import os
import logging

from kink import di

from umlars_translator.app.adapters.message_brokers import config
from umlars_translator.logger import add_file_handler


def bootstrap_di() -> None:
    logger_name = config.APP_LOGGER_NAME
    logs_file = config.LOG_FILE
    logger_level = config.LOG_LEVEL

    messaging_logger = di[logging.Logger].getChild(logger_name)
    messaging_logger.setLevel(logger_level)
    add_file_handler(messaging_logger, logs_file, config.LOG_LEVEL)

    di["messaging_logger"] = messaging_logger
