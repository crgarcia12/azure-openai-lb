import logging
import os

from litellm import Router
# we must do litellm.telemetry = False or telemetry will be send to litellm

from azure.functions import HttpRequest, HttpResponse

model_list = [{ # list of model deployments 
    "model_name": "text-embedding-ada-002", # model alias 
    "litellm_params": { # params for litellm completion/embedding call 
        "model": "azure/text-embedding-ada-002", # actual model name
        "api_version": "2023-05-15",
        "api_key": os.get_env("AZURE_OPENAI_API_KEY"),
        "api_base": os.get_env("AZURE_OPENAI_ENDPOINT")
    }
}, {
    "model_name": "text-embedding-ada-002", 
    "litellm_params": { # params for litellm completion/embedding call 
        "model": "azure/text-embedding-ada-002", # actual model name
        "api_version": "2023-05-15",
        "api_key": os.get_env("AZURE_OPENAI_API_KEY"),
        "api_base": os.get_env("AZURE_OPENAI_ENDPOINT")
    }
}]

async def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    global model_list
    os.environ["LITELLM_TELEMETRY"] = "False"
    os.environ["OPENAI_API_VERSION"] = "2023-05-15"

    router = Router(
        fallbacks=[{"azure/text-embedding-ada-002": ["azure/2-text-embedding-ada-002"]},
                   {"azure/2-text-embedding-ada-002": ["azure/text-embedding-ada-002"]}],
        model_list=model_list,
        set_verbose=True,
        debug_level="DEBUG",
        num_retries=0) # you can even add debug_level="DEBUG"
    
    for num in range(1, 11):
        response = await router.aembedding(
            input = "Your text string goes here",
            model= "text-embedding-ada-002",
        )

    #print(response.model_dump_json(indent=2))

    return HttpResponse(f"We have used client: {response.model_dump_json(indent=2)}.")


