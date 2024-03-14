import logging
import os

from azure.functions import HttpRequest, HttpResponse

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return HttpResponse(f"code version: 0.10. OAI endpoint: {os.environ['AZURE_OPENAI_ENDPOINT_1']} and {os.environ['AZURE_OPENAI_ENDPOINT_2']}")
