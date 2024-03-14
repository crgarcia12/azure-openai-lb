from openai import AsyncAzureOpenAI
import logging
import asyncio
import random
import os

class OpenAIService:
    clients = [
        AsyncAzureOpenAI(
            api_version = "2023-05-15",
            api_key = os.environ["AZURE_OPENAI_API_KEY_1"],
            azure_endpoint =os.environ["AZURE_OPENAI_ENDPOINT_1"],
            max_retries=0
        ),
        AsyncAzureOpenAI(
            api_version = "2023-05-15",
            api_key = os.environ["AZURE_OPENAI_API_KEY_2"],  
            azure_endpoint =os.environ["AZURE_OPENAI_ENDPOINT_2"],
            max_retries=0
        )
    ]

    number_of_active_calls_per_endpoint = [0,0]

    def __init__(self):
        pass

    def get_openai_client(self):
        min_index = 0
        min_calls = self.number_of_active_calls_per_endpoint[0]

        for i in range(1, len(self.number_of_active_calls_per_endpoint)):
            if self.number_of_active_calls_per_endpoint[i] < min_calls:
                min_index = i
                min_calls = self.number_of_active_calls_per_endpoint[i]

        self.number_of_active_calls_per_endpoint[min_index] += 1
        return (min_index, self.clients[min_index])
    
    async def create_parallel_embeddings(self):
        # Method logic here
        
        tasks = []
        for counter in range(20):
            index, client  = self.get_openai_client()
            task = asyncio.create_task(
                self.create_text_embeddings(index, client, counter))
            tasks.append(task)
            
            logging.info(f"we have used client nuber {index}")

        results = await asyncio.gather(*tasks)
        return results[0]
    

    async def create_text_embeddings(self, client_index, client, counter):
        success = False
        retries = 0
        total_waiting_time = 0
        while success == False:
            try:
                embedding_response = await client.embeddings.create(
                    input="Your text string goeshereYour text string goes hereYour",
                    model="text-embedding-ada-002"
                )
                self.number_of_active_calls_per_endpoint[client_index] -= 1
                success = True
            except Exception as e:
                waiting_time = random.randint(10, 20)
                total_waiting_time += waiting_time
                retries += 1
                logging.info(f"[{counter}] failed with client {client_index}. waiting {waiting_time} seconds")
                await asyncio.sleep(waiting_time)

        logging.info(f"[{counter}] succeeded with client {client_index} and {retries} retries and waiting {total_waiting_time} seconds.")
        return embedding_response.model_dump_json(indent=2)
    