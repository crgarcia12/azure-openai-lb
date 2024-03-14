import logging

from azure.functions import ServiceBusMessage
from .openai_service import OpenAIService

async def main(msg: ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s', msg.get_body().decode('utf-8'))
    operation_id = int(msg.get_body().decode('utf-8'))
    service = OpenAIService()
    response = await service.create_embeddings(operation_id)
    logging.info(f"{response}")