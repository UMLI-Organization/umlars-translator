import os


"""
Core logger settings
"""
SYSTEM_NAME = "Core"
LOGGER_BASE_NAME = SYSTEM_NAME

LOG_LEVEL = os.getenv("CORE_LOG_LEVEL", "WARNING")
LOG_FILE = os.getenv("CORE_LOG_FILE", "logs/umlars-core.log")
