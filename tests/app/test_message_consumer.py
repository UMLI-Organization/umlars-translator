import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch

from aio_pika import IncomingMessage
from pydantic import ValidationError

from src.umlars_translator.app.exceptions import QueueUnavailableError, InputDataError
from src.umlars_translator.app.adapters.message_brokers.rabbitmq_message_producer import RabbitMQProducer
from src.umlars_translator.app.dtos.messages import ModelToTranslateMessage
from src.umlars_translator.app.adapters.apis.rest_api_connector import RestApiConnector
from src.umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository
from src.umlars_translator.core.translator import ModelTranslator
from src.umlars_translator.app.adapters.message_brokers.rabbitmq_message_consumer import RabbitMQConsumer


@pytest.fixture
def mock_dependencies():
    repository_api_connector = AsyncMock(spec=RestApiConnector)
    uml_model_repository = AsyncMock(spec=UmlModelRepository)
    message_producer = AsyncMock(spec=RabbitMQProducer)
    model_translator = AsyncMock(spec=ModelTranslator)
    logger = MagicMock()
    return {
        'repository_api_connector': repository_api_connector,
        'uml_model_repository': uml_model_repository,
        'message_producer': message_producer,
        'model_translator': model_translator,
        'logger': logger,
    }

@pytest.fixture
def rabbitmq_consumer(mock_dependencies):
    return RabbitMQConsumer(
        queue_name='test_queue',
        rabbitmq_host='localhost',
        repository_api_connector=mock_dependencies['repository_api_connector'],
        uml_model_repository=mock_dependencies['uml_model_repository'],
        messaging_logger=mock_dependencies['logger'],
        model_translator=mock_dependencies['model_translator'],
        message_producer=mock_dependencies['message_producer']
    )


@pytest.mark.asyncio
async def test_connect_channel(rabbitmq_consumer):
    with patch('aio_pika.connect_robust', new=AsyncMock()) as mock_connect_robust:
        await rabbitmq_consumer.connect_channel()
        mock_connect_robust.assert_called_once()
        assert rabbitmq_consumer._channel is not None
        assert rabbitmq_consumer._queue is not None
