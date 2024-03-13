import logging
import os
from openai import AzureOpenAI

from azure.functions import HttpRequest, HttpResponse

clients = [
    AzureOpenAI(
        #api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version = "2023-05-15",
        #azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT") 
        api_key = "cd8db66561b74d42a418b50209b6dbef",
        azure_endpoint ="https://crgar-openai-openai-sw.openai.azure.com/"
    ),
    AzureOpenAI(
        #api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version = "2023-05-15",
        #azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT") 
        api_key = "cd8db66561b74d42a418b50209b6dbef",
        azure_endpoint ="https://crgar-openai-openai-sw.openai.azure.com/"
    )
]

lastthrottling = []

openai_client_index = 0

def get_openai_client():
    global openai_client_index
    global clients
    openai_client_index = (openai_client_index + 1) % len(clients)
    return openai_client_index

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    global clients

    index = get_openai_client()
    client = clients[index]

    for num in range(1, 11):
        response = client.embeddings.create(
            input = "Your text string goes hereYour text string goes hereYour text string goes hereYour text string goes hereYour text string goes here",
            model= "text-embedding-ada-002"
        )

    print(response.model_dump_json(indent=2))

    return HttpResponse(f"We have used client {index}: {response.model_dump_json(indent=2)}.")