import aiohttp
from typing import NamedTuple


class ServiceConnectionData(NamedTuple):
    jwt: str


class ServiceConnector:
    __services_data = {}

    @staticmethod
    def get_service_data(service_url: str) -> ServiceConnectionData:
        return ServiceConnector.__services_data.get(service_url)

    def __init__(self, service_url: str, create_token_endpoint: str) -> None:
        self._service_url = service_url
        self._create_token_url = f"{self._service_url}/{create_token_endpoint}"
        self._service_data: ServiceConnectionData = None

    @property
    def service_data(self) -> ServiceConnectionData:
        return self._service_data

    @service_data.setter
    def service_data(self, data: ServiceConnectionData):
        self._service_data = data
        self.__class__.__services_data[self._service_url] = data

    async def authenticate(self, user: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self._create_token_url, json=user) as response:
                response = await response.json()
                self.service_data = ServiceConnectionData(jwt=response["access"])
                return response
