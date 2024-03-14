import logging
import os
from azure.functions import HttpRequest, HttpResponse

from langchain_openai import AzureOpenAIEmbeddings
from openai import RateLimitError

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    embeddings_model = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key =os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment="text-embedding-ada-002",
        #openai_api_version="2023-05-15",
    )

    # embeddings_model.with_fallbacks([embeddings_model])

    for num in range(1, 11):
        embeddings = embeddings_model.embed_documents(
            [
                "Hi there!",
                "Oh, hello!",
                "What's your name?",
                "My friends call me World",
                "Hello World!"
            ]
        )

    response = len(embeddings[0])
    logging.info(response)
    return HttpResponse(f"Embeddings calculated: {response}")
    