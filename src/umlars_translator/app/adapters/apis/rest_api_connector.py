from typing import Optional
import aiohttp

from src.umlars_translator.app.adapters.apis.api_connector import ApiConnector, ServiceConnectionData
from src.umlars_translator.app.utils.functions import retry_async
from src.umlars_translator.app.exceptions import ServiceConnectionError, NotYetAvailableError


class RestApiConnector(ApiConnector):
    @retry_async(exception_class_raised_when_all_attempts_failed=ServiceConnectionError)
    async def authenticate(self, user: dict, create_token_endpoint: Optional[str] = None, create_token_url: Optional[str] = None) -> dict:
        create_token_url = create_token_url if create_token_url is not None else f"{self._service_url}/{create_token_endpoint}"
        try:
            response = await self.post_data(create_token_url, user, add_auth_headers=False)
            self.service_data = ServiceConnectionData(jwt=response["access"])
            return response
        except aiohttp.ClientConnectorError as ex:
            error_message = f"Failed to authenticate - unable to connect to the service: {ex}"
            self._logger.error(error_message)
            raise NotYetAvailableError(error_message) from ex

    async def get_data(self, url: str, add_auth_headers: bool = True) -> dict:
        headers = dict()
        self._logger.error(f"self.service_data: {self.service_data}")
        if add_auth_headers:
            jwt_token = self.service_data.jwt
            headers.update({"Authorization": f"Bearer {jwt_token}"})

        async with aiohttp.ClientSession() as session:
            # In case of any problems with JWT - BasicAuth code works as well
            # async with aiohttp_client.get(models_repository_api_url, auth=aiohttp.BasicAuth(app_config.REPOSITORY_SERVICE_USER, app_config.REPOSITORY_SERVICE_PASSWORD)) as response:
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def post_data(self, url: str, data: dict, add_auth_headers: bool = True) -> dict:
        headers = dict()
        if add_auth_headers:
            jwt_token = self.service_data.jwt
            headers.update({"Authorization": f"Bearer {jwt_token}"})

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                return await response.json()
