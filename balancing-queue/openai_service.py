from openai import AsyncAzureOpenAI
import timeit
import logging

from .async_azure_openai_context import AsyncAzureOpenAIContext

# For statistics purposes
execution_count = 0

class OpenAIService:
    def __init__(self):
        pass

    async def create_embeddings(self, operation_id):
        global execution_count
        global number_of_active_calls_per_endpoint

        # Print statistics
        start_time = timeit.default_timer()
        execution_count += 1

        # Randomly select an OAI client
        logging.info(f"[op: {operation_id}][exec: {execution_count}] Operation started")

        # Create embeddings. We use a 'with' context to be able to track some statistics and send it to the console
        with AsyncAzureOpenAIContext(operation_id, execution_count) as client:
            embedding_response = await client.create_embedding(
                "Your text string goeshereYour text string goes hereYour",
            )

        logging.info(f"[op: {operation_id}][exec: {execution_count}]Operation finished in {int((timeit.default_timer() - start_time)*1000)}")

        #return embedding_response.model_dump_json(indent=2)
        return f"[op: {operation_id}][exec: {execution_count}]Operation finished {int((timeit.default_timer() - start_time)*1000)}"