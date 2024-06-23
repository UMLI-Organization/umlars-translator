import os


DB_NAME = os.getenv("MONGO_INITDB_DATABASE")
DB_COLLECTION_NAME = os.getenv("MONGO_DB_COLLECTION_NAME", "UML_MODEL")

MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
# For tests outside the docker: MONGO_HOST = "127.0.0.1"
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
DB_CONN_STR = f"mongodb://{(MONGO_INITDB_ROOT_USERNAME)}:{(MONGO_INITDB_ROOT_PASSWORD)}@{(MONGO_HOST)}:{(MONGO_PORT)}/{(MONGO_INITDB_DATABASE)}?authSource=admin"


# LOGGER
APP_LOGGER_NAME = "APP_LOGGER"
LOG_LEVEL = "DEBUG"
LOG_FILE = "umlars=server.log"
