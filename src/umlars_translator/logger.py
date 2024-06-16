from logging import getLogger, StreamHandler, Formatter, Logger, FileHandler


def create_logger(level: int | str, logger_name: str, logs_file: str) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()
        
    stream_handler = StreamHandler()
    file_handler = FileHandler(logs_file)
    stream_handler.setLevel(level)
    file_handler.setLevel(level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
