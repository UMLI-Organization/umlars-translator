import os
from enum import Enum


# LOGGER
APP_LOGGER_NAME = "MESSAGING_LOGGER"
LOG_LEVEL = os.getenv("MESSAGING_LOG_LEVEL", "DEBUG")
LOG_FILE = os.getenv("MESSAGINGE_LOG_FILE", "logs/umlars-messaging.log")


# RABBITMQ
MESSAGE_BROKER_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
MESSAGE_BROKER_PORT = int(os.getenv("RABBITMQ_NODE_PORT", 5672))
MESSAGE_BROKER_USER = os.getenv("RABBITMQ_DEFAULT_USER", "admin")
MESSAGE_BROKER_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS", "admin")
MESSAGE_BROKER_QUEUE_NAME = os.environ.get("RABBITMQ_QUEUE_NAME", "uploaded_files")
MESSAGE_BROKER_PREFETCH_COUNT = 100


class TranslationStatusEnum(str, Enum):
    FINISHED = "finished"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    RUNNING = "running"
