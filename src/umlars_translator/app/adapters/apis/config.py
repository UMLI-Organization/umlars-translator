import os


# LOGGER
LOGGER_NAME = "API_CONNECTOR_LOGGER"
LOG_LEVEL = os.getenv("EXTERNAL_APIS_LOG_LEVEL", "WARNING")
LOG_FILE = os.getenv("EXTERNAL_APIS_LOG_FILE", "logs/umlars-external-apis.log")
