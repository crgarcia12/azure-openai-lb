from openai import AsyncAzureOpenAI
import asyncio
import random
import os
import timeit

clients = [
    AsyncAzureOpenAI(
        api_version = "2023-05-15",
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
        max_retries=5
    ),
    AsyncAzureOpenAI(
        api_version = "2023-05-15",
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT"),
        max_retries=5
    )
]

number_of_active_calls_per_endpoint = [0,0]
execution_count = 0

class OpenAIService:

    global clients
    global number_of_active_calls_per_endpoint

    def __init__(self):
        pass

    def get_openai_client(self):
        min_index = min(range(len(number_of_active_calls_per_endpoint)), key=number_of_active_calls_per_endpoint.__getitem__)
        return min_index, clients[min_index]
    
    async def create_embeddings(self, operation_id):
        start_time = timeit.default_timer()

        global execution_count
        execution_count += 1

        # Randomly select an OAI client
        openai_client_index, client  = self.get_openai_client()
        print(f"[op: {operation_id}][exec: {execution_count}][oai: {openai_client_index}] Operation started")

        # Create embeddings
        number_of_active_calls_per_endpoint[openai_client_index] += 1
        embedding_response = await client.embeddings.create(
            input="Your text string goeshereYour text string goes hereYour",
            model="text-embedding-ada-002"
        )
        number_of_active_calls_per_endpoint[openai_client_index] -= 1

        print(f"[op: {operation_id}][exec: {execution_count}][oai: {openai_client_index}] Operation finished in {timeit.default_timer() - start_time}")

        #return embedding_response.model_dump_json(indent=2)
        return f"[op: {operation_id}][exec: {execution_count}][oai: {openai_client_index}] Operation finished {timeit.default_timer() - start_time}"

    # async def create_embeddings(self, client_index, client, execution_count):
    #     success = False
    #     retries = 0
    #     total_waiting_time = 0
    #     while success == False:
    #         try:
    #             embedding_response = await client.embeddings.create(
    #                 input="Your text string goeshereYour text string goes hereYour",
    #                 model="text-embedding-ada-002"
    #             )
    #             self.number_of_active_calls_per_endpoint[client_index] -= 1
    #             success = True
    #         except Exception as e:
    #             waiting_time = random.randint(10, 20)
    #             total_waiting_time += waiting_time
    #             retries += 1
    #             print(f"[{execution_count}] failed with client {client_index}. waiting {waiting_time} seconds")
    #             await asyncio.sleep(waiting_time)

    #     print(f"[{execution_count}] succeeded with client {client_index} and {retries} retries and waiting {total_waiting_time} seconds.")
    #     return embedding_response.model_dump_json(indent=2)
    