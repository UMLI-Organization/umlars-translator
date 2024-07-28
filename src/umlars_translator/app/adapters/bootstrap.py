from kink import di

from src.umlars_translator.app.adapters.apis.rest_api_connector import RestApiConnector
from src.umlars_translator.app import config


def bootstrap_di() -> None:
    di["repository_api_connector"] = RestApiConnector(config.REPOSITORY_API_URL)
