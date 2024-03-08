import logging
import os

from litellm import Router

from azure.functions import HttpRequest, HttpResponse

model_list = [{ # list of model deployments 
    "model_name": "text-embedding-ada-002", # model alias 
    "litellm_params": { # params for litellm completion/embedding call 
        "model": "azure/text-embedding-ada-002", # actual model name
        "api_key": "cd8db66561b74d42a418b50209b6dbef",
        "api_base":"https://crgar-openai-openai-sw.openai.azure.com/"
    }
}, {
    "model_name": "text-embedding-ada-002", 
    "litellm_params": { # params for litellm completion/embedding call 
        "model": "azure/text-embedding-ada-002", # actual model name
        "api_key": "cd8db66561b74d42a418b50209b6dbef",
        "api_base":"https://crgar-openai-openai-sw.openai.azure.com/"
    }
}]

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    global model_list

    router = Router(model_list=model_list)
    response = router.embedding(
        input = "Your text string goes here",
        model= "text-embedding-ada-002"
    )

    print(response.model_dump_json(indent=2))

    return HttpResponse(f"We have used client: {response.model_dump_json(indent=2)}.")