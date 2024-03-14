from openai import AsyncAzureOpenAI
import logging
import os
import timeit
import json

clients = [
    AsyncAzureOpenAI(
        api_version = "2023-05-15",
        api_key = os.environ["AZURE_OPENAI_API_KEY_1"],
        azure_endpoint =os.environ["AZURE_OPENAI_ENDPOINT_1"],
        max_retries=5
    ),
    AsyncAzureOpenAI(
        api_version = "2023-05-15",
        api_key = os.environ["AZURE_OPENAI_API_KEY_2"],
        azure_endpoint =os.environ["AZURE_OPENAI_ENDPOINT_2"],
        max_retries=5
    )
]

# Track the number of active calls for each endpoint
number_of_active_calls_per_endpoint = [0] * len(clients)

class AsyncAzureOpenAIContext: 
    def __init__ (self, operation_id, execution_count):
        global number_of_active_calls_per_endpoint

        self.operation_id = operation_id
        self.execution_count = execution_count
        self.start_time = timeit.default_timer()

        # Select the least used OAI client 
        self._selected_client_index, self._selected_client = self._get_openai_client()
        number_of_active_calls_per_endpoint[self._selected_client_index] += 1

        # Print statistics
        logging.info(f"[op: {operation_id}][exec: {execution_count}][oai: {self._selected_client_index}] Selected OpenAI client: {self._selected_client_index}")
        logging.info(f"oai state: [{json.dumps(number_of_active_calls_per_endpoint)}]")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global number_of_active_calls_per_endpoint
        number_of_active_calls_per_endpoint[self._selected_client_index] -= 1
        logging.info(f"oai state: [{json.dumps(number_of_active_calls_per_endpoint)}]")
        logging.info(f"[op: {self.operation_id}][exec: {self.execution_count}][oai: {self._selected_client_index}] Finished OpenAI client. Duration: {int((timeit.default_timer() - self.start_time)*1000)} msec")
    
    async def create_embedding(self, input_text):
        return await self._selected_client.embeddings.create(
            input=input_text,
            model="text-embedding-ada-002"
        )

    def _get_openai_client(self):
        # get the client that has the least active calls
        min_index = min(
            range(len(number_of_active_calls_per_endpoint)),
            key=number_of_active_calls_per_endpoint.__getitem__)
        return min_index, clients[min_index]