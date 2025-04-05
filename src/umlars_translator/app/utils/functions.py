from typing import Callable, Type
import asyncio
from functools import wraps

from umlars_translator.app.exceptions import NotYetAvailableError, ServiceConnectionError


def retry_async(reconnect_attempts: int = 5, sleep_seconds_between_recconnects: int = 5, exception_class_raised_when_all_attempts_failed: Type["Exception"] = ServiceConnectionError) -> None:
    def wrapper(function_to_attempt: Callable) -> Callable:
        @wraps(function_to_attempt)
        async def inner(*args, **kwargs):
            max_reconnect_attempt_number = reconnect_attempts - 1
            for reconnect_attempt_number in range(reconnect_attempts):
                try:
                    return await function_to_attempt(*args, **kwargs)
                except NotYetAvailableError as ex:
                    if reconnect_attempt_number == max_reconnect_attempt_number:
                        raise exception_class_raised_when_all_attempts_failed(str(ex)) from ex
                    await asyncio.sleep(sleep_seconds_between_recconnects)

        return inner
    return wrapper
