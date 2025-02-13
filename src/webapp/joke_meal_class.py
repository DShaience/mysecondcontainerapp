import logging

from PIL import Image
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class JokeMeal:
    def __init__(self, llm_config: dict, prompt: str):
        logger.info("Initializing Azure OpenAI client")
        self.llm_config = llm_config
        self.prompt = prompt
        credential = DefaultAzureCredential()
        token = credential.get_token(self.llm_config['azure_credentials_url'])

        self.client = AzureOpenAI(azure_endpoint=self.llm_config["endpoint_url"],
                                  api_version=self.llm_config["api_version"],
                                  azure_deployment=self.llm_config["deployment_name"],
                                  api_key=token.token,
                                  timeout=3000)        
        logger.info("Azure OpenAI client initialized successfully.")
        self.model_name = self.llm_config["model"]

    def infer(self, image: Image.Image):
        logger.info("Querying meal from image.")
        response = self.client.chat.completions.create(
            model=self.model_name,
            response_format={ "type": "json_object" },
            messages=[
            {
                "role": "user",
                "content": [
                {"type": "text", "text": self.prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}} 
                ],
            }
            ],
            max_tokens=500,
            temperature=0.2,
        )
        logger.info("Query complete.")
        return response.choices[0].message.content
    
