from typing import Optional
import aiohttp

from umlars_translator.app.adapters.apis.api_connector import ApiConnector, ServiceConnectionData
from umlars_translator.app.utils.functions import retry_async
from umlars_translator.app.exceptions import ServiceConnectionError, NotYetAvailableError, ExternalServiceOperationError, ServiceUnexpectedBehaviorError


class RestApiConnector(ApiConnector):
    @retry_async(exception_class_raised_when_all_attempts_failed=ServiceConnectionError)
    async def authenticate(self, user: dict, create_token_endpoint: Optional[str] = None, create_token_url: Optional[str] = None) -> dict:
        create_token_url = create_token_url if create_token_url is not None else f"{self._service_url}/{create_token_endpoint}"
        try:
            response = await self.post_data(create_token_url, user, add_auth_headers=False)
            try:
                new_service_data = ServiceConnectionData(jwt=response["access"])
                self.service_data = new_service_data
            except KeyError as ex:
                error_message = f"Failed to authenticate - missing JWT token in the response: {response}. Error: {ex}"
                self._logger.error(error_message)
                raise ServiceUnexpectedBehaviorError(error_message) from ex
            return response
        except aiohttp.ClientConnectorError as ex:
            error_message = f"Failed to authenticate - unable to connect to the service: {ex}"
            self._logger.error(error_message)
            raise NotYetAvailableError(error_message) from ex

    async def get_data(self, url: str, add_auth_headers: bool = True, add_tech_request_params: bool = True) -> dict:
        headers = dict()
        query_params = dict()
        if add_auth_headers:
            jwt_token = self.service_data.jwt
            headers.update({"Authorization": f"Bearer {jwt_token}"})

        if add_tech_request_params:
            query_params.update({"format": "json"})
            query_params_str = "&".join([f"{key}={value}" for key, value in query_params.items()])
            url = f"{url}?{query_params_str}"

        async with aiohttp.ClientSession() as session:
            # In case of any problems with JWT - BasicAuth code works as well
            # async with aiohttp_client.get(models_repository_api_url, auth=aiohttp.BasicAuth(app_config.REPOSITORY_SERVICE_USER, app_config.REPOSITORY_SERVICE_PASSWORD)) as response:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    response_text = await response.read()
                    error_message = f"Failed to get data - unexpected response status: {response.status}."
                    self._logger.error(error_message + f" Response: {response_text}")
                    raise ExternalServiceOperationError(error_message)
                else:
                    try:
                        return await response.json()
                    except aiohttp.client_exceptions.ContentTypeError as ex:
                        response_text = await response.read()
                        error_message = f"Failed to get data - unexpected response content type: {response.content_type}. Error: {ex}"
                        self._logger.error(error_message + f" Response: {response_text}")
                        raise ServiceUnexpectedBehaviorError(error_message) from ex

    async def post_data(self, url: str, data: dict, add_auth_headers: bool = True, add_tech_request_params: bool = True) -> dict:
        headers = dict()
        query_params = dict()
        if add_auth_headers:
            jwt_token = self.service_data.jwt
            headers.update({"Authorization": f"Bearer {jwt_token}"})

        if add_tech_request_params:
            query_params.update({"format": "json"})
            query_params_str = "&".join([f"{key}={value}" for key, value in query_params.items()])
            url = f"{url}?{query_params_str}"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status != 200:
                    response_text = await response.read()
                    error_message = f"Failed to get data - unexpected response status: {response.status}."
                    self._logger.error(error_message + f" Response: {response_text}")
                    raise ExternalServiceOperationError(error_message)
                else:
                    try:
                        return await response.json()
                    except aiohttp.client_exceptions.ContentTypeError as ex:
                        response_text = await response.read()
                        error_message = f"Failed to get data - unexpected response content type: {response.content_type}. Error: {ex}"
                        self._logger.error(error_message + f" Response: {response_text}")
                        raise ServiceUnexpectedBehaviorError(error_message) from ex
