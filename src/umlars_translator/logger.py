import os
from logging import getLogger, StreamHandler, Formatter, Logger, FileHandler


def get_default_formatter() -> Formatter:
    return Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def add_file_handler(logger: Logger, logs_file: str, level: int | str) -> None:
    os.makedirs(os.path.dirname(logs_file), exist_ok=True)
    file_handler = FileHandler(logs_file)
    file_handler.setLevel(level)
    formatter = get_default_formatter()
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def add_stream_handler(logger: Logger, level: int | str) -> None:
    stream_handler = StreamHandler()
    stream_handler.setLevel(level)
    formatter = get_default_formatter()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def create_logger(level: int | str, logger_name: str, logs_file: str, stream_logs: bool = True) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    add_file_handler(logger, logs_file, level)

    if stream_logs:
        add_stream_handler(logger, level)

    return logger
