from logging import getLogger, StreamHandler, Formatter, Logger, FileHandler


def create_logger(level: int | str, logger_name: str, logs_file: str, stream_logs: bool = True) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = FileHandler(logs_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if stream_logs:
        stream_handler = StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
