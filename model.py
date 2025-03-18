import openai
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from config import Config


class ModelManager:
    def __init__(self):
        """
        Initialize the model manager, supporting OpenAI, Azure, and local models.
        """
        self.openai_api_key = Config.OPENAI_API_KEY
        self.azure_api_key = Config.AZURE_API_KEY
        self.azure_endpoint = Config.AZURE_ENDPOINT
        self.azure_api_version = Config.AZURE_API_VERSION
        self.local_model_path = Config.LOCAL_MODEL_PATH
        self.base_url = Config.OPENAI_BASE_URL

        # Initialize the local model
        self.local_model = None
        self.local_tokenizer = None
        if self.local_model_path:
            self._load_local_model()

    def _load_local_model(self):
        """Load the local model (supports .safetensors format)"""
        try:
            self.local_tokenizer = AutoTokenizer.from_pretrained(self.local_model_path)
            self.local_model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )
            print(f"Loaded local model from {self.local_model_path}")
        except Exception as e:
            raise ValueError(f"Failed to load local model: {e}")

    def call_openai(self, prompt, model="gpt-3.5-turbo"):
        """
        Call the OpenAI model.
        :param prompt: Input prompt text
        :param model: OpenAI model name to use
        :return: Generated text
        """
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is not provided.")

        client = openai.OpenAI(api_key=self.openai_api_key, base_url=self.base_url)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=prompt,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"OpenAI API call failed: {e}")

    def call_azure(self, prompt, deployment_name="gpt-4o-mini"):
        """
        Call the Azure OpenAI model.
        :param prompt: Input prompt text
        :param deployment_name: Azure deployment name
        :return: Generated text
        """
        if not self.azure_api_key or not self.azure_endpoint:
            raise ValueError("Azure API key or endpoint is not provided.")

        client = openai.AzureOpenAI(
            api_key=self.azure_api_key,
            api_version=self.azure_api_version,
            azure_endpoint=self.azure_endpoint
        )

        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=prompt
            )
            response_message = response.choices[0].message.content.replace("```json", "").replace("```", '').strip()
            try:
                return json.loads(response_message)
            except Exception as e:
                print(f"Error while parsing the Azure response: {e}")
                return {"content": response_message}
        except Exception as e:
            raise ValueError(f"Azure API call failed: {e}")

    def call_local_model(self, prompt, max_tokens=5000):
        """
        Call the local model.
        :param prompt: Input prompt text
        :param max_tokens: Maximum number of tokens to generate
        :return: Generated text
        """
        if not self.local_model or not self.local_tokenizer:
            raise ValueError("Local model is not loaded.")

        try:
            inputs = self.local_tokenizer(prompt, return_tensors="pt").to(self.local_model.device)
            outputs = self.local_model.generate(
                inputs.input_ids,
                max_new_tokens=max_tokens,
                pad_token_id=self.local_tokenizer.eos_token_id
            )
            return self.local_tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise ValueError(f"Local model call failed: {e}")
