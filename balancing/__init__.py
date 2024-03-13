import logging

from azure.functions import HttpRequest, HttpResponse
from .openai_service import OpenAIService


async def main(req: HttpRequest) -> HttpResponse:    
    service = OpenAIService()
    return HttpResponse(f"Hello, {await service.create_embeddings()}. This HTTP triggered function executed successfully.")