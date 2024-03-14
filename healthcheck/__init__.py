import logging
import os

from azure.functions import HttpRequest, HttpResponse

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return HttpResponse(f"code version: 0.4. OAI endpoint: {os.environ['AZURE_OPENAI_ENDPOINT']}")
