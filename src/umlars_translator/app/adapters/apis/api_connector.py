from typing import NamedTuple, Optional
from abc import ABC, abstractmethod
import logging

from kink import inject


class ServiceConnectionData(NamedTuple):
    jwt: str


@inject
class ApiConnector(ABC):
    _services_data = {}

    @classmethod
    def get_service_data(cls, service_url: str) -> ServiceConnectionData:
        return cls._services_data.get(service_url)

    def __init__(self, service_url: str, service_data: Optional[ServiceConnectionData] = None, api_connector_logger: Optional[logging.Logger] = None) -> None:
        self._logger = api_connector_logger.getChild(self.__class__.__name__)
        self._service_url = service_url
        self.service_data = service_data

    @property
    def service_data(self) -> ServiceConnectionData:
        return self._service_data

    @service_data.setter
    def service_data(self, data: ServiceConnectionData | None):
        self._service_data = data
        self.__class__._services_data[self._service_url] = data

    @abstractmethod
    async def authenticate(self, user: dict, create_token_endpoint: Optional[str] = None, create_token_url: Optional[str] = None) -> dict:
        ...

    @abstractmethod
    async def get_data(self, url: str) -> dict:
        ...

    @abstractmethod
    async def post_data(self, url: str, data: dict) -> dict:
        ...
