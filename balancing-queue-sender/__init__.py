import logging
import os
from azure.functions import HttpRequest, HttpResponse
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

batch_initial_number = 100

async def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    NAMESPACE_CONNECTION_STR = os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"]

    global batch_initial_number
    batch_initial_number += 100

    async with ServiceBusClient.from_connection_string(conn_str=NAMESPACE_CONNECTION_STR, logging_enable=True) as servicebus_client:

        # Get a Queue Sender object to send messages to the queue
        sender = servicebus_client.get_queue_sender(queue_name="embeddingqueue")
        async with sender:                    
            batch_message = await sender.create_message_batch()
            for operation_id in range(batch_initial_number, batch_initial_number + 10):
                try:
                    # Add a message to the batch
                    batch_message.add_message(ServiceBusMessage(str(operation_id)))
                except ValueError:
                    # ServiceBusMessageBatch object reaches max_size.
                    # New ServiceBusMessageBatch object can be created here to send more data.
                    break
            # Send the batch of messages to the queue
            await sender.send_messages(batch_message)
    logging.info("Sent a batch of 10 messages")

    return HttpResponse(f"Sent 10 messages to the queue")
