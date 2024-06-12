from logging import getLogger, StreamHandler, Formatter, Logger


def create_logger(level: int | str, logger_name: str) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(level)
    handler = StreamHandler()
    handler.setLevel(level)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
