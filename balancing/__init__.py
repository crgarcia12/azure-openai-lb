import logging

from azure.functions import HttpRequest, HttpResponse
from .openai_service import OpenAIService


async def main(req: HttpRequest) -> HttpResponse:    
    service = OpenAIService()
    return HttpResponse(f"{await service.create_parallel_embeddings()}")