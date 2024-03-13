from openai import AsyncAzureOpenAI

class OpenAIService:
    clients = [
        AsyncAzureOpenAI(
            #api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = "2023-05-15",
            #azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT") 
            api_key = "cd8db66561b74d42a418b50209b6dbef",
            azure_endpoint ="https://crgar-openai-openai-sw.openai.azure.com/"
        ),
        AsyncAzureOpenAI(
            #api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = "2023-05-15",
            #azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT") 
            api_key = "cd8db66561b74d42a418b50209b6dbef",
            azure_endpoint ="https://crgar-openai-openai-sw.openai.azure.com/",
        )
    ]

    def __init__(self):
        pass

    async def create_embeddings(self):
        # Method logic here
        client = self.clients[0]
    
        try:
            for _ in range(20):
                embedding_response = await client.embeddings.create(
                    input = "Your text string goeshereYour text string goes hereYour",
                    model= "text-embedding-ada-002"
                )
                print("[CARLOS]CATCHED 429 ERROR")
        except Exception as e:
            if e.status == 429:
                # Handle the 429 error here
                print("[CARLOS]CATCHED 429 ERROR")
            else:
                # Handle other exceptions
                print("[CARLOS]ANTOTHER ERROR", str(e))

        return f"We have used client: {embedding_response.model_dump_json(indent=2)}."
    
