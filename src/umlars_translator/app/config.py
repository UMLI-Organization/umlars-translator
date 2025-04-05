import os


DB_NAME = os.getenv("MONGO_INITDB_DATABASE")
DB_COLLECTION_NAME = os.getenv("MONGO_DB_COLLECTION_NAME", "UML_MODEL")

MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST', "127.0.0.1")
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
DB_CONN_STR = f"mongodb://{(MONGO_INITDB_ROOT_USERNAME)}:{(MONGO_INITDB_ROOT_PASSWORD)}@{(MONGO_HOST)}:{(MONGO_PORT)}/{(MONGO_INITDB_DATABASE)}?authSource=admin"

# LOGGER
APP_LOGGER_NAME = "APP_LOGGER"
LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "WARNING")
LOG_FILE = os.getenv("APP_LOG_FILE", "logs/umlars-server.log")

# RABBITMQ
MESSAGE_BROKER_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
MESSAGE_BROKER_QUEUE_UPLOADED_FILES_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "uploaded_files")


# MAIN REPOSITORY SERVICE
REPOSITORY_SERVICE_HOST = os.getenv("REPOSITORY_SERVICE_HOST", "umlars-backend-backend-1")
REPOSITORY_SERVICE_PORT = os.getenv("REPOSITORY_SERVICE_PORT", 8000)
REPOSITORY_SERVICE_MODELS_ENDPOINT = os.getenv("REPOSITORY_SERVICE_MODELS_ENDPOINT", "model-files")
REPOSITORY_SERVICE_CREATE_JWT_ENDPOINT = os.getenv("REPOSITORY_SERVICE_CREATE_JWT_ENDPOINT", "auth/jwt/create")
API_VERSION = "v1"
REPOSITORY_API_URL = f"http://{REPOSITORY_SERVICE_HOST}:{REPOSITORY_SERVICE_PORT}/api/{API_VERSION}"
REPOSITORY_SERVICE_USER = os.getenv("REPOSITORY_SERVICE_USER", "admin")
REPOSITORY_SERVICE_PASSWORD = os.getenv("REPOSITORY_SERVICE_PASSWORD", "admin")
